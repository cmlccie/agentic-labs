"""Main CLI application for Agentic LLM Labs."""

import typer

from .check_setup import check_setup_cmd
from .download_models import download_models_cmd

cli = typer.Typer(
    name="agentic-llm-labs",
    help="CLI tools for Agentic LLM Labs",
)

# Register commands
cli.command(name="check-setup")(check_setup_cmd)
cli.command(name="download-models")(download_models_cmd)


if __name__ == "__main__":
    cli()
