from pydantic import BaseModel


class CandidateCreate(BaseModel):
    name: str
    location: str
    skills: list[str]


class CandidateResponse(BaseModel):
    id: int
    name: str
    location: str
    skills: str

    class Config:
        from_attributes = True