# Local Weather Agent Lab

This lab demonstrates a simple local weather agent that uses tools to provide weather information. You'll learn about the distinction between agents and tools, how LLMs call tools, and the iterative nature of tool-based conversations.

## Key Concepts

### Agents vs Tools

- **Agent**: The complete system that orchestrates the conversation, manages context, and executes tool calls. The agent handles the flow between user input, LLM responses, tool execution, and final output.
- **Tools**: Specific functions that the LLM can request to perform actions or retrieve information.

### Stateless LLMs and Tool Calling

LLMs are stateless - they don't remember previous interactions. Every request must include all the context you want the LLM to consider when generating a response.

When using tools, we use an iterative process:

1. Send full conversation history and descriptions of available tools to the LLM to generate a response.
2. If the LLM determines it needs additional context, it responds with a tool request.
3. The agent calls the requested tools.
4. The agent adds both the tool request and tool results to the conversation history.
5. Repeat steps 1-4 until the LLM provides a response without a tool request.
6. Send the LLM's final response to the user.

## Note on System Requirements

This lab uses HuggingFace Transformers to run the Llama-3.2-3B-Instruct model locally. This model can run on:

1. **CPU**: Works on most modern laptops (16GB+ RAM recommended, as the model will use ~6GB).
2. **GPU**: Any compatible GPU with 8GB+ VRAM for faster inference.

The smaller 3B model makes this lab accessible on developer laptops without requiring high-end hardware.

## Running the Lab

Run the weather agent script:

```bash
uv run labs/local-agent/weather.py
```

Try these example queries:

- "What's the weather in New York?"
- "How's the weather in London?"
- "Is it going to rain in Tokyo today?"

Type `quit` or `exit` to end the conversation or `clear` to clear the conversation history.

## What You'll Observe

When you ask about weather in a location, you'll see the agent perform the following steps:

1. **First LLM call**: The model receives your question, decides it needs coordinates for the location, and returns a `get_coordinates` tool request.
2. **First tool call**: The agent calls `get_coordinates()` to obtain the latitude/longitude for the location and adds both the tool request and results to the conversation.
3. **Second LLM call**: The model receives the conversation with the coordinates in the context, decides it needs weather data for the coordinates, and returns a `get_weather` tool request.
4. **Second tool call**: The agent calls `get_weather()` with the coordinates and adds both the tool request and results to the conversation.
5. **Final LLM call**: The model receives the conversation with your original question, the coordinates for the location, and the weather data for those coordinates and generates a human-readable response.

Each step adds more context to the conversation, building up the information needed for the final response.

## Understanding the Code

### Tool Functions (`tools.py`)

Two weather-related tools are available:

- `get_coordinates()` - Uses OpenMeteo's geocoding API to convert location names to coordinates
- `get_weather()` - Uses OpenMeteo's forecast API to get weather data for specific coordinates

### Agent Loop (`weather.py`)

The main script implements the agent pattern using HuggingFace Transformers:

1. **Model Setup** - Loads Llama-3.2-3B-Instruct using the transformers pipeline
2. **Template Rendering** - Uses the tokenizer's chat template with tool definitions
3. **Tool Request Detection** - Attempts to parse the model's response to determine if it is a JSON tool request
4. **Tool Execution** - Uses pattern matching to route tool requests to the correct functions
5. **Iterative Processing** - Continues until no more tool calls are needed

### Key Implementation Details

- **Local Model** - Runs Llama-3.2-3B-Instruct directly using HuggingFace Transformers
- **Chat Templates** - Uses the model's built-in chat template with tool support
- **Pattern Matching** - Uses Python 3.10+ `match` statements for routing tool requests
- **Conversation Management** - Adds tool requests and results to the conversation to enrich the context

## Experiments to Try

1. **Break the chain** - Ask for weather without specifying a location and observe how the LLM handles missing information.
2. **Multiple locations** - Ask about weather in multiple cities in one request.
3. **Context building** - Ask follow-up questions about the same location and notice how previous tool results remain in context.
4. **Model behavior** - Observe how the model decides when to call tools vs. when to provide direct responses.

This lab illustrates how agents coordinate between local LLMs and external tools to create interactive, capable AI systems using modern Python features like structural pattern matching.
