import requests


class OllamaClient:
    BASE_URL = "http://localhost:11434/api/generate"
    MODEL = "llama3.2"

    @staticmethod
    def generate(prompt: str) -> str:
        response = requests.post(
            OllamaClient.BASE_URL,
            json={
                "model": OllamaClient.MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        return response.json()["response"]