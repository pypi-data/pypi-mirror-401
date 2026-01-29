from pathlib import Path
from store import VectorStore
from rag import answer


def load_documents() -> list[str]:
    docs = []
    for path in Path("data/documents").glob("*.txt"):
        docs.append(path.read_text())
    return docs


def run():
    store = VectorStore()
    documents = load_documents()

    if not documents:
        print("No documents found in data/documents/")
        return

    store.add(documents)
    print("Documents indexed.")

    while True:
        question = input("> ")
        print(answer(question, store))


if __name__ == "__main__":
    run()
