from pydantic import BaseModel, HttpUrl
from typing import Optional


class JobCreate(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    salary: Optional[str] = None
    url: HttpUrl
    description: Optional[str] = None


class JobResponse(JobCreate):
    id: int

    class Config:
        from_attributes = True