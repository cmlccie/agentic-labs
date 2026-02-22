# Agentic Labs

This repository contains simple hands-on labs to help you get started interacting with LLMs and understanding Agentic AI (AI Agent) protocols and components.

## Requirements

- Python 3.12
- [uv](https://github.com/astral-sh/uv) for dependency management
- HuggingFace account with access to Llama models
- HuggingFace CLI and API token configured

## Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/cmlccie/agentic-labs
   cd agentic-labs
   ```

2. Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/) (if not already installed):

   macOS and Linux:

   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   Windows:

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. Install dependencies using the `extra` option appropriate for your system:

   ```sh
   uv sync --extra metal      # Apple Silicon Macs
   uv sync --extra cu124      # Systems w/ NVIDIA GPUs supporting CUDA 12.4
   uv sync --extra cu121      # Systems w/ NVIDIA GPUs supporting CUDA 12.1
   uv sync --extra default    # All other systems
   ```

4. Set up HuggingFace access:

   a. Create a HuggingFace account at [https://huggingface.co](https://huggingface.co)

   b. Request access to the following models:
   - [`meta-llama/Llama-3.2-1B-Instruct`](https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct)

   c. Login with your HuggingFace token:

   ```sh
   uv run hf auth login
   ```

5. Check your environment setup:

   ```sh
   uv run agentic-labs check-setup
   ```

6. Download the LLM models used in the labs:

   ```sh
   uv run agentic-labs download-models
   ```

## Usage

Edit and run the labs!

_Example:_

```sh
uv run labs/llm/chat.py
```
