"""CLI command for listing recent deployments or branch events."""

from __future__ import annotations

import time
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed

import typer
from rich.table import Table
from rich.console import Console

from sb0 import Sb0
from sb0.lib.utils.logging import make_logger
from sb0.lib.cli.utils.cli_utils import get_agent_name, normalize_branch, format_relative_time, parse_agent_name

logger = make_logger(__name__)
console = Console()


@dataclass
class VersionDisplay:
    """Version data for display."""

    id: str
    git_branch: str
    git_hash: str
    git_message: str | None
    status: str
    deployed_at: datetime
    author_name: str
    is_dirty: bool


@dataclass
class EventDisplay:
    """Event data for display."""

    created_at: datetime
    event_type: str
    version_id: str
    triggered_by: str | None
    actor_email: str | None


def _format_status(status: str) -> str:
    """Format version status with color."""
    status_upper = status.upper()
    if status_upper == "ACTIVE":
        return "[green]ready[/green]"
    elif status_upper == "DEPLOYING":
        return "[yellow]deploying[/yellow]"
    elif status_upper == "FAILED":
        return "[red]failed[/red]"
    elif status_upper in ("RETIRED", "ROLLED_BACK", "DRAINING"):
        return f"[dim]{status.lower()}[/dim]"
    return status.lower()


def _format_event_type(event_type: str) -> str:
    """Format event type with color."""
    # Remove VERSION_ prefix for cleaner display
    display_type = event_type.replace("VERSION_", "")

    if display_type in ("CREATED", "ACTIVATED"):
        return f"[green]{display_type}[/green]"
    elif display_type == "FAILED":
        return f"[red]{display_type}[/red]"
    elif display_type in ("ROLLED_BACK_FROM", "ROLLED_BACK_TO"):
        return f"[yellow]{display_type}[/yellow]"
    elif display_type in ("DRAINING", "RETIRED"):
        return f"[dim]{display_type}[/dim]"
    elif display_type == "REDEPLOYED":
        return f"[cyan]{display_type}[/cyan]"
    return display_type


def _format_git_info(git_hash: str, git_message: str | None, is_dirty: bool = False, max_len: int = 30) -> str:
    """Format git hash and truncated message.

    Args:
        git_hash: The git commit hash
        git_message: The commit message (optional)
        is_dirty: Whether the working directory had uncommitted changes
        max_len: Maximum length for the commit message

    Returns:
        Formatted string like "d abc1234 (message)" where "d" prefix indicates dirty
    """
    # Prefix with "d" if deployed with uncommitted changes
    prefix = "d " if is_dirty else ""
    info = f"{prefix}{git_hash[:7]}"
    if git_message:
        msg = git_message.split("\n")[0][:max_len]
        if len(git_message) > max_len:
            msg += "..."
        info += f" ({msg})"
    return info




def _list_versions(
    client: Sb0,
    agent_name: str,
    limit: int,
    include_retired: bool,
) -> None:
    """List recent versions across all branches."""
    start_time = time.time()
    namespace_slug, short_name = parse_agent_name(agent_name)

    # Step 1: Get all deployments (branches)
    deployments_response = client.agents.deployments.list(
        namespace_slug=namespace_slug,
        agent_name=short_name,
        include_retired=include_retired,
    )

    if not deployments_response.deployments:
        console.print(f"No deployments found for agent '[bold]{agent_name}[/bold]'.")
        console.print("\nDeploy with: [cyan]sb0 agents deploy[/cyan]")
        return

    # Step 2: Fetch versions from each branch in parallel
    all_versions: list[VersionDisplay] = []
    versions_per_branch = max(3, limit // len(deployments_response.deployments) + 1)

    def fetch_versions(dep):
        try:
            response = client.agents.deployments.versions.list(
                branch=dep.branch_normalized,
                namespace_slug=namespace_slug,
                agent_name=short_name,
                limit=versions_per_branch,
            )
            return [
                VersionDisplay(
                    id=v.id,
                    git_branch=v.git_branch,
                    git_hash=v.git_hash,
                    git_message=v.git_message,
                    status=v.status,
                    deployed_at=v.deployed_at,
                    author_name=v.author_name,
                    is_dirty=v.is_dirty or False,
                )
                for v in response.versions
            ]
        except Exception as e:
            logger.warning(f"Failed to fetch versions for {dep.branch}: {e}")
            return []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_versions, dep) for dep in deployments_response.deployments]
        for future in as_completed(futures):
            all_versions.extend(future.result())

    if not all_versions:
        console.print(f"No versions found for agent '[bold]{agent_name}[/bold]'.")
        return

    # Step 3: Sort by deployed_at and limit
    all_versions.sort(key=lambda v: v.deployed_at, reverse=True)
    display_versions = all_versions[:limit]

    # Step 4: Display
    elapsed_ms = int((time.time() - start_time) * 1000)
    console.print(f"> Versions for [bold]{agent_name}[/bold] [{elapsed_ms}ms]\n")

    table = Table(show_header=True, header_style="bold")
    table.add_column("AGE", style="dim")
    table.add_column("BRANCH", style="cyan")
    table.add_column("VERSION", style="dim")
    table.add_column("STATUS")
    table.add_column("GIT")
    table.add_column("AUTHOR")

    for ver in display_versions:
        table.add_row(
            format_relative_time(ver.deployed_at),
            ver.git_branch,
            ver.id[:12],
            _format_status(ver.status),
            _format_git_info(ver.git_hash, ver.git_message, ver.is_dirty),
            ver.author_name,
        )

    console.print(table)

    if len(all_versions) > limit:
        console.print(f"\n[dim]Showing {limit} of {len(all_versions)}. Use -n to see more.[/dim]")


