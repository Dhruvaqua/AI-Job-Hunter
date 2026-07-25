from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.search_service import SearchService

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.post("/greenhouse")
def search_greenhouse(db: Session = Depends(get_db)):
    return SearchService.search_greenhouse(db)


@router.post("/lever")
def search_lever(db: Session = Depends(get_db)):
    return SearchService.search_lever(db)


@router.post("/all")
def search_all(db: Session = Depends(get_db)):
    return SearchService.search_all(db)