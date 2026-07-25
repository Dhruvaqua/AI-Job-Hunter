from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.job import JobCreate, JobResponse
from app.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/", response_model=list[JobResponse])
def get_jobs(
    company: Optional[str] = Query(default=None),
    location: Optional[str] = Query(default=None),
    keyword: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    sort: str = Query(default="latest"),
    db: Session = Depends(get_db),
):
    return JobService.get_jobs(
        db=db,
        company=company,
        location=location,
        keyword=keyword,
        page=page,
        limit=limit,
        sort=sort,
    )


@router.post("/", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    created_job, _ = JobService.create_job(db, job)
    return created_job