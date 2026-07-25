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
                url = f"{cls.BASE_URL}/{company}/jobs"

                response = requests.get(url, timeout=10)

                if response.status_code != 200:
                    continue

                data = response.json()

                for job in data.get("jobs", []):

                    jobs.append(
                        {
                            "title": job["title"],
                            "company": company.capitalize(),
                            "location": job["location"]["name"],
                            "salary": None,
                            "url": job["absolute_url"],
                            "description": None,
                        }
                    )

            except Exception:
                logger.exception(f"Failed to fetch jobs for {company}")

        return jobs