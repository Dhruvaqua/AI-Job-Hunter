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
                url = f"{cls.BASE_URL}/{company}?mode=json"

                response = requests.get(url, timeout=10)

                if response.status_code != 200:
                    logger.warning(
                        f"Failed to fetch Lever jobs for {company}. "
                        f"Status Code: {response.status_code}"
                    )
                    continue

                data = response.json()

                for job in data:

                    jobs.append(
                        {
                            "title": job.get("text"),
                            "company": company.capitalize(),
                            "location": job.get("categories", {}).get("location"),
                            "salary": None,
                            "url": job.get("hostedUrl"),
                            "description": None,
                        }
                    )

            except Exception:
                logger.exception(f"Error fetching Lever jobs for {company}")

        return jobs