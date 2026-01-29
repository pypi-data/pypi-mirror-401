import typer
from typing import Optional
from pathlib import Path


from aikit_cli.new import (
    decide_new_project,
    InteractiveResolutionRequired,
    InvalidProjectType,
    InvalidProvider,
    IncompatibleCombination,
)
from aikit_cli.prompts import prompt_project_type, prompt_provider, prompt_create_venv
from aikit_cli.utils import create_project, get_template_path, create_virtual_environment

app = typer.Typer(help="aikit – scaffold minimal AI projects")


@app.callback()
def callback():
    """
    aikit – scaffold minimal AI projects
    """

@app.command("new")
def new(
    project_name: str = typer.Argument(..., help="Name of the project directory"),
    project_type: Optional[str] = typer.Option(
        None,
        "--type",
        "-t",
        help="Project type: chatbot or rag",
    ),
    provider: Optional[str] = typer.Option(
        None,
        "--provider",
        "-p",
        help="AI provider: openai or ollama",
    ),
    create_venv: bool = typer.Option(
        False,
        "--create-venv",
        help="Create a .venv virtual environment",
    ),
    non_interactive: bool = typer.Option(
        False,
        "--non-interactive",
        help="Fail instead of prompting for missing options",
    ),
):
    """
    Create a new AI project.
    """

    # --- First decision attempt ---
    try:
        decision = decide_new_project(
            project_name=project_name,
            project_type=project_type,
            provider=provider,
            create_venv=create_venv,
            non_interactive=non_interactive,
        )

    except InteractiveResolutionRequired:
        # Prompt only for missing values
        if project_type is None:
            project_type = prompt_project_type()
            if project_type is None:
                typer.echo("✘ Operation cancelled.")
                raise typer.Exit(code=130)

        if provider is None:
            provider = prompt_provider()
            if provider is None:
                typer.echo("✘ Operation cancelled.")
                raise typer.Exit(code=130)

        # Ask for venv if not explicitly set (default is False, so we only ask if
        # we are already in interactive mode)
        # However, typer defaults create_venv to False. We can check if it was provided?
        # A simpler approach: if we are prompting, we might as well ask.
        if not create_venv:
             create_venv = prompt_create_venv()
             if create_venv is None:
                 typer.echo("✘ Operation cancelled.")
                 raise typer.Exit(code=130)


        # Second attempt (must succeed or hard-fail)
        decision = decide_new_project(
            project_name=project_name,
            project_type=project_type,
            create_venv=create_venv,
            provider=provider,
            non_interactive=True,
        )

    except (InvalidProjectType, InvalidProvider, IncompatibleCombination) as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    # --- Show warnings ---
    for warning in decision.warnings:
        typer.secho(f"⚠ {warning}", fg=typer.colors.YELLOW)

    # --- Create project ---
    typer.echo(f"✔ Creating project '{decision.project_name}'")

    create_project(
        project_name=decision.project_name,
        template_path=get_template_path(decision.project_type.value, decision.provider.value),
        variables={
            "project_name": decision.project_name,
        },
    )

    if decision.create_venv:
        typer.echo("✔ Creating virtual environment (.venv)...")
        create_virtual_environment(Path(decision.project_name))

    typer.echo("✔ Project created successfully\n")

    typer.echo("Next steps:")
    typer.echo(f"  cd {decision.project_name}")
    if decision.create_venv:
        typer.echo("  .venv/Scripts/activate  # on Windows")
        typer.echo("  source .venv/bin/activate # on Unix")
    typer.echo("  python app/main.py")


if __name__ == "__main__":
    app()
