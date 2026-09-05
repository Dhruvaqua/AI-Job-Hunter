import requests

from app.config import (
    MAX_LLM_INPUT_LENGTH,
    MAX_LLM_OUTPUT_LENGTH,
    OLLAMA_MODEL,
    OLLAMA_TIMEOUT,
    OLLAMA_URL,
)


class OllamaClient:

    URL = f"{OLLAMA_URL.rstrip('/')}/api/generate"
    MODEL = OLLAMA_MODEL

    @classmethod
    def generate(cls, prompt: str) -> str:

        if not prompt or not prompt.strip():
            return "⚠️ AI request could not be generated."

        # Prevent unexpectedly large prompts.
        prompt = prompt[:MAX_LLM_INPUT_LENGTH]

        payload = {
            "model": cls.MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 2000,
            },
        }

        try:
            response = requests.post(
                cls.URL,
                json=payload,
                timeout=OLLAMA_TIMEOUT,
            )

            response.raise_for_status()

            data = response.json()

            result = data.get("response")

            if not isinstance(result, str):
                return (
                    "⚠️ Ollama returned an invalid response."
                )

            result = result.strip()

            if not result:
                return (
                    "⚠️ Ollama returned an empty response."
                )

            return result[:MAX_LLM_OUTPUT_LENGTH]

        except requests.exceptions.Timeout:
            return (
                "⚠️ AI request timed out. "
                "Please try again."
            )

        except requests.exceptions.ConnectionError:
            return (
                "⚠️ Ollama is not running. "
                "Start Ollama and make sure the configured "
                "model is available."
            )

        except requests.exceptions.RequestException:
            return (
                "⚠️ AI service is currently unavailable."
            )

        except ValueError:
            return (
                "⚠️ Ollama returned an invalid response."
            )