#!/usr/bin/env python3
"""LLM Response Lab."""

import torch
from transformers import AutoTokenizer
from transformers.pipelines import pipeline

MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
SYSTEM_PROMPT = "You are a helpful assistant."
MAX_NEW_TOKENS = 256


user_input = input("\n❯ ").strip()

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": user_input},
]

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

generate = pipeline(
    "text-generation",
    model=MODEL_NAME,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    pad_token_id=tokenizer.eos_token_id,  # Explicitly set to suppress warning
)

output = generate(messages, max_new_tokens=MAX_NEW_TOKENS)

print(output)
