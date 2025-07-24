#!/usr/bin/env python3
"""Simple LLM Chat Lab.

Local Inference with HuggingFace Transformers Pipeline.
A minimal chat interface using a locally-hosted language model.
"""

import sys

from transformers import AutoTokenizer
from transformers.pipelines import pipeline

# --------------------------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------------------------

MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
SYSTEM_PROMPT = (
    "You are a helpful assistant. "
    "You will always respond in a helpful and informative manner. "
    "If you don't know the answer, you will say 'I don't know'. "
    "If you are unsure about something, ask for clarification. "
)
TEMPERATURE = 0.8
REPETITION_PENALTY = 1.1
GENERATE_MAX_TOKENS = 100

USER_PROMPT = "\n\033[94m❯ \033[0m"  # Blue arrow


# --------------------------------------------------------------------------------------
# Create Chat Pipeline
# --------------------------------------------------------------------------------------


def create_chat_pipeline():
    """Create a text generation pipeline with the specified model."""

    print(f"Loading model: {MODEL_NAME}")
    print("This may take a few minutes on first run (downloading model)...")

    # Load tokenizer first to get special token IDs
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    # Get pad token ID - use eos_token_id if pad_token_id doesn't exist
    pad_token_id = (
        tokenizer.pad_token_id
        if tokenizer.pad_token_id is not None
        else tokenizer.eos_token_id
    )

    # Create the pipeline - this will automatically download the model if needed
    chat_pipeline = pipeline(
        "text-generation",
        model=MODEL_NAME,
        tokenizer=tokenizer,
        pad_token_id=pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
        device_map="auto",  # Automatically use GPU if available
        torch_dtype="auto",  # Use optimal precision
    )

    print("Model loaded successfully!\n")

    return chat_pipeline


# --------------------------------------------------------------------------------------
# Chat Loop
# --------------------------------------------------------------------------------------


def chat_with_model(chat_pipeline):
    """Interactive chat loop with the loaded model."""

    print("LLM Chat Lab - Local Inference")
    print("==============================")
    print()
    print("Type 'quit', 'exit', or 'bye' to end the conversation")
    print("Type 'clear' to reset conversation history")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Chat loop
    while True:
        try:
            user_prompt = input(USER_PROMPT).strip()

            # Handle special commands
            if user_prompt.lower().strip() in ["quit", "exit", "bye"]:
                print("\n👋 Thanks for chatting! Goodbye!")
                break

            elif user_prompt.lower() == "clear":
                messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                print("\n🧹 Conversation history cleared!")
                continue

            # Handle empty input
            elif not user_prompt:
                continue

            # Add user prompt to context
            else:
                messages.append({"role": "user", "content": user_prompt})

            # Prepare context for the model
            context = tokenizer.apply_chat_template(
                messages,
                tokenize=False,  # The pipeline will handle tokenization
                add_generation_prompt=True,  # Add generation prompt for the model
            )

            # Generate a response
            response = chat_pipeline(
                context,
                temperature=TEMPERATURE,
                max_new_tokens=GENERATE_MAX_TOKENS,
                repetition_penalty=REPETITION_PENALTY,
                do_sample=True,
            )

            # Extract and clean-up the generated text
            generated_text = response[0]["generated_text"][len(context) :].strip()

            # Update context with the new response
            messages.append({"role": "assistant", "content": generated_text})

            print(f"\n{generated_text}")

        except KeyboardInterrupt:
            print("\n\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.\n")


def main():
    """Initialize and run the chat application."""
    try:
        # Create the chat pipeline
        chat_pipeline = create_chat_pipeline()

        # Start the interactive chat
        chat_with_model(chat_pipeline)

    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        print("Make sure you have installed the dependencies with: uv sync")
        sys.exit(1)


if __name__ == "__main__":
    main()
