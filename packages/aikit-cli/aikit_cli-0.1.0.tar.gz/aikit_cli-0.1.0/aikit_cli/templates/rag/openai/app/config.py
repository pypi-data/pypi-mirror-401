import os
from dotenv import load_dotenv

load_dotenv()


def get_api_key() -> str:
    return os.environ["OPENAI_API_KEY"]


def get_chat_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def get_embedding_model() -> str:
    return os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
