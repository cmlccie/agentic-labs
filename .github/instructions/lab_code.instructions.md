---
applyTo: "labs/**/*.py"
---

# Lab Code Instructions

## Lab Contents

- Focus on practical foundational principles of LLM operations, tool use, and agentic behavior.
- Use HuggingFace Transformers for local LLM generation.
- Only use dependencies already in `pyproject.toml`.
- Labs are designed to be run in a terminal environment.

## Lab Scripts

- Lab scripts must be less than 100 lines of code.
- Lab scripts should use the shebang line `#!/usr/bin/env python3` at the top and be executable.
- Use flat, single-file scripts for most labs.

## Lab Code

- Lab code must be simple and easy to follow.
- Lab code is designed for clarity and educational purposes, not production use.
- Lab code should be simple, linear, and easy to read from top to bottom.
- Lab code should be consistent with other lab code in style, structure, formatting, and variable naming.
- Lab code should run with minimal setup.
- Lab code should not require any additional setup beyond `uv sync`.
- Lab code should be run via `uv run <relative-path-to-script>` from the repository root directory.
- Lab code should only define functions or classes when required and absolutely necessary.

## Supporting Code

- Supporting code must support the main lab code by providing utilities that make the lab code cleaner and easier to understand.
- Supporting code should be used rarely, and only when it makes the lab code significantly clearer.
- Supporting code should be placed in `src/agentic_labs/`.
- Supporting code may not implement core lab functionality.

## Avoid

- Don't use complex abstractions or design patterns.
- Don't add error handling or abstractions unless absolutely necessary.
- Don't use advanced Python features that may confuse learners.

## Terminal IO Consistency

- Use a simple Chevron prompt: `❯ ` to prompt users for input.
- Handle special commands: `quit`, `exit`, and `clear`.
- Use consistent print formatting for outputs.
- Use `tabulate` for displaying tabular data.
