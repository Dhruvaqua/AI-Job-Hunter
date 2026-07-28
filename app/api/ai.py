from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.job import Job
from app.services.candidate_service import CandidateService
from app.ai.ai_explainer import AIExplainer

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.get("/candidate/{candidate_id}/job/{job_id}")
def explain_job(
    candidate_id: int,
    job_id: int,
    db: Session = Depends(get_db),
):
    candidate = CandidateService.get_candidate(
        db,
        candidate_id,
    )

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
        "skills": candidate.skills.split(","),
        "location": candidate.location,
    }

    score = CandidateService.get_job_score(
        candidate_data,
        job,
    )

    explanation = AIExplainer.explain(
        candidate=candidate_data,
        job={
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "required_skills": job.required_skills or "",
        },
        score_result=score,
    )

    return {
        "job": {
            "id": job.id,
            "title": job.title,
            "company": job.company,
        },
        "score": score,
        "ai_explanation": explanation,
    }