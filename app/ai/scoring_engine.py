class ScoringEngine:

    @staticmethod
    def _normalize_skills(skills):
        """
        Convert skills from either a list or a comma-separated string
        into a clean set of lowercase skill names.
        """

        if not skills:
            return set()

        if isinstance(skills, str):
            skills = skills.split(",")

        return {
            str(skill).lower().strip()
            for skill in skills
            if str(skill).strip()
        }

    @staticmethod
    def score(candidate: dict, job: dict):

        candidate_skills = ScoringEngine._normalize_skills(
            candidate.get("skills", [])
        )

        job_skills = ScoringEngine._normalize_skills(
            job.get("required_skills", [])
        )

        matched_skills = sorted(candidate_skills & job_skills)
        missing_skills = sorted(job_skills - candidate_skills)

        if job_skills:
            skill_score = int(
                (len(matched_skills) / len(job_skills)) * 70
            )
        else:
            skill_score = 0

        candidate_location = (
            candidate.get("location", "") or ""
        ).lower().strip()

        job_location = (
            job.get("location", "") or ""
        ).lower().strip()

        if (
            "remote" in job_location
            or (
                candidate_location
                and candidate_location in job_location
            )
        ):
            location_score = 20
        else:
            location_score = 0

        experience = candidate.get("experience", 0) or 0
        experience_score = 10 if experience >= 1 else 0

        score = min(
            skill_score + location_score + experience_score,
            100,
        )

        breakdown = {
            "skills": skill_score,
            "location": location_score,
            "experience": experience_score,
        }

        strengths = []

        if matched_skills:
            strengths.append(
                f"Matched {len(matched_skills)} required skills."
            )

        if location_score:
            strengths.append("Location matches.")

        if experience_score:
            strengths.append("Experience matches job.")

        improvements = []

        if missing_skills:
            improvements.append(
                "Missing: " + ", ".join(missing_skills)
            )

        if not location_score:
            improvements.append(
                "Location preference does not match."
            )

        if not experience_score:
            improvements.append(
                "Gain more relevant professional or internship experience."
            )

        if score >= 80:
            recommendation = "Apply"
        elif score >= 60:
            recommendation = "Maybe"
        else:
            recommendation = "Skip"

        return {
            "score": score,
            "recommendation": recommendation,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "strengths": strengths,
            "improvements": improvements,
            "breakdown": breakdown,
        }