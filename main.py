#!/usr/bin/env python3
"""Simple LLM function call script."""

import json

from openai import OpenAI

from functions import get_coordinates, get_weather

USER_PROMPT = "What's the weather like in Paris today?"
MODEL = "ministral-8b-instruct-2410"

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current temperature for provided coordinates in celsius.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "Coordinate latitude in degrees.",
                    },
                    "longitude": {
                        "type": "number",
                        "description": "Coordinate longitude in degrees.",
                    },
                },
            },
            "required": ["latitude", "longitude"],
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_coordinates",
            "description": "Get the longitude and latitude coordinates for a location.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "location_name": {
                        "type": "string",
                        "description": "Location city (e.g. Berlin).",
                    },
                    "country_code": {
                        "type": "string",
                        "description": "ISO-3166-1 alpha2 country code (e.g. DE).",
                    },
                },
            },
            "required": ["location_name"],
        },
    },
]

functions = {
    "get_weather": get_weather,
    "get_coordinates": get_coordinates,
}


messages = [{"role": "user", "content": USER_PROMPT}]

completion = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools,
)

while completion.choices[0].message.tool_calls:
    for tool_call in completion.choices[0].message.tool_calls or []:
        args = json.loads(tool_call.function.arguments)
        result = functions[tool_call.function.name](**args)

        messages.append(completion.choices[0].message)
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

print(completion.choices[0].message.content)
