#!/usr/bin/env python3
"""Simple Agent script."""

import json

from openai import OpenAI

from tools import functions, tools

MODEL = "ministral-8b-instruct-2410"
SYSTEM_PROMPT = (
    "You are a helpful weather assistant that can answer questions and perform tasks using the provided tools. "
    "You can call tools to get information or perform actions. "
    "If you don't know the answer, you will say 'I don't know'. "
    "You will always use the tools provided to you, and you will not make up information. "
    "You will always respond in a helpful and informative manner. "
    "Do not use bold, italics, or emphasis formatting in your responses. "
    "Be friendly and empathic in your responses. "
    "If you are unsure about something, ask for clarification. "
    "Always use AM and PM time formats and US customary units. "
)

# Client connection to Inference Engine
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Define the messages list with the correct structure
messages = [{"role": "system", "content": SYSTEM_PROMPT}]


# --------------------------------------------------------------------------------------
# Chat Loop
# --------------------------------------------------------------------------------------

while True:
    # Get user prompt
    user_prompt = input("\n\033[94m❯ \033[0m")

    # Exit on "exit"
    if user_prompt.lower().strip() == "exit":
        break

    messages.append({"role": "user", "content": user_prompt})

    # Send messages and available tools to the model
    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
    )

    # -------------------------------------------------------------------------
    # Handle Tool Calls
    # -------------------------------------------------------------------------

    while completion.choices[0].message.tool_calls:
        for tool_call in completion.choices[0].message.tool_calls or []:
            # Add the tool call message to the conversation
            messages.append(completion.choices[0].message)

            # Get the details of the tool the model wants to call
            function_to_call = functions[tool_call.function.name]
            arguments = json.loads(tool_call.function.arguments)

            # Call the tool (function) with the provided arguments
            result = function_to_call(**arguments)

            # Add the tool call result to the conversation
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )

        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
        )

    # Print agent response
    print(completion.choices[0].message.content)

    # Add the model's response to the conversation
    messages.append(completion.choices[0].message)
