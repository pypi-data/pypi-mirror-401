from pathlib import Path
from typing import Dict
import shutil


# ------------------------
# Paths
# ------------------------

def get_templates_root() -> Path:
    return Path(__file__).parent / "templates"


def get_template_path(project_type: str, provider: str) -> Path:
    return get_templates_root() / project_type / provider


# ------------------------
# Project creation
# ------------------------

def create_project(
    project_name: str,
    template_path: Path,
    variables: Dict[str, str],
):
    destination = Path(project_name)

    _validate_destination(destination)
    _copy_template(template_path, destination)
    _apply_variables(destination, variables)


def create_virtual_environment(project_path: Path):
    """
    Create a standard Python virtual environment in the project directory.
    """
    import venv
    venv_dir = project_path / ".venv"
    # prompt="aikit-env" is optional, but nice
    venv.create(venv_dir, with_pip=True, prompt=project_path.name)


# ------------------------
# Internal helpers
# ------------------------

def _validate_destination(destination: Path):
    if destination.exists():
        raise FileExistsError(
            f"Destination '{destination}' already exists."
        )


def _copy_template(template_path: Path, destination: Path):
    if not template_path.exists():
        raise FileNotFoundError(
            f"Template not found: {template_path}"
        )

    shutil.copytree(template_path, destination)


def _apply_variables(destination: Path, variables: Dict[str, str]):
    """
    Apply variable substitution to:
    - directory names
    - file names
    - file contents (text files only)
    """

    # 1. Rename paths bottom-up (files first, then dirs)
    all_paths = sorted(
        destination.rglob("*"),
        key=lambda p: len(p.parts),
        reverse=True,
    )

    for path in all_paths:
        _rename_path(path, variables)

    # 2. Replace contents in files
    for file_path in destination.rglob("*"):
        if file_path.is_file():
            _replace_file_contents(file_path, variables)


def _rename_path(path: Path, variables: Dict[str, str]):
    new_name = path.name

    for key, value in variables.items():
        new_name = new_name.replace(f"{{{{ {key} }}}}", value)

    if new_name != path.name:
        path.rename(path.with_name(new_name))


def _replace_file_contents(file_path: Path, variables: Dict[str, str]):
    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Binary or non-UTF8 file — skip silently
        return

    original = content

    for key, value in variables.items():
        content = content.replace(f"{{{{ {key} }}}}", value)

    if content != original:
        file_path.write_text(content, encoding="utf-8")
