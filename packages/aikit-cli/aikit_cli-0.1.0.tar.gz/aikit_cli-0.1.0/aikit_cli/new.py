from dataclasses import dataclass
from typing import Optional
from pathlib import Path
from enum import Enum


# ------------------------
# Constants
# ------------------------

class ProjectType(str, Enum):
    CHATBOT = "chatbot"
    RAG = "rag"

class Provider(str, Enum):
    OPENAI = "openai"
    OLLAMA = "ollama"

DEFAULT_PROJECT_TYPE = ProjectType.CHATBOT
DEFAULT_PROVIDER = Provider.OPENAI


# ------------------------
# Exceptions
# ------------------------

class AikitError(Exception):
    """Base error for aikit decision logic."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InvalidProjectType(AikitError):
    """Raised when an unsupported project type is provided."""
    pass


class InvalidProvider(AikitError):
    """Raised when an unsupported provider is provided."""
    pass


class IncompatibleCombination(AikitError):
    """Raised when the project type and provider do not work together."""
    pass


class InteractiveResolutionRequired(AikitError):
    """Raised when CLI must prompt the user."""
    def __init__(self, message: str = "Interaction required"):
        super().__init__(message)


# ------------------------
# Decision result
# ------------------------

@dataclass
class DecisionResult:
    project_name: str
    project_type: ProjectType
    provider: Provider
    create_venv: bool
    template_path: Path
    warnings: list[str]


# ------------------------
# Decision engine
# ------------------------

def decide_new_project(
    *,
    project_name: str,
    project_type: Optional[str],
    provider: Optional[str],
    create_venv: bool,
    non_interactive: bool,
) -> DecisionResult:
    warnings: list[str] = []

    if create_venv is not None:
        pass

    # --- Validate explicit values ---
    if project_type is not None:
        try:
            pt = ProjectType(project_type)
        except ValueError:
            valid = ", ".join([t.value for t in ProjectType])
            raise InvalidProjectType(f"Invalid project type '{project_type}'. Valid options: {valid}")
    else:
        pt = None

    if provider is not None:
        try:
            pv = Provider(provider)
        except ValueError:
            valid = ", ".join([p.value for p in Provider])
            raise InvalidProvider(f"Invalid provider '{provider}'. Valid options: {valid}")
    else:
        pv = None

    # --- Resolve missing values ---
    if pt is None or pv is None:
        if non_interactive:
            raise InteractiveResolutionRequired(
                "Missing required options and non-interactive mode is enabled."
            )

        # CLI layer must prompt
        raise InteractiveResolutionRequired

    # --- Compatibility rules (explicit, future-proof) ---
    if (pt, pv) not in {
        (ProjectType.CHATBOT, Provider.OPENAI),
        (ProjectType.CHATBOT, Provider.OLLAMA),
        (ProjectType.RAG, Provider.OPENAI),
        (ProjectType.RAG, Provider.OLLAMA),
    }:
        raise IncompatibleCombination(
            f"{pt.value} + {pv.value} is not supported"
        )

    # --- Non-blocking warnings ---
    if pv == Provider.OPENAI:
        warnings.append("Requires OPENAI_API_KEY in .env")

    if pt == ProjectType.RAG and pv == Provider.OLLAMA:
        warnings.append("Ensure 'nomic-embed-text' model is pulled")

    # --- Template resolution ---
    template_path = f"{pt.value}/{pv.value}"

    return DecisionResult(
        project_name=project_name,
        project_type=pt,
        provider=pv,
        create_venv=create_venv,
        template_path=Path(template_path),
        warnings=warnings,
    )

