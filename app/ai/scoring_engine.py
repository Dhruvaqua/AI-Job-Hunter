from typing import Dict
import re

from app.models import job

def extract_experience(text: str) -> int:
    match = re.search(r"(\d+)\+?\s*(?:years|year|yrs|yr)", text.lower())
    if match:
        return int(match.group(1))
    return 0

TECH_STACK = {
    "python",
    "java",
    "c++",
    "javascript",
    "typescript",
    "react",
    "angular",
    "vue",
    "node",
    "express",
    "fastapi",
    "django",
    "flask",
    "spring",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "redis",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "git",
    "github",
    "linux",
    "graphql",
    "rest",
}


class ScoringEngine:
    SKILL_WEIGHT = 40
    TECH_WEIGHT = 25
    EXPERIENCE_WEIGHT = 15
    LOCATION_WEIGHT = 10
    SALARY_WEIGHT = 10

    @staticmethod
    def score(candidate: Dict, job: Dict) -> Dict:
        candidate_skills = {
            s.lower().strip()
            for s in candidate.get("skills", [])
        }

        job_text = (
            f"{job.get('title', '')} "
            f"{job.get('description', '')}"
        ).lower()

        job_skills = {
            tech
            for tech in TECH_STACK
            if tech in job_text
        }

        matched = sorted(candidate_skills & job_skills)
        missing = sorted(job_skills - candidate_skills)

        if job_skills:
            ratio = len(matched) / len(job_skills)
        else:
            ratio = 0

        skill_score = round(ratio * ScoringEngine.SKILL_WEIGHT)
        tech_score = round(ratio * ScoringEngine.TECH_WEIGHT)

        location_score = 0

        candidate_location = candidate.get("location", "").lower()
        job_location = job.get("location", "").lower()
        
        candidate_exp = candidate.get("experience", 0)
        job_exp = extract_experience(job.get("description", ""))

        experience_score = 0

        if job_exp == 0:
            experience_score = ScoringEngine.EXPERIENCE_WEIGHT
        elif candidate_exp >= job_exp:
            experience_score = ScoringEngine.EXPERIENCE_WEIGHT
        else:
            experience_score = round(
                (candidate_exp / job_exp)
                * ScoringEngine.EXPERIENCE_WEIGHT
         )

        if (
            candidate_location == "remote"
            and "remote" in job_location
        ) or (
            candidate_location
            and candidate_location == job_location
        ):
            location_score = ScoringEngine.LOCATION_WEIGHT

        total = (
            skill_score
            + tech_score
            + experience_score
            + location_score
        )

        if total >= 80:
            recommendation = "Apply"
        elif total >= 60:
            recommendation = "Maybe"
        else:
            recommendation = "Skip"

        return {
            "score": total,
            "recommendation": recommendation,
            "breakdown": {
                "skills": skill_score,
                "technology": tech_score,
                "experience": experience_score,
                "location": location_score,
                "salary": 0,
            },
            "matched_skills": matched,
            "missing_skills": missing,
            "job_skills": sorted(job_skills),
        }