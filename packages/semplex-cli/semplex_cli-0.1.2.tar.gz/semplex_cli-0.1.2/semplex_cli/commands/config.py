"""Configuration commands."""

from pathlib import Path

import typer
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from ..utils.config import Config, OrganizationConfig

app = typer.Typer(help="Configuration management")
console = Console()


@app.command("init")
def init_config() -> None:
    """Initialize configuration with interactive wizard."""
    console.print("\n[bold cyan]Semplex CLI Configuration Wizard[/bold cyan]\n")

    # Load existing config or create new
    config = Config.load()

    # Configure user information
    console.print("[bold]1. Machine Information[/bold]")
    console.print("This information helps identify which machine is running the indexing.\n")

    if not config.api.is_authenticated():
        console.print("[yellow]Tip:[/yellow] Run 'semplex auth login' to authenticate and set your email.\n")

    config.user.machine_name = Prompt.ask(
        "Machine/cluster name (e.g., 'broad-cluster', 'personal-laptop')",
        default=config.user.machine_name or "",
    )

    # Configure organizations
    console.print("\n[bold]2. Organization & Directory Configuration[/bold]")
    console.print("Configure organizations and their directories.\n")

    organizations = []

    # Ask if user wants to configure organizations
    configure_orgs = Confirm.ask(
        "Do you want to configure directories for multiple organizations?",
        default=len(config.organizations) > 0,
    )

    if configure_orgs:
        console.print("\nYou'll add organizations one at a time. Each organization can have multiple directories.\n")

        while True:
            org_handle = Prompt.ask(
                "\nOrganization handle (e.g., 'acme', 'broad-institute') [or press Enter to finish]",
                default="",
            )

            if not org_handle:
                break

            # Collect directories for this organization
            console.print(f"\n[cyan]Adding directories for organization: {org_handle}[/cyan]")
            org_directories = []

            while True:
                directory = Prompt.ask(
                    "  Directory path (or press Enter to finish this org)",
                    default="",
                )

                if not directory:
                    break

                dir_path = Path(directory).expanduser().resolve()

                if not dir_path.exists():
                    console.print(f"  [yellow]Warning:[/yellow] Directory does not exist: {dir_path}")
                    if not Confirm.ask("  Add anyway?"):
                        continue

                org_directories.append(str(dir_path))
                console.print(f"  [green]✓[/green] Added: {dir_path}")

            if org_directories:
                organizations.append(OrganizationConfig(
                    handle=org_handle,
                    directories=org_directories,
                ))
                console.print(f"[green]✓[/green] Organization '{org_handle}' configured with {len(org_directories)} director{'y' if len(org_directories) == 1 else 'ies'}")
            else:
                console.print(f"[yellow]Warning:[/yellow] No directories added for '{org_handle}', skipping.")

        if organizations:
            config.organizations = organizations
    else:
        # Legacy mode: single set of directories without organization mapping
        console.print("\n[bold]Directory Configuration (No Organization Mapping)[/bold]")
        console.print("Enter directories to watch (one at a time, press Enter with empty input to finish):\n")

        directories = []
        while True:
            directory = Prompt.ask(
                "Directory path (or press Enter to finish)",
                default="" if directories else None,
            )

            if not directory:
                break

            dir_path = Path(directory).expanduser().resolve()

            if not dir_path.exists():
                console.print(f"[yellow]Warning:[/yellow] Directory does not exist: {dir_path}")
                if not Confirm.ask("Add anyway?"):
                    continue

            directories.append(str(dir_path))
            console.print(f"[green]✓[/green] Added: {dir_path}")

        if directories:
            config.watch.directories = directories

    # Configure file types
    console.print("\n[bold]3. File Type Configuration[/bold]")
    console.print("By default, all common file types are processed:")
    console.print(f"[dim]{', '.join(config.watch.file_types[:10])}...[/dim]\n")

    exclude_types = Confirm.ask(
        "Do you want to exclude any file types?",
        default=len(config.watch.excluded_file_types) > 0,
    )

    if exclude_types:
        default_excluded = ",".join(config.watch.excluded_file_types) if config.watch.excluded_file_types else ""
        excluded_str = Prompt.ask(
            "File extensions to exclude (comma-separated, e.g., .pdf,.docx)",
            default=default_excluded,
        )
        if excluded_str.strip():
            config.watch.excluded_file_types = [ft.strip() for ft in excluded_str.split(",") if ft.strip()]
        else:
            config.watch.excluded_file_types = []
    else:
        config.watch.excluded_file_types = []

    # Configure recursive watching
    config.watch.recursive = Confirm.ask(
        "\nWatch directories recursively?",
        default=config.watch.recursive,
    )

    # Configure API
    console.print("\n[bold]4. API Configuration[/bold]")
    config.api.url = Prompt.ask(
        "Backend API URL",
        default=config.api.url,
    )

    # Configure debug mode
    config.api.debug_mode = Confirm.ask(
        "\nEnable debug mode? (writes to file instead of sending to API)",
        default=config.api.debug_mode,
    )

    if config.api.debug_mode:
        default_debug_file = config.api.debug_output_file or str(
            Path.home() / ".config" / "semplex" / "debug_output.jsonl"
        )
        config.api.debug_output_file = Prompt.ask(
            "Debug output file path",
            default=default_debug_file,
        )

    # Save configuration
    config.save()

    console.print("\n[bold green]✓ Configuration saved successfully![/bold green]")
    console.print(f"Config file: {Config.get_config_path()}\n")

    # Show summary
    show_config_summary(config)


