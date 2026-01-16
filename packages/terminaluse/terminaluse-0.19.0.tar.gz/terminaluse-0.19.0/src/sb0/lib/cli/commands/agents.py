from __future__ import annotations

import builtins
from pathlib import Path
from typing import TYPE_CHECKING

import typer
from rich.console import Console

# Lazy imports - these are deferred to function scope for faster CLI startup
if TYPE_CHECKING:
    from sb0 import Sb0
    from sb0.lib.cli.debug import DebugMode, DebugConfig
    from sb0.lib.sdk.config.agent_manifest import AgentManifest

console = Console()
agents = typer.Typer(no_args_is_help=True)


def _get_logger():
    """Lazy logger creation to avoid import overhead at module load."""
    from sb0.lib.utils.logging import make_logger
    return make_logger(__name__)


@agents.command()
def get(
    agent_id: str = typer.Argument(..., help="ID of the agent to get"),
):
    """
    Get the agent with the given name.
    """
    from rich import print_json
    from sb0 import Sb0

    logger = _get_logger()
    logger.info(f"Getting agent with ID: {agent_id}")
    client = Sb0()
    agent = client.agents.retrieve(agent_id=agent_id)
    logger.info(f"Agent retrieved: {agent}")
    print_json(data=agent.to_dict(), default=str)


@agents.command()
def list():
    """
    List all agents.
    """
    from rich import print_json
    from sb0 import Sb0

    logger = _get_logger()
    logger.info("Listing all agents")
    client = Sb0()
    agents_list = client.agents.list()
    logger.info(f"Agents retrieved: {agents_list}")
    print_json(data=[agent.to_dict() for agent in agents_list], default=str)


@agents.command()
def delete(
    agent_name: str = typer.Argument(..., help="Name of the agent to delete (namespace/agent-name format)"),
):
    """
    Delete the agent with the given name.
    """
    from sb0 import Sb0
    from sb0.lib.cli.utils.cli_utils import parse_agent_name

    logger = _get_logger()
    logger.info(f"Deleting agent with name: {agent_name}")
    namespace_slug, agent_short = parse_agent_name(agent_name)
    client = Sb0()
    client.agents.delete_by_name(namespace_slug=namespace_slug, agent_name=agent_short)
    logger.info(f"Agent deleted: {agent_name}")


@agents.command()
def logs(
    agent_name: str = typer.Argument(..., help="Name of the agent to view logs for"),
    tail: bool = typer.Option(False, "--tail", "-f", help="Follow log output"),
    limit: int = typer.Option(100, "--limit", "-n", help="Number of log entries to fetch"),
):
    """
    View logs from a deployed agent.

    Shows stdout, stderr, and server logs from the agent's execution.
    Use --tail to follow logs in real-time.
    """
    from sb0.lib.cli.handlers.log_handlers import get_logs, stream_logs

    logger = _get_logger()
    try:
        if tail:
            stream_logs(agent_name)
        else:
            get_logs(agent_name, limit)
    except Exception as e:
        console.print(f"[red]Error viewing logs: {str(e)}[/red]")
        logger.exception("Error viewing agent logs")
        raise typer.Exit(1) from e


@agents.command()
def cleanup_workflows(
    agent_name: str = typer.Argument(..., help="Name of the agent to cleanup workflows for (namespace/agent-name format)"),
    force: bool = typer.Option(
        False, help="Force cleanup using direct Temporal termination (bypasses development check)"
    ),
):
    """
    Clean up all running workflows for an agent.

    By default, uses graceful cancellation via agent RPC.
    With --force, directly terminates workflows via Temporal client.
    This is a convenience command that does the same thing as 'sb0 tasks cleanup'.
    """
    from sb0.lib.cli.handlers.cleanup_handlers import cleanup_agent_workflows

    logger = _get_logger()
    try:
        console.print(f"[blue]Cleaning up workflows for agent '{agent_name}'...[/blue]")

        cleanup_agent_workflows(agent_name=agent_name, force=force, development_only=True)

        console.print(f"[green]✓ Workflow cleanup completed for agent '{agent_name}'[/green]")

    except Exception as e:
        console.print(f"[red]Cleanup failed: {str(e)}[/red]")
        logger.exception("Agent workflow cleanup failed")
        raise typer.Exit(1) from e


