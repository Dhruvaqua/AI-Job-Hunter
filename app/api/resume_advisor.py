from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.candidate import Candidate
from app.models.job import Job
from app.ai.scoring_engine import ScoringEngine
from app.schemas.ats import ATSRequest

router = APIRouter(prefix="/advisor", tags=["Resume Advisor"])


@router.post("/improve")
def improve_resume(request: ATSRequest, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(
        Candidate.id == request.candidate_id
    ).first()

    if not candidate:
        raise HTTPException(404, "Candidate not found")

    job = db.query(Job).filter(
        Job.id == request.job_id
    ).first()

    if not job:
        raise HTTPException(404, "Job not found")

    result = ScoringEngine.score(
        candidate={
            "skills": candidate.skills.split(","),
            "location": candidate.location,
            "experience": candidate.experience,
        },
        job={
            "title": job.title,
            "description": job.description or "",
            "location": job.location or "",
            "required_skills": (job.required_skills or "").split(","),
        },
    )

    suggestions = list(result["improvements"])

    return {
        "ats_score": result["score"],
        "recommendation": result["recommendation"],
        "strengths": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "improvements": suggestions,
    }