@app.command("show")
def show_config() -> None:
    """Show current configuration."""
    config = Config.load()

    if not config.is_configured():
        console.print("[yellow]No configuration found. Run 'semplex config init' to set up.[/yellow]")
        return

    show_config_summary(config)


@app.command("set")
def set_config_value(
    key: str = typer.Argument(..., help="Configuration key (e.g., api.url)"),
    value: str = typer.Argument(..., help="Configuration value"),
) -> None:
    """Set a configuration value."""
    config = Config.load()

    try:
        # Parse key path
        parts = key.split(".")

        if len(parts) != 2:
            console.print("[red]Invalid key format. Use: section.key (e.g., api.url)[/red]")
            raise typer.Exit(1)

        section, field = parts

        # Update the value
        if section == "user":
            setattr(config.user, field, value)
        elif section == "api":
            setattr(config.api, field, value)
        elif section == "watch":
            # Handle lists for watch section
            if field in ["directories", "file_types", "ignore_patterns"]:
                setattr(config.watch, field, value.split(","))
            elif field in ["recursive", "count_rows"]:
                setattr(config.watch, field, value.lower() in ["true", "1", "yes"])
            else:
                setattr(config.watch, field, value)
        else:
            console.print(f"[red]Unknown section: {section}[/red]")
            raise typer.Exit(1)

        config.save()
        console.print(f"[green]✓[/green] Set {key} = {value}")

    except AttributeError:
        console.print(f"[red]Unknown configuration key: {key}[/red]")
        raise typer.Exit(1)


