from sqlalchemy.orm import Session

from app.models.job import Job
from app.schemas.job import JobCreate


class JobService:

    @staticmethod
    def create_job(db: Session, job: JobCreate):

        existing = (
            db.query(Job)
            .filter(Job.url == str(job.url))
            .first()
        )

        if existing:
            return existing, False

        data = job.model_dump()

        data["url"] = str(data["url"])

        db_job = Job(**data)

        db.add(db_job)
        db.commit()
        db.refresh(db_job)

        return db_job, True

    @staticmethod
    def get_jobs(
        db: Session,
        company=None,
        location=None,
        keyword=None,
        page=1,
        limit=20,
        sort="latest",
    ):
        query = db.query(Job)

        if company:
            query = query.filter(Job.company.ilike(f"%{company}%"))

        if location:
            query = query.filter(Job.location.ilike(f"%{location}%"))

        if keyword:
            query = query.filter(
                Job.title.ilike(f"%{keyword}%")
            )

        if sort == "latest":
            query = query.order_by(Job.id.desc())

        elif sort == "oldest":
            query = query.order_by(Job.id.asc())

        return (
            query.offset((page - 1) * limit)
            .limit(limit)
            .all()
        )