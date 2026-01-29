import ollama
from config import get_embedding_model


def embed(texts: list[str]) -> list[list[float]]:
    embeddings = []

    for text in texts:
        response = ollama.embeddings(
            model=get_embedding_model(),
            prompt=text,
        )
        embeddings.append(response["embedding"])

    return embeddings
