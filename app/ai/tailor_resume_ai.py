from app.ai.prompt_builder import PromptBuilder
from app.ai.ollama_client import OllamaClient


class ResumeTailorAI:

    @staticmethod
    def generate(candidate, job):

        prompt = PromptBuilder.resume_tailor(
            candidate,
            job,
        )

        return OllamaClient.generate(prompt)