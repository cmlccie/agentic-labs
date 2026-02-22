"""Download models command for Agentic Labs CLI."""

import logging

import click
import typer
from huggingface_hub import snapshot_download
from huggingface_hub.errors import HfHubHTTPError

from agentic_labs import LAB_MODELS

DEFAULT_IGNORE_PATTERNS = [
    "original/*",
    "*.bin",
]

DEFAULT_ALLOW_PATTERNS = [
    "*.safetensors*",
    "*.json",
    "tokenizer*",
    "*.txt",
    "*.md",
    ".gitattributes",
    "generation_config.json",
]

# --------------------------------------------------------------------------------------
# CLI Command
# --------------------------------------------------------------------------------------


def download_models() -> None:
    """Download models from HuggingFace Hub for use in the labs.

    This command downloads the models used by the Agentic Labs to your local
    machine.
    """
    click.echo(f"📦 Downloading {len(LAB_MODELS)} model(s)...")
    success_count = 0
    error_count = 0

    for model_name, model_info in LAB_MODELS.items():
        click.echo(f"\n🔄 Downloading {model_name}...")

        try:
            snapshot_download(
                repo_id=model_name,
                local_files_only=False,
                ignore_patterns=model_info.ignore_patterns or DEFAULT_IGNORE_PATTERNS,
                allow_patterns=model_info.allow_patterns or DEFAULT_ALLOW_PATTERNS,
            )

            click.echo(f"✅ Successfully downloaded {model_name}")
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
