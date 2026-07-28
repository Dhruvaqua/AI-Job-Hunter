import re


class ScoringEngine:

    @staticmethod
    def score(candidate: dict, job: dict):

        score = 0
        strengths = []
        missing = []
        improvements = []

        candidate_skills = {
            s.lower().strip()
            for s in candidate.get("skills", [])
            if s.strip()
        }

        job_skills = {
            s.lower().strip()
            for s in job.get("required_skills", [])
            if s.strip()
        }

        matched = candidate_skills & job_skills
        missing = sorted(job_skills - candidate_skills)

        if job_skills:
            skill_score = int((len(matched) / len(job_skills)) * 70)
        else:
            skill_score = 0

        score += skill_score

        if matched:
            strengths.append(
                f"Matched {len(matched)} required skills."
            )

        candidate_location = (
            candidate.get("location", "").lower()
        )

        job_location = (
            job.get("location", "").lower()
        )

        if (
            "remote" in job_location
            or candidate_location in job_location
        ):
            score += 20
            strengths.append("Location matches.")
        else:
            improvements.append(
                "Location preference does not match."
            )

        title = (
            job.get("title", "").lower()
        )

        if "software" in title or "engineer" in title:
            score += 10

        score = min(score, 100)

        if score >= 80:
            recommendation = "Apply"

        elif score >= 60:
            recommendation = "Maybe"

        else:
            recommendation = "Skip"

        return {
            "score": score,
            "recommendation": recommendation,
            "strengths": strengths,
            "missing_skills": missing,
            "improvements": improvements,
        }