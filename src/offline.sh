#!/usr/bin/env bash
# This script enables offline mode for dependencies that attempt to access the network.
# It may not be comprehensive for all tools, but it covers some common ones.

# Because this script modifies environment variables, it should be sourced:
#   source src/offline.sh

# --------------------------------------------------------------------------------------
# Transformers
# --------------------------------------------------------------------------------------

# Transformers library offline mode
# Prevents HTTP calls to download models/configs, only uses cached files
export TRANSFORMERS_OFFLINE=1


# --------------------------------------------------------------------------------------
# HuggingFace Hub
# --------------------------------------------------------------------------------------


# Hugging Face Hub (used by transformers, accelerate, etc.)
# Prevents HTTP calls to the Hub, only uses cached files
export HF_HUB_OFFLINE=1

# Disable Hugging Face telemetry (privacy)
export HF_HUB_DISABLE_TELEMETRY=1

# Accelerate (uses Hugging Face Hub cache and offline settings)
# No additional offline variable needed; respects HF_HUB_OFFLINE


# --------------------------------------------------------------------------------------
# OpenAI
# --------------------------------------------------------------------------------------

# OpenAI Python SDK
# No documented offline mode, but you can disable logging to limit logging messages
export OPENAI_LOG=error
