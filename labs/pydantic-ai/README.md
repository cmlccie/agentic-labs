# Pydantic AI Agent Lab

This lab introduces [Pydantic AI](https://ai.pydantic.dev/), a Python framework for building type-safe AI agents. You'll see how to point Pydantic AI at a local model using its standard OpenAI provider, so the same agent code works against any OpenAI-compatible endpoint.

## Key Concepts

### Pydantic AI

Pydantic AI is an agent framework built on top of Pydantic. It provides:

- **`Agent`** — the central object that holds a model, a system prompt, and optional tools.
- **Type-safe results** — `agent.run_sync()` returns a `RunResult` whose `.data` field is validated by Pydantic.
- **OpenAI provider** — `OpenAIChatModel` + `OpenAIProvider` wrap any OpenAI-compatible endpoint, making it trivial to swap backends.

### The Local LLM Backend

This lab uses `llama-cpp-python` to serve Llama-3.2-3B-Instruct via a local OpenAI-compatible REST server. Once running, any library that speaks the OpenAI API can use it — no library-specific inference code required.

See the [repository README](../../README.md) for setup and system requirements.

## Running the Lab

First, start the local LLM server in a separate terminal. The server runs in the foreground, so keep the terminal open while you work through the lab.

```sh
uv run agentic-labs local-llm
```

Then, in another terminal, run the lab script:

```sh
uv run labs/pydantic-ai/agent.py
```

## What You'll Observe

When the script runs you'll see:

1. The agent sends "What is the capital of France?" to the local model.
2. The model's answer — "Paris" — is printed to the terminal.

The response comes from `result.output`, the validated string returned by the agent.

## Understanding the Code

Open `agent.py` and read it top to bottom:

1. **`OpenAIProvider`** — points Pydantic AI at `127.0.0.1:8080/v1`, where the local server is listening.
2. **`OpenAIChatModel`** — wraps the provider so Pydantic AI can talk to it.
3. **`Agent`** — holds the model and system prompt; `run_sync()` sends a message and waits for the response.
4. **`result.output`** — the validated text response.

The model name passed to `OpenAIModel` (`"local"`) is arbitrary — the server ignores it and uses whichever GGUF model it loaded.

## Experiments to Try

1. **Change the question** — replace the hardcoded question with `input("❯ ")` to make it interactive.
2. **Structured output** — define a Pydantic model (e.g. `class Answer(BaseModel): capital: str`) and pass it as `result_type=Answer` to `Agent`. Observe how Pydantic AI validates the response.
3. **Add a tool** — decorate a function with `@agent.tool` and ask a question that requires it.

This lab shows how frameworks like Pydantic AI abstract away the model backend, letting you focus on agent behavior rather than inference plumbing.
