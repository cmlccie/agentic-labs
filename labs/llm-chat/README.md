# LLM Chat Lab - Local Inference

A simple, minimal chat interface using locally-hosted language models via HuggingFace Transformers.

## Prerequisites

- HuggingFace account with access to Llama models
- HuggingFace CLI installed and authenticated
- See the main repository README for detailed setup instructions

## Features

- 🚀 **Local inference** - Everything runs locally (HuggingFace authentication required for model access)
- 🤖 **Automatic model management** - Models are downloaded and cached automatically
- 💬 **Interactive chat interface** - Simple command-line conversation

## Quick Start

1. Run the chat application:

   ```bash
   uv run labs/llm-chat/local.py
   ```

2. Start chatting! The model will be downloaded automatically on first run.

## Available Commands

- Type your message and press Enter to chat
- `clear` - Reset conversation history
- `quit`, `exit`, or `bye` - End the conversation

## Model Options

The lab uses `meta-llama/Llama-3.2-1B` by default for a good balance of speed and quality. You can easily switch to other models by modifying the `MODEL_NAME` constant in `local.py`:

- `meta-llama/Llama-3.2-1B` - Compact Llama model (~2.5GB)
- `microsoft/DialoGPT-small` - Conversational model (~117MB)
- `microsoft/DialoGPT-medium` - Larger conversational model (~345MB)
- `distilgpt2` - Smaller general-purpose model (~320MB)
- `gpt2` - Full GPT-2 model (~500MB)

## First Run

On the first run, the selected model will be downloaded and cached locally. This may take a few minutes depending on your internet connection and the model size. Subsequent runs will be much faster.

## Technical Details

- Uses HuggingFace Transformers library with pipeline API
- Local inference with PyTorch backend
- Conversation context is maintained across exchanges
- Configurable temperature and repetition penalty settings
- Automatic GPU detection and usage when available
