from __future__ import annotations

import builtins
from pathlib import Path
from typing import TYPE_CHECKING

import typer
from rich.console import Console

if TYPE_CHECKING:
    pass

console = Console()


def _get_logger():
    """Lazy logger creation to avoid import overhead at module load."""
    from sb0.lib.utils.logging import make_logger
    return make_logger(__name__)


def deploy(
    manifest: str = typer.Option("manifest.yaml", "--manifest", "-m", help="Path to the manifest file"),
    tag: str | None = typer.Option(None, help="Override the image tag (default: git commit hash)"),
    branch: str | None = typer.Option(None, help="Override git branch (default: auto-detect)"),
    skip_build: bool = typer.Option(False, help="Skip image build, use existing image"),
    interactive: bool = typer.Option(True, "--interactive/--no-interactive", help="Enable interactive prompts"),
):
    """Deploy an agent to the sb0 platform.

    This command:
    1. Reads the manifest and detects git info
    2. Validates authentication and namespace access
    3. Gets registry credentials from the platform
    4. Builds and pushes the Docker image
    5. Triggers deployment via platform API
    6. Polls for deployment completion
    """
    import questionary
    from rich.panel import Panel
    from sb0 import Sb0
    from sb0.lib.cli.handlers.agent_handlers import build_agent
    from sb0.lib.cli.handlers.deploy_handlers import (
        DeploymentError,
        docker_login,
        docker_logout,
        build_deploy_config,
        poll_deployment_status,
        check_dockerfile_exists,
        validate_docker_running,
    )
    from sb0.lib.cli.utils.cli_utils import handle_questionary_cancellation
    from sb0.lib.cli.utils.git_utils import detect_git_info, detect_git_author, generate_image_tag
    from sb0.lib.cli.utils.credentials import get_stored_credentials
    from sb0.lib.sdk.config.agent_manifest import AgentManifest
    from sb0.lib.sdk.config.deployment_config import EnvironmentDeploymentConfig

    logger = _get_logger()
    console.print(Panel.fit("🚀 [bold blue]Deploy Agent[/bold blue]", border_style="blue"))

    try:
        # =================================================================
        # Phase 1: Initialization
        # =================================================================

        # 1.1 Validate manifest exists
        manifest_path = Path(manifest)
        if not manifest_path.exists():
            console.print("[red]Error:[/red] manifest.yaml not found in current directory")
            raise typer.Exit(1)

        # Load manifest
        manifest_obj = AgentManifest.from_yaml(str(manifest_path))

        # Agent name format is "namespace/agent-name"
        # Extract namespace and short name using existing properties
        full_name = manifest_obj.agent.name
        try:
            namespace = manifest_obj.agent.namespace_slug
            agent_name = manifest_obj.agent.short_name
        except (IndexError, AttributeError):
            console.print(f"[red]Error:[/red] Invalid agent name format: '{full_name}'")
            console.print("  Expected format: 'namespace/agent-name' (e.g., 'acme-corp/my-agent')")
            raise typer.Exit(1)

        console.print(f"[green]✓[/green] Loaded manifest: {full_name}")

        # 1.2 Detect git info
        git_info = detect_git_info(str(manifest_path.parent))
        git_author = detect_git_author(str(manifest_path.parent))
        if git_info.is_git_repo:
            console.print(f"[green]✓[/green] Git repo detected: {git_info.branch or 'detached HEAD'}")
            if git_info.is_dirty:
                console.print("[yellow]⚠ Warning:[/yellow] You have uncommitted changes.")
                console.print("  The deployed image will include these uncommitted changes.")
                if interactive:
                    proceed = questionary.confirm("Deploy anyway?").ask()
                    proceed = handle_questionary_cancellation(proceed, "dirty repo confirmation")
                    if not proceed:
                        console.print("Deployment cancelled")
                        raise typer.Exit(0)
        else:
            console.print("[yellow]⚠[/yellow] Not a git repository, using timestamp-based tag")

        # TODO: Re-enable auth check when login is implemented
        # 1.3 Validate authentication
        # if not is_authenticated():
        #     console.print("[red]Error:[/red] Not authenticated. Run 'sb0 login' first.")
        #     raise typer.Exit(1)

        # Initialize client
        client = Sb0()
        console.print("[green]✓[/green] Authenticated")

        # 1.4 Validate namespace access (uses auto-generated API)
        try:
            client.namespaces.retrieve_by_slug(namespace)
            console.print(f"[green]✓[/green] Namespace access validated: {namespace}")
        except Exception as e:
            # After SDK regeneration, this will be proper NotFoundError/ForbiddenError
            error_msg = str(e).lower()
            if "404" in error_msg or "not found" in error_msg:
                console.print(f"[red]Error:[/red] Namespace '{namespace}' not found")
            elif "403" in error_msg or "forbidden" in error_msg:
                console.print(f"[red]Error:[/red] You don't have access to namespace '{namespace}'")
            else:
                console.print(f"[red]Error:[/red] Failed to validate namespace: {e}")
            raise typer.Exit(1) from e

        # =================================================================
        # Phase 2: Registry Authentication
        # =================================================================

        console.print("\nGetting registry credentials...")
        try:
            registry_auth = client.registry.auth(namespace=namespace)
            console.print(f"[green]✓[/green] Registry: {registry_auth.registry_url}")
        except Exception as e:
            console.print(f"[red]Error:[/red] Failed to get registry credentials: {e}")
            raise typer.Exit(1) from e

        # Determine effective branch early (needed for env resolution)
        effective_branch = branch or git_info.branch or "main"

        # =================================================================
        # Phase 2.5: Resolve Environment
        # =================================================================

        console.print(f"\nResolving environment for branch '{effective_branch}'...")
        try:
            resolved_env = client.agents.resolve_env(
                namespace_slug=namespace,
                agent_name=agent_name,
                branch=effective_branch,
            )
            console.print(f"[green]✓[/green] Resolved environment: {resolved_env.environment.name}")
        except Exception as e:
            logger.warning(f"Failed to resolve environment: {e}")
            console.print(f"[yellow]⚠[/yellow] Could not resolve environment, using preview config")
            resolved_env = None

        # Get deployment config for resolved environment
        env_config: EnvironmentDeploymentConfig
        if manifest_obj.deployment:
            if resolved_env and resolved_env.environment.is_prod:
                env_config = manifest_obj.deployment.production
                console.print(f"  Using production config (replicaCount={env_config.replicaCount})")
            else:
                # Fallback to preview for any non-production environment
                env_config = manifest_obj.deployment.preview
                if resolved_env and resolved_env.environment.name != "preview":
                    console.print(f"[yellow]⚠[/yellow] No '{resolved_env.environment.name}' config in manifest, using preview")
                console.print(f"  Using preview config (replicaCount={env_config.replicaCount})")
        else:
            # No deployment section, use defaults
            env_config = EnvironmentDeploymentConfig()
            console.print("  Using default config (no deployment section in manifest)")

        # =================================================================
        # Phase 3: Build Image
        # =================================================================

        # Determine image tag
        image_tag = tag or generate_image_tag(git_info)

        # Build full image URL
        full_image = f"{registry_auth.registry_url}/{registry_auth.repository}/{namespace}/{agent_name}:{image_tag}"

        console.print(f"\n[bold]Build Configuration:[/bold]")
        console.print(f"  Agent: {full_name}")
        console.print(f"  Image: {full_image}")
        console.print(f"  Branch: {effective_branch}")
        if git_info.commit_hash:
            console.print(f"  Commit: {git_info.commit_hash[:12]}")

        if not skip_build:
            # Validate Docker is running
            if not validate_docker_running():
                console.print("[red]Error:[/red] Docker is not running. Please start Docker.")
                raise typer.Exit(1)

            # Validate Dockerfile exists
            if not check_dockerfile_exists(str(manifest_path)):
                console.print("[red]Error:[/red] Dockerfile not found in current directory")
                raise typer.Exit(1)

            # Docker login with platform-provided token
            console.print("\nLogging into registry...")
            docker_login(
                registry=registry_auth.registry_url,
                username=registry_auth.username,
                password=registry_auth.token,
            )
            console.print("[green]✓[/green] Logged into registry")

            # Build and push image
            console.print("\nBuilding and pushing image...")
            try:
                build_agent(
                    manifest_path=str(manifest_path),
                    registry_url=registry_auth.registry_url,
                    repository_name=f"{registry_auth.repository}/{namespace}/{agent_name}",
                    tag=image_tag,
                    push=True,
                    platforms=["linux/amd64"],
                )
                console.print(f"[green]✓[/green] Built and pushed: {agent_name}:{image_tag}")
            except Exception as e:
                console.print(f"[red]Error:[/red] Docker build failed: {e}")
                raise typer.Exit(1) from e
            finally:
                # Logout from registry
                docker_logout(registry_auth.registry_url)
        else:
            console.print("\n[yellow]Skipping build[/yellow] (--skip-build)")

        # =================================================================
        # Phase 5: Trigger Deployment
        # =================================================================

        console.print(f"\nDeploying to {namespace}/{agent_name}@{effective_branch}...")

        # Build deployment config from resolved environment config
        is_production = resolved_env is not None and resolved_env.environment.is_prod
        deploy_config = build_deploy_config(env_config, is_production=is_production)

        # Show task stickiness setting
        are_tasks_sticky = deploy_config.get("are_tasks_sticky", False)
        sticky_behavior = "tasks stay on old version" if are_tasks_sticky else "tasks migrate immediately"
        sticky_color = "green" if are_tasks_sticky else "dim"
        console.print(f"  Task stickiness: [{sticky_color}]{are_tasks_sticky}[/{sticky_color}] ({sticky_behavior})")

        # Get author info from git or stored credentials
        stored_creds = get_stored_credentials()
        author_email = git_author.email or (stored_creds.email if stored_creds else None) or "unknown@sb0.dev"
        author_name = git_author.name or (stored_creds.email if stored_creds else None) or "Unknown"

        try:
            # Trigger deployment via platform API (uses auto-generated API)
            deploy_response = client.agents.deploy(
                agent_name=full_name,  # namespace/agent-name format
                author_email=author_email,
                author_name=author_name,
                branch=effective_branch,
                git_hash=git_info.commit_hash or image_tag,
                git_message=git_info.commit_message,
                image_url=full_image,
                is_dirty=git_info.is_dirty,
                replicas=deploy_config.get("replicas", 1),
                resources=deploy_config.get("resources"),
                are_tasks_sticky=deploy_config.get("are_tasks_sticky"),
            )

            console.print(f"  Agent ID: {deploy_response.agent_id}")
            console.print(f"  Deployment ID: {deploy_response.deployment_id}")
            console.print(f"  Version ID: {deploy_response.version_id}")

        except Exception as e:
            console.print(f"[red]Error:[/red] Deployment failed: {e}")
            raise typer.Exit(1) from e

        # =================================================================
        # Phase 9: Poll and Complete
        # =================================================================

        console.print()
        try:
            status = poll_deployment_status(
                client,
                deploy_response.deployment_id,
                timeout=300,  # 5 minutes
                interval=2,
            )

            if status.status.lower() == "ready":
                console.print(f"\n[bold green]✓ Deployed version {image_tag}[/bold green]")
                console.print(f"\nYour agent is live:")
                console.print(f"  Agent ref: {namespace}/{agent_name}@{effective_branch}")
                console.print(f"  API: https://api.sb0.dev/agents/rpc")
            else:
                console.print(f"\n[red]✗ Deployment failed[/red]")
                console.print(f"\nDebug:")
                console.print(f"  Logs: sb0 agents logs {agent_name} --version {image_tag}")
                raise typer.Exit(1)

        except DeploymentError as e:
            console.print(f"\n[red]✗ {str(e)}[/red]")
            console.print(f"\nDebug:")
            console.print(f"  Logs: sb0 agents logs {agent_name} --version {image_tag}")
            raise typer.Exit(1) from e

    except DeploymentError as e:
        console.print(f"[red]Deployment failed:[/red] {str(e)}")
        logger.exception("Deployment failed")
        raise typer.Exit(1) from e
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {str(e)}")
        logger.exception("Unexpected error during deployment")
        raise typer.Exit(1) from e
