# Agentic LLM Labs

This repository contains simple hands-on labs to help you get started interacting with LLMs and understanding Agentic AI (AI Agent) protocols and components.

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) for dependency management
- HuggingFace account with access to Llama models
- HuggingFace CLI and API token configured

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/cmlccie/agentic-llm-labs
   cd agentic-llm-labs
   ```

2. Install uv (if not already installed):

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Install dependencies:

   ```bash
   uv sync --no-install-project
   ```

4. Set up HuggingFace access:

   a. Create a HuggingFace account at [https://huggingface.co](https://huggingface.co)

   b. Request access to the following Llama collections at [https://huggingface.co/meta-llama](https://huggingface.co/meta-llama):

   - Llama 3.2

   c. Login with your HuggingFace token:

   ```bash
   uv run huggingface-cli login
   ```

## Usage

Edit and run the labs!

_Example:_

```bash
uv run labs/llm-chat/local.py
```