@app.command("add-org")
def add_organization() -> None:
    """Add a new organization with directories."""
    config = Config.load()

    console.print("\n[bold cyan]Add Organization[/bold cyan]\n")

    # Get organization handle
    org_handle = Prompt.ask("Organization handle (e.g., 'acme', 'broad-institute')")

    # Check if organization already exists
    existing_org = next((org for org in config.organizations if org.handle == org_handle), None)
    if existing_org:
        console.print(f"[yellow]Warning:[/yellow] Organization '{org_handle}' already exists.")
        if not Confirm.ask("Do you want to add more directories to this organization?"):
            return
        org_directories = list(existing_org.directories)
    else:
        org_directories = []

    # Collect directories for this organization
    console.print(f"\n[cyan]Adding directories for organization: {org_handle}[/cyan]")
    console.print("Enter directories one at a time (press Enter with empty input to finish):\n")

    while True:
        directory = Prompt.ask(
            "  Directory path (or press Enter to finish)",
            default="",
        )

        if not directory:
            break

        dir_path = Path(directory).expanduser().resolve()

        if not dir_path.exists():
            console.print(f"  [yellow]Warning:[/yellow] Directory does not exist: {dir_path}")
            if not Confirm.ask("  Add anyway?"):
                continue

        # Check if directory is already assigned to another org
        existing_org_for_dir = None
        for org in config.organizations:
            if str(dir_path) in org.directories:
                existing_org_for_dir = org.handle
                break

        if existing_org_for_dir and existing_org_for_dir != org_handle:
            console.print(
                f"  [yellow]Warning:[/yellow] Directory is already assigned to organization '{existing_org_for_dir}'"
            )
            if not Confirm.ask("  Add anyway?"):
                continue

        if str(dir_path) in org_directories:
            console.print(f"  [yellow]Directory already added:[/yellow] {dir_path}")
            continue

        org_directories.append(str(dir_path))
        console.print(f"  [green]✓[/green] Added: {dir_path}")

    if not org_directories:
        console.print(f"[yellow]No directories added for '{org_handle}'.[/yellow]")
        return

    # Update or add organization
    if existing_org:
        existing_org.directories = org_directories
        console.print(
            f"\n[green]✓[/green] Updated organization '{org_handle}' with {len(org_directories)} director{'y' if len(org_directories) == 1 else 'ies'}"
        )
    else:
        config.organizations.append(
            OrganizationConfig(
                handle=org_handle,
                directories=org_directories,
            )
        )
        console.print(
            f"\n[green]✓[/green] Added organization '{org_handle}' with {len(org_directories)} director{'y' if len(org_directories) == 1 else 'ies'}"
        )

    config.save()
    console.print(f"Config file: {Config.get_config_path()}\n")


@app.command("remove-org")
def remove_organization(
    handle: str = typer.Argument(..., help="Organization handle to remove"),
) -> None:
    """Remove an organization and its directories."""
    config = Config.load()

    # Find organization
    org_to_remove = next((org for org in config.organizations if org.handle == handle), None)

    if not org_to_remove:
        console.print(f"[red]Error:[/red] Organization '{handle}' not found.")
        raise typer.Exit(1)

    # Confirm removal
    console.print(f"\n[yellow]Organization:[/yellow] {handle}")
    console.print(f"[yellow]Directories:[/yellow]")
    for directory in org_to_remove.directories:
        console.print(f"  • {directory}")

    if not Confirm.ask(f"\nAre you sure you want to remove organization '{handle}'?"):
        console.print("Cancelled.")
        return

    # Remove organization
    config.organizations = [org for org in config.organizations if org.handle != handle]
    config.save()

    console.print(f"[green]✓[/green] Organization '{handle}' removed.")


@app.command("list-orgs")
def list_organizations() -> None:
    """List all configured organizations."""
    config = Config.load()

    if not config.organizations:
        console.print("[yellow]No organizations configured.[/yellow]")
        console.print("Use 'semplex config add-org' to add an organization.")
        return

    console.print("\n[bold]Configured Organizations[/bold]\n")

    for org in config.organizations:
        console.print(f"[cyan]{org.handle}[/cyan]")
        for directory in org.directories:
            console.print(f"  • {directory}")
        console.print()


@app.command("add-ignore")
def add_ignore_pattern(
    pattern: str = typer.Argument(..., help="Gitignore-style pattern to add (e.g., '*.log', 'temp/', '**/cache')"),
) -> None:
    """Add a gitignore-style pattern to ignore files/directories.

    Examples:
        *.log              - Ignore all .log files
        temp/              - Ignore temp directory
        **/cache           - Ignore cache directories anywhere
        /root-only.txt     - Ignore only in root of watched directory
        !important.log     - Negate pattern (don't ignore)
    """
    config = Config.load()

    if pattern in config.watch.ignore_patterns:
        console.print(f"[yellow]Pattern already exists:[/yellow] {pattern}")
        return

    config.watch.ignore_patterns.append(pattern)
    config.save()

    console.print(f"[green]✓[/green] Added ignore pattern: {pattern}")


