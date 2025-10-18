"""Check setup command for Agentic LLM Labs CLI."""

import logging
import shutil
import subprocess
from pathlib import Path
from typing import Annotated, List, Optional, Tuple

import click
import typer
from huggingface_hub import whoami
from huggingface_hub.errors import HfHubHTTPError

import agentic_llm_labs.logging

# --------------------------------------------------------------------------------------
# CLI Command
# --------------------------------------------------------------------------------------


def check_setup_cmd(
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Enable verbose output with detailed information about each check.",
        ),
    ] = False,
    fix: Annotated[
        bool,
        typer.Option(
            "--fix",
            "-f",
            help="Attempt to automatically fix common setup issues.",
        ),
    ] = False,
) -> None:
    """Check that the environment is properly set up for the labs.

    This command verifies that users have correctly and completely set up their
    environment for the Agentic LLM Labs.
    """
    return check_setup(verbose=verbose, fix=fix)


# --------------------------------------------------------------------------------------
# Functions
# --------------------------------------------------------------------------------------


def check_setup(
    verbose: bool = False,
    fix: bool = False,
) -> None:
    """Check that the environment is properly set up for the labs.

    This function verifies that users have correctly and completely set up their
    environment for the Agentic LLM Labs.
    """
    # Configure logging
    if verbose:
        agentic_llm_labs.logging.fancy_config(level=logging.INFO)
    else:
        agentic_llm_labs.logging.colorized_config(level=logging.WARNING)

    click.echo("🔍 Checking Agentic LLM Labs environment setup...\n")

    checks = [
        _check_uv_installed,
        _check_project_dependencies,
        _check_huggingface_token,
    ]

    results = []
    overall_success = True

    for check_func in checks:
        try:
            success, message, details = check_func(verbose=verbose, fix=fix)
            results.append((success, message, details))

            if success:
                click.echo(f"✅ {message}")
            else:
                click.echo(f"❌ {message}")
                overall_success = False

            if details and verbose:
                for detail in details:
                    click.echo(f"   {detail}")

        except Exception as e:
            click.echo(f"❌ Unexpected error during check: {e}")
            logging.error(f"Check failed with error: {e}")
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

        if not fix:
            click.echo("\n💡 Troubleshooting tips:")
            click.echo("   • Run with --fix to attempt automatic fixes")
            click.echo("   • Run with --verbose for detailed information")
            click.echo("   • Check the repository README for setup instructions")

        raise typer.Exit(1)


# --------------------------------------------------------------------------------------
# Environment Checks
# --------------------------------------------------------------------------------------


def _check_uv_installed(
    verbose: bool = False, fix: bool = False
) -> Tuple[bool, str, Optional[List[str]]]:
    """Check if uv package manager is installed and accessible."""
    details = []

    # Check if uv is in PATH
    uv_path = shutil.which("uv")
    if not uv_path:
        message = "uv package manager not found in PATH"
        if fix:
            details.append(
                "⚠️  Cannot automatically install uv. Please install manually:"
            )
            details.append("   curl -LsSf https://astral.sh/uv/install.sh | sh")
            details.append(
                "   Or visit: https://docs.astral.sh/uv/getting-started/installation/"
            )
        return False, message, details

    if verbose:
        details.append(f"Found uv at: {uv_path}")

    # Check uv version
    try:
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        version = result.stdout.strip()
        if verbose:
            details.append(f"Version: {version}")

    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        message = f"uv is installed but not working properly: {e}"
        return False, message, details

    return True, "uv package manager is installed and working", details


