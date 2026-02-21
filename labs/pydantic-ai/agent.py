#!/usr/bin/env python3
"""Pydantic AI Agent Lab."""

from agentic_labs.engine import start_local_llm
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

base_url = start_local_llm("bartowski/Llama-3.2-3B-Instruct-GGUF")

model = OpenAIChatModel(
    "local",
    provider=OpenAIProvider(base_url=base_url, api_key="local"),
)
agent = Agent(model=model, system_prompt="You are a helpful assistant.")

result = agent.run_sync("What is the capital of France?")
print(result.output)
