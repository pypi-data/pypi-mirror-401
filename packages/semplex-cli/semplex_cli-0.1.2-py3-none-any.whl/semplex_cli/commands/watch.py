"""Watch commands for managing the file watcher."""

import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import typer
from rich.console import Console
from rich.table import Table
import pathspec

from ..utils.config import Config
from ..utils.process import cleanup_pid_file, is_process_running, read_pid, stop_process
from ..watcher import FileWatcher
from ..extractors import get_supported_document_extensions

app = typer.Typer(help="File watcher management")
console = Console()


@app.command("start")
def start_watcher(
    foreground: bool = typer.Option(
        False,
        "--foreground",
        "-f",
        help="Run in foreground (default: background)",
    ),
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
        help="Use polling mode instead of inotify (slower but avoids watch limits on large directories)",
    ),
) -> None:
    """Start the file watcher."""
    config = Config.load()

    # Clear state if --force is used
    if force:
        from ..utils.state import StateManager
        state_manager = StateManager()
        state_manager.clear_all()
        console.print("[yellow]State cleared. All files will be rescanned.[/yellow]")

    # Check if configured
    if not config.is_configured():
        console.print("[red]Error:[/red] CLI not configured. Run 'semplex config init' first.")
        raise typer.Exit(1)

    # Check if already running
    pid_path = Config.get_pid_path()
    existing_pid = read_pid(pid_path)

    if existing_pid and is_process_running(existing_pid):
        console.print(f"[yellow]File watcher is already running (PID: {existing_pid})[/yellow]")
        console.print("Use 'semplex stop' to stop it first.")
        raise typer.Exit(1)

    # Clean up stale PID file
    if existing_pid:
        cleanup_pid_file(pid_path)

    # Run in foreground
    if foreground:
        watcher = FileWatcher(config, scan_depth=scan_depth, use_polling=polling)
        watcher.start()
        return

    # Run in background (daemon mode)
    console.print("[cyan]Starting file watcher in background...[/cyan]")

    # Fork process
    try:
        pid = os.fork()
        if pid > 0:
            # Parent process
            console.print(f"[green]✓[/green] File watcher started (PID: {pid})")
            console.print(f"Use 'semplex status' to check status")
            console.print(f"Use 'semplex stop' to stop the watcher")
            sys.exit(0)
    except OSError as e:
        console.print(f"[red]Error:[/red] Failed to start background process: {e}")
        raise typer.Exit(1)

    # Child process continues here
    # Detach from parent
    os.setsid()

    # Redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()

    # Start watcher
    watcher = FileWatcher(config, scan_depth=scan_depth, use_polling=polling)
    watcher.start()


@app.command("stop")
def stop_watcher() -> None:
    """Stop the file watcher."""
    pid_path = Config.get_pid_path()
    pid = read_pid(pid_path)

    if not pid:
        console.print("[yellow]No running file watcher found.[/yellow]")
        return

    if not is_process_running(pid):
        console.print("[yellow]File watcher process not found (stale PID file).[/yellow]")
        cleanup_pid_file(pid_path)
        return

    console.print(f"[cyan]Stopping file watcher (PID: {pid})...[/cyan]")

    if stop_process(pid):
        cleanup_pid_file(pid_path)
        console.print("[green]✓[/green] File watcher stopped successfully.")
    else:
        console.print("[red]Error:[/red] Failed to stop file watcher.")
        raise typer.Exit(1)


