from pydantic import BaseModel, HttpUrl
from typing import Optional


class NormalizedJob(BaseModel):
    """
    Common job format used internally by every job provider.
    """

    title: str
    company: str
    location: Optional[str] = None
    salary: Optional[str] = None
    url: HttpUrl
    description: Optional[str] = None