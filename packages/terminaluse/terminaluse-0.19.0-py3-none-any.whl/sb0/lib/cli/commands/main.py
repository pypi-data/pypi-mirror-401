import typer

from sb0.lib.cli.commands.ls import ls
from sb0.lib.cli.commands.uv import uv
from sb0.lib.cli.commands.env import env
from sb0.lib.cli.commands.auth import login, logout, whoami
from sb0.lib.cli.commands.init import init
from sb0.lib.cli.commands.tasks import tasks
from sb0.lib.cli.commands.agents import agents
from sb0.lib.cli.commands.deploy import deploy
from sb0.lib.cli.commands.rollback import rollback
from sb0.lib.cli.commands.versions import versions
from sb0.lib.cli.commands.deployments import deployments

# Create the main Typer application
app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"], "max_content_width": 800},
    pretty_exceptions_show_locals=False,
    pretty_exceptions_enable=False,
    add_completion=False,
    no_args_is_help=True,
)

# Add the subcommands
app.add_typer(agents, name="agents", help="Get, list, and manage agents")
app.add_typer(tasks, name="tasks", help="Get, list, and delete tasks")
app.add_typer(env, name="env", help="Manage environment variables")
app.add_typer(versions, name="versions", help="View deployment versions")
app.add_typer(deployments, name="deployments", help="Manage deployments")
app.add_typer(uv, name="uv", help="Wrapper for uv command with Sb0-specific enhancements")

# Add init command with documentation
app.command(
    help="Initialize a new agent project with a template (interactive)",
)(init)

# Add auth commands as top-level commands
app.command(help="Authenticate with the sb0 platform")(login)
app.command(help="Log out and clear stored credentials")(logout)
app.command(help="Show current authentication status")(whoami)

# Add rollback as a top-level command (not a subcommand group)
app.command(help="Rollback an environment to a previous version")(rollback)

# Add ls as a top-level command for listing versions/events
app.command(help="List recent versions, or events for a branch")(ls)

# Add deploy as a top-level command
app.command(help="Deploy an agent to the sb0 platform")(deploy)


if __name__ == "__main__":
    app()
