import os

import requests
import streamlit as st


API_BASE_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

API_KEY = os.getenv("API_KEY", "")


def _headers():
    headers = {}

    if API_KEY:
        headers["X-API-Key"] = API_KEY

    return headers


def _get(path, **kwargs):
    response = requests.get(
        f"{API_BASE_URL}{path}",
        headers=_headers(),
        timeout=30,
        **kwargs,
    )
    response.raise_for_status()
    return response.json()


def _post(path, **kwargs):
    response = requests.post(
        f"{API_BASE_URL}{path}",
        headers=_headers(),
        timeout=120,
        **kwargs,
    )
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------
# JOBS
# ---------------------------------------------------------

def get_jobs():
    return _get("/jobs/")


def search_jobs(
    keyword=None,
    company=None,
    location=None,
):
    params = {}

    if keyword:
        params["keyword"] = keyword

    if company:
        params["company"] = company

    if location:
        params["location"] = location

    return _get(
        "/jobs/",
        params=params,
    )


# ---------------------------------------------------------
# CANDIDATES
# ---------------------------------------------------------

def get_candidates():
    return _get("/candidate/")


def get_candidate(candidate_id):
    return _get(
        f"/candidate/{candidate_id}"
    )


def get_recommendations(candidate_id):
    return _get(
        f"/candidate/{candidate_id}/recommendations"
    )


# ---------------------------------------------------------
# RESUME
# ---------------------------------------------------------

def upload_resume(file):
    files = {
        "file": (
            file.name,
            file.getvalue(),
            file.type or "application/pdf",
        )
    }

    response = requests.post(
        f"{API_BASE_URL}/resume/upload",
        files=files,
        headers=_headers(),
        timeout=120,
    )

    response.raise_for_status()

    return response.json()


# ---------------------------------------------------------
# AI JOB ANALYSIS
# ---------------------------------------------------------

def ai_explain(candidate_id, job_id):
    return _get(
        f"/ai/candidate/{candidate_id}/job/{job_id}"
    )


# ---------------------------------------------------------
# AI RESUME TAILORING
# ---------------------------------------------------------

def resume_tailor(candidate_id, job_id):
    return _post(
        "/ai/resume-tailor",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
        },
    )


# ---------------------------------------------------------
# AI INTERVIEW QUESTIONS
# ---------------------------------------------------------

def interview_questions(candidate_id, job_id):
    return _post(
        "/ai/interview",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
        },
    )


# ---------------------------------------------------------
# AI LEARNING ROADMAP
# ---------------------------------------------------------

def learning_roadmap(candidate_id, job_id):
    return _post(
        "/ai/roadmap",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
        },
    )


# ---------------------------------------------------------
# ATS
# ---------------------------------------------------------

def ats_score(candidate_id, job_id):
    return _post(
        "/ats/score",
        json={
            "candidate_id": candidate_id,
            "job_id": job_id,
        },
    )


# ---------------------------------------------------------
# RESUME ADVISOR
# ---------------------------------------------------------

def improve_resume(candidate_id):
    return _post(
        "/advisor/improve",
        json={
            "candidate_id": candidate_id,
        },
    )

