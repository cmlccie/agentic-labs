"""Check setup command for Agentic Labs CLI."""

import shutil
import subprocess
from typing import List, Optional, Tuple

import click
import typer
from huggingface_hub import whoami
from huggingface_hub.errors import HfHubHTTPError

# --------------------------------------------------------------------------------------
# CLI Command
# --------------------------------------------------------------------------------------


def check_setup() -> None:
    """Check that the environment is properly set up for the labs.

    This function verifies that users have correctly set up their environment
    for the Agentic Labs.
    """
    click.echo("🔍 Checking Agentic Labs environment setup...\n")

    checks = [
        _check_uv_installed,
        _check_huggingface_token,
    ]

    results = []
    overall_success = True

    for check_func in checks:
        try:
            success, message, details = check_func()
            results.append((success, message, details))

            if success:
                click.echo(f"✅ {message}")
            else:
                click.echo(f"❌ {message}")
                overall_success = False

        except Exception as e:
            click.echo(f"❌ Unexpected error during check: {e}")
            overall_success = False

    # Summary
    click.echo("\n📊 Setup Check Summary:")
    passed = sum(1 for success, _, _ in results if success)
    total = len(results)
    click.echo(f"   ✅ Passed: {passed}/{total}")

    if overall_success:
        click.echo("\n🎉 Environment is properly set up! You're ready to run the labs.")
    else:
        click.echo(
            f"\n⚠️  {total - passed} issue(s) found. Please address them before running the labs."
        )

        click.echo("\n💡 Troubleshooting tips:")
        click.echo("   • Check the repository README for setup instructions")

        raise typer.Exit(1)


# --------------------------------------------------------------------------------------
# Environment Checks
# --------------------------------------------------------------------------------------


def _check_uv_installed() -> Tuple[bool, str, Optional[List[str]]]:
    """Check if uv package manager is installed and accessible."""
    details = []

    # Check if uv is in PATH
    uv_path = shutil.which("uv")
    if not uv_path:
        message = "uv package manager not found in PATH"
        return False, message, details

    # Check uv version
    try:
        subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )

    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        message = f"uv is installed but not working properly: {e}"
        return False, message, details

    return True, "uv package manager is installed and working", details


def _check_huggingface_token() -> Tuple[bool, str, Optional[List[str]]]:
    """Check if HuggingFace CLI is configured with a valid token."""
    details = []

    # Check if hf (or legacy huggingface-cli) is available
    hf_cli_path = shutil.which("hf") or shutil.which("huggingface-cli")
    if not hf_cli_path:
        message = "HuggingFace CLI (hf) not found in PATH"
        details.append("HuggingFace CLI should be installed with project dependencies")
        details.append("Try running: uv sync")
        return False, message, details

    # Check if user is logged in by trying to get user info
    try:
        user_info = whoami()
        if user_info is None:
            message = "HuggingFace token not configured"
            details.append("Run 'uv run hf login' to configure your token")
            return False, message, details

        # Successfully got user info
        username = user_info.get("name", "unknown")
        return True, f"HuggingFace CLI is configured (logged in as {username})", details

    except HfHubHTTPError as e:
        if e.response.status_code == 401:
            message = "HuggingFace token is invalid or expired"
            details.append("Run 'uv run hf login' with a valid token")
        else:
            message = f"Error checking HuggingFace authentication: {e}"
        return False, message, details

    except Exception as e:
        message = f"Unexpected error checking HuggingFace authentication: {e}"
        return False, message, details
