import requests

BASE_URL = "http://127.0.0.1:8000"


def upload_resume(file):
    files = {
        "file": (
            file.name,
            file.getvalue(),
            "application/pdf",
        )
    }

    response = requests.post(
        f"{BASE_URL}/resume/upload",
        files=files,
    )

    response.raise_for_status()
    return response.json()


def import_jobs():
    response = requests.post(
        f"{BASE_URL}/search/all"
    )

    response.raise_for_status()
    return response.json()


def get_jobs(
    company=None,
    location=None,
    keyword=None,
    page=1,
    limit=100,
    sort="latest",
):
    params = {
        "company": company,
        "location": location,
        "keyword": keyword,
        "page": page,
        "limit": limit,
        "sort": sort,
    }

    response = requests.get(
        f"{BASE_URL}/jobs",
        params=params,
    )

    response.raise_for_status()
    return response.json()


def get_recommendations(candidate_id):
    response = requests.get(
        f"{BASE_URL}/candidates/{candidate_id}/recommendations"
    )
    return response.json()


def ats_score(candidate_id: int, job_id: int):
    response = requests.get(
        f"{BASE_URL}/candidate/{candidate_id}/ats/{job_id}"
    )

    response.raise_for_status()
    return response.json()


def ai_explain(candidate_id: int, job_id: int):
    response = requests.get(
        f"{BASE_URL}/candidate/{candidate_id}/explain/{job_id}"
    )

    response.raise_for_status()
    return response.json()

def get_candidates():
    response = requests.get(f"{BASE_URL}/candidates")
    return response.json()


def get_jobs():
    response = requests.get(f"{BASE_URL}/jobs?page=1&limit=100")
    return response.json()

