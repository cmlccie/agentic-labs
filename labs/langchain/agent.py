#!/usr/bin/env python3
"""LangChain Agent Lab."""

from agentic_labs.engine import start_local_llm
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

base_url = start_local_llm("bartowski/Llama-3.2-3B-Instruct-GGUF")

llm = ChatOpenAI(model="local", base_url=base_url, api_key="local")


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"It's sunny and 72°F in {city}."


agent_llm = llm.bind_tools([get_weather])
response = agent_llm.invoke("What's the weather in Paris?")
print(response.content)
