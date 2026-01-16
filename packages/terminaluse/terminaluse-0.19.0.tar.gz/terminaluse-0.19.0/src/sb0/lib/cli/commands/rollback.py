"""CLI command for rolling back environments to previous versions."""

from __future__ import annotations

import typer
import questionary
from rich.table import Table
from rich.console import Console

from sb0 import Sb0
from sb0.lib.utils.logging import make_logger
from sb0.lib.cli.utils.cli_utils import (
    get_agent_name,
    format_relative_time,
    handle_questionary_cancellation,
    parse_agent_name,
)

logger = make_logger(__name__)
console = Console()


def rollback(
    env: str = typer.Option(..., "--env", "-e", help="Environment to rollback"),
    version: str | None = typer.Option(None, "--version", "-v", help="Target version ID (defaults to previous)"),
    yes: bool = typer.Option(False, "-y", "--yes", help="Skip confirmation"),
    agent: str | None = typer.Option(None, "--agent", "-a", help="Agent name (defaults to manifest)"),
):
    """
    Rollback an environment to a previous version.

    By default, rolls back to the immediately previous version.
    Use --version to specify a specific version ID.

    NOTE: Pending secrets (in EnvVar table) are NOT modified by rollback.
    The rollback uses the secrets_snapshot from the target version.
    """
    agent_name = get_agent_name(agent)
    namespace_slug, agent_short = parse_agent_name(agent_name)
    client = Sb0()

    try:
        # First, get the environment to check its branch rules
        env_response = client.agents.environments.retrieve(
            env_name=env,
            namespace_slug=namespace_slug,
            agent_name=agent_short,
        )
        branch_rules = env_response.branch_rules

        # Check for wildcard environments
        if len(branch_rules) != 1:
            console.print(f"[red]Error:[/red] Cannot rollback environment '{env}'.")
            console.print(f"  Environment has {len(branch_rules)} branch rules: {branch_rules}")
            console.print("  Rollback only works for environments with a single branch rule.")
            console.print()
            console.print("[dim]Hint: For environments with multiple branches, rollback each deployment individually:[/dim]")
            console.print("  sb0 versions list --branch <branch>")
            raise typer.Exit(1)

        branch_rule = branch_rules[0]
        if "*" in branch_rule:
            console.print(f"[red]Error:[/red] Cannot rollback environment '{env}'.")
            console.print(f"  Environment has wildcard branch rule: '{branch_rule}'")
            console.print("  Rollback only works for environments with a single, literal branch rule.")
            console.print()
            console.print("[dim]Hint: Wildcard environments can match multiple branches.[/dim]")
            console.print("[dim]Use 'sb0 deployments list' to see all deployments, then rollback by version:[/dim]")
            console.print("  sb0 versions list --branch <specific-branch>")
            raise typer.Exit(1)

        # Get recent versions for this deployment
        try:
            versions_response = client.agents.deployments.versions.list(
                branch=branch_rule,
                namespace_slug=namespace_slug,
                agent_name=agent_short,
                limit=10,
            )
        except Exception as e:
            if "not found" in str(e).lower():
                console.print(f"[red]Error:[/red] No deployment found for branch '{branch_rule}'.")
                console.print("\nThe environment may not have been deployed yet.")
                raise typer.Exit(1) from e
            raise

        if not versions_response.versions:
            console.print(f"[red]Error:[/red] No versions found for environment '{env}'.")
            console.print("\nDeploy first before attempting rollback.")
            raise typer.Exit(1)

        if len(versions_response.versions) < 2 and version is None:
            console.print(f"[red]Error:[/red] Cannot rollback - only one version exists for '{env}'.")
            console.print("\nNo previous version to rollback to.")
            raise typer.Exit(1)

        # Show recent versions
        console.print(f"\n[bold]Recent versions for '{env}' (branch: {branch_rule}):[/bold]")

        table = Table()
        table.add_column("VERSION ID", style="cyan")
        table.add_column("GIT HASH")
        table.add_column("STATUS")
        table.add_column("DEPLOYED")
        table.add_column("MESSAGE")

        for i, ver in enumerate(versions_response.versions[:5]):
            status = ver.status
            if i == 0:
                status = "[green]current[/green]"

            msg = ver.git_message or ""
            if len(msg) > 40:
                msg = msg[:37] + "..."

            table.add_row(
                ver.id,
                ver.git_hash[:7],
                status,
                format_relative_time(ver.deployed_at),
                msg,
            )

        console.print(table)
        console.print()

        # Determine target version
        target_version_id = version
        target_version = None

        if target_version_id:
            # Find the specified version
            target_version = next(
                (v for v in versions_response.versions if v.id == target_version_id),
                None
            )
            if not target_version:
                console.print(f"[red]Error:[/red] Version '{target_version_id}' not found.")
                console.print("\nUse one of the version IDs shown above.")
                raise typer.Exit(1)
        else:
            # Default to previous version
            if len(versions_response.versions) < 2:
                console.print("[red]Error:[/red] No previous version to rollback to.")
                raise typer.Exit(1)
            target_version = versions_response.versions[1]
            target_version_id = target_version.id

        current_version = versions_response.versions[0]

        # Show what will change
        console.print("[bold]Rollback summary:[/bold]")
        console.print(f"  [cyan]From:[/cyan] {current_version.git_hash[:7]} → [cyan]To:[/cyan] {target_version.git_hash[:7]}")
        if target_version.git_message:
            msg = target_version.git_message.split("\n")[0]
            if len(msg) > 60:
                msg = msg[:57] + "..."
            console.print(f"  [cyan]Target message:[/cyan] {msg}")
        console.print()
        console.print("[yellow]Note:[/yellow] Pending secrets will NOT be modified.")
        console.print("  The rollback uses the secrets snapshot from the target version.")
        console.print()

        # Confirmation
        if not yes:
            confirm = questionary.confirm(
                f"Rollback '{env}' to version {target_version.git_hash[:7]}?"
            ).ask()
            if not handle_questionary_cancellation(str(confirm) if confirm else None, "rollback") or not confirm:
                console.print("[yellow]Rollback cancelled.[/yellow]")
                raise typer.Exit(0)

        # Execute rollback
        console.print(f"Rolling back '{env}'...")

        response = client.agents.environments.rollback.create(
            env_name=env,
            namespace_slug=namespace_slug,
            agent_name=agent_short,
            target_version_id=target_version_id,
        )

        console.print()
        console.print(f"[green]✓[/green] Rollback initiated for '{env}'")
        console.print(f"  [cyan]From:[/cyan] {response.from_git_hash[:7]} ({response.from_version_id})")
        console.print(f"  [cyan]To:[/cyan]   {response.to_git_hash[:7]} ({response.to_version_id})")
        console.print(f"  [cyan]Status:[/cyan] {response.status}")
        console.print(f"  [cyan]Message:[/cyan] {response.message}")
        console.print()
        console.print(f"[dim]Check status with: sb0 deployments show {branch_rule}[/dim]")

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {e!s}")
        logger.exception("Failed to rollback")
        raise typer.Exit(1) from e
