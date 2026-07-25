from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.job import Job
from app.schemas.score import ScoreRequest
from app.ai.scoring_engine import ScoringEngine

router = APIRouter(prefix="/score", tags=["Score"])


@router.post("/")
def score_job(request: ScoreRequest, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == request.job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return ScoringEngine.score(
        candidate=request.candidate.model_dump(),
        job={
            "title": job.title,
            "description": job.description or "",
            "location": job.location or "",
        },
    )
    
    