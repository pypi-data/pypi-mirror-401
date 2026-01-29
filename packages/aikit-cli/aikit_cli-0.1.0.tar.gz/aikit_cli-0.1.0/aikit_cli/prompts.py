from aikit_cli.new import ProjectType, Provider
import questionary


PROJECT_TYPE_CHOICES = [t.value for t in ProjectType]
PROVIDER_CHOICES = [p.value for p in Provider]



def prompt_project_type() -> str:
    """
    Prompt the user to select a project type.
    """
    return questionary.select(
        "Project type",
        choices=PROJECT_TYPE_CHOICES,
        default="chatbot",
    ).ask()


def prompt_provider() -> str:
    """
    Prompt the user to select an AI provider.
    """
    return questionary.select(
        "AI provider",
        choices=PROVIDER_CHOICES,
        default="openai",
    ).ask()


def prompt_create_venv() -> bool:
    """
    Prompt the user to confirm virtual environment creation.
    """
    return questionary.confirm(
        "Create virtual environment?",
        default=False,
    ).ask()

