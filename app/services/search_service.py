from sqlalchemy.orm import Session

from app.schemas.job import JobCreate
from app.services.greenhouse_service import GreenhouseService
from app.services.job_service import JobService
from app.services.lever_service import LeverService
from app.services.web_scraper import WebScraper
from app.ai.skill_extractor import SkillExtractor


class SearchService:
    @staticmethod
    def import_jobs(db: Session, jobs: list[dict]) -> dict:

        jobs_saved = 0
        duplicates = 0

        for job in jobs:

            description = WebScraper.fetch_job_description(job["url"])

            job["description"] = description

            job["required_skills"] = ",".join(
                SkillExtractor.extract(description)
            )

            _, created = JobService.create_job(
             db,
                JobCreate(**job)
            )

            if created:
                jobs_saved += 1
            else:
                duplicates += 1

        return {
            "jobs_found": len(jobs),
            "jobs_saved": jobs_saved,
            "duplicates": duplicates,
        }

    @staticmethod
    def search_greenhouse(db: Session):
        jobs = GreenhouseService.fetch_jobs()
        return SearchService.import_jobs(db, jobs)

    @staticmethod
    def search_lever(db: Session):
        jobs = LeverService.fetch_jobs()
        return SearchService.import_jobs(db, jobs)

    @staticmethod
    def search_all(db: Session):
        jobs = []

        jobs.extend(GreenhouseService.fetch_jobs())
        jobs.extend(LeverService.fetch_jobs())

        return SearchService.import_jobs(db, jobs)