#!/usr/bin/env python3
"""LLM Tokens Lab."""

from transformers import AutoTokenizer

MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
SYSTEM_PROMPT = "You are a helpful assistant."


user_input = input("\n❯ ").strip()

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": user_input},
]

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

input_tokens = tokenizer.apply_chat_template(
    messages,
    tokenize=True,  # Return as tokens
    add_generation_prompt=True,  # Add the generation prompt
)

print("\nInput tokens:")
print(input_tokens)
