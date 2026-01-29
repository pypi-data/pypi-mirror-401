import ollama
from config import get_model


class OllamaProvider:
    def __init__(self):
        self.model = get_model()

    def chat(self, messages: list[dict]) -> str:
        response = ollama.chat(
            model=self.model,
            messages=messages,
        )
        return response["message"]["content"]
