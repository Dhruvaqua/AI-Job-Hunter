from app.ai.prompt_builder import PromptBuilder
from app.ai.ollama_client import OllamaClient


class InterviewAI:

    @staticmethod
    def generate(candidate, job):

        prompt = PromptBuilder.interview_questions(
            candidate,
            job,
        )

        return OllamaClient.generate(prompt)