@agents.command(hidden=True)
def build(
    manifest: str = typer.Option(..., "--manifest", "-m", help="Path to the manifest you want to use"),
    registry: str | None = typer.Option(None, help="Registry URL for pushing the built image"),
    repository_name: str | None = typer.Option(None, help="Repository name to use for the built image"),
    platforms: str | None = typer.Option(
        None, help="Platform to build the image for. Please enter a comma separated list of platforms."
    ),
    push: bool = typer.Option(False, help="Whether to push the image to the registry"),
    secret: str | None = typer.Option(
        None,
        help="Docker build secret in the format 'id=secret-id,src=path-to-secret-file'",
    ),
    tag: str | None = typer.Option(None, help="Image tag to use (defaults to 'latest')"),
    build_arg: builtins.list[str] | None = typer.Option(  # noqa: B008
        None,
        help="Docker build argument in the format 'KEY=VALUE' (can be used multiple times)",
    ),
):
    """
    Build an agent image locally from the given manifest.
    """
    from sb0.lib.cli.handlers.agent_handlers import build_agent

    logger = _get_logger()
    typer.echo(f"Building agent image from manifest: {manifest}")

    # Validate required parameters for building
    if push and not registry:
        typer.echo("Error: --registry is required when --push is enabled", err=True)
        raise typer.Exit(1)

    # Only proceed with build if we have a registry (for now, to match existing behavior)
    if not registry:
        typer.echo("No registry provided, skipping image build")
        return

    platform_list = platforms.split(",") if platforms else ["linux/amd64"]

    try:
        image_url = build_agent(
            manifest_path=manifest,
            registry_url=registry,
            repository_name=repository_name,
            platforms=platform_list,
            push=push,
            secret=secret or "",  # Provide default empty string
            tag=tag or "latest",  # Provide default
            build_args=build_arg or [],  # Provide default empty list
        )
        if image_url:
            typer.echo(f"Successfully built image: {image_url}")
        else:
            typer.echo("Image build completed but no URL returned")
    except Exception as e:
        typer.echo(f"Error building agent image: {str(e)}", err=True)
        logger.exception("Error building agent image")
        raise typer.Exit(1) from e


@agents.command(hidden=True)
def run(
    manifest: str = typer.Option(..., "--manifest", "-m", help="Path to the manifest you want to use"),
    cleanup_on_start: bool = typer.Option(False, help="Clean up existing workflows for this agent before starting"),
    # Debug options
    debug: bool = typer.Option(False, help="Enable debug mode for both worker and ACP (disables auto-reload)"),
    debug_worker: bool = typer.Option(False, help="Enable debug mode for temporal worker only"),
    debug_acp: bool = typer.Option(False, help="Enable debug mode for ACP server only"),
    debug_port: int = typer.Option(5678, help="Port for remote debugging (worker uses this, ACP uses port+1)"),
    wait_for_debugger: bool = typer.Option(False, help="Wait for debugger to attach before starting"),
) -> None:
    """
    Run an agent locally from the given manifest.
    """
    from sb0.lib.cli.debug import DebugMode, DebugConfig
    from sb0.lib.cli.handlers.agent_handlers import run_agent
    from sb0.lib.cli.handlers.cleanup_handlers import cleanup_agent_workflows
    from sb0.lib.sdk.config.agent_manifest import AgentManifest

    logger = _get_logger()
    typer.echo(f"Running agent from manifest: {manifest}")

    # Optionally cleanup existing workflows before starting
    if cleanup_on_start:
        try:
            # Parse manifest to get agent name
            manifest_obj = AgentManifest.from_yaml(file_path=manifest)
            agent_name = manifest_obj.agent.name

            console.print(f"[yellow]Cleaning up existing workflows for agent '{agent_name}'...[/yellow]")
            cleanup_agent_workflows(agent_name=agent_name, force=False, development_only=True)
            console.print("[green]✓ Pre-run cleanup completed[/green]")

        except Exception as e:
            console.print(f"[yellow]⚠ Pre-run cleanup failed: {str(e)}[/yellow]")
            logger.warning(f"Pre-run cleanup failed: {e}")

    # Create debug configuration based on CLI flags
    debug_config = None
    if debug or debug_worker or debug_acp:
        # Determine debug mode
        if debug:
            mode = DebugMode.BOTH
        elif debug_worker and debug_acp:
            mode = DebugMode.BOTH
        elif debug_worker:
            mode = DebugMode.WORKER
        elif debug_acp:
            mode = DebugMode.ACP
        else:
            mode = DebugMode.NONE

        debug_config = DebugConfig(
            enabled=True,
            mode=mode,
            port=debug_port,
            wait_for_attach=wait_for_debugger,
            auto_port=False,  # Use fixed port to match VS Code launch.json
        )

        console.print(f"[blue]🐛 Debug mode enabled: {mode.value}[/blue]")
        if wait_for_debugger:
            console.print("[yellow]⏳ Processes will wait for debugger attachment[/yellow]")

    try:
        run_agent(manifest_path=manifest, debug_config=debug_config)
    except Exception as e:
        typer.echo(f"Error running agent: {str(e)}", err=True)
        logger.exception("Error running agent")
        raise typer.Exit(1) from e


