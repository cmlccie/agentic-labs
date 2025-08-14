# Local Weather Agent Lab

This lab demonstrates a simple local weather agent that uses tools to provide weather information. You'll learn about the distinction between agents and tools, how LLMs call tools, and the iterative nature of tool-based conversations.

## Key Concepts

### Agents vs Tools

- **Agent**: The complete system that orchestrates the conversation, manages context, and executes tool calls. The agent handles the flow between user input, LLM responses, tool execution, and final output.
- **Tools**: Specific functions that the LLM can request to perform actions or retrieve information.

### Stateless LLMs and Tool Calling

LLMs are stateless - they don't remember previous interactions. Every request must include all the context you want the LLM to consider when generating a response.

When using tools, we have to use an iterative process:

1. Send user input (includes full conversation history) to LLM
2. LLM determines it needs additional context and responds with a request to call tool(s)
3. Agent executes the requested tool call(s)
4. Agent adds tool calls and results to the conversation history
5. Agent sends a new request to the LLM with the full conversation history (original conversation history + tool call requests + tool call responses)
6. Repeat until LLM provides a final response that will be returned to the user

## Setup

This lab uses HuggingFace Transformers to run the Llama-3.1-8B-Instruct model locally. Make sure you have:

1. A compatible GPU with sufficient VRAM (16GB+ recommended for the 8B model)
2. Access to the Meta Llama models on HuggingFace (may require accepting license terms)

## Running the Lab

Start the weather agent:

```bash
uv run labs/local-agent/weather.py
```

Try these example queries:

- "What's the weather in New York?"
- "How's the weather in London?"
- "Is it going to rain in Tokyo today?"

Type `quit` or `exit` to end the conversation.

## What You'll Observe

When you ask about weather in a location, you'll see the agent:

1. **First LLM call**: The model receives your question and decides it needs location coordinates
2. **Tool execution**: The agent calls `get_coordinates()` to find the latitude/longitude
3. **Second LLM call**: The model receives the coordinates and decides it needs weather data
4. **Tool execution**: The agent calls `get_weather()` with the coordinates
5. **Final LLM call**: The model receives weather data and formats a human-readable response

Each step adds more context to the conversation, building up the information needed for the final response.

## Understanding the Code

### Tool Functions (`tools.py`)

Two weather-related tools are available:

- `get_coordinates()`: Uses OpenMeteo's geocoding API to convert location names to coordinates
- `get_weather()`: Uses OpenMeteo's forecast API to get weather data for specific coordinates

### Agent Loop (`weather.py`)

The main script implements the agent pattern using HuggingFace Transformers:

1. **Model Setup**: Loads Llama-3.1-8B-Instruct using the transformers pipeline
2. **Template Rendering**: Uses the tokenizer's chat template with tool definitions
3. **Tool Call Detection**: Parses JSON responses to detect tool requests
4. **Tool Execution**: Uses pattern matching to route tool calls to the correct functions
5. **Iterative Processing**: Continues until no more tool calls are needed

### Key Implementation Details

- **Local Model**: Runs Llama-3.1-8B-Instruct directly using HuggingFace Transformers
- **Chat Templates**: Uses the model's built-in chat template with tool support
- **Pattern Matching**: Uses Python 3.10+ `match` statements for tool routing
- **Message Threading**: Tool calls and results are properly added to maintain conversation context

## Experiments to Try

1. **Break the chain**: Ask for weather without specifying a location - observe how the LLM handles missing information.
2. **Multiple locations**: Ask about weather in multiple cities in one request.
3. **Context building**: Ask follow-up questions about the same location - notice how previous tool results remain in context.
4. **Model behavior**: Observe how the model decides when to call tools vs. when to provide direct responses.

This lab illustrates how agents coordinate between local LLMs and external tools to create interactive, capable AI systems using modern Python features like structural pattern matching.
