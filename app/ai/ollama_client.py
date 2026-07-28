import requests


class OllamaClient:

    URL = "http://localhost:11434/api/generate"
    MODEL = "llama3.2"

    @classmethod
    def generate(cls, prompt: str):

        try:
            response = requests.post(
                cls.URL,
                json={
                    "model": cls.MODEL,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=120,
            )

            response.raise_for_status()

            return response.json()["response"]

        except requests.exceptions.RequestException:
            return (
                "⚠️ Ollama is not running. "
                "Start Ollama and pull the llama3.2 model to enable AI explanations."
            )