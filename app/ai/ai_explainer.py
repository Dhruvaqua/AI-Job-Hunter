from app.ai.ollama_client import OllamaClient


class AIExplainer:

    @staticmethod
    def explain(candidate: dict, job: dict, score_result: dict):

        prompt = f"""
You are an expert career coach.

Candidate Skills:
{candidate["skills"]}

Candidate Location:
{candidate["location"]}

Job Title:
{job["title"]}

Company:
{job["company"]}

Job Location:
{job["location"]}

Required Skills:
{job.get("required_skills","")}

Deterministic Score:
{score_result["score"]}

Recommendation:
{score_result["recommendation"]}

Matched Skills:
{score_result["strengths"]}

Missing Skills:
{score_result["missing_skills"]}

Write your response using this format.

### Summary

### Why this score?

### Missing Skills

### Should the candidate apply?

### Learning Roadmap

Keep the answer under 250 words.
"""

        return OllamaClient.generate(prompt)