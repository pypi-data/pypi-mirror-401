import ollama
from config import get_chat_model
from store import VectorStore


def answer(question: str, store: VectorStore) -> str:
    contexts = store.search(question)

    prompt = (
        "Answer the question using the context below.\n\n"
        "Context:\n"
        + "\n\n".join(contexts)
        + "\n\nQuestion:\n"
        + question
    )

    response = ollama.chat(
        model=get_chat_model(),
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return response["message"]["content"]
