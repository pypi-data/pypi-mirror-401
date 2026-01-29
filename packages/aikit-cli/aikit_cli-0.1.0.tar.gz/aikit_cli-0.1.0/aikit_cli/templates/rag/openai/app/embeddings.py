from openai import OpenAI
from config import get_api_key, get_embedding_model

client = OpenAI(api_key=get_api_key())


def embed(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        model=get_embedding_model(),
        input=texts,
    )
    return [d.embedding for d in response.data]
