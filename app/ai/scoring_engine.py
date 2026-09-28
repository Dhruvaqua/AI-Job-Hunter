import re


ALIASES = {
    "google cloud platform": "gcp",
    "google cloud": "gcp",
    "gcp": "gcp",
    "rest api": "rest",
    "restful api": "rest",
    "postgres": "postgresql",
    "mongodb": "mongodb",
    "mongo": "mongodb",
    "big query": "bigquery",
    "bigquery": "bigquery",
    "llama": "llm",
    "llama 3.2": "llm",
    "generative ai": "llm",
    "genai": "llm",
}


class ScoringEngine:
    @staticmethod
    def _normalize(value):
        if not value:
            return set()
        if isinstance(value, str):
            value = value.split(",")
        normalized = set()
        for item in value:
            item = str(item).lower().strip()
            if not item:
                continue
            normalized.add(ALIASES.get(item, item))
        return normalized

    @staticmethod
    def _required_experience(description):
        if not description:
            return None
        matches = re.findall(
            r"(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years|year|yrs|yr)\b",
            description.lower(),
        )
        return max((float(x) for x in matches), default=None)

    @staticmethod
    def _location_match(candidate_location, job_location):
        c = (candidate_location or "").lower()
        j = (job_location or "").lower()

        if "remote" in j:
            return True
        if "india" in j and c in {"india", "hyderabad", "bengaluru", "bangalore",
                                  "chennai", "pune", "mumbai", "delhi", "gurgaon",
                                  "gurugram", "noida", "kolkata", "ahmedabad", "jaipur"}:
            return True
        return c and c in j

    @staticmethod
    def score(candidate: dict, job: dict):
        candidate_skills = ScoringEngine._normalize(candidate.get("skills"))
        job_skills = ScoringEngine._normalize(job.get("required_skills"))

        matched = sorted(candidate_skills & job_skills)
        missing = sorted(job_skills - candidate_skills)

        skill_score = round((len(matched) / len(job_skills)) * 55) if job_skills else 0

        title = (job.get("title") or "").lower()
        candidate_title_terms = {
            "software engineer", "backend", "data engineer", "python",
            "cloud", "ai engineer", "platform", "developer"
        }
        title_score = 10 if any(term in title for term in candidate_title_terms) else 0

        location_ok = ScoringEngine._location_match(
            candidate.get("location"), job.get("location")
        )
        location_score = 20 if location_ok else 0

        candidate_exp = float(candidate.get("experience") or 0)
        required_exp = ScoringEngine._required_experience(job.get("description") or "")

        if required_exp is None:
            experience_score = 10
            experience_note = "No explicit experience requirement detected."
        elif candidate_exp >= required_exp:
            experience_score = 15
            experience_note = f"Candidate has ~{candidate_exp:g} years; JD asks ~{required_exp:g}+ years."
        elif candidate_exp + 0.5 >= required_exp:
            experience_score = 8
            experience_note = f"Candidate is slightly below the stated ~{required_exp:g}+ year requirement."
        else:
            experience_score = 0
            experience_note = f"Candidate has ~{candidate_exp:g} years; JD asks ~{required_exp:g}+ years."

        score = min(skill_score + title_score + location_score + experience_score, 100)

        strengths = []
        if matched:
            strengths.append(f"Matched skills: {', '.join(matched)}.")
        if location_ok:
            strengths.append("Location/workplace eligibility matches.")
        if required_exp is None or candidate_exp >= required_exp:
            strengths.append(experience_note)

        improvements = []
        if missing:
            improvements.append("Missing skills: " + ", ".join(missing) + ".")
        if not location_ok:
            improvements.append("Location/workplace eligibility does not clearly match.")
        if required_exp is not None and candidate_exp < required_exp:
            improvements.append(experience_note)

        recommendation = "Apply" if score >= 75 else "Review" if score >= 60 else "Skip"

        return {
            "score": score,
            "recommendation": recommendation,
            "matched_skills": matched,
            "missing_skills": missing,
            "strengths": strengths,
            "improvements": improvements,
            "breakdown": {
                "skills": skill_score,
                "title": title_score,
                "location": location_score,
                "experience": experience_score,
            },
        }
