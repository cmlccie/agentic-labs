#!/usr/bin/env python3
"""Pydantic AI Agent Lab.

Requires a running local LLM server. Start one with:
    uv run agentic-labs local-llm
"""

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIChatModel(
    "local",
    provider=OpenAIProvider(base_url="http://127.0.0.1:8080/v1", api_key="local"),
)
agent = Agent(model=model, system_prompt="You are a helpful assistant.")

result = agent.run_sync("What is the capital of France?")
print(result.output)
