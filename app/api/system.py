from fastapi import APIRouter
import requests

router = APIRouter(
    prefix="/system",
    tags=["System"],
)


@router.get("/health")
def health():

    ollama = False

    try:
        requests.get(
            "http://localhost:11434/api/tags",
            timeout=2,
        )
        ollama = True

    except Exception:
        ollama = False

    return {
        "api": "running",
        "ollama": ollama,
    }