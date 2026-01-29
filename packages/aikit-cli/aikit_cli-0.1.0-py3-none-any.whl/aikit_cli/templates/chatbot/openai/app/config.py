import os
from dotenv import load_dotenv

load_dotenv()


def get_openai_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    return key


def get_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
