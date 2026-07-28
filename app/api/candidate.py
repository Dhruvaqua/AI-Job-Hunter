from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.candidate import CandidateCreate, CandidateResponse
from app.services.candidate_service import CandidateService

router = APIRouter(
    prefix="/candidate",
    tags=["Candidate"],
)


@router.get("/", response_model=list[CandidateResponse])
def get_candidates(
    db: Session = Depends(get_db),
):
    return CandidateService.get_all_candidates(db)


@router.post("/", response_model=CandidateResponse)
def create_candidate(
    candidate: CandidateCreate,
    db: Session = Depends(get_db),
):
    return CandidateService.create_candidate(
        db,
        candidate,
    )


@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(
    candidate_id: int,
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

    return candidate


@router.get("/{candidate_id}/recommendations")
def get_recommendations(
    candidate_id: int,
    db: Session = Depends(get_db),
):
    return CandidateService.get_recommended_jobs(
        db,
        candidate_id,
    )