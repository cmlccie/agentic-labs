# Pydantic AI Agent Labs

This lab introduces [Pydantic AI](https://ai.pydantic.dev/), a Python framework for building type-safe AI agents. You explore three progressively richer agents — a simple chat agent, a weather-forecast agent with real API tools, and a natural-language database agent — all pointed at a local OpenAI-compatible server.

## Key Concepts

### Pydantic AI

Pydantic AI is an agent framework built on top of Pydantic. It provides:

- **`Agent`** — the central object that holds a model, a system prompt, and optional tools.
- **Tools** — plain Python functions decorated with `@agent.tool()` that the model can call during a run.
- **Dynamic system prompts** — functions decorated with `@agent.system_prompt()` that inject context at runtime.
- **OpenAI provider** — `OpenAIChatModel` + `OpenAIProvider` wrap any OpenAI-compatible endpoint, making it easy to swap backends without changing agent logic.

### The Local LLM Backend

These labs connect to a local LLM server that speaks the OpenAI API. Start one in a separate terminal before running any lab script:

```sh
uv run agentic-labs local-llm
```

Keep that terminal open while you work through the labs.

## Lab 1 — Simple Agent (`simple.py`)

### Running the Lab

```sh
uv run labs/pydantic-ai/simple.py
```

### What You'll Observe

The script drops you into an interactive chat loop. Type any message and the agent replies using the local model. Type `/exit` to end the session.

The agent loop is provided entirely by `agent.to_cli_sync()` — no manual loop code is needed.

### Understanding the Code

Open `simple.py` and read it top to bottom:

1. **`OpenAIProvider`** — points Pydantic AI at `localhost:8080/v1`, where the local server listens.
2. **`OpenAIChatModel`** — wraps the provider so Pydantic AI can talk to it.
3. **`Agent`** — holds the model and a system prompt.
4. **`agent.to_cli_sync()`** — runs a built-in interactive REPL, handling the input loop and conversation history automatically.

### Experiments to Try

1. **Change the system prompt** — modify the string passed to `system_prompt=` and observe how the agent's tone and behavior shift.
2. **Structured output** — add `result_type=` to `Agent` with a Pydantic model and see how Pydantic AI validates the response.

## Lab 2 — Weather Agent (`weather.py`)

### Running the Lab

```sh
uv run labs/pydantic-ai/weather.py
```

### What You'll Observe

You enter a chat loop where you can ask about weather for any location and date range, for example:

```
❯ What is the weather forecast for Seattle this week?
```

The agent calls the `get_locations` tool to resolve the city to coordinates, then calls `get_weather_forecast` to retrieve the forecast from the [Open-Meteo](https://open-meteo.com/) API. Each tool call prints a progress line so you can follow the agent's reasoning in real time.

### Understanding the Code

Open `weather.py` and read it top to bottom:

1. **`@agent.system_prompt()`** — a function that runs before each request and injects today's date and the next 16 available forecast dates into the system prompt; this gives the model accurate temporal context without hardcoding anything.
2. **`get_locations` tool** — calls the Open-Meteo geocoding API to turn a place name into latitude/longitude coordinates.
3. **`get_weather_forecast` tool** — calls the Open-Meteo forecast API with the resolved coordinates and requested date range.
4. **`agent.to_cli_sync()`** — runs the interactive chat loop, preserving conversation history across turns.

### Experiments to Try

1. **Ask a multi-turn question** — ask for Seattle's forecast, then follow-up with "What about Portland?" and observe how the agent retains context.
2. **Request specific variables** — ask for snowfall or wind speed and see how the agent maps your request to the correct `WeatherVariables` values.
3. **Change units** — ask for temperatures in Celsius or wind speed in knots.

## Lab 3 — Database Agent (`database.py`)

The database agent answers natural-language questions about a SQLite database. It first inspects the schema, then writes and runs SELECT queries to answer your question.

### Running the Lab

```sh
uv run labs/pydantic-ai/database.py
```

### What You'll Observe

You enter a chat loop where you can ask questions in plain English, for example:

```
❯ Which customers placed the most orders last year?
```

The agent calls `get_schema` to understand the available tables, then calls `query_database` with a SQL SELECT statement and returns the results in a readable format.

### Understanding the Code

Open `database.py` and read it top to bottom:

1. **`get_schema` tool** — queries `sqlite_master` to return the DDL for every table, giving the model a complete picture of the database structure.
2. **`query_database` tool** — accepts a SQL string from the model, validates that it is a SELECT statement, and returns the rows as a list of dictionaries.
3. **Safety guard** — the tool raises `ValueError` if the query is not a SELECT, preventing the model from modifying data.
4. **`agent.to_cli_sync()`** — runs the interactive chat loop.

### Experiments to Try

1. **Ask aggregation questions** — try "How many orders did each customer place?" and observe the GROUP BY query the agent generates.
2. **Ask multi-table questions** — ask a question that requires a JOIN and inspect the SQL the agent constructs.
3. **Add a new tool** — add an `insert_row` tool that only accepts INSERT statements, and update the system prompt to allow writes. Observe how the agent's behavior changes.

## Going Further

These three agents share the same structure: an `OpenAIProvider`, an `OpenAIChatModel`, an `Agent`, and `agent.to_cli_sync()`. The differences are entirely in the tools and system prompts. This pattern scales to any domain — swap the tools and prompt for your own use case, and the rest of the framework handles the agentic loop.
