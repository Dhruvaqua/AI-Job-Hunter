from app.ai.ai_explainer import AIExplainer

candidate = {
    "skills": ["python", "fastapi", "sql"],
    "location": "Remote",
}

job = {
    "title": "Backend Engineer",
    "company": "Stripe",
    "location": "Remote",
    "required_skills": "python,docker,aws,fastapi",
}

score = {
    "score": 82,
    "recommendation": "Apply",
    "strengths": [
        "Python",
        "FastAPI",
    ],
    "missing_skills": [
        "Docker",
        "AWS",
    ],
}

print(AIExplainer.explain(candidate, job, score))