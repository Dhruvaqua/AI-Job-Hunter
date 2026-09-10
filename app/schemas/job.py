from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class JobCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    company: str = Field(..., min_length=1, max_length=200)
    location: str = Field(..., min_length=1, max_length=200)
    salary: Optional[str] = Field(default=None, max_length=200)
    url: HttpUrl
    description: Optional[str] = Field(default=None, max_length=50000)
    required_skills: Optional[str] = Field(default=None, max_length=5000)


class JobResponse(JobCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)