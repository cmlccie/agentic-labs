# Agentic LLM Labs

This repository contains simple hands-on labs to help you get started interacting with LLMs and understanding Agentic AI (AI Agent) protocols and components.

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) for dependency management
- HuggingFace account with access to Llama models
- HuggingFace CLI and API token configured

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/cmlccie/agentic-llm-labs
   cd agentic-llm-labs
   ```

2. Install [`uv`](https://docs.astral.sh/uv/) (if not already installed):

   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Install dependencies:

   ```sh
   uv sync
   ```

4. Set up HuggingFace access:

   a. Create a HuggingFace account at [https://huggingface.co](https://huggingface.co)

   b. Request access to the following models (requesting access to a model in a collection should grant you access to all models in the collection - e.g. Llama 3.2):

   - [`meta-llama/Llama-3.2-1B-Instruct`](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct)
   - [`meta-llama/Llama-3.2-3B-Instruct`](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct)

   c. Login with your HuggingFace token:

   ```sh
   uv run huggingface-cli login
   ```

5. Check your environment setup:

   ```sh
   uv agentic-llm-labs check-setup
   ```

6. Download the LLM models used in the labs:

   ```sh
   uv run agentic-llm-labs download-models
   ```

## Usage

Edit and run the labs!

_Example:_

```sh
uv run labs/llm/chat.py
```
