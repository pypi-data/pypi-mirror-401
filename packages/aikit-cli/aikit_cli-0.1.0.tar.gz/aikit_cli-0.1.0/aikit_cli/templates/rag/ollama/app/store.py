import numpy as np
from app.embeddings import embed


class VectorStore:
    def __init__(self):
        self.texts: list[str] = []
        self.vectors: np.ndarray | None = None

    def add(self, texts: list[str]):
        vectors = embed(texts)
        self.texts.extend(texts)

        matrix = np.array(vectors)
        if self.vectors is None:
            self.vectors = matrix
        else:
            self.vectors = np.vstack([self.vectors, matrix])

    def search(self, query: str, k: int = 3) -> list[str]:
        query_vec = np.array(embed([query])[0])

        scores = self.vectors @ query_vec
        top_k = scores.argsort()[-k:][::-1]

        return [self.texts[i] for i in top_k]
