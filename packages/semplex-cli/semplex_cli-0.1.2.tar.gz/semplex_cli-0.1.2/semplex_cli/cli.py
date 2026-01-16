"""Main CLI application."""

from typing import Optional

import typer
from rich.console import Console

from . import __version__
from .commands import auth, config, watch

app = typer.Typer(
    name="semplex",
    help="Semplex CLI - Silent metadata tracking and curation for data files",
    add_completion=True,
)

console = Console()

# Register command groups
app.add_typer(auth.app, name="auth")
app.add_typer(config.app, name="config")
app.add_typer(watch.app, name="watch")


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        console.print(f"Semplex CLI v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
    """
    Semplex CLI - Silent metadata tracking and curation for data files.

    The CLI monitors specified directories for changes to data files (Excel, CSV, TSV),
    extracts headers/metadata, and sends them to a backend service for curation.

    Getting Started:
        1. Configure the CLI: semplex config init
        2. Start watching: semplex watch start
        3. Check status: semplex watch status
        4. Stop watching: semplex watch stop

    For help with a specific command:
        semplex [command] --help
    """
    pass


# Convenience aliases at top level
@app.command("start")
def start_alias(
    foreground: bool = typer.Option(False, "--foreground", "-f", help="Run in foreground"),
    scan_depth: int = typer.Option(
        0,
        "--scan-depth",
        help="Show directory scanning progress up to this depth (0 = no output, 1 = root only, 2 = two levels, etc.)",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Reset state and rescan all files (ignores previously processed files)",
    ),
    polling: bool = typer.Option(
        False,
        "--polling",
        "-p",
        help="Use polling mode instead of inotify (avoids watch limits on large directories)",
    ),
) -> None:
    """Alias for 'watch start' - Start the file watcher."""
    watch.start_watcher(foreground=foreground, scan_depth=scan_depth, force=force, polling=polling)


@app.command("stop")
def stop_alias() -> None:
    """Alias for 'watch stop' - Stop the file watcher."""
    watch.stop_watcher()


@app.command("status")
def status_alias() -> None:
    """Alias for 'watch status' - Check watcher status."""
    watch.check_status()


@app.command("init")
def init_alias() -> None:
    """Alias for 'config init' - Initialize configuration."""
    config.init_config()


@app.command("login")
def login_alias(
    api_key: Optional[str] = typer.Option(None, "--api-key", "-k", help="API key for headless authentication", envvar="SEMPLEX_API_KEY"),
    email: Optional[str] = typer.Option(None, "--email", "-e", help="Email for API key auth", envvar="SEMPLEX_USER_EMAIL"),
    organization: Optional[str] = typer.Option(None, "--organization", "-o", help="Default organization", envvar="SEMPLEX_ORGANIZATION"),
    api_url: Optional[str] = typer.Option(None, "--api-url", help="Custom API URL"),
) -> None:
    """Alias for 'auth login' - Authenticate with Semplex."""
    auth.login(api_key=api_key, email=email, organization=organization, api_url=api_url)


@app.command("logout")
def logout_alias() -> None:
    """Alias for 'auth logout' - Clear authentication."""
    auth.logout()


@app.command("whoami")
def whoami_alias() -> None:
    """Alias for 'auth whoami' - Show authenticated user."""
    auth.whoami()


@app.command("scan")
def scan_alias(
    show_files: bool = typer.Option(False, "--show-files", "-v", help="Show individual file paths"),
    by_type: bool = typer.Option(False, "--by-type", "-t", help="Group results by file type"),
    by_org: bool = typer.Option(False, "--by-org", "-o", help="Group results by organization"),
    include_processed: bool = typer.Option(False, "--include-processed", "-a", help="Include already processed files"),
) -> None:
    """Scan directories and report files that would be indexed (dry-run)."""
    watch.scan_files(
        show_files=show_files,
        by_type=by_type,
        by_org=by_org,
        include_processed=include_processed,
    )
