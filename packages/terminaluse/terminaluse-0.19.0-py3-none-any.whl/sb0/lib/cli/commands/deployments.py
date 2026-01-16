"""CLI commands for managing deployments."""

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

deployments = typer.Typer(no_args_is_help=True)


def _format_status(status: str) -> str:
    """Format deployment status with color."""
    status_lower = status.lower()
    if status_lower == "ready":
        return "[green]ready[/green]"
    elif status_lower == "deploying":
        return "[yellow]deploying[/yellow]"
    elif status_lower == "failed":
        return "[red]failed[/red]"
    elif status_lower == "retired":
        return "[dim]retired[/dim]"
    return status


@deployments.command("list")
def list_deployments(
    include_retired: bool = typer.Option(False, "--include-retired", help="Include retired deployments"),
    agent: str | None = typer.Option(None, "--agent", "-a", help="Agent name (defaults to manifest)"),
):
    """
    List all deployments for the current agent.

    Each deployment represents an active branch. By default, retired
    deployments are hidden.
    """
    agent_name = get_agent_name(agent)
    namespace_slug, agent_short = parse_agent_name(agent_name)
    client = Sb0()

    try:
        response = client.agents.deployments.list(
            agent_name=agent_short,
            namespace_slug=namespace_slug,
            include_retired=include_retired,
        )

        if not response.deployments:
            if include_retired:
                console.print(f"No deployments found for agent '{agent_name}'.")
            else:
                console.print(f"No active deployments found for agent '{agent_name}'.")
                console.print("\nDeploy with: sb0 agents deploy")
            return

        table = Table(title=f"Deployments for {agent_name}")
        table.add_column("BRANCH", style="cyan")
        table.add_column("STATUS")
        table.add_column("VERSION")
        table.add_column("REPLICAS", justify="right")
        table.add_column("DEPLOYED")

        for dep in response.deployments:
            # Get version info
            version_info = "-"
            if dep.current_version:
                version_info = f"{dep.current_version.git_hash[:7]}"
                if dep.current_version.git_message:
                    msg = dep.current_version.git_message.split("\n")[0][:30]
                    if len(dep.current_version.git_message) > 30:
                        msg += "..."
                    version_info += f" ({msg})"

            # Get deployed time
            deployed_at = "-"
            if dep.current_version:
                deployed_at = format_relative_time(dep.current_version.deployed_at)
            elif dep.updated_at:
                deployed_at = format_relative_time(dep.updated_at)

            table.add_row(
                dep.branch,
                _format_status(dep.status),
                version_info,
                str(dep.replicas),
                deployed_at,
            )

        console.print(table)
        console.print(f"\n{response.total} deployment(s)")

        if not include_retired:
            console.print("\n[dim]Use --include-retired to see retired deployments.[/dim]")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e!s}")
        logger.exception("Failed to list deployments")
        raise typer.Exit(1) from e


@deployments.command("show")
def show_deployment(
    branch: str = typer.Argument(..., help="Branch name"),
    agent: str | None = typer.Option(None, "--agent", "-a", help="Agent name (defaults to manifest)"),
):
    """Show details for a specific deployment by branch."""
    agent_name = get_agent_name(agent)
    namespace_slug, agent_short = parse_agent_name(agent_name)
    branch_normalized = normalize_branch(branch)
    client = Sb0()

    try:
        dep = client.agents.deployments.retrieve(
            branch=branch_normalized,
            namespace_slug=namespace_slug,
            agent_name=agent_short,
        )

        console.print(Panel.fit(f"[bold]Deployment: {dep.branch}[/bold]", border_style="blue"))
        console.print()

        console.print(f"  [cyan]ID:[/cyan]               {dep.id}")
        console.print(f"  [cyan]Status:[/cyan]           {_format_status(dep.status)}")
        console.print(f"  [cyan]Branch:[/cyan]           {dep.branch}")
        console.print(f"  [cyan]Branch (norm):[/cyan]    {dep.branch_normalized}")
        console.print(f"  [cyan]Replicas:[/cyan]         {dep.replicas}")

        if dep.acp_url:
            console.print(f"  [cyan]ACP URL:[/cyan]          {dep.acp_url}")

        console.print()

        if dep.current_version:
            console.print("[bold]Current Version[/bold]")
            console.print(f"  [cyan]Version ID:[/cyan]  {dep.current_version.id}")
            console.print(f"  [cyan]Git Hash:[/cyan]    {dep.current_version.git_hash}")
            console.print(f"  [cyan]Status:[/cyan]      {dep.current_version.status}")
            console.print(f"  [cyan]Deployed:[/cyan]    {format_relative_time(dep.current_version.deployed_at)}")
            if dep.current_version.git_message:
                msg = dep.current_version.git_message
                if len(msg) > 100:
                    msg = msg[:97] + "..."
                console.print(f"  [cyan]Message:[/cyan]     {msg}")
            console.print()

        # Timestamps
        if dep.created_at:
            console.print(f"  [cyan]Created:[/cyan]  {format_relative_time(dep.created_at)}")
        if dep.updated_at:
            console.print(f"  [cyan]Updated:[/cyan]  {format_relative_time(dep.updated_at)}")

        if dep.retired_at:
            console.print()
            console.print("[bold yellow]Retired[/bold yellow]")
            console.print(f"  [cyan]Retired at:[/cyan]  {format_relative_time(dep.retired_at)}")
            if dep.retired_reason:
                console.print(f"  [cyan]Reason:[/cyan]      {dep.retired_reason}")

        console.print()
        console.print("[dim]Commands:[/dim]")
        console.print(f"  [dim]View versions:[/dim] sb0 versions list --branch {branch}")
        console.print(f"  [dim]View logs:[/dim]     sb0 agents logs --branch {branch}")

    except Exception as e:
        if "not found" in str(e).lower():
            console.print(f"[red]Error:[/red] No deployment found for branch '{branch}'.")
            console.print("\nThe branch may not have been deployed yet.")
            console.print("Deploy with: sb0 agents deploy")
            raise typer.Exit(1) from e
        console.print(f"[red]Error:[/red] {e!s}")
        logger.exception("Failed to get deployment")
        raise typer.Exit(1) from e
