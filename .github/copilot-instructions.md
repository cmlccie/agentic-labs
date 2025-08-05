# Agentic LLM Labs - Copilot Instructions

## Project Overview

This is an educational repository for experimenting with LLMs and agentic AI patterns.

- Code samples should run with minimal setup.
- Code is designed for clarity and educational purposes, not production use.
- Code structure should be simple, linear, and easy to follow.
- Use flat, single-file scripts for most labs.
- Don't add error handling or abstractions unless absolutely necessary.
- Only use functions and classes when necessary.
- Focus on practical examples of LLM interactions, tool use, and agentic behavior.
- Emphasis on using open-source models and libraries.
- Uses HuggingFace Transformers and other libraries for LLM interactions.
- Experimentation is encouraged, and users should feel free to modify and extend the code.

## Lab Instructions

When generating lab instructions, follow these guidelines:

- Use concise, clear language.
- Use active voice.
- Provide step-by-step instructions.
- Don't include code from a lab's scripts.
- If necessary, refer the learner to the code in the lab scripts.
- Use the tell, show, tell method for the top-level README instructions. Tell the user what they will see, walk them through running the code, and then tell them what they just saw.

## Key Architectural Patterns

### Dependency Management & Script Execution

- Use `uv` (not pip/poetry) for all package management.
- Dependencies defined in `pyproject.toml`, locked in `uv.lock`.
- Scripts should have a shebang line (`#!/usr/bin/env python3`) at the top and be executable.
- Always run commands via: `uv run <script>`.

### Code Organization

- Shared utilities in `src/agentic_llm_labs/` (installable package).
- Executable labs in `labs/` subdirectories.
- Each lab has its own README with specific instructions.

### Logging System (`src/agentic_llm_labs/logging.py`)

- Three logging modes:
  - `colorized_config()` - Simple colored output without timestamps.
  - `fancy_config()` - Full formatting with timestamps and log levels.
  - `silent_config()` - Disables logging output entirely.

## Critical Implementation Details

### Message Format Consistency

All chat interfaces use OpenAI-compatible message format:

```python
messages = [
    {"role": "system", "content": "system prompt"},
    {"role": "user", "content": "user input"},
    {"role": "assistant", "content": "model response"}
]
```

### Terminal IO Consistency

- Use a simple Chevron prompt: `❯ ` to prompt users for input.
- Handle special commands: `quit`, `exit`.

## Avoid

- Don't use `pip install` - always use `uv sync`.
