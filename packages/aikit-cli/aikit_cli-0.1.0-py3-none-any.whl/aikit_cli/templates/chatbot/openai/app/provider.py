from openai import OpenAI
from config import get_openai_api_key, get_model


class OpenAIProvider:
    def __init__(self):
        self.client = OpenAI(api_key=get_openai_api_key())
        self.model = get_model()

    def chat(self, messages: list[dict]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return response.choices[0].message.content
