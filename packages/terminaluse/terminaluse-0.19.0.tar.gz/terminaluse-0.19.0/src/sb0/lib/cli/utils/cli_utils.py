from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone

import typer
from rich.console import Console

console = Console()


def handle_questionary_cancellation(result: str | None, operation: str = "operation") -> str:
    """Handle questionary cancellation by checking for None and exiting gracefully"""
    if result is None:
        console.print(f"[yellow]{operation.capitalize()} cancelled by user[/yellow]")
        raise typer.Exit(0)
    return result


def get_agent_name(agent: str | None = None) -> str:
    """
    Resolve agent name from --agent flag or manifest.yaml.

    Resolution order:
    1. From --agent flag if provided
    2. From manifest.yaml in current directory
    3. Error if neither available

    Returns:
        Agent name in 'namespace/agent-name' format
    """
    if agent:
        return agent
    try:
        from sb0.lib.sdk.config.agent_manifest import AgentManifest

        manifest_path = Path("manifest.yaml")
        if not manifest_path.exists():
            raise FileNotFoundError("manifest.yaml not found")

        manifest = AgentManifest.from_yaml(str(manifest_path))
        return manifest.agent.name  # Returns "namespace/agent-name"
    except FileNotFoundError:
        console.print("[red]Error:[/red] No manifest.yaml found and --agent not specified")
        raise typer.Exit(1) from None


def normalize_branch(branch: str) -> str:
    """
    Normalize a branch name to match backend expectations.

    Converts slashes and underscores to hyphens, lowercases the result.
    Example: 'vr/massive_cli_update-wt' -> 'vr-massive-cli-update-wt'
    """
    return branch.lower().replace("/", "-").replace("_", "-")


def parse_agent_name(agent_name: str) -> tuple[str, str]:
    """
    Parse 'namespace/agent-name' into (namespace_slug, short_name).

    Args:
        agent_name: Full agent name in 'namespace/agent-name' format

    Returns:
        Tuple of (namespace_slug, agent_short_name)

    Raises:
        typer.Exit: If agent_name is not in the correct format
    """
    if "/" not in agent_name:
        console.print(f"[red]Error:[/red] Agent name must be 'namespace/agent-name', got '{agent_name}'")
        raise typer.Exit(1)
    parts = agent_name.split("/", 1)
    return parts[0], parts[1]


def format_relative_time(dt: datetime | None) -> str:
    """Format a datetime as a human-readable relative time string."""
    if dt is None:
        return "-"

    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    diff = now - dt
    seconds = diff.total_seconds()

    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} min{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    else:
        return dt.strftime("%b %d, %Y")
