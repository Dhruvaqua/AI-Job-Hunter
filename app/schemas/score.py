from pydantic import BaseModel


class CandidateProfile(BaseModel):
    skills: list[str]
    location: str


class ScoreRequest(BaseModel):
    job_id: int
    candidate: CandidateProfile