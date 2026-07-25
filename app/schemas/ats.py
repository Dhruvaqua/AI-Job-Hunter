from pydantic import BaseModel


class ATSRequest(BaseModel):
    candidate_id: int
    job_id: int