@app.command("remove-ignore")
def remove_ignore_pattern(
    pattern: str = typer.Argument(..., help="Pattern to remove"),
) -> None:
    """Remove an ignore pattern."""
    config = Config.load()

    if pattern not in config.watch.ignore_patterns:
        console.print(f"[red]Error:[/red] Pattern not found: {pattern}")
        raise typer.Exit(1)

    config.watch.ignore_patterns.remove(pattern)
    config.save()

    console.print(f"[green]✓[/green] Removed ignore pattern: {pattern}")


@app.command("list-ignore")
def list_ignore_patterns() -> None:
    """List all ignore patterns."""
    config = Config.load()

    if not config.watch.ignore_patterns:
        console.print("[yellow]No ignore patterns configured.[/yellow]")
        return

    console.print("\n[bold]Ignore Patterns (Gitignore-style)[/bold]\n")

    for pattern in config.watch.ignore_patterns:
        console.print(f"  • {pattern}")

    console.print("\nExamples of what these patterns match:", style="dim")
    console.print("  *.tmp       - All .tmp files anywhere", style="dim")
    console.print("  temp/       - The temp directory", style="dim")
    console.print("  **/cache    - Any cache directory (nested)", style="dim")
    console.print("  /root.txt   - Only root.txt in watch root\n", style="dim")


@app.command("reset")
def reset_config() -> None:
    """Reset configuration to defaults."""
    if Confirm.ask("Are you sure you want to reset the configuration?"):
        config = Config()
        config.save()
        console.print("[green]✓[/green] Configuration reset to defaults")


def show_config_summary(config: Config) -> None:
    """Display configuration summary."""
    console.print("[bold]Configuration Summary[/bold]\n")

    # User settings
    user_table = Table(title="User Settings", show_header=False)
    user_table.add_column("Setting", style="cyan")
    user_table.add_column("Value", style="white")

    user_table.add_row("Email", config.api.get_user_email() or "[dim]Not authenticated[/dim]")
    user_table.add_row("Machine Name", config.user.machine_name or "[dim]Not set[/dim]")

    console.print(user_table)

    # Organizations
    if config.organizations:
        for org in config.organizations:
            org_table = Table(title=f"Organization: {org.handle}", show_header=False)
            org_table.add_column("Setting", style="cyan")
            org_table.add_column("Value", style="white")

            org_table.add_row("Directories", "\n".join(org.directories) or "[dim]None[/dim]")

            console.print(org_table)

    # Watch settings
    table = Table(title="Watch Settings", show_header=False)
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="white")

    if config.watch.directories:
        table.add_row("Legacy Directories", "\n".join(config.watch.directories))

    active_types = config.watch.get_active_file_types()
    table.add_row("Active File Types", f"{len(active_types)} types")
    if config.watch.excluded_file_types:
        table.add_row("Excluded Types", ", ".join(config.watch.excluded_file_types))
    table.add_row("Recursive", "Yes" if config.watch.recursive else "No")
    table.add_row("Ignore Patterns", ", ".join(config.watch.ignore_patterns[:5]) + ("..." if len(config.watch.ignore_patterns) > 5 else ""))

    console.print(table)

    # API settings
    api_table = Table(title="API Settings", show_header=False)
    api_table.add_column("Setting", style="cyan")
    api_table.add_column("Value", style="white")

    api_table.add_row("URL", config.api.url)
    api_table.add_row("Debug Mode", "Enabled" if config.api.debug_mode else "Disabled")

    if config.api.debug_mode and config.api.debug_output_file:
        api_table.add_row("Debug Output", config.api.debug_output_file)

    console.print(api_table)
    console.print()
