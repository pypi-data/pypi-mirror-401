"""Authentication commands for sb0 CLI.

Provides login, logout, and whoami commands for managing CLI authentication.
"""

from __future__ import annotations

import typer
import questionary
from rich.console import Console
from rich.table import Table

from sb0.lib.utils.logging import make_logger
from sb0.lib.cli.utils.credentials import (
    clear_credentials,
    get_credentials_info,
    is_authenticated,
    store_credentials,
)

logger = make_logger(__name__)
console = Console()

# Create the auth typer app - will be registered as top-level commands
# (login, logout, whoami are top-level, not under "sb0 auth")


def login(
    token: str | None = typer.Option(None, "--token", "-t", help="API token (if not provided, will prompt)"),
    interactive: bool = typer.Option(True, "--interactive/--no-interactive", help="Enable interactive prompts"),
) -> None:
    """Authenticate with the sb0 platform.

    Stores credentials at ~/.sb0/credentials.json for subsequent commands.
    """
    console.print("[bold blue]sb0 Login[/bold blue]\n")

    # Check if already authenticated
    if is_authenticated():
        creds_info = get_credentials_info()
        if creds_info and creds_info.get("email"):
            console.print(f"[yellow]Already logged in as {creds_info['email']}[/yellow]")
        else:
            console.print("[yellow]Already logged in[/yellow]")

        if interactive:
            proceed = questionary.confirm("Do you want to log in with a different account?").ask()
            if not proceed:
                console.print("Login cancelled")
                raise typer.Exit(0)

    # Get token
    if not token:
        if interactive:
            console.print("Enter your API token from https://app.sb0.dev/settings/api-keys\n")
            token = questionary.password("API Token:").ask()
            if not token:
                console.print("[red]Login cancelled[/red]")
                raise typer.Exit(1)
        else:
            console.print("[red]Error:[/red] --token is required in non-interactive mode")
            raise typer.Exit(1)

    # Validate token by calling API (uses auto-generated client)
    # For now, we just store the token - validation will work after SDK regeneration
    try:
        # TODO: After SDK regeneration, validate token:
        # from sb0 import Sb0
        # client = Sb0(api_key=token)
        # user = client.users.me()  # or similar endpoint
        # user_id = user.id
        # email = user.email

        # For now, store without validation
        user_id = None
        email = None

        store_credentials(
            token=token,
            user_id=user_id,
            email=email,
        )

        console.print("\n[green]Successfully logged in![/green]")
        if email:
            console.print(f"Logged in as: {email}")
        console.print("\nCredentials stored at ~/.sb0/credentials.json")

    except Exception as e:
        console.print(f"[red]Login failed:[/red] {str(e)}")
        logger.exception("Login failed")
        raise typer.Exit(1) from e


def logout() -> None:
    """Log out and clear stored credentials."""
    if not is_authenticated():
        console.print("[yellow]Not currently logged in[/yellow]")
        raise typer.Exit(0)

    clear_credentials()
    console.print("[green]Successfully logged out[/green]")
    console.print("Credentials removed from ~/.sb0/credentials.json")


def whoami() -> None:
    """Show current authentication status and user info."""
    if not is_authenticated():
        console.print("[yellow]Not logged in[/yellow]")
        console.print("\nRun 'sb0 login' to authenticate")
        raise typer.Exit(0)

    creds_info = get_credentials_info()
    if not creds_info:
        console.print("[yellow]Not logged in[/yellow]")
        raise typer.Exit(0)

    console.print("[bold blue]Current Authentication[/bold blue]\n")

    table = Table(show_header=False, box=None)
    table.add_column("Field", style="bold")
    table.add_column("Value")

    if creds_info.get("email"):
        table.add_row("Email", creds_info["email"])
    if creds_info.get("user_id"):
        table.add_row("User ID", creds_info["user_id"])
    table.add_row("Token", creds_info["token"])
    if creds_info.get("created_at"):
        table.add_row("Logged in", creds_info["created_at"])
    if creds_info.get("expires_at"):
        table.add_row("Expires", creds_info["expires_at"])

    console.print(table)

    # TODO: After SDK regeneration, fetch and display current user info:
    # try:
    #     from sb0 import Sb0
    #     client = Sb0()
    #     user = client.users.me()
    #     console.print(f"\nAccount: {user.email}")
    #     console.print(f"Organization: {user.organization.name}")
    # except Exception:
    #     pass
