from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.job import Job
from app.schemas.ai import AIRequest
from app.services.candidate_service import CandidateService

from app.ai.ai_explainer import AIExplainer
from app.ai.tailor_resume_ai import ResumeTailorAI
from app.ai.interview_ai import InterviewAI
from app.ai.roadmap_ai import RoadmapAI

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


def get_candidate_and_job(db: Session, candidate_id: int, job_id: int):

    candidate = CandidateService.get_candidate(db, candidate_id)

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found",
        )

    job = (
        db.query(Job)
        .filter(Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    candidate_data = {
        "name": candidate.name,
        "skills": candidate.skills.split(","),
        "experience": candidate.experience,
        "location": candidate.location,
    }

    job_data = {
        "title": job.title,
        "company": job.company,
        "description": job.description or "",
        "required_skills": job.required_skills or "",
        "location": job.location,
    }

    return candidate_data, job_data, job


@router.get("/candidate/{candidate_id}/job/{job_id}")
def explain_job(
    candidate_id: int,
    job_id: int,
    db: Session = Depends(get_db),
):

    candidate_data, job_data, job = get_candidate_and_job(
        db,
        candidate_id,
        job_id,
    )

    score = CandidateService.get_job_score(
        candidate_data,
        job,
    )

    response = AIExplainer.explain(
        candidate_data,
        job_data,
        score,
    )

    return {
        "response": response
    }


@router.post("/resume-tailor")
def tailor_resume(
    request: AIRequest,
    db: Session = Depends(get_db),
):

    candidate, job, _ = get_candidate_and_job(
        db,
        request.candidate_id,
        request.job_id,
    )

    return {
        "response": ResumeTailorAI.generate(
            candidate,
            job,
        )
    }


@router.post("/interview")
def interview_questions(
    request: AIRequest,
    db: Session = Depends(get_db),
):

    candidate, job, _ = get_candidate_and_job(
        db,
        request.candidate_id,
        request.job_id,
    )

    return {
        "response": InterviewAI.generate(
            candidate,
            job,
        )
    }


@router.post("/roadmap")
def learning_roadmap(
    request: AIRequest,
    db: Session = Depends(get_db),
):

    candidate, job, _ = get_candidate_and_job(
        db,
        request.candidate_id,
        request.job_id,
    )

    return {
        "response": RoadmapAI.generate(
            candidate,
            job,
        )
    }