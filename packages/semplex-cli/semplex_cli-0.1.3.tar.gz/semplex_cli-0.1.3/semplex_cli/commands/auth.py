"""Authentication commands for Semplex CLI."""

import socket
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from ..utils.config import Config

app = typer.Typer(
    name="auth",
    help="Authentication commands for Semplex",
)

console = Console()


class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for receiving OAuth callback."""

    credentials: dict = {}

    def log_message(self, format: str, *args) -> None:
        """Suppress default logging."""
        pass

    def do_GET(self) -> None:
        """Handle GET request from OAuth callback."""
        parsed = urlparse(self.path)

        if parsed.path == "/callback":
            params = parse_qs(parsed.query)
            success = params.get("success", [None])[0]

            if success == "true":
                key = params.get("key", [None])[0]
                email = params.get("email", [None])[0]
                organization = params.get("organization", [None])[0]

                if key and email:
                    CallbackHandler.credentials = {
                        "key": key,
                        "email": email,
                        "organization": organization,
                    }
                    self._send_success_response()
                else:
                    self._send_error_response("Missing credentials in callback")
            else:
                error = params.get("error", ["Unknown error"])[0]
                self._send_error_response(error)
        else:
            self._send_error_response("Invalid callback path")

    def _send_success_response(self) -> None:
        """Send success HTML response."""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Semplex CLI - Authenticated</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                       display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0;
                       background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
                .card { background: white; padding: 48px; border-radius: 16px; text-align: center;
                        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); }
                .success { color: #10b981; font-size: 64px; margin-bottom: 16px; }
                h1 { color: #1e293b; margin: 0 0 8px 0; }
                p { color: #64748b; margin: 0; }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="success">&#10003;</div>
                <h1>Authenticated!</h1>
                <p>You can close this window and return to your terminal.</p>
            </div>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def _send_error_response(self, error: str) -> None:
        """Send error HTML response."""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Semplex CLI - Error</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                       display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0;
                       background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); }}
                .card {{ background: white; padding: 48px; border-radius: 16px; text-align: center;
                        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); }}
                .error {{ color: #ef4444; font-size: 64px; margin-bottom: 16px; }}
                h1 {{ color: #1e293b; margin: 0 0 8px 0; }}
                p {{ color: #64748b; margin: 0; }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="error">&#10007;</div>
                <h1>Authentication Failed</h1>
                <p>{error}</p>
            </div>
        </body>
        </html>
        """
        self.send_response(400)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())


