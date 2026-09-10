from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_jobs():
    response = client.get("/jobs/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_jobs_with_pagination():
    response = client.get("/jobs/?page=1&limit=10")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_invalid_page():
    response = client.get("/jobs/?page=0")

    assert response.status_code == 422


def test_invalid_limit():
    response = client.get("/jobs/?limit=101")

    assert response.status_code == 422


def test_invalid_sort():
    response = client.get("/jobs/?sort=invalid")

    assert response.status_code == 422


def test_job_filtering():
    response = client.get("/jobs/?keyword=python")

    assert response.status_code == 200
    assert isinstance(response.json(), list)