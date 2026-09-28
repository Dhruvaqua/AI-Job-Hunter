import requests
from app.utils.logger import logger

GREENHOUSE_BOARDS = [
    "stripe",
    "airbnb",
    "coinbase",
    "notion",
    "discord",
]

class GreenhouseService:
    BASE_URL = "https://boards-api.greenhouse.io/v1/boards"

    @classmethod
    def fetch_jobs(cls):
        jobs = []
        for company in GREENHOUSE_BOARDS:
            try:
                response = requests.get(
                    f"{cls.BASE_URL}/{company}/jobs",
                    params={"content": "true"},
                    timeout=20,
                )
                response.raise_for_status()
                for item in response.json().get("jobs", []):
                    jobs.append({
                        "title": item.get("title") or "",
                        "company": company.capitalize(),
                        "location": (item.get("location") or {}).get("name") or "Unspecified",
                        "salary": None,
                        "url": item.get("absolute_url"),
                        "description": item.get("content") or "",
                    })
            except Exception:
                logger.exception("Failed to fetch Greenhouse jobs for %s", company)
        return jobs