def find_free_port() -> int:
    """Find a free port to use for the callback server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def start_callback_server(port: int) -> HTTPServer:
    """Start the callback server."""
    server = HTTPServer(("localhost", port), CallbackHandler)
    return server


def wait_for_callback(server: HTTPServer, timeout: int = 120) -> Optional[dict]:
    """Wait for the OAuth callback with timeout."""
    # Reset credentials
    CallbackHandler.credentials = {}

    # Set socket timeout
    server.socket.settimeout(1.0)

    elapsed = 0
    while elapsed < timeout:
        try:
            server.handle_request()
            if CallbackHandler.credentials:
                return CallbackHandler.credentials
        except socket.timeout:
            pass
        elapsed += 1

    return None


@app.command("login")
def login(
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        "-k",
        help="API key for headless authentication (get from web dashboard)",
        envvar="SEMPLEX_API_KEY",
    ),
    email: Optional[str] = typer.Option(
        None,
        "--email",
        "-e",
        help="Email address associated with the API key",
        envvar="SEMPLEX_USER_EMAIL",
    ),
    organization: Optional[str] = typer.Option(
        None,
        "--organization",
        "-o",
        help="Default organization handle",
        envvar="SEMPLEX_ORGANIZATION",
    ),
    api_url: Optional[str] = typer.Option(
        None,
        "--api-url",
        help="Custom API URL (defaults to config value or http://localhost:3000)",
    ),
) -> None:
    """
    Authenticate with Semplex.

    For headless environments (servers, HPC clusters), use --api-key:

        semplex auth login --api-key <key> --email <email>

    Or set environment variables:

        export SEMPLEX_API_KEY=<key>
        export SEMPLEX_USER_EMAIL=<email>
        semplex auth login

    For interactive environments, omit --api-key to open browser authentication.
    """
    config = Config.load()

    # Headless authentication with API key
    if api_key:
        if not email:
            console.print(
                Panel(
                    "[bold red]Email required for API key authentication.[/bold red]\n\n"
                    "Use [cyan]--email[/cyan] or set [cyan]SEMPLEX_USER_EMAIL[/cyan]:\n\n"
                    "  semplex auth login --api-key <key> --email <email>",
                    title="Missing Email",
                    border_style="red",
                )
            )
            raise typer.Exit(1)

        # Save credentials
        config.api.api_key = api_key
        config.api.user_email = email
        if organization:
            config.api.default_organization = organization
        if api_url:
            config.api.url = api_url

        config.save()

        org_msg = ""
        if organization:
            org_msg = f"\nDefault organization: [cyan]{organization}[/cyan]"

        console.print()
        console.print(
            Panel(
                f"[bold green]Successfully authenticated![/bold green]\n\n"
                f"Email: [cyan]{email}[/cyan]\n"
                f"API key: [dim]{api_key[:12]}...[/dim]"
                f"{org_msg}",
                title="Authentication Complete",
                border_style="green",
            )
        )
        return

    # Browser-based authentication (original flow)
    # Get base URL (remove /api/metadata suffix)
    base_url = api_url or config.api.url
    if base_url.endswith("/api/metadata"):
        base_url = base_url[: -len("/api/metadata")]
    elif base_url.endswith("/"):
        base_url = base_url[:-1]

    # Start local callback server
    port = find_free_port()
    server = start_callback_server(port)

    # Build auth URL
    auth_url = f"{base_url}/auth/cli?port={port}"

    console.print()
    console.print(
        Panel(
            "[bold]Opening browser to authenticate...[/bold]\n\n"
            f"If the browser doesn't open, visit:\n[cyan]{auth_url}[/cyan]\n\n"
            "[dim]For headless environments, use:[/dim]\n"
            "[dim]  semplex auth login --api-key <key> --email <email>[/dim]",
            title="Semplex Authentication",
            border_style="blue",
        )
    )

    # Open browser
    webbrowser.open(auth_url)

    # Wait for callback
    console.print("\n[dim]Waiting for authentication...[/dim]")

    credentials = wait_for_callback(server, timeout=120)

    server.server_close()

    if credentials:
        # Save credentials to config
        config.api.api_key = credentials["key"]
        config.api.user_email = credentials["email"]

        # Set default organization if provided
        if credentials.get("organization"):
            config.api.default_organization = credentials["organization"]

        config.save()

        # Build success message
        org_msg = ""
        if credentials.get("organization"):
            org_msg = f"\nDefault organization: [cyan]{credentials['organization']}[/cyan]"

        console.print()
        console.print(
            Panel(
                f"[bold green]Successfully authenticated![/bold green]\n\n"
                f"Logged in as: [cyan]{credentials['email']}[/cyan]\n"
                f"API key: [dim]{credentials['key'][:12]}...[/dim]"
                f"{org_msg}",
                title="Authentication Complete",
                border_style="green",
            )
        )
    else:
        console.print()
        console.print(
            Panel(
                "[bold red]Authentication timed out or failed.[/bold red]\n\n"
                "Please try again with [cyan]semplex auth login[/cyan]\n\n"
                "[dim]For headless environments, use:[/dim]\n"
                "[dim]  semplex auth login --api-key <key> --email <email>[/dim]",
                title="Authentication Failed",
                border_style="red",
            )
        )
        raise typer.Exit(1)


@app.command("logout")
def logout() -> None:
    """
    Clear stored authentication credentials.
    """
    config = Config.load()

    if not config.api.is_authenticated():
        console.print("[yellow]Not currently authenticated.[/yellow]")
        return

    email = config.api.user_email
    config.api.api_key = None
    config.api.user_email = None
    config.api.default_organization = None
    config.save()

    console.print(f"[green]Logged out successfully.[/green]")
    if email:
        console.print(f"[dim]Previous user: {email}[/dim]")


@app.command("whoami")
def whoami() -> None:
    """
    Show the currently authenticated user.
    """
    import os

    config = Config.load()

    if not config.api.is_authenticated():
        console.print(
            Panel(
                "[yellow]Not authenticated.[/yellow]\n\n"
                "Run [cyan]semplex auth login[/cyan] to authenticate.\n\n"
                "[dim]For headless environments:[/dim]\n"
                "[dim]  semplex auth login --api-key <key> --email <email>[/dim]",
                title="Authentication Status",
                border_style="yellow",
            )
        )
        return

    # Get credentials (from env or config)
    api_key = config.api.get_api_key()
    user_email = config.api.get_user_email()
    organization = config.api.get_organization()

    # Determine source of credentials
    source_info = ""
    if os.environ.get("SEMPLEX_API_KEY"):
        source_info = "\n[dim](credentials from environment variables)[/dim]"

    org_info = ""
    if organization:
        org_info = f"\nDefault Organization: [cyan]{organization}[/cyan]"

    console.print(
        Panel(
            f"[bold green]Authenticated[/bold green]\n\n"
            f"Email: [cyan]{user_email}[/cyan]\n"
            f"API Key: [dim]{api_key[:12] if api_key else 'None'}...[/dim]\n"
            f"API URL: [dim]{config.api.url}[/dim]"
            f"{org_info}"
            f"{source_info}",
            title="Authentication Status",
            border_style="green",
        )
    )


@app.command("status")
def status() -> None:
    """
    Alias for whoami - Show authentication status.
    """
    whoami()
