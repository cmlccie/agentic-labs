"""Download models command for Agentic LLM Labs CLI."""

import logging
from pathlib import Path
from typing import Annotated, List, Optional

import click
import typer
from huggingface_hub import snapshot_download
from huggingface_hub.errors import HfHubHTTPError

import agentic_llm_labs.logging
from agentic_llm_labs import LAB_MODELS

# --------------------------------------------------------------------------------------
# CLI Command
# --------------------------------------------------------------------------------------


def download_models_cmd(
    models: Annotated[
        Optional[List[str]],
        typer.Option(
            "--model",
            "-m",
            help="Specify models to download. Can be used multiple times. If not specified, downloads default models used in labs.",
        ),
    ] = None,
    cache_dir: Annotated[
        Optional[Path],
        typer.Option(
            "--cache-dir",
            "-c",
            help="Directory to store downloaded models. Defaults to HuggingFace cache.",
        ),
    ] = None,
    force_download: Annotated[
        bool,
        typer.Option(
            "--force",
            "-f",
            help="Force re-download even if models are already cached.",
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Enable verbose logging.",
        ),
    ] = False,
) -> None:
    """Download models from HuggingFace Hub for use in the labs.

    This command downloads the models used by the Agentic LLM Labs to your local
    machine. By default, it downloads all models used in the repository labs.
    """
    return download_models(
        models=models,
        cache_dir=cache_dir,
        force_download=force_download,
        verbose=verbose,
    )


# --------------------------------------------------------------------------------------
# Functions
# --------------------------------------------------------------------------------------


def download_models(
    models: Optional[List[str]] = None,
    cache_dir: Optional[Path] = None,
    force_download: bool = False,
    verbose: bool = False,
) -> None:
    """Download models from HuggingFace Hub for use in the labs.

    This command downloads the models used by the Agentic LLM Labs to your local
    machine. By default, it downloads all models used in the repository labs.
    """
    # Configure logging
    if verbose:
        agentic_llm_labs.logging.fancy_config(level=logging.INFO)
    else:
        agentic_llm_labs.logging.colorized_config(level=logging.WARNING)

    # Use default models if none specified
    models_to_download = models if models else LAB_MODELS

    click.echo(f"📦 Downloading {len(models_to_download)} model(s)...")
    if verbose:
        click.echo(f"Models: {', '.join(models_to_download)}")
        click.echo(
            "🎯 Excluding original/ files and focusing on essential lab files (.safetensors, configs, tokenizers)"
        )

    success_count = 0
    error_count = 0

    for model_name in models_to_download:
        click.echo(f"\n🔄 Downloading {model_name}...")

        try:
            # Download the model, excluding original/ files and focusing on essential files
            local_path = snapshot_download(
                repo_id=model_name,
                cache_dir=cache_dir,
                force_download=force_download,
                local_files_only=False,
                ignore_patterns=[
                    "original/*",  # Exclude all files in the original/ directory
                    "*.bin",  # Exclude legacy .bin files (prefer .safetensors)
                ],
                allow_patterns=[
                    "*.safetensors*",  # Model weights in safetensors format
                    "*.json",  # Configuration files
                    "tokenizer*",  # Tokenizer files
                    "*.txt",  # License, README, etc.
                    "*.md",  # Documentation files
                    ".gitattributes",  # Git attributes
                    "generation_config.json",  # Generation configuration
                ],
            )

            click.echo(f"✅ Successfully downloaded {model_name}")
            if verbose:
                click.echo(f"   Cached at: {local_path}")

            success_count += 1

        except HfHubHTTPError as e:
            if e.response.status_code == 401:
                click.echo(
                    f"❌ Authentication error for {model_name}. "
                    f"Please ensure you're logged in with 'uv run huggingface-cli login' "
                    f"and have access to this model.",
                    err=True,
                )
            elif e.response.status_code == 403:
                click.echo(
                    f"❌ Access denied for {model_name}. "
                    f"Please request access to this model on HuggingFace Hub.",
                    err=True,
                )
            else:
                click.echo(f"❌ HTTP error downloading {model_name}: {e}", err=True)

            error_count += 1
            logging.error(f"Failed to download {model_name}: {e}")

        except Exception as e:
            click.echo(f"❌ Unexpected error downloading {model_name}: {e}", err=True)
            error_count += 1
            logging.error(f"Failed to download {model_name}: {e}")

    # Summary
    click.echo("\n📊 Download Summary:")
    click.echo(f"   ✅ Successful: {success_count}")
    click.echo(f"   ❌ Failed: {error_count}")

    if error_count > 0:
        click.echo("\n💡 Troubleshooting tips:")
        click.echo("   • Ensure you're logged in: uv run huggingface-cli login")
        click.echo("   • Request access to gated models on HuggingFace Hub")
        click.echo("   • Check your internet connection")
        raise typer.Exit(1)
    else:
        click.echo("\n🎉 All models downloaded successfully!")
