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

5. Download the required models:

   ```sh
   # Download all models used in the labs (optimized for lab usage)
   uv run agentic-llm-labs

   # Or download specific models
   uv run agentic-llm-labs -m meta-llama/Llama-3.2-1B-Instruct

   # Download with verbose output
   uv run agentic-llm-labs --verbose
   ```

   > **Note:** The download is optimized to exclude unnecessary files (like `original/` PyTorch files) and focuses on the `.safetensors` files and configurations needed for the labs.

## Usage

Edit and run the labs!

_Example:_

```sh
uv run labs/llm/chat.py
```

## CLI Tools

The repository includes a CLI tool for common tasks:

### Download Models

Download all models used in the labs:

```sh
uv run agentic-llm-labs
```

**Options:**

- `--model, -m`: Specify specific models to download (can be used multiple times)
- `--cache-dir, -c`: Custom cache directory (defaults to HuggingFace cache)
- `--force, -f`: Force re-download even if models are already cached
- `--verbose, -v`: Enable verbose logging

**Examples:**

```sh
# Download all default models
uv run agentic-llm-labs

# Download specific models
uv run agentic-llm-labs -m meta-llama/Llama-3.2-1B-Instruct -m meta-llama/Llama-3.2-3B-Instruct

# Download with verbose output
uv run agentic-llm-labs --verbose

# Force re-download to custom directory
uv run agentic-llm-labs --force --cache-dir ./models
```
