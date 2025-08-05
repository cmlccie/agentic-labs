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

This lab uses a local LLM server via LM Studio. Make sure you have:

1. LM Studio running locally on port 1234
2. A compatible model loaded (the script uses `ministral-8b-instruct-2410`)

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

### Tool Definitions (`tools.py`)

The tools module exports two key components:

- `functions`: A dictionary mapping function names to executable Python functions.
- `tools`: OpenAI-compatible tool descriptions that tell the LLM what functions are available.

### Agent Loop (`weather.py`)

The main script implements the agent pattern:

1. **Message Management**: Maintains conversation history in OpenAI message format
2. **Tool Call Detection**: Checks if the LLM response includes tool calls
3. **Tool Execution**: Runs requested functions and adds results to conversation
4. **Iterative Processing**: Continues until no more tool calls are needed

### Key Implementation Details

- **Stateless Context**: Every LLM call includes the complete conversation history.
- **Tool Call Loop**: The `while completion.choices[0].message.tool_calls:` loop handles multiple tool calls.
- **Message Threading**: Tool calls and results are properly added to maintain conversation context.

## Experiments to Try

1. **Break the chain**: Ask for weather without specifying a location - observe how the LLM handles missing information.
2. **Multiple locations**: Ask about weather in multiple cities in one request.
3. **Context building**: Ask follow-up questions about the same location - notice how previous tool results remain in context.

This lab illustrates how agents coordinate between stateless LLMs and external tools to create interactive, capable AI systems.
