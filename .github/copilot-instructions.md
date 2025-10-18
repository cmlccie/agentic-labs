# Agentic Labs - Copilot Instructions

## Project Overview

This is an educational repository for experimenting with LLMs and agentic AI patterns.

## Learning Labs

Each directory in `labs/` contains a self-contained lab focused on a specific aspect of working with LLMs and agentic AI patterns. Each lab includes:

- A `README.md` file with detailed instructions that guide the user through the lab exercises.
- One or more Python scripts that implement the lab exercises.

## Style Guidelines

### List Style Guidelines

- All items in a list should be consistently structured (either simple phrases or complete sentences).
- When a list contains sentences, each sentence should end with a period.
- When a list contains simple phrases, do not use periods.
- Maintain parallel structure across all items in the same list.

## Key Architectural Patterns

### Dependency Management & Script Execution

- Use `uv` (not `pip` or `poetry`) for all package management.
- Dependencies defined in `pyproject.toml`, locked in `uv.lock`.
- Scripts should have a shebang line (`#!/usr/bin/env python3`) at the top and be executable.
- Always run commands via `uv run <relative-path-to-script>` from the repository root directory.

### Code Organization

- Shared utilities in `src/agentic_labs/` (installable package).
- Executable labs in `labs/` subdirectories.
- Each lab has its own README with specific instructions.

### Logging System (`src/agentic_labs/logging.py`)

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

## Avoid

- Don't use `pip install` - always use `uv sync`.

## User Tools

- The repository includes command-line interface (CLI) tool contained in the `agentic_labs` package for user interaction.
- Use `typer` for command-line interfaces (CLIs).
- Organize the CLI code in the `agentic_labs.cli` package.
- Organize CLI commands under a main `cli` Typer app instance contained in `agentic_labs.cli.main`.
- Each CLI command should be defined in its own module within the `agentic_labs.cli` package.

## Developer Tools

### Makefile

The `Makefile` in the repository root provides common developer (contributor) operations. Use `make help` to see all available targets and their descriptions.

The Makefile is for **developer (contributor) operations only**. User operations (running labs) should follow the instructions in lab README files using `uv run` commands.

When adding new development tools or changing project structure, update the Makefile accordingly. The Makefile uses a dynamic help system - add new targets with `## Description` comments to automatically include them in the help output.
