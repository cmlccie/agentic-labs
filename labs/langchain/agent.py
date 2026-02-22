#!/usr/bin/env python3
"""LangChain Agent Lab.

Requires a running local LLM server. Start one with:
    uv run agentic-labs local-llm
"""

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="local", base_url="http://127.0.0.1:8080/v1", api_key="local")


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"It's sunny and 72°F in {city}."


agent_llm = llm.bind_tools([get_weather])
response = agent_llm.invoke("What's the weather in Paris?")
print(response.content)
