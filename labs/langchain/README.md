# LangChain Agent Lab

This lab introduces [LangChain](https://python.langchain.com/), a popular framework for composing LLM-powered applications. You'll see how to bind tools to a `ChatOpenAI` model pointed at a local server, so the same patterns you'd use with the OpenAI API work against a model running on your laptop.

## Key Concepts

### LangChain's Tool-Binding Pattern

LangChain separates the LLM from the tools:

- **`ChatOpenAI`** — a chat model that wraps any OpenAI-compatible endpoint.
- **`@tool`** — a decorator that turns a plain Python function into a LangChain tool, complete with schema generation from the docstring and type hints.
- **`llm.bind_tools()`** — attaches tool definitions to the model. When the model is invoked, it can choose to respond with text or with a tool call request.

### How the Local Server Handles Tool Calls

This lab uses `llama-cpp-python` to serve Llama-3.2-3B-Instruct via a local OpenAI-compatible REST server. The server implements the `/v1/chat/completions` endpoint, including the `tools` parameter. When the model decides to call a tool, the server returns a response with `tool_calls` populated instead of `content`. LangChain reads this and surfaces it through `response.content` or `response.tool_calls`.

See the [repository README](../../README.md) for setup and system requirements.

## Running the Lab

```sh
uv run labs/langchain/agent.py
```

On first run the model file (~2 GB) is downloaded and cached. Subsequent runs start in a few seconds.

## What You'll Observe

When the script runs you'll see:

1. A status line as the model loads.
2. The agent sends "What's the weather in Paris?" to the local model with the `get_weather` tool available.
3. The model's response is printed — either the tool's return value summarized in prose, or (if the model chose to call the tool directly) an indication that a tool call was made.

Note: small local models sometimes respond with text instead of issuing a tool call. This is normal and reflects differences in instruction-following capability. Observe the raw `response` object to understand what the model actually returned.

## Understanding the Code

Open `agent.py` and read it top to bottom:

1. **`start_local_llm()`** — starts the server and returns its base URL.
2. **`ChatOpenAI`** — standard LangChain chat model pointed at `127.0.0.1:8080/v1`.
3. **`@tool get_weather`** — a simple stub that returns a hard-coded weather string; the docstring becomes the tool description the model sees.
4. **`llm.bind_tools()`** — creates a new runnable that includes tool definitions in every request.
5. **`agent_llm.invoke()`** — sends the message and returns an `AIMessage`.
6. **`response.content`** — the text content of the response (empty if the model issued a tool call instead).

## Experiments to Try

1. **Inspect tool calls** — print `response.tool_calls` alongside `response.content` to see the raw structured output when the model requests a tool.
2. **Execute the tool** — check `response.tool_calls`, call `get_weather.invoke(...)` with the arguments, and send the result back to the model to get a final answer.
3. **Add more tools** — define a second `@tool` function and add it to `bind_tools()`. Ask a question that requires choosing between them.
4. **Use a chain** — replace `agent_llm.invoke()` with a LangChain Expression Language (LCEL) chain, e.g. `prompt | agent_llm | output_parser`.

This lab shows how LangChain's composable primitives let you quickly add tool support to any OpenAI-compatible model, local or remote.
