from __future__ import annotations

from enum import Enum
from typing import Any, Dict
from pathlib import Path

import questionary
from jinja2 import Environment, FileSystemLoader
from rich.panel import Panel
from rich.console import Console

from sb0.lib.utils.logging import make_logger

logger = make_logger(__name__)
console = Console()

# Get the templates directory relative to this file
TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


class TemplateType(str, Enum):
    TEMPORAL = "temporal"
    DEFAULT = "default"


def render_template(template_path: str, context: Dict[str, Any], template_type: TemplateType) -> str:
    """Render a template with the given context"""
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR / template_type.value))
    template = env.get_template(template_path)
    return template.render(**context)


def create_project_structure(path: Path, context: Dict[str, Any], template_type: TemplateType, use_uv: bool):
    """Create the project structure from templates"""
    # Create project directory
    project_dir: Path = path / context["project_name"]
    project_dir.mkdir(parents=True, exist_ok=True)

    # Create project/code directory
    code_dir: Path = project_dir / "project"
    code_dir.mkdir(parents=True, exist_ok=True)

    # Create __init__.py
    (code_dir / "__init__.py").touch()

    # Define project files based on template type
    project_files = {
        TemplateType.TEMPORAL: ["acp.py", "workflow.py", "run_worker.py"],
        TemplateType.DEFAULT: ["acp.py"],
    }[template_type]

    # Create project/code files
    for template in project_files:
        template_path = f"project/{template}.j2"
        output_path = code_dir / template
        output_path.write_text(render_template(template_path, context, template_type))

    # Create root files
    root_templates = {
        ".dockerignore.j2": ".dockerignore",
        "manifest.yaml.j2": "manifest.yaml",
        "README.md.j2": "README.md",
        "environments.yaml.j2": "environments.yaml",
    }

    # Add package management file based on uv choice
    if use_uv:
        root_templates["pyproject.toml.j2"] = "pyproject.toml"
        root_templates["Dockerfile-uv.j2"] = "Dockerfile"
    else:
        root_templates["requirements.txt.j2"] = "requirements.txt"
        root_templates["Dockerfile.j2"] = "Dockerfile"

    # Add development notebook for agents
    root_templates["dev.ipynb.j2"] = "dev.ipynb"

    for template, output in root_templates.items():
        output_path = project_dir / output
        output_path.write_text(render_template(template, context, template_type))

    console.print(f"\n[green]✓[/green] Created project structure at: {project_dir}")


def get_project_context(answers: Dict[str, Any], project_path: Path, manifest_root: Path) -> Dict[str, Any]:  # noqa: ARG001
    """Get the project context from user answers"""
    # Use agent_directory_name as project_name
    project_name = answers["agent_directory_name"].replace("-", "_")

    # Now, this is actually the exact same as the project_name because we changed the build root to be ../
    project_path_from_build_root = project_name

    # Use the already-parsed namespace and agent short name from answers
    agent_short_name = answers["agent_short_name"]

    return {
        **answers,
        "project_name": project_name,
        "workflow_class": "".join(word.capitalize() for word in agent_short_name.split("-")) + "Workflow",
        "workflow_name": agent_short_name,
        "queue_name": project_name + "_queue",
        "project_path_from_build_root": project_path_from_build_root,
    }


def init():
    """Initialize a new agent project"""
    console.print(
        Panel.fit(
            "[bold blue]Create New Agent[/bold blue]",
            border_style="blue",
        )
    )
    console.print()

    def validate_slug(text: str) -> bool | str:
        """Validate a slug (lowercase alphanumeric with hyphens)"""
        if not (len(text) >= 1 and text.replace("-", "").isalnum() and text.islower()):
            return "Invalid format. Use only lowercase letters, numbers, and hyphens (e.g., 'acme-corp')"
        return True

    # Question 1: Namespace slug (required)
    namespace_slug = questionary.text(
        "Namespace slug (e.g., 'acme-corp'):",
        validate=validate_slug,
    ).ask()
    if not namespace_slug:
        return

    # Question 2: Agent name (required)
    agent_short_name = questionary.text(
        "Agent name (e.g., 'my-agent'):",
        validate=validate_slug,
    ).ask()
    if not agent_short_name:
        return

    # Combine into full agent name
    agent_name = f"{namespace_slug}/{agent_short_name}"

    # Question 3: Description (optional with default)
    description = questionary.text("Description (optional):", default="An Sb0 agent").ask()
    if description is None:
        return

    # Use sensible defaults
    project_path = "."
    # Use the agent short name for directory
    agent_directory_name = agent_short_name
    use_uv = True
    template_type = TemplateType.DEFAULT

    answers = {
        "template_type": template_type,
        "project_path": project_path,
        "agent_name": agent_name,
        "namespace_slug": namespace_slug,
        "agent_short_name": agent_short_name,
        "agent_directory_name": agent_directory_name,
        "description": description,
        "use_uv": use_uv,
    }

    # Derive all names from agent_directory_name and path
    project_path = Path(answers["project_path"]).resolve()
    manifest_root = Path("../../")

    # Get project context
    context = get_project_context(answers, project_path, manifest_root)
    context["template_type"] = answers["template_type"].value
    context["use_uv"] = answers["use_uv"]

    # Create project structure
    create_project_structure(project_path, context, answers["template_type"], answers["use_uv"])

    # Show success message with quick start
    console.print()
    console.print(f"[bold green]Created {context['project_name']}/[/bold green]")
    console.print()

    # Simple next steps
    console.print("[bold]Get started:[/bold]")
    console.print(f"  [cyan]cd {context['project_name']}[/cyan]")
    console.print("  [cyan]uv venv && uv sync && source .venv/bin/activate[/cyan]")
    console.print("  [cyan]sb0 agents run --manifest manifest.yaml[/cyan]")
    console.print()

    console.print(f"[dim]Edit [yellow]project/acp.py[/yellow] to customize your agent.[/dim]")
    console.print("[dim]Docs: https://sb0.example.com/docs[/dim]")
    console.print()
