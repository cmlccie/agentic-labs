#!/usr/bin/env python3
"""LLM Chat Lab."""

import logging
import warnings

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


# Construct the initial messages list with the system prompt
messages = [{"role": "system", "content": SYSTEM_PROMPT}]


# Chat loop
while True:
    user_input = input("\n❯ ").strip()
    match user_input.lower():
        case "clear":
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("\nConversation history cleared.")
            continue
        case "exit" | "quit":
            break
        case "":
            continue

    messages.append({"role": "user", "content": user_input})

    output = generate(messages, max_new_tokens=MAX_NEW_TOKENS)

    assistant_response = output[0]["generated_text"][-1]
    messages.append(assistant_response)

    print(f"\n{assistant_response['content']}")
