from app.ai.prompt_builder import PromptBuilder
from app.ai.ollama_client import OllamaClient


class RoadmapAI:

    @staticmethod
    def generate(candidate, job):

        prompt = PromptBuilder.learning_roadmap(
            candidate,
            job,
        )

        return OllamaClient.generate(prompt)