@app.command("status")
def check_status() -> None:
    """Check file watcher status."""
    config = Config.load()
    pid_path = Config.get_pid_path()
    pid = read_pid(pid_path)

    console.print("[bold]File Watcher Status[/bold]\n")

    if not config.is_configured():
        console.print("[yellow]Status:[/yellow] Not configured")
        console.print("Run 'semplex config init' to set up.")
        return

    if not pid:
        console.print("[yellow]Status:[/yellow] Not running")
        return

    if is_process_running(pid):
        console.print(f"[green]Status:[/green] Running (PID: {pid})")

        # Show watched directories by organization
        if config.organizations:
            console.print(f"\n[bold]Watched Directories by Organization:[/bold]")
            for org in config.organizations:
                console.print(f"\n  [cyan]{org.handle}:[/cyan]")
                for directory in org.directories:
                    console.print(f"    • {directory}")

        # Show legacy directories if any
        if config.watch.directories:
            console.print(f"\n[bold]Legacy Directories (No Organization):[/bold]")
            for directory in config.watch.directories:
                console.print(f"  • {directory}")

        console.print(f"\n[bold]File Types:[/bold] {', '.join(config.watch.file_types)}")

        if config.api.debug_mode:
            console.print(f"[bold]Debug Mode:[/bold] Enabled")
            console.print(f"[bold]Output File:[/bold] {config.api.debug_output_file}")
        else:
            console.print(f"[bold]API Endpoint:[/bold] {config.api.url}")
    else:
        console.print("[yellow]Status:[/yellow] Not running (stale PID file)")
        cleanup_pid_file(pid_path)


@app.command("restart")
def restart_watcher() -> None:
    """Restart the file watcher."""
    pid_path = Config.get_pid_path()
    pid = read_pid(pid_path)

    if pid and is_process_running(pid):
        console.print("[cyan]Stopping current watcher...[/cyan]")
        stop_watcher()

    console.print("[cyan]Starting watcher...[/cyan]")
    start_watcher(foreground=False)


