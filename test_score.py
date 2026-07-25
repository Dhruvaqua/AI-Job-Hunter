from app.ai.scoring_engine import ScoringEngine

candidate = {
    "skills": [
        "Python",
        "FastAPI",
        "Docker",
        "AWS",
    ],
    "location": "Remote",
}

job = {
    "title": "Python Backend Engineer",
    "description": "Looking for Python, FastAPI and Docker experience.",
    "location": "Remote",
}

print(ScoringEngine.score(candidate, job))