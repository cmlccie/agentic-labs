"""Local LLM command — starts an OpenAI-compatible server backed by llama-cpp-python."""

from typing import Annotated

import click
import typer
import uvicorn
from huggingface_hub import hf_hub_download
from llama_cpp.server.app import create_app
from llama_cpp.server.settings import ModelSettings, ServerSettings

from agentic_labs import LAB_MODELS

DEFAULT_MODEL = "bartowski/Llama-3.2-3B-Instruct-GGUF"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8080
DEFAULT_CONTEXT_WINDOW = 8192


# --------------------------------------------------------------------------------------
# CLI Command
# --------------------------------------------------------------------------------------


def local_llm_cmd(
    model: Annotated[
        str,
        typer.Option(
            "--model",
            "-m",
            help="GGUF model to serve. Must be a key in LAB_MODELS with a .gguf allow_pattern.",
        ),
    ] = DEFAULT_MODEL,
    host: Annotated[
        str,
        typer.Option(
            "--host",
            help="Host address to bind the server to.",
        ),
    ] = DEFAULT_HOST,
    port: Annotated[
        int,
        typer.Option(
            "--port",
            "-p",
            help="Port to run the server on.",
        ),
    ] = DEFAULT_PORT,
    context_window: Annotated[
        int,
        typer.Option(
            "--context-window",
            "-c",
            help="Context window size (number of tokens).",
        ),
    ] = DEFAULT_CONTEXT_WINDOW,
) -> None:
    """Start a local OpenAI-compatible LLM server.

    Serves a GGUF model using llama-cpp-python with an OpenAI-compatible REST
    API. The model must already be downloaded — run 'agentic-labs download-models'
    first.

    The server runs in the foreground and can be stopped with Ctrl+C.
    """
    model_path = _resolve_model_path(model)

    click.echo("🚀 Starting local LLM server...")
    click.echo(f"   Model:          {model}")
    click.echo(f"   Context window: {context_window}")
    click.echo(f"   Endpoint:       http://{host}:{port}/v1")
    click.echo("   API key:        local")
    click.echo()

    model_settings = ModelSettings(
        model=str(model_path),
        n_gpu_layers=-1,
        n_ctx=context_window,
        chat_format="llama-3",
    )
    server_settings = ServerSettings(host=host, port=port, api_key="local")
    app = create_app(server_settings=server_settings, model_settings=[model_settings])

    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    uvicorn.Server(config).run()


# --------------------------------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------------------------------


def _resolve_model_path(model: str) -> str:
    """Resolve a model key to a local file path using the HuggingFace cache.

    Looks up the model in LAB_MODELS to find the GGUF filename from
    allow_patterns, then checks the local HuggingFace cache for the file.

    Raises a friendly error if the model is not recognized or not yet
    downloaded.
    """
    if model not in LAB_MODELS:
        available = ", ".join(LAB_MODELS.keys())
        click.echo(
            f"❌ Unknown model '{model}'.\n   Available models: {available}",
            err=True,
        )
        raise typer.Exit(1)

    info = LAB_MODELS[model]
    gguf_files = [p for p in (info.allow_patterns or []) if p.endswith(".gguf")]

    if not gguf_files:
        click.echo(
            f"❌ Model '{model}' has no GGUF file in its allow_patterns.\n"
            f"   This model cannot be served with the local LLM server.",
            err=True,
        )
        raise typer.Exit(1)

    filename = gguf_files[0]

    try:
        path = hf_hub_download(repo_id=model, filename=filename, local_files_only=True)
    except Exception:
        click.echo(
            f"❌ Model '{model}' is not downloaded yet.\n"
            f"   Run 'agentic-labs download-models' first to download it.",
            err=True,
        )
        raise typer.Exit(1) from None

    return path
