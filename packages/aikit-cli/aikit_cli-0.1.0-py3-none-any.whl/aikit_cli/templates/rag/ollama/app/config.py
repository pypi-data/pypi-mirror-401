import os
from dotenv import load_dotenv

load_dotenv()


def get_chat_model() -> str:
    return os.getenv("OLLAMA_CHAT_MODEL", "llama3")


def get_embedding_model() -> str:
    return os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
