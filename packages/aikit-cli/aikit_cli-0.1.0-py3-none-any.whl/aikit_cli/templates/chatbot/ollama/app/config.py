import os
from dotenv import load_dotenv

load_dotenv()


def get_model() -> str:
    return os.getenv("OLLAMA_MODEL", "llama3")