@app.command("scan")
def scan_files(
    show_files: bool = typer.Option(
        False,
        "--show-files",
        "-v",
        help="Show individual file paths",
    ),
    by_type: bool = typer.Option(
        False,
        "--by-type",
        "-t",
        help="Group results by file type",
    ),
    by_org: bool = typer.Option(
        False,
        "--by-org",
        "-o",
        help="Group results by organization",
    ),
    include_processed: bool = typer.Option(
        False,
        "--include-processed",
        "-a",
        help="Include already processed files in the count",
    ),
) -> None:
    """
    Scan directories and report files that would be indexed.

    This is a dry-run that doesn't send any requests or start the watcher.
    Useful for verifying configuration before indexing.

    Examples:

        semplex scan                    # Quick summary
        semplex scan --by-type          # Group by file extension
        semplex scan --by-org           # Group by organization
        semplex scan --show-files       # List all files
    """
    from ..utils.state import StateManager

    config = Config.load()

    if not config.is_configured():
        console.print("[red]Error:[/red] CLI not configured. Run 'semplex config init' first.")
        raise typer.Exit(1)

    # Build list of all file types to look for
    tabular_types = set(config.watch.get_active_file_types())
    document_types = set()
    if config.documents.enabled:
        document_types = set(ft.lower() for ft in config.documents.file_types)

    all_file_types = tabular_types | document_types

    # Build ignore pattern matcher
    ignore_spec = pathspec.PathSpec.from_lines(
        pathspec.patterns.GitWildMatchPattern,
        config.watch.ignore_patterns
    )

    # State manager for checking processed files
    state_manager = StateManager()

    # Collect files
    files_by_org: Dict[str, List[Path]] = defaultdict(list)
    files_by_type: Dict[str, List[Path]] = defaultdict(list)
    all_files: List[Path] = []
    skipped_processed = 0
    skipped_size = 0

    console.print("[cyan]Scanning directories...[/cyan]\n")

    from rich.live import Live
    from rich.text import Text

    def make_status(current_dir: str, found: int) -> Text:
        text = Text()
        text.append("📁 ", style="cyan")
        text.append(current_dir, style="dim")
        text.append(f"\n✓  Found: ", style="green")
        text.append(f"{found}", style="bold green")
        text.append(" file(s) to index", style="green")
        return text

    with Live(make_status("Starting...", 0), console=console, refresh_per_second=10) as live:
        for directory in config.get_all_directories():
            dir_path = Path(directory).expanduser().resolve()
            if not dir_path.exists():
                continue

            # Determine organization for this directory
            org_handle = config.get_organization_for_path(dir_path) or "(no organization)"

            # Walk directory
            if config.watch.recursive:
                for root, dirs, files in os.walk(dir_path):
                    current_dir = Path(root)
                    live.update(make_status(str(current_dir), len(all_files)))

                    # Filter ignored directories
                    dirs[:] = [
                        d for d in dirs
                        if not ignore_spec.match_file(str((current_dir / d).as_posix()))
                    ]

                    for filename in files:
                        file_path = current_dir / filename
                        suffix = file_path.suffix.lower()

                        # Check file type
                        if suffix not in all_file_types:
                            continue

                        # Check ignore patterns
                        if ignore_spec.match_file(str(file_path.as_posix())):
                            continue

                        # Check file size for documents
                        if suffix in document_types:
                            try:
                                if file_path.stat().st_size > config.documents.max_file_size:
                                    skipped_size += 1
                                    continue
                            except OSError:
                                continue

                        # Check if already processed
                        if not include_processed and state_manager.is_processed(file_path):
                            skipped_processed += 1
                            continue

                        all_files.append(file_path)
                        files_by_org[org_handle].append(file_path)
                        files_by_type[suffix].append(file_path)

                        # Update display periodically (every 10 files)
                        if len(all_files) % 10 == 0:
                            live.update(make_status(str(current_dir), len(all_files)))
            else:
                # Non-recursive scan
                live.update(make_status(str(dir_path), len(all_files)))
                for file_path in dir_path.glob("*"):
                    if not file_path.is_file():
                        continue

                    suffix = file_path.suffix.lower()

                    if suffix not in all_file_types:
                        continue

                    if ignore_spec.match_file(str(file_path.as_posix())):
                        continue

                    if suffix in document_types:
                        try:
                            if file_path.stat().st_size > config.documents.max_file_size:
                                skipped_size += 1
                                continue
                        except OSError:
                            continue

                    if not include_processed and state_manager.is_processed(file_path):
                        skipped_processed += 1
                        continue

                    all_files.append(file_path)
                    files_by_org[org_handle].append(file_path)
                    files_by_type[suffix].append(file_path)

        live.update(make_status("Done!", len(all_files)))

    console.print()  # Add blank line after live display

    # Display results
    total_files = len(all_files)

    if total_files == 0:
        console.print("[yellow]No files found to index.[/yellow]")
        if skipped_processed > 0:
            console.print(f"[dim]({skipped_processed} files already processed, use --include-processed to show)[/dim]")
        return

    # Summary
    console.print(f"[bold green]Found {total_files} file(s) to index[/bold green]\n")

    if skipped_processed > 0:
        console.print(f"[dim]Skipped {skipped_processed} already processed file(s)[/dim]")
    if skipped_size > 0:
        console.print(f"[dim]Skipped {skipped_size} file(s) exceeding size limit[/dim]")
    if skipped_processed > 0 or skipped_size > 0:
        console.print()

    # Group by organization
    if by_org:
        table = Table(title="Files by Organization")
        table.add_column("Organization", style="cyan")
        table.add_column("Count", justify="right", style="green")

        for org, files in sorted(files_by_org.items(), key=lambda x: -len(x[1])):
            table.add_row(org, str(len(files)))

        console.print(table)
        console.print()

    # Group by file type
    if by_type:
        table = Table(title="Files by Type")
        table.add_column("Extension", style="cyan")
        table.add_column("Count", justify="right", style="green")
        table.add_column("Category", style="dim")

        for ext, files in sorted(files_by_type.items(), key=lambda x: -len(x[1])):
            category = "tabular" if ext in tabular_types else "document"
            table.add_row(ext, str(len(files)), category)

        console.print(table)
        console.print()

    # Show individual files
    if show_files:
        console.print("[bold]Files:[/bold]")
        for file_path in sorted(all_files):
            org = config.get_organization_for_path(file_path) or ""
            org_prefix = f"[dim][{org}][/dim] " if org else ""
            console.print(f"  {org_prefix}{file_path}")
        console.print()

    # Show directories being scanned
    console.print("[bold]Configured Directories:[/bold]")
    for directory in config.get_all_directories():
        org = config.get_organization_for_path(Path(directory).expanduser().resolve())
        org_suffix = f" [dim]({org})[/dim]" if org else ""
        console.print(f"  • {directory}{org_suffix}")
