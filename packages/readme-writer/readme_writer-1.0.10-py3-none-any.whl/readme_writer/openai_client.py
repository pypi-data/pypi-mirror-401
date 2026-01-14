"""OpenAI API client for documentation generation."""

import logging
import tiktoken
import os
from typing import Optional, List, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI

from .config import Config, get_model_encoding, get_model_context_window, DEFAULT_ENCODING

logger = logging.getLogger(__name__)

# Default number of parallel workers for chunk processing
DEFAULT_PARALLEL_WORKERS = 6


class OpenAIClient:
    """Client for interacting with OpenAI API."""
    
    def __init__(self, config: Config, api_key: Optional[str] = None):
        """Initialize OpenAI client."""
        self.config = config
        self.api_key = api_key or self._get_api_key()
        self.client = OpenAI(api_key=self.api_key)
        self.encoding = self._get_encoding(config.model)
        self.context_window = get_model_context_window(config.model)
        # Reserve tokens for response and overhead
        self.max_input_tokens = int(self.context_window * 0.85)  # 85% for input, 15% for response
        # Parallel processing settings (from config or env var)
        self.parallel_workers = config.parallel_workers if hasattr(config, 'parallel_workers') else int(os.getenv("PARALLEL_WORKERS", DEFAULT_PARALLEL_WORKERS))
    
    def _get_encoding(self, model: str) -> tiktoken.Encoding:
        """Get tiktoken encoding for model with fallback support.
        
        GPT-5 and other new models may not be directly supported by tiktoken yet,
        so we use explicit encoding names from our config.
        """
        encoding_name = get_model_encoding(model)
        try:
            return tiktoken.get_encoding(encoding_name)
        except Exception as e:
            logger.warning(f"Failed to get encoding '{encoding_name}' for model '{model}': {e}")
            logger.warning(f"Falling back to {DEFAULT_ENCODING} encoding")
            return tiktoken.get_encoding(DEFAULT_ENCODING)
    
    def _get_api_key(self) -> str:
        """Get API key from environment."""
        import os
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        return api_key
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoding.encode(text))
    
    def estimate_cost(self, tokens: int) -> float:
        """Estimate cost for token count."""
        cost_per_1k = self.config.cost_per_1k_tokens.get(self.config.model, 0.005)
        return (tokens / 1000) * cost_per_1k
    
    def get_available_tokens(self, system_prompt: str) -> int:
        """Calculate available tokens for content after accounting for system prompt."""
        system_tokens = self.count_tokens(system_prompt)
        return self.max_input_tokens - system_tokens
    
    def split_text_into_chunks(self, text: str, max_tokens_per_chunk: int) -> List[str]:
        """Split text into chunks that fit within token limits.
        
        Tries to split at natural boundaries (file markers) when possible.
        """
        tokens = self.encoding.encode(text)
        
        if len(tokens) <= max_tokens_per_chunk:
            return [text]
        
        chunks = []
        current_start = 0
        
        while current_start < len(tokens):
            chunk_end = min(current_start + max_tokens_per_chunk, len(tokens))
            chunk_tokens = tokens[current_start:chunk_end]
            chunk_text = self.encoding.decode(chunk_tokens)
            
            # Try to find a natural break point (file boundary) near the end
            if chunk_end < len(tokens):
                # Look for "## File:" marker in the last 20% of the chunk
                search_start = int(len(chunk_text) * 0.8)
                last_file_marker = chunk_text.rfind('\n## File:', search_start)
                
                if last_file_marker > search_start:
                    chunk_text = chunk_text[:last_file_marker]
                    chunk_tokens = self.encoding.encode(chunk_text)
                else:
                    # Fall back to newline boundary
                    last_newline = chunk_text.rfind('\n', search_start)
                    if last_newline > search_start:
                        chunk_text = chunk_text[:last_newline + 1]
                        chunk_tokens = self.encoding.encode(chunk_text)
            
            chunks.append(chunk_text)
            current_start += len(chunk_tokens)
        
        return chunks
    
    def check_content_fits(self, content: str, system_prompt: str) -> bool:
        """Check if content fits within the model's context window."""
        available_tokens = self.get_available_tokens(system_prompt)
        content_tokens = self.count_tokens(content)
        return content_tokens <= available_tokens
    
    def summarize_chunk(self, chunk: str, chunk_num: int, total_chunks: int) -> str:
        """Generate a comprehensive summary of a content chunk.
        
        Uses dynamic token allocation based on chunk size to capture all important details.
        Thread-safe - can be called in parallel.
        """
        chunk_tokens = self.count_tokens(chunk)
        # Use ~15-20% of chunk tokens for summary (min 4000, max 12000)
        summary_tokens = min(max(int(chunk_tokens * 0.18), 4000), 12000)
        
        logger.debug(f"Chunk {chunk_num}: {chunk_tokens:,} tokens, summary budget: {summary_tokens:,}")
        
        # Count files in chunk to set expectations
        file_count = chunk.count("## File:")
        min_words_per_file = 150
        expected_min_words = file_count * min_words_per_file
        
        summary_prompt = f"""You are a technical documentation expert creating EXHAUSTIVE documentation.

CRITICAL REQUIREMENTS:
- This chunk contains approximately {file_count} files
- You MUST write AT LEAST {expected_min_words} words total (approximately {min_words_per_file} words per file)
- You have a budget of {summary_tokens:,} tokens - USE IT ALL
- DO NOT be brief. DO NOT summarize in one sentence. BE VERBOSE AND DETAILED.

For EACH file, create a FULL documentation section including:

### [filename]
**Purpose:** [2-3 sentences explaining what this file does and why it exists]

**Classes:**
- `ClassName`: [description]
  - `method1(params)`: [what it does, returns]
  - `method2(params)`: [what it does, returns]

**Functions:**
- `function_name(param1, param2)`: [detailed description of purpose, parameters, return value]

**Configuration/Constants:**
- `CONSTANT_NAME`: [value and purpose]
- Environment variables: [list any env vars used]

**Dependencies:** [list all imports and what they're used for]

**Code Examples:** [include relevant code snippets showing usage]

**Integration:** [how this file connects to other parts of the system]

---

REMEMBER: Write DETAILED documentation for EVERY file. This will be the basis for the final README.
Your response should be LONG and COMPREHENSIVE. Short responses are NOT acceptable."""
        
        user_content = f"Analyzing chunk {chunk_num} of {total_chunks} ({chunk_tokens:,} tokens, ~{file_count} files)\n\n{chunk}"
        
        try:
            request_params = {
                "model": self.config.model,
                "messages": [
                    {"role": "system", "content": summary_prompt},
                    {"role": "user", "content": user_content}
                ],
                "temperature": 0.4,  # Slightly higher for more verbose output
            }
            
            if self._uses_max_completion_tokens():
                request_params["max_completion_tokens"] = summary_tokens
            else:
                request_params["max_tokens"] = summary_tokens
            
            response = self.client.chat.completions.create(**request_params)
            
            if not response.choices:
                return f"[Summary unavailable for chunk {chunk_num}]\n{chunk[:1000]}..."
            
            summary = response.choices[0].message.content.strip()
            summary_size = self.count_tokens(summary)
            
            logger.info(f"Chunk {chunk_num}: generated {summary_size:,}/{summary_tokens:,} tokens ({summary_size*100//summary_tokens}%)")
            
            # Warn if summary is too short
            if summary_size < summary_tokens * 0.3:
                logger.warning(f"Chunk {chunk_num}: summary too short - only {summary_size*100//summary_tokens}% of budget used")
            
            return summary
            
        except Exception as e:
            logger.error(f"Error summarizing chunk {chunk_num}: {e}")
            return f"[Summary failed for chunk {chunk_num}: {e}]\nChunk preview: {chunk[:2000]}..."
    
    def _uses_max_completion_tokens(self) -> bool:
        """Check if model uses max_completion_tokens instead of max_tokens.
        
        GPT-5, GPT-4.1, o3, o4 and newer models require max_completion_tokens.
        """
        model = self.config.model.lower()
        new_model_prefixes = ("gpt-5", "gpt-4.1", "o3", "o4")
        return any(model.startswith(prefix) for prefix in new_model_prefixes)
    
    def generate_documentation(self, content: str, system_prompt: str) -> str:
        """Generate documentation using OpenAI API.
        
        If content exceeds context window, automatically uses chunking to process
        all content and combines the results.
        """
        try:
            # Check if content fits within model context window
            if self.check_content_fits(content, system_prompt):
                return self._single_request(content, system_prompt)
            else:
                # Content too large - use chunking approach
                return self._chunked_request(content, system_prompt)
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            raise
    
    def _single_request(self, content: str, system_prompt: str) -> str:
        """Make a single API request."""
        request_params = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ],
            "temperature": self.config.temperature,
        }
        
        if self._uses_max_completion_tokens():
            request_params["max_completion_tokens"] = self.config.max_tokens_per_request
        else:
            request_params["max_tokens"] = self.config.max_tokens_per_request
        
        response = self.client.chat.completions.create(**request_params)
        
        if not response.choices:
            raise ValueError("Empty response from OpenAI API")
        
        return response.choices[0].message.content.strip()
    
    def _chunked_request(self, content: str, system_prompt: str) -> str:
        """Process content in chunks when it exceeds context window.
        
        Strategy:
        1. Split content into chunks that fit in context
        2. Generate detailed summary for each chunk IN PARALLEL (with dynamic token allocation)
        3. Combine summaries
        4. Generate final documentation from combined summaries
        """
        from rich.console import Console
        import time
        console = Console()
        
        content_tokens = self.count_tokens(content)
        available_tokens = self.get_available_tokens(system_prompt)
        
        console.print(f"[yellow]Content ({content_tokens:,} tokens) exceeds context window ({available_tokens:,} available tokens)[/yellow]")
        console.print("[yellow]Using chunked processing to capture all context...[/yellow]")
        
        # Split into chunks (use 80% of available tokens per chunk for safety margin)
        chunk_size = int(available_tokens * 0.8)
        chunks = self.split_text_into_chunks(content, chunk_size)
        
        console.print(f"[cyan]Split content into {len(chunks)} chunks[/cyan]")
        console.print(f"[cyan]Processing with {self.parallel_workers} parallel workers...[/cyan]")
        
        start_time = time.time()
        
        # Process chunks in parallel
        summaries = [None] * len(chunks)  # Pre-allocate to maintain order
        
        def process_chunk(args):
            idx, chunk = args
            chunk_tokens = self.count_tokens(chunk)
            return idx, chunk_tokens, self.summarize_chunk(chunk, idx + 1, len(chunks))
        
        with ThreadPoolExecutor(max_workers=self.parallel_workers) as executor:
            # Submit all chunks
            futures = {executor.submit(process_chunk, (i, chunk)): i for i, chunk in enumerate(chunks)}
            
            # Collect results as they complete
            completed = 0
            for future in as_completed(futures):
                try:
                    idx, chunk_tokens, summary = future.result()
                    summaries[idx] = f"=== CHUNK {idx+1}/{len(chunks)} DETAILED ANALYSIS ===\n\n{summary}"
                    completed += 1
                    console.print(f"[green]✓ Chunk {idx+1}/{len(chunks)} completed ({chunk_tokens:,} tokens)[/green]")
                except Exception as e:
                    idx = futures[future]
                    summaries[idx] = f"=== CHUNK {idx+1}/{len(chunks)} FAILED ===\n\nError: {e}"
                    completed += 1
                    console.print(f"[red]✗ Chunk {idx+1}/{len(chunks)} failed: {e}[/red]")
        
        elapsed = time.time() - start_time
        console.print(f"[green]All {len(chunks)} chunks processed in {elapsed:.1f}s[/green]")
        
        # Combine all summaries
        combined_summaries = "\n\n".join(summaries)
        combined_tokens = self.count_tokens(combined_summaries)
        
        console.print(f"[cyan]Combined summaries: {combined_tokens:,} tokens[/cyan]")
        
        # If combined summaries still too large, recursively process
        if combined_tokens > available_tokens:
            console.print("[yellow]Combined summaries still too large, condensing...[/yellow]")
            condense_prompt = """You are a technical documentation expert. Condense these detailed chunk analyses into a single comprehensive summary that preserves ALL important information about:
- Every file and its purpose
- All key classes, functions, and their functionality
- Configuration options and environment variables
- Dependencies and requirements
- API endpoints and CLI commands
- Architecture patterns and design decisions

Do NOT lose any important technical details. This will be used to generate final documentation."""
            combined_summaries = self._chunked_request(combined_summaries, condense_prompt)
        
        # Generate final documentation from summaries
        console.print("[green]Generating final documentation from all chunks...[/green]")
        
        # Calculate expected README size
        total_summary_tokens = self.count_tokens(combined_summaries)
        console.print(f"[cyan]Total summary content: {total_summary_tokens:,} tokens[/cyan]")
        
        # Generate README in sections for better detail
        return self._generate_sectioned_readme(combined_summaries, system_prompt, content_tokens, len(chunks))
    
    def _generate_sectioned_readme(self, summaries: str, system_prompt: str, total_source_tokens: int, num_chunks: int) -> str:
        """Generate README in sections for comprehensive documentation.
        
        Instead of generating one README with limited tokens, generate each major section
        separately with generous token budgets, then combine them.
        """
        from rich.console import Console
        import time
        console = Console()
        
        summary_tokens = self.count_tokens(summaries)
        
        # Define README sections with their prompts
        sections = [
            {
                "name": "Overview & Installation",
                "max_tokens": 3000,
                "prompt": """Based on the project analysis, generate ONLY these sections:

# [Project Name]

## Overview
[Comprehensive 3-5 paragraph description of the project, its purpose, architecture, and key features]

## Key Features
[Bullet list of main features and capabilities]

## Installation

### Prerequisites
[List all prerequisites]

### Setup Steps
[Detailed step-by-step installation instructions with code blocks]

Be detailed and comprehensive. Include all relevant information from the analysis."""
            },
            {
                "name": "Project Structure",
                "max_tokens": 4000,
                "prompt": """Based on the project analysis, generate ONLY the Project Structure section:

## Project Structure

```
[directory tree showing all main directories and key files]
```

### Directory Descriptions

[For each main directory, provide:
- Directory name and purpose
- Key files within it and what they do
- How it relates to other parts of the project]

Be thorough - list ALL directories and explain their contents."""
            },
            {
                "name": "Core Components",
                "max_tokens": 6000,
                "prompt": """Based on the project analysis, generate ONLY the Core Components section:

## Core Components

[For EACH major module/component in the project, create a subsection with:]

### [Component Name]

**Purpose:** [What this component does]

**Key Classes:**
- `ClassName`: [Description]
  - `method1()`: [What it does]
  - `method2()`: [What it does]

**Key Functions:**
- `function_name(params)`: [Description, parameters, returns]

**Usage Example:**
```python
[Real code example showing how to use this component]
```

Document ALL major components found in the analysis. Be comprehensive."""
            },
            {
                "name": "Configuration & API",
                "max_tokens": 4000,
                "prompt": """Based on the project analysis, generate ONLY these sections:

## Configuration

### Environment Variables
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
[List ALL environment variables found]

### Constants
[List key constants and their purposes]

### Configuration Files
[Describe any configuration files]

## API Reference

### CLI Commands
[List all CLI commands with usage examples]

### API Endpoints
[If applicable, list all endpoints with methods, parameters, and responses]

### Public Interfaces
[Document public classes/functions meant for external use]

Be thorough and include everything found in the analysis."""
            },
            {
                "name": "Usage, Testing & Contributing",
                "max_tokens": 3000,
                "prompt": """Based on the project analysis, generate ONLY these sections:

## Usage Examples

[Provide 3-5 detailed, real-world usage examples with code blocks]

### Example 1: [Basic Usage]
```python
[code]
```

### Example 2: [Common Task]
```python
[code]
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
[List ALL dependencies from requirements.txt or similar]

## Testing

### Running Tests
```bash
[commands to run tests]
```

### Test Coverage
[Describe what is tested]

## Contributing

[Standard contribution guidelines]

## License

[License information if found]"""
            }
        ]
        
        console.print(f"[cyan]Generating README in {len(sections)} sections for maximum detail...[/cyan]")
        
        start_time = time.time()
        section_results = []
        
        # Process sections in parallel
        def generate_section(section):
            section_content = f"""PROJECT ANALYSIS ({summary_tokens:,} tokens from {num_chunks} chunks, {total_source_tokens:,} source tokens):

{summaries}

---

{section['prompt']}"""
            
            try:
                request_params = {
                    "model": self.config.model,
                    "messages": [
                        {"role": "system", "content": "You are an expert technical documentation writer. Generate ONLY the requested sections, nothing else. Be comprehensive and detailed."},
                        {"role": "user", "content": section_content}
                    ],
                    "temperature": 0.3,
                }
                
                if self._uses_max_completion_tokens():
                    request_params["max_completion_tokens"] = section['max_tokens']
                else:
                    request_params["max_tokens"] = section['max_tokens']
                
                response = self.client.chat.completions.create(**request_params)
                
                if response.choices:
                    return section['name'], response.choices[0].message.content.strip()
                return section['name'], f"[Section generation failed]"
                
            except Exception as e:
                logger.error(f"Error generating section {section['name']}: {e}")
                return section['name'], f"[Error generating {section['name']}: {e}]"
        
        with ThreadPoolExecutor(max_workers=min(len(sections), self.parallel_workers)) as executor:
            futures = {executor.submit(generate_section, section): section['name'] for section in sections}
            
            for future in as_completed(futures):
                section_name = futures[future]
                try:
                    name, content = future.result()
                    section_results.append((name, content))
                    result_tokens = self.count_tokens(content)
                    console.print(f"[green]✓ Section '{name}' completed ({result_tokens:,} tokens)[/green]")
                except Exception as e:
                    console.print(f"[red]✗ Section '{section_name}' failed: {e}[/red]")
        
        elapsed = time.time() - start_time
        console.print(f"[green]All sections generated in {elapsed:.1f}s[/green]")
        
        # Sort sections back to original order and combine
        section_order = {s['name']: i for i, s in enumerate(sections)}
        section_results.sort(key=lambda x: section_order.get(x[0], 999))
        
        # Combine all sections
        final_readme = "\n\n---\n\n".join([content for _, content in section_results])
        
        # Clean up any duplicate headers or section markers
        final_readme = self._clean_readme(final_readme)
        
        final_tokens = self.count_tokens(final_readme)
        console.print(f"[cyan]Final README: {final_tokens:,} tokens[/cyan]")
        
        return final_readme
    
    def _clean_readme(self, readme: str) -> str:
        """Clean up the final README by removing duplicates and fixing formatting."""
        import re
        
        # Remove duplicate horizontal rules
        readme = re.sub(r'\n---\n---\n', '\n---\n', readme)
        readme = re.sub(r'\n\n\n+', '\n\n', readme)
        
        # Remove any "ONLY generate" instruction leakage
        readme = re.sub(r'(?i)\[?generate only.*?\]?', '', readme)
        
        return readme.strip() 