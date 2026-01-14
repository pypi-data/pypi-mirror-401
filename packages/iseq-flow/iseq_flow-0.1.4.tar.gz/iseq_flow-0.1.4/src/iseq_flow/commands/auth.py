"""Authentication commands."""

import asyncio

import click
from rich.console import Console

from iseq_flow.auth import (
    AuthError,
    TokenInfo,
    clear_token,
    device_flow_login,
    get_stored_token,
    is_token_expired,
    password_login,
    store_token,
)

console = Console()


@click.command()
@click.option("--email", "-e", envvar="FLOW_EMAIL", help="Email for password auth (or set FLOW_EMAIL)")
@click.option("--password", "-p", envvar="FLOW_PASSWORD", help="Password for auth (or set FLOW_PASSWORD)")
@click.option("--token", "-t", envvar="FLOW_TOKEN", help="Personal Access Token for headless auth (or set FLOW_TOKEN)")
def login(email: str | None, password: str | None, token: str | None):
    """
    Login to Flow.

    \b
    By default uses OAuth Device Flow (opens browser).
    For headless/CI environments, use --token option with a PAT.

    \b
    Examples:
      flow login                           # Interactive Device Flow
      flow login --token YOUR_PAT          # PAT auth (recommended for CI)
      FLOW_TOKEN=YOUR_PAT flow login       # Via env var
      flow login -e user@example.com -p x  # Password auth (if ROPC enabled)
    """
    import time

    try:
        if token:
            # Use Personal Access Token directly
            console.print("[dim]Using Personal Access Token...[/dim]")
            token_info = TokenInfo(
                access_token=token,
                refresh_token=None,
                expires_at=time.time() + 86400 * 365,  # Assume 1 year validity
                token_type="Bearer",
            )
            store_token(token_info)
            console.print()
            console.print("[green]Successfully logged in with PAT![/green]")
            return

        if email and password:
            # Use password-based authentication (ROPC)
            console.print(f"[dim]Logging in as {email}...[/dim]")
            token_info = asyncio.run(password_login(email, password))
        else:
            # Use Device Flow (interactive)
            token_info = asyncio.run(device_flow_login())

        store_token(token_info)
        console.print()
        console.print("[green]Successfully logged in![/green]")
    except AuthError as e:
        console.print(f"[red]Login failed:[/red] {e}")
        raise SystemExit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Login cancelled.[/yellow]")
        raise SystemExit(1)


@click.command()
def logout():
    """Logout and clear stored credentials."""
    clear_token()
    console.print("[green]Logged out successfully.[/green]")


@click.command()
def status():
    """Show current authentication status."""
    token = get_stored_token()

    if not token:
        console.print("[yellow]Not logged in.[/yellow]")
        console.print("Run [bold]flow login[/bold] to authenticate.")
        return

    if is_token_expired(token):
        console.print("[yellow]Token expired.[/yellow]")
        console.print("Run [bold]flow login[/bold] to re-authenticate.")
        return

    console.print("[green]Logged in.[/green]")

    # Try to decode token to show user info
    try:
        import base64
        import json

        # Decode JWT payload (middle part)
        payload_b64 = token.access_token.split(".")[1]
        # Add padding if needed
        payload_b64 += "=" * (4 - len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))

        if "email" in payload:
            console.print(f"User: [cyan]{payload['email']}[/cyan]")
        elif "sub" in payload:
            console.print(f"Subject: [cyan]{payload['sub']}[/cyan]")

    except Exception:
        pass  # Don't fail if we can't decode token
