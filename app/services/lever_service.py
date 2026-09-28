import requests
from app.utils.logger import logger

LEVER_COMPANIES = [
    "postman",
    "canva",
    "miro",
    "sourcegraph",
]

class LeverService:
    BASE_URL = "https://api.lever.co/v0/postings"

    @classmethod
    def fetch_jobs(cls):
        jobs = []
        for company in LEVER_COMPANIES:
            try:
                response = requests.get(
                    f"{cls.BASE_URL}/{company}",
                    params={"mode": "json"},
                    timeout=20,
                )
                response.raise_for_status()
                for item in response.json():
                    categories = item.get("categories") or {}
                    jobs.append({
                        "title": item.get("text") or "",
                        "company": company.capitalize(),
                        "location": categories.get("location") or "Remote",
                        "salary": None,
                        "url": item.get("hostedUrl"),
                        "description": item.get("descriptionPlain") or item.get("description") or "",
                    })
            except Exception:
                logger.exception("Failed to fetch Lever jobs for %s", company)
        return jobs
