#!/usr/bin/env python3
"""Local Weather Agent Lab (Llama-3.1-8B-Instruct, Transformers)."""

import json
import logging
from typing import Any, Dict, List

import torch
from tools import get_coordinates, get_weather
from transformers import AutoTokenizer
from transformers.pipelines import pipeline

import agentic_llm_labs.logging

agentic_llm_labs.logging.colorized_config(level=logging.INFO)

MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"
SYSTEM_PROMPT = (
    "You are a helpful weather assistant. "
    "Use the provided tools to get weather information. "
    "Only call one tool at a time, and only if necessary. "
    "After getting the weather data, provide a clear, conversational summary of the weather conditions."
)
MAX_NEW_TOKENS = 256


messages: List[Dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

generate = pipeline(
    "text-generation",
    model=MODEL_NAME,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    pad_token_id=tokenizer.eos_token_id,
)

# Chat loop
while True:
    user_input = input("\n❯ ").strip()
    if not user_input.strip():
        continue
    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append({"role": "user", "content": user_input})

    # Tool call loop
    while True:
        rendered_template = tokenizer.apply_chat_template(
            messages,
            tools=[get_coordinates, get_weather],
            tokenize=False,
            add_generation_prompt=True,
        )

        logging.info("Generating...")
        output = generate(rendered_template, max_new_tokens=MAX_NEW_TOKENS)

        generated_text = output[0]["generated_text"]
        logging.debug(f"Generated text:\n{generated_text}")

        response = generated_text[len(rendered_template) :].strip()

        try:
            # Detect tool request, expects JSON: {"name": ..., "parameters": {...}}
            tool_request = json.loads(response)
            logging.info(f"Tool Request: {tool_request}")

            match tool_request:
                case {"name": "get_coordinates", "parameters": parameters}:
                    tool_result = get_coordinates(**parameters)
                case {"name": "get_weather", "parameters": parameters}:
                    tool_result = get_weather(**parameters)
                case _:
                    logging.error(f"Unknown tool request: {tool_request}")
                    break

            # Add the tool request and result to the conversation
            messages.append({"role": "assistant", "content": tool_request})
            messages.append(
                {"role": "tool", "name": tool_request["name"], "content": tool_result}
            )
            continue

        except json.JSONDecodeError:
            # Not a tool call response, just a text response.
            messages.append({"role": "assistant", "content": response})
            print(f"\n{response}")
            break
