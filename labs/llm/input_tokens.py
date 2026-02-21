#!/usr/bin/env python3
"""LLM Input Tokens Lab."""

import numpy as np
import torch
from tabulate import tabulate
from transformers import AutoModel, AutoTokenizer

MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
SYSTEM_PROMPT = "You are a helpful assistant."


tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)


# Get user input and construct messages
user_input = input("\n❯ ").strip()

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": user_input},
]


# Render the chat template to get the full input string for the model
rendered_template = tokenizer.apply_chat_template(
    messages,
    tokenize=False,  # Return as tokens
    add_generation_prompt=True,  # Add the generation prompt
)

print(f"\nRendered template:\n{rendered_template}")


# Get the token embeddings for the rendered template
tokens = tokenizer.tokenize(rendered_template)
token_ids = tokenizer.convert_tokens_to_ids(tokens)
token_embeddings = (
    model.get_input_embeddings()(torch.tensor(token_ids)).to(torch.float32).data.numpy()
)


# Print the token table
token_table = zip(tokens, token_ids, token_embeddings, strict=True)
np.set_printoptions(precision=4, suppress=True)
print(
    tabulate(
        token_table,
        headers=["Token", "Token ID", "Embedding (truncated)"],
        tablefmt="pretty",
    )
)

print(f"\nTotal Input Tokens: {len(tokens)}")
