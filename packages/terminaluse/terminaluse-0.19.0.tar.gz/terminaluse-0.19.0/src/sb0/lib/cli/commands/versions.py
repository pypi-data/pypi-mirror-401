"""CLI commands for viewing deployment versions."""

from __future__ import annotations

import typer
from rich.panel import Panel
from rich.table import Table
from rich.console import Console

from sb0 import Sb0
from sb0.lib.utils.logging import make_logger
from sb0.lib.cli.utils.cli_utils import get_agent_name, format_relative_time, normalize_branch, parse_agent_name

logger = make_logger(__name__)
console = Console()

versions = typer.Typer(no_args_is_help=True)


@versions.command("list")
def list_versions(
    branch: str = typer.Option(..., "--branch", "-b", help="Branch name (e.g., 'main')"),
    limit: int = typer.Option(20, "--limit", "-n", help="Number of versions to show"),
    agent: str | None = typer.Option(None, "--agent", "-a", help="Agent name (defaults to manifest)"),
):
    """
    List versions for a branch deployment.

    Versions are ordered by deployed_at (most recent first).
    Each version represents a deployment to that branch.
    """
    agent_name = get_agent_name(agent)
    namespace_slug, agent_short = parse_agent_name(agent_name)
    branch_normalized = normalize_branch(branch)
    client = Sb0()

    try:
        response = client.agents.deployments.versions.list(
            branch=branch_normalized,
            namespace_slug=namespace_slug,
            agent_name=agent_short,
            limit=limit,
        )

        if not response.versions:
            console.print(f"No versions found for branch '{branch}'.")
            console.print("\nThe branch may not have been deployed yet.")
            return

        table = Table(title=f"Versions for '{branch}' ({response.total} total)")
        table.add_column("VERSION ID", style="cyan")
        table.add_column("GIT HASH")
        table.add_column("STATUS")
        table.add_column("DEPLOYED")
        table.add_column("AUTHOR")
        table.add_column("ROLLBACKS", justify="right")

        for i, ver in enumerate(response.versions):
            # Mark current version
            version_id = ver.id
            if i == 0 and ver.status == "ACTIVE":
                version_id = f"[green]{ver.id}[/green] ←"

            # Format status with color
            status = ver.status
            if status == "ACTIVE":
                status = "[green]active[/green]"
            elif status == "RETIRED":
                status = "[dim]retired[/dim]"
            elif status == "ROLLED_BACK":
                status = "[yellow]rolled_back[/yellow]"

            rollback_info = str(ver.rollback_count or 0)
            if ver.last_rollback_at:
                rollback_info += f" ({format_relative_time(ver.last_rollback_at)})"

            table.add_row(
                version_id,
                ver.git_hash[:7],
                status,
                format_relative_time(ver.deployed_at),
                ver.author_name,
                rollback_info,
            )

        console.print(table)

        if response.total > len(response.versions):
            console.print(f"\n[dim]Showing {len(response.versions)} of {response.total}. Use --limit to see more.[/dim]")

        console.print(f"\n[dim]Use 'sb0 versions show <VERSION_ID>' for full details.[/dim]")

    except Exception as e:
        if "not found" in str(e).lower():
            console.print(f"[red]Error:[/red] No deployment found for branch '{branch}'.")
            console.print("\nThe branch may not have been deployed yet.")
            console.print("Deploy with: sb0 agents deploy")
            raise typer.Exit(1) from e
        console.print(f"[red]Error:[/red] {e!s}")
        logger.exception("Failed to list versions")
        raise typer.Exit(1) from e


@versions.command("show")
def show_version(
    version_id: str = typer.Argument(..., help="Version ID to show"),
):
    """Show details for a specific version."""
    client = Sb0()

    try:
        ver = client.versions.retrieve(version_id=version_id)

        console.print(Panel.fit(f"[bold]Version: {ver.id}[/bold]", border_style="blue"))
        console.print()

        # Status with color
        status = ver.status
        if status == "ACTIVE":
            status_display = "[green]active[/green] (current deployment)"
        elif status == "RETIRED":
            status_display = "[dim]retired[/dim]"
        elif status == "ROLLED_BACK":
            status_display = "[yellow]rolled_back[/yellow]"
        else:
            status_display = status

        console.print(f"  [cyan]Status:[/cyan]       {status_display}")
        console.print(f"  [cyan]Deployed:[/cyan]     {format_relative_time(ver.deployed_at)}")
        console.print(f"  [cyan]Deployment ID:[/cyan] {ver.deployment_id}")
        console.print()

        console.print("[bold]Git Info[/bold]")
        console.print(f"  [cyan]Branch:[/cyan]  {ver.git_branch}")
        console.print(f"  [cyan]Hash:[/cyan]    {ver.git_hash}")
        if ver.git_message:
            # Truncate long messages
            msg = ver.git_message
            if len(msg) > 100:
                msg = msg[:97] + "..."
            console.print(f"  [cyan]Message:[/cyan] {msg}")
        console.print(f"  [cyan]Author:[/cyan]  {ver.author_name} <{ver.author_email}>")
        console.print()

        console.print("[bold]Image[/bold]")
        console.print(f"  [cyan]URL:[/cyan]     {ver.image_url}")
        if ver.image_expires_at:
            console.print(f"  [cyan]Expires:[/cyan] {format_relative_time(ver.image_expires_at)}")
        console.print()

        # Rollback info
        if ver.rollback_count and ver.rollback_count > 0:
            console.print("[bold]Rollback History[/bold]")
            console.print(f"  [cyan]Rollback count:[/cyan]     {ver.rollback_count}")
            if ver.last_rollback_at:
                console.print(f"  [cyan]Last rollback to:[/cyan]   {format_relative_time(ver.last_rollback_at)}")

        if ver.rolled_back_at:
            console.print(f"  [cyan]Rolled back from:[/cyan]  {format_relative_time(ver.rolled_back_at)}")

        if ver.retired_at:
            console.print()
            console.print(f"  [dim]Retired: {format_relative_time(ver.retired_at)}[/dim]")

        if ver.replicas is not None:
            console.print()
            console.print(f"  [cyan]Replicas:[/cyan] {ver.replicas}")

    except Exception as e:
        if "not found" in str(e).lower():
            console.print(f"[red]Error:[/red] Version '{version_id}' not found.")
            raise typer.Exit(1) from e
        console.print(f"[red]Error:[/red] {e!s}")
        logger.exception("Failed to get version")
        raise typer.Exit(1) from e
