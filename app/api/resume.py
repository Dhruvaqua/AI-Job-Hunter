from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.config import (
    MAX_UPLOAD_SIZE,
)
from app.database.session import get_db
from app.security import (
    safe_filename,
    validate_pdf_signature,
)
from app.services.candidate_service import CandidateService
from app.services.resume_service import ResumeService
from app.security import (
    require_api_key,
    safe_filename,
    validate_pdf_signature,
)


router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
    dependencies=[Depends(require_api_key)],
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(
    exist_ok=True,
)


@router.post("/upload")
async def upload_resume(
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
):
    """
    Securely upload and process a PDF resume.

    Security controls:
    - PDF extension validation
    - PDF MIME validation
    - PDF magic-byte validation
    - upload size limit
    - random server-generated filename
    - no path traversal through user filename
    - cleanup after processing
    """

    original_filename = file.filename or ""

    extension = Path(
        original_filename
    ).suffix.lower()

    if extension != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed",
        )

    allowed_content_types = {
        "application/pdf",
        "application/octet-stream",
    }

    if file.content_type not in allowed_content_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid PDF content type",
        )

    filename = safe_filename()
    file_path = UPLOAD_DIR / filename

    total_size = 0
    first_chunk = True

    try:
        with open(file_path, "wb") as output_file:

            while True:
                chunk = await file.read(64 * 1024)

                if not chunk:
                    break

                if first_chunk:
                    first_chunk = False

                    if not validate_pdf_signature(chunk):
                        raise HTTPException(
                            status_code=400,
                            detail="Invalid PDF file",
                        )

                total_size += len(chunk)

                if total_size > MAX_UPLOAD_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail=(
                            "Resume file is too large. "
                            f"Maximum size is "
                            f"{MAX_UPLOAD_SIZE // (1024 * 1024)} MB."
                        ),
                    )

                output_file.write(chunk)

        if total_size == 0:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty",
            )

        text = ResumeService.extract_text(
            str(file_path)
        )

        resume = ResumeService.parse_resume(
            text
        )

        candidate = CandidateService.create_or_update_from_resume(
            db,
            resume,
        )

        return {
            "candidate_id": candidate.id,
            "candidate": resume,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to process the uploaded resume",
        )

    finally:
        try:
            if file_path.exists():
                file_path.unlink()
        except OSError:
            pass

        await file.close()