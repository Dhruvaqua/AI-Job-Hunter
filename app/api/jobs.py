from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.job import JobCreate, JobResponse
from app.services.job_service import JobService
from app.security import require_api_key

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
    dependencies=[Depends(require_api_key)],
)


@router.get("/")
def get_jobs(
    company: Optional[str] = None,
    location: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = Query(1, ge=1, le=1000),
    limit: int = Query(20, ge=1, le=100),
    sort: str = Query("latest", pattern="^(latest|oldest)$"),
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
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
):
    created_job, _ = JobService.create_job(db, job)
    return created_job