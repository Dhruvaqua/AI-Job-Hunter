from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.resume_service import ResumeService
from app.services.candidate_service import CandidateService

router = APIRouter(prefix="/resume", tags=["Resume"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_resume(
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = ResumeService.extract_text(str(file_path))
    resume = ResumeService.parse_resume(text)

    candidate = CandidateService.create_or_update_from_resume(
        db,
        resume,
    )

    return {
        "candidate_id": candidate.id,
        "candidate": resume,
    }
    