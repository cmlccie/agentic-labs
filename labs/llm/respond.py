#!/usr/bin/env python3
"""LLM Response Lab."""

import logging
import warnings
from pprint import pprint

from transformers.pipelines import pipeline
from transformers.utils import logging as transformers_logging

# Suppress noisy output from transformers and its dependencies.
logging.getLogger().setLevel(logging.CRITICAL)
warnings.filterwarnings("ignore")
transformers_logging.set_verbosity_error()


MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
SYSTEM_PROMPT = "You are a helpful assistant."
MAX_NEW_TOKENS = 256


# Create the text generation pipeline
generate = pipeline(
    "text-generation",
    model=MODEL_NAME,
    device_map="auto",
    max_new_tokens=MAX_NEW_TOKENS,
)


# Get user input and construct messages
user_input = input("\n❯ ").strip()

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": user_input},
]


# Generate and print the response
output = generate(messages)
pprint(output)
