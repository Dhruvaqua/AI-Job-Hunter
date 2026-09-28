from sqlalchemy.orm import Session

from app.schemas.job import JobCreate
from app.services.greenhouse_service import GreenhouseService
from app.services.job_service import JobService
from app.services.lever_service import LeverService
from app.services.himalayas_service import HimalayasService
from app.services.web_scraper import WebScraper
from app.ai.skill_extractor import SkillExtractor


class SearchService:
    @staticmethod
    def import_jobs(db: Session, jobs: list[dict]) -> dict:
        saved = 0
        duplicates = 0

        for raw in jobs:
            if not raw.get("title") or not raw.get("url"):
                continue

            job = dict(raw)

            # Prefer source-provided description; scrape only when missing.
            if not job.get("description"):
                job["description"] = WebScraper.fetch_job_description(job["url"])

            job["required_skills"] = ",".join(
                SkillExtractor.extract(job.get("description") or "")
            )

            try:
                _, created = JobService.create_job(db, JobCreate(**job))
                if created:
                    saved += 1
                else:
                    duplicates += 1
            except Exception:
                db.rollback()

        return {
            "jobs_found": len(jobs),
            "jobs_saved": saved,
            "duplicates": duplicates,
        }

    @staticmethod
    def search_greenhouse(db: Session):
        return SearchService.import_jobs(db, GreenhouseService.fetch_jobs())

    @staticmethod
    def search_lever(db: Session):
        return SearchService.import_jobs(db, LeverService.fetch_jobs())

    @staticmethod
    def search_himalayas(db: Session, keyword=None, country=None):
        return SearchService.import_jobs(
            db, HimalayasService.fetch_jobs(keyword=keyword, country=country, limit=20)
        )

    @staticmethod
    def search_all(db: Session):
        jobs = GreenhouseService.fetch_jobs() + LeverService.fetch_jobs()
        try:
            jobs += HimalayasService.fetch_jobs(keyword="software engineer", country="India", limit=20)
            jobs += HimalayasService.fetch_jobs(keyword="data engineer", country="India", limit=20)
            jobs += HimalayasService.fetch_jobs(keyword="python", country="India", limit=20)
        except Exception:
            # Core ATS sources should still work if the optional public API is unavailable.
            pass
        return SearchService.import_jobs(db, jobs)
