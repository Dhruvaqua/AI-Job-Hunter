from typing import Optional

from pydantic import BaseModel, HttpUrl


class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    salary: Optional[str] = None
    url: HttpUrl
    description: Optional[str] = None
    required_skills: Optional[str] = None


class JobResponse(JobCreate):
    id: int

    class Config:
        from_attributes = True