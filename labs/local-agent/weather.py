#!/usr/bin/env python3
"""Local Weather Agent Lab."""

import json
import logging

from openai import OpenAI
from tools import functions, tools

import agentic_llm_labs.logging

MODEL = "ministral-8b-instruct-2410"
SYSTEM_PROMPT = "You are a helpful weather assistant. Use the provided tools to get weather information."


agentic_llm_labs.logging.colorized_config(level=logging.INFO)
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

while True:
    user_input = input("\n❯ ").strip()
    if not user_input.strip():
        continue
    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append({"role": "user", "content": user_input})

    # Get the initial model response to the user's input
    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
    )

    # If the model requests tool calls, add the tool call request to messages
    # and execute the functions, then add the results to the messages and
    # prompt the model to respond. Continue until there are no more tool call
    # requests.
    while completion.choices[0].message.tool_calls:
        for tool_call in completion.choices[0].message.tool_calls:
            # Add tool call request to messages
            messages.append(completion.choices[0].message)

            # Call the function
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            logging.info(
                f"LLM Requested Tool Call: {function_name!r} with arguments: {arguments!r}"
            )
            result = functions[function_name](**arguments)

            # Add tool call result to messages
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )

        # Get the model's response after the tool calls have been made and
        # results included.
        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
        )

    # Print and save the final response
    response = completion.choices[0].message.content
    messages.append(completion.choices[0].message)
    print(f"\n{response}")
