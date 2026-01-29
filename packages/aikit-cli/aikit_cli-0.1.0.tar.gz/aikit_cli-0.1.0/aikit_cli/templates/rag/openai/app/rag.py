from openai import OpenAI
from config import get_api_key, get_chat_model
from store import VectorStore

client = OpenAI(api_key=get_api_key())

# naive implementation of RAG
def answer(question: str, store: VectorStore) -> str:
    contexts = store.search(question)

    prompt = (
        "Answer the question using the context below.\n\n"
        "Context:\n"
        + "\n\n".join(contexts)
        + "\n\nQuestion:\n"
        + question
    )

    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content
