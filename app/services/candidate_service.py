from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.job import Job
from app.schemas.candidate import CandidateCreate
from app.ai.scoring_engine import ScoringEngine


class CandidateService:

    @staticmethod
    def create_or_update_from_resume(db: Session, resume_data: dict):
        candidate = (
            db.query(Candidate)
            .filter(Candidate.name == resume_data["name"])
            .first()
        )

        skills = ",".join(resume_data["skills"])

        if candidate:
            candidate.location = "Remote"
            candidate.experience = resume_data["experience"]
            candidate.skills = skills

            db.commit()
            db.refresh(candidate)

            return candidate

        candidate = Candidate(
            name=resume_data["name"],
            location="Remote",
            experience=resume_data["experience"],
            skills=skills,
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        return candidate
    
    @staticmethod
    def get_all_candidates(db: Session):
        return db.query(Candidate).all()

    @staticmethod
    def create_candidate(db: Session, candidate: CandidateCreate):
        db_candidate = Candidate(
            name=candidate.name,
            location=candidate.location,
            experience=candidate.experience,
            skills=",".join(candidate.skills),
        )

        db.add(db_candidate)
        db.commit()
        db.refresh(db_candidate)

        return db_candidate

    @staticmethod
    def get_candidate(db: Session, candidate_id: int):
        return (
            db.query(Candidate)
            .filter(Candidate.id == candidate_id)
            .first()
        )

    @staticmethod
    def get_job_score(candidate_data: dict, job: Job):
        return ScoringEngine.score(
            candidate=candidate_data,
            job={
                "title": job.title,
                "description": job.description or "",
                "location": job.location or "",
                "required_skills": (
                    job.required_skills.split(",")
                    if job.required_skills
                    else []
                ),
            },
        )

    @staticmethod
    def get_recommended_jobs(db: Session, candidate_id: int):
        candidate = CandidateService.get_candidate(db, candidate_id)

        if not candidate:
            return None

        candidate_data = {
            "skills": candidate.skills.split(","),
            "location": candidate.location,
        }

        jobs = db.query(Job).all()

        recommendations = []

        for job in jobs:
            result = CandidateService.get_job_score(
                candidate_data,
                job,
            )

            recommendations.append(
                {
                    "job_id": job.id,
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                    "score": result["score"],
                    "recommendation": result["recommendation"],
                    "strengths": result["strengths"],
                    "missing_skills": result["missing_skills"],
                    "improvements": result["improvements"],
                }
            )

        recommendations.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return recommendations