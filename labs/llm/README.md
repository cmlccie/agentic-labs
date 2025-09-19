# LLM Processing Pipeline

## What You'll Learn

This lab demonstrates the fundamental pipeline that transforms human conversations into LLM responses. You'll observe how messages are formatted, tokenized, and processed by language models, and discover why LLMs are stateless - requiring the full conversation history each time.

## The Four-Step Journey

### 1. Template Lab - Message Formatting

**What it does**: Converts your message into the model's expected format (the format it has been trained to expect).

```bash
uv run labs/llm/template.py
```

Enter any message and see how it gets wrapped with special tokens and system prompts. This is the first step in making your text "speak" the model's language.

### 2. Input Tokens Lab - From Messages to Model Input

**What it does**: Shows the full transformation from a conversation (`messages`) to the input array (token matrix) that the model receives for generation.

```bash
uv run labs/llm/input_tokens.py
```

Enter the same message and see how your conversation is formatted, tokenized, and turned into the exact input matrix that is fed into the model. This helps you understand the complete preprocessing pipeline from human text to model-ready input.

### 3. Response Lab - Single Generation

**What it does**: Processes tokens through the model to generate a response.

```bash
uv run labs/llm/respond.py
```

Enter a message and watch the complete pipeline in action. You'll see the raw model output including your original message plus the generated response.

### 4. Chat Lab - Conversation Management

**What it does**: Maintains conversation context across multiple exchanges.

```bash
uv run labs/llm/chat.py
```

Have a conversation with the model. Type `quit` or `exit` to end or `clear` to clear the conversation history. Notice how each response takes longer as the conversation grows - the model processes the entire conversation every time.

## What You Just Learned

You've witnessed the complete LLM pipeline:

1. **Messages** → **Formatted Template** (human conversation becomes structured input)
2. **Template** → **Token IDs** (text becomes numbers the model understands)
3. **Tokens** → **Model Processing** → **Response** (neural network generates new tokens)
4. **Stateless Nature** (each generation requires sending the full conversation history)

This same pipeline runs every time you interact with ChatGPT, Claude, or any other LLM - understanding it helps you work more effectively with AI systems.

## Key Insights

- **LLMs are stateless**: They don't remember previous conversations
- **Context window matters**: Longer conversations = more processing time and cost
- **Templates vary**: Different models format conversations differently
- **Tokens are everything**: Understanding tokenization helps optimize prompts and system designs.