def _check_project_dependencies(
    verbose: bool = False, fix: bool = False
) -> Tuple[bool, str, Optional[List[str]]]:
    """Check if project dependencies are installed and up to date."""
    details = []

    # Check if we're in a uv project
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        message = "Not in a uv project directory (pyproject.toml not found)"
        return False, message, details

    # Check if uv.lock exists (indicates dependencies have been resolved)
    lock_path = Path("uv.lock")
    if not lock_path.exists():
        message = "Dependencies not installed (uv.lock not found)"
        if fix:
            details.append("🔧 Attempting to install dependencies...")
            try:
                subprocess.run(
                    ["uv", "sync"],
                    check=True,
                    timeout=300,  # 5 minutes timeout
                )
                details.append("✅ Dependencies installed successfully")
                return True, "Project dependencies are now installed", details
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                details.append(f"❌ Failed to install dependencies: {e}")
                details.append("Please run manually: uv sync")
        return False, message, details

    if verbose:
        details.append("Found uv.lock - dependencies appear to be installed")

    # Check if dependencies are up to date by checking sync status
    try:
        result = subprocess.run(
            ["uv", "sync", "--dry-run"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        # If dry-run shows changes needed, dependencies are out of sync
        if "would" in result.stdout.lower() or "installing" in result.stdout.lower():
            message = "Dependencies are out of sync"
            if fix:
                details.append("🔧 Attempting to sync dependencies...")
                try:
                    subprocess.run(
                        ["uv", "sync"],
                        check=True,
                        timeout=300,
                    )
                    details.append("✅ Dependencies synced successfully")
                    return True, "Project dependencies are now up to date", details
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                    details.append(f"❌ Failed to sync dependencies: {e}")
                    details.append("Please run manually: uv sync")
            else:
                details.append("Run 'uv sync' to update dependencies")
            return False, message, details

    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        if verbose:
            details.append(f"Could not check sync status: {e}")
        # Assume dependencies are OK if we can't check

    # Verify key lab dependencies can be imported
    # (Excludes CLI dependencies like click/typer since they must be working for this to run)
    key_dependencies = [
        ("transformers", "Transformers"),
        ("torch", "PyTorch"),
        ("accelerate", "Accelerate"),
        ("openai", "OpenAI"),
        ("huggingface_hub", "HuggingFace Hub"),
        ("requests", "Requests"),
        ("tabulate", "Tabulate"),
    ]

    missing_imports = []
    for module_name, display_name in key_dependencies:
        try:
            __import__(module_name)
            if verbose:
                details.append(f"✓ {display_name} can be imported")
        except ImportError as e:
            missing_imports.append((display_name, module_name, str(e)))
            if verbose:
                details.append(f"✗ {display_name} cannot be imported: {e}")

    if missing_imports:
        message = f"Cannot import {len(missing_imports)} key dependencies"
        for display_name, module_name, error in missing_imports:
            details.append(f"❌ {display_name} ({module_name}): {error}")
        if fix:
            details.append("🔧 Attempting to reinstall dependencies...")
            try:
                subprocess.run(
                    ["uv", "sync", "--reinstall"],
                    check=True,
                    timeout=300,
                )
                details.append("✅ Dependencies reinstalled successfully")
                details.append("⚠️  Please run the check again to verify imports")
                return False, message, details
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                details.append(f"❌ Failed to reinstall dependencies: {e}")
                details.append("Please run manually: uv sync --reinstall")
        else:
            details.append("Run 'uv sync --reinstall' to fix import issues")
        return False, message, details

    return True, "Project dependencies are installed and up to date", details


def _check_huggingface_token(
    verbose: bool = False, fix: bool = False
) -> Tuple[bool, str, Optional[List[str]]]:
    """Check if HuggingFace CLI is configured with a valid token."""
    details = []

    # Check if huggingface-cli is available
    hf_cli_path = shutil.which("huggingface-cli")
    if not hf_cli_path:
        message = "huggingface-cli not found in PATH"
        details.append("HuggingFace CLI should be installed with project dependencies")
        details.append("Try running: uv sync")
        return False, message, details

    if verbose:
        details.append(f"Found huggingface-cli at: {hf_cli_path}")

    # Check if user is logged in by trying to get user info
    try:
        user_info = whoami()
        if user_info is None:
            message = "HuggingFace token not configured"
            if fix:
                details.append("🔧 Please log in to HuggingFace manually:")
                details.append("   uv run huggingface-cli login")
                details.append("   Then paste your HuggingFace token when prompted")
            else:
                details.append(
                    "Run 'uv run huggingface-cli login' to configure your token"
                )
            return False, message, details

        # Successfully got user info
        username = user_info.get("name", "unknown")
        if verbose:
            details.append(f"Logged in as: {username}")
            if "orgs" in user_info:
                orgs = [org.get("name", "unknown") for org in user_info["orgs"]]
                details.append(f"Member of organizations: {', '.join(orgs)}")

        return True, f"HuggingFace CLI is configured (logged in as {username})", details

    except HfHubHTTPError as e:
        if e.response.status_code == 401:
            message = "HuggingFace token is invalid or expired"
            if fix:
                details.append("🔧 Please log in to HuggingFace again:")
                details.append("   uv run huggingface-cli login")
                details.append(
                    "   Make sure to use a valid token with appropriate permissions"
                )
            else:
                details.append("Run 'uv run huggingface-cli login' with a valid token")
        else:
            message = f"Error checking HuggingFace authentication: {e}"
            if verbose:
                details.append(f"HTTP error: {e.response.status_code}")
        return False, message, details

    except Exception as e:
        message = f"Unexpected error checking HuggingFace authentication: {e}"
        logging.error(f"HuggingFace auth check failed: {e}")
        return False, message, details
