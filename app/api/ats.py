from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.candidate import Candidate
from app.models.job import Job
from app.schemas.ats import ATSRequest
from app.ai.scoring_engine import ScoringEngine

router = APIRouter(prefix="/ats", tags=["ATS"])


@router.post("/score")
def ats_score(request: ATSRequest, db: Session = Depends(get_db)):
    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == request.candidate_id)
        .first()
    )

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    job = (
        db.query(Job)
        .filter(Job.id == request.job_id)
        .first()
    )

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    candidate_data = {
        "skills": candidate.skills.split(","),
        "location": candidate.location,
        "experience": candidate.experience,
    }

    result = ScoringEngine.score(
        candidate=candidate_data,
        job={
            "title": job.title,
            "description": job.description or "",
            "location": job.location or "",
            "required_skills": (job.required_skills or "").split(","),
        },
    )

    return {
        "candidate": candidate.name,
        "job": job.title,
        "ats_score": result["score"],
        "recommendation": result["recommendation"],
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "strengths": result["strengths"],
        "weaknesses": result["improvements"],
        "breakdown": result["breakdown"],
    }