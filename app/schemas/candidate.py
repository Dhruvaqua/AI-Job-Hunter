from pydantic import BaseModel


class CandidateCreate(BaseModel):
    name: str
    location: str
    experience: int = 0
    skills: list[str]


class CandidateResponse(BaseModel):
    id: int
    name: str
    location: str
    experience: int
    skills: str

    class Config:
        from_attributes = True