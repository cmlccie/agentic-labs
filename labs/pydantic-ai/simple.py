#!/usr/bin/env python3
"""Simplest Agent - chat with a local LLM server.

Requires a running local LLM server. Start one with:
    uv run agentic-labs local-llm
"""

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

BASE_URL = "http://localhost:8080/v1"
API_KEY = "local"
MODEL = "local"

provider = OpenAIProvider(base_url=BASE_URL, api_key=API_KEY)
model = OpenAIChatModel(MODEL, provider=provider)

agent = Agent(model, system_prompt="You are a helpful assistant.")

if __name__ == "__main__":
    agent.to_cli_sync(prog_name="simple-agent")
