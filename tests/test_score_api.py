from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_score_nonexistent_job():
    response = client.post(
        "/score/",
        json={
            "job_id": 999999999,
            "candidate": {
                "name": "Test Candidate",
                "location": "Hyderabad",
                "experience": 1,
                "skills": ["Python", "FastAPI", "SQL"],
            },
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"


def test_score_requires_valid_request():
    response = client.post(
        "/score/",
        json={},
    )

    assert response.status_code == 422