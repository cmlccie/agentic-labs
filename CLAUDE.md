# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational repository for experimenting with LLMs and agentic AI patterns. Contains progressive labs from basic tokenization through tool-calling agents and MCP servers. Uses local Llama models via HuggingFace Transformers.

## Commands

```bash
# Install dependencies
uv sync

# Run labs (always from repo root)
uv run labs/llm/template.py
uv run labs/llm/input_tokens.py
uv run labs/llm/respond.py
uv run labs/llm/chat.py
uv run labs/local-agent/weather.py

# CLI tools
uv run agentic-labs check-setup
uv run agentic-labs download-models

# Developer operations (contributors only)
make lint        # Run ruff checks
make format      # Format and auto-fix
make check       # lint + format check
make setup       # Reset and setup dev environment
make help        # Show all targets
```

Never use `pip install` — always use `uv sync` for dependencies.

## Architecture

### Code Organization

- `src/agentic_labs/` — Installable shared library (CLI tools, logging, model config)
- `labs/` — Standalone executable lab scripts, each in its own directory with a README

### Lab Progression

1. **`labs/llm/`** — Four scripts demonstrating the pipeline: message formatting → tokenization → single response → multi-turn chat
2. **`labs/local-agent/`** — Agentic loop with tool calling (`weather.py` + `tools.py`). Agent iteratively calls tools until the LLM returns a final response without tool requests.
3. **`labs/weather-agent/weather-mcp-server/`** — FastMCP server exposing weather tools via Model Context Protocol, with Docker container for deployment

### Key Patterns

**Message format:** All chat interfaces use OpenAI-compatible format:
```python
messages = [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
]
```

**Logging** (`src/agentic_labs/logging.py`): Three modes — `colorized_config()`, `fancy_config()`, `silent_config()`

**CLI** (`src/agentic_labs/cli/`): Uses Typer. Each command lives in its own module, registered under the main `cli` app in `main.py`.

**Lab scripts:** Have `#!/usr/bin/env python3` shebang and are executable. Run via `uv run <relative-path>` from repo root.

### Docker

Follow the pattern in `labs/weather-agent/weather-mcp-server/Dockerfile`: multi-stage build, Alpine Linux base, working dir `/app`, `requirements.txt` from `uv export`, multi-platform (amd64/arm64).

### GitHub Actions

Follow `.github/workflows/build-weather-mcp-server.yml`: triggers on push/PR/release with path filters, builds to `ghcr.io`, semantic version tags, build attestations, GHA caching.

## Instruction Files

Detailed rules for each code area live in `.github/instructions/`:

| File | Applies To |
|------|------------|
| `agentic_labs.instructions.md` | `src/agentic_labs/**/*.py` |
| `lab_code.instructions.md` | `labs/**/*.py` |
| `lab.instructions.md` | `labs/**/*.md` |
| `containerization.instructions.md` | `**/Dockerfile` |
| `github_actions.instructions.md` | `.github/workflows/*.yml` |
