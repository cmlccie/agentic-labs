"""Local LLM engine — starts an OpenAI-compatible server backed by llama-cpp-python."""

from __future__ import annotations

import logging
import socket
import threading
import time
from pathlib import Path

from huggingface_hub import hf_hub_download

logger = logging.getLogger(__name__)

GGUF_MODELS: dict[str, dict[str, str]] = {
    "bartowski/Llama-3.2-1B-Instruct-GGUF": {
        "repo": "bartowski/Llama-3.2-1B-Instruct-GGUF",
        "filename": "Llama-3.2-1B-Instruct-Q4_K_M.gguf",
    },
    "bartowski/Llama-3.2-3B-Instruct-GGUF": {
        "repo": "bartowski/Llama-3.2-3B-Instruct-GGUF",
        "filename": "Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    },
}

_server_started = False


def _download_model(model_key: str) -> Path:
    """Download the GGUF model file from HuggingFace Hub and return its local path.

    Models are public and do not require a HuggingFace token. The file is
    cached in the default HuggingFace cache directory (~/.cache/huggingface/).
    """
    if model_key not in GGUF_MODELS:
        available = ", ".join(GGUF_MODELS.keys())
        raise ValueError(f"Unknown model '{model_key}'. Available models: {available}")
    meta = GGUF_MODELS[model_key]
    logger.debug(f"Downloading model '{model_key}' from {meta['repo']}")
    path = hf_hub_download(repo_id=meta["repo"], filename=meta["filename"])
    return Path(path)


def _start_server(model_path: Path, port: int) -> None:
    """Start the llama-cpp-python OpenAI-compatible server in the current thread.

    This function blocks indefinitely and is meant to be run in a daemon thread.
    """
    from llama_cpp.server.app import create_app
    from llama_cpp.server.settings import ModelSettings, ServerSettings
    import uvicorn

    model_settings = ModelSettings(
        model=str(model_path),
        n_gpu_layers=-1,
        n_ctx=4096,
        chat_format="llama-3",
    )
    server_settings = ServerSettings(port=port, api_key="local")
    app = create_app(server_settings=server_settings, model_settings=[model_settings])
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error")
    uvicorn.Server(config).run()


def start_local_llm(model: str = "bartowski/Llama-3.2-3B-Instruct-GGUF", port: int = 8080) -> str:
    """Download (if needed) and start a local LLM server.

    Starts an OpenAI-compatible REST server backed by llama-cpp-python.
    The server runs in a daemon thread and exits automatically when the
    calling script exits — no cleanup required.

    Subsequent calls with the same port are no-ops and return the same URL.

    Args:
        model: Key from GGUF_MODELS. Defaults to "bartowski/Llama-3.2-3B-Instruct-GGUF".
        port:  Local port for the server. Defaults to 8080.

    Returns:
        The base URL for OpenAI-compatible clients, e.g. ``http://127.0.0.1:8080/v1``.
    """
    global _server_started
    if _server_started:
        return f"http://127.0.0.1:{port}/v1"

    print(f"Loading model '{model}'... (first run downloads ~2 GB)")
    model_path = _download_model(model)

    thread = threading.Thread(
        target=_start_server, args=(model_path, port), daemon=True
    )
    thread.start()

    # Poll until the server accepts connections or the thread dies.
    deadline = time.time() + 60
    while time.time() < deadline:
        if not thread.is_alive():
            raise RuntimeError("LLM server thread exited unexpectedly. Check logs above.")
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                break
        except OSError:
            time.sleep(0.5)
    else:
        raise RuntimeError(f"LLM server did not start within 60 seconds on port {port}.")

    _server_started = True
    print("Model ready.\n")
    return f"http://127.0.0.1:{port}/v1"
