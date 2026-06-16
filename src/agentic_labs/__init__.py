"""Agentic Labs."""

from dataclasses import dataclass

# --------------------------------------------------------------------------------------
# Default Models & Model Info
# --------------------------------------------------------------------------------------


@dataclass
class ModelInfo:
    ignore_patterns: list[str] | None = None
    allow_patterns: list[str] | None = None


LAB_MODELS: dict[str, ModelInfo] = {
    "meta-llama/Llama-3.2-1B-Instruct": ModelInfo(),
    # Moving agent and tools labs to use LM Studio hosted models for better performance and reliability.
    # "bartowski/Llama-3.2-3B-Instruct-GGUF": ModelInfo(
    #     allow_patterns=["Llama-3.2-3B-Instruct-Q4_K_M.gguf"],
    # ),
}
