import requests

BASE_URL = "http://127.0.0.1:8000"


def get_jobs():
    return requests.get(f"{BASE_URL}/jobs").json()


def search_jobs():
    return requests.post(f"{BASE_URL}/search/all").json()


def upload_resume(file):
    files = {"file": file}
    return requests.post(
        f"{BASE_URL}/resume/upload",
        files=files,
    ).json()


def get_candidates():
    return requests.get(
        f"{BASE_URL}/candidate/"
    ).json()


def get_recommendations(candidate_id):
    return requests.get(
        f"{BASE_URL}/candidate/{candidate_id}/recommendations"
    ).json()


def ai_explain(candidate_id, job_id):
    return requests.get(
        f"{BASE_URL}/ai/candidate/{candidate_id}/job/{job_id}"
    ).json()