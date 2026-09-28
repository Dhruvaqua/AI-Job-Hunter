from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.job import Job
from app.schemas.candidate import CandidateCreate
from app.ai.scoring_engine import ScoringEngine


class CandidateService:
    @staticmethod
    def create_or_update_from_resume(db: Session, resume_data: dict):
        # Email is a much safer stable identifier than the first line of a PDF.
        candidate = None
        if resume_data.get("email"):
            candidate = db.query(Candidate).filter(
                Candidate.name == resume_data["name"]
            ).first()

        skills = ",".join(resume_data.get("skills", []))
        location = resume_data.get("location") or "India"

        if candidate:
            candidate.location = location
            candidate.experience = resume_data.get("experience", 0)
            candidate.skills = skills
            db.commit()
            db.refresh(candidate)
            return candidate

        candidate = Candidate(
            name=resume_data["name"],
            location=location,
            experience=int(round(resume_data.get("experience", 0))),
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
        return db.query(Candidate).filter(Candidate.id == candidate_id).first()

    @staticmethod
    def get_recommended_jobs(db: Session, candidate_id: int):
        candidate = CandidateService.get_candidate(db, candidate_id)
        if not candidate:
            return None

        candidate_data = {
            "skills": candidate.skills.split(","),
            "location": candidate.location,
            "experience": candidate.experience,
        }

        recommendations = []
        for job in db.query(Job).all():
            result = ScoringEngine.score(
                candidate=candidate_data,
                job={
                    "title": job.title,
                    "description": job.description or "",
                    "location": job.location or "",
                    "required_skills": (job.required_skills or "").split(","),
                },
            )
            recommendations.append({
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "url": job.url,
                "score": result["score"],
                "recommendation": result["recommendation"],
                "strengths": result["strengths"],
                "missing_skills": result["missing_skills"],
                "improvements": result["improvements"],
                "breakdown": result["breakdown"],
            })

        return sorted(recommendations, key=lambda x: x["score"], reverse=True)