def _list_events(
    client: Sb0,
    agent_name: str,
    branch: str,
    limit: int,
) -> None:
    """List events for a specific branch."""
    start_time = time.time()
    namespace_slug, short_name = parse_agent_name(agent_name)
    branch_normalized = normalize_branch(branch)

    # Step 1: Get the deployment for this branch
    try:
        deployment = client.agents.deployments.retrieve(
            namespace_slug=namespace_slug,
            agent_name=short_name,
            branch=branch_normalized,
        )
    except Exception as e:
        console.print(f"[red]Error:[/red] Deployment for branch '{branch}' not found.")
        console.print(f"\nAvailable branches can be seen with: [cyan]sb0 ls[/cyan]")
        logger.debug(f"Failed to get deployment: {e}")
        raise typer.Exit(1) from e

    # Step 2: Fetch events
    try:
        events_response = client.deployments.events.list(deployment_id=deployment.id, limit=limit)
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to fetch events: {e}")
        raise typer.Exit(1) from e

    if not events_response.events:
        console.print(f"No events found for [bold]{agent_name}[/bold]@{branch}.")
        return

    # Step 3: Build display data and sort chronologically (most recent first)
    events: list[EventDisplay] = []
    for ev in events_response.events:
        events.append(
            EventDisplay(
                created_at=ev.created_at,
                event_type=ev.event_type,
                version_id=ev.version_id,
                triggered_by=ev.content.triggered_by if ev.content else None,
                actor_email=ev.content.actor_email if ev.content else None,
            )
        )
    events.sort(key=lambda e: e.created_at, reverse=True)

    # Step 4: Fetch version details for git hash display
    unique_version_ids = {ev.version_id for ev in events if ev.version_id}
    version_info: dict[str, tuple[str, bool]] = {}  # version_id -> (git_hash, is_dirty)

    def fetch_version(version_id: str) -> tuple[str, str, bool] | None:
        try:
            version = client.versions.retrieve(version_id)
            return (version_id, version.git_hash, version.is_dirty or False)
        except Exception as e:
            logger.debug(f"Failed to fetch version {version_id}: {e}")
            return None

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_version, vid) for vid in unique_version_ids]
        for future in as_completed(futures):
            result = future.result()
            if result:
                vid, git_hash, is_dirty = result
                version_info[vid] = (git_hash, is_dirty)

    # Step 5: Display
    elapsed_ms = int((time.time() - start_time) * 1000)
    console.print(f"> Events for [bold]{agent_name}[/bold]@{branch} [{elapsed_ms}ms]\n")

    table = Table(show_header=True, header_style="bold")
    table.add_column("AGE", style="dim")
    table.add_column("EVENT")
    table.add_column("VERSION", style="dim")
    table.add_column("GIT")
    table.add_column("TRIGGER", style="dim")

    for ev in events:
        git_display = "-"
        if ev.version_id and ev.version_id in version_info:
            git_hash, is_dirty = version_info[ev.version_id]
            prefix = "d " if is_dirty else ""
            git_display = f"{prefix}{git_hash[:7]}"

        table.add_row(
            format_relative_time(ev.created_at),
            _format_event_type(ev.event_type),
            ev.version_id[:12] if ev.version_id else "-",
            git_display,
            ev.triggered_by.lower() if ev.triggered_by else "-",
        )

    console.print(table)

    if events_response.has_more:
        console.print(f"\n[dim]Showing {len(events)} events. Use -n to see more.[/dim]")


def ls(
    branch: Optional[str] = typer.Argument(None, help="Branch name to show events for"),
    limit: int = typer.Option(10, "--limit", "-n", help="Number of items to show"),
    agent: Optional[str] = typer.Option(None, "--agent", "-a", help="Agent name (defaults to manifest)"),
    include_retired: bool = typer.Option(False, "--all", help="Include retired branches (versions mode only)"),
):
    """
    List recent deployments or events for a branch.

    Without arguments, shows recent versions across all branches.
    With a branch name, shows lifecycle events for that branch.

    Examples:
        sb0 ls              # List recent versions
        sb0 ls main         # List events for 'main' branch
        sb0 ls -n 20        # Show 20 most recent versions
    """
    agent_name = get_agent_name(agent)
    client = Sb0()

    try:
        if branch:
            # Show events for specific branch
            _list_events(client, agent_name, branch, limit)
        else:
            # Show versions across all branches
            _list_versions(client, agent_name, limit, include_retired)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {e!s}")
        logger.exception("Failed to list deployments")
        raise typer.Exit(1) from e
