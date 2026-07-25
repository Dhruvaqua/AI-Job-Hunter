from typing import Optional

from sqlalchemy.orm import Session

from app.models.job import Job
from app.schemas.job import JobCreate


class JobService:
    @staticmethod
    def create_job(db: Session, job: JobCreate) -> tuple[Job, bool]:
        """
        Creates a new job if it doesn't already exist.

        Returns:
            (job, created)
        """

        existing = db.query(Job).filter(Job.url == str(job.url)).first()

        if existing:
            return existing, False

        db_job = Job(
            title=job.title,
            company=job.company,
            location=job.location,
            salary=job.salary,
            url=str(job.url),
            description=job.description,
        )

        db.add(db_job)
        db.commit()
        db.refresh(db_job)

        return db_job, True

    @staticmethod
    def get_jobs(
        db: Session,
        company: Optional[str] = None,
        location: Optional[str] = None,
        keyword: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
        sort: str = "latest",
    ):
        """
        Get jobs with optional filters, pagination and sorting.
        """

        query = db.query(Job)

        # Filter by company
        if company:
            query = query.filter(Job.company.ilike(f"%{company}%"))

        # Filter by location
        if location:
            query = query.filter(Job.location.ilike(f"%{location}%"))

        # Search by title
        if keyword:
            query = query.filter(Job.title.ilike(f"%{keyword}%"))

        # Sorting
        if sort == "oldest":
            query = query.order_by(Job.id.asc())
        else:
            query = query.order_by(Job.id.desc())

        # Pagination
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

        return query.all()