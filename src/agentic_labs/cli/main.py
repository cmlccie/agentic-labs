"""Main CLI application for Agentic Labs."""

import typer

from .check_setup import check_setup
from .download_models import download_models
from .local_llm import local_llm_cmd

cli = typer.Typer(
    name="agentic-labs",
    help="CLI tools for Agentic Labs",
)

# Register commands
cli.command(name="check-setup")(check_setup)
cli.command(name="download-models")(download_models)
cli.command(name="local-llm")(local_llm_cmd)


if __name__ == "__main__":
    cli()
