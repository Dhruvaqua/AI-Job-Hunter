from pydantic import BaseModel


class AIRequest(BaseModel):
    candidate_id: int
    job_id: int


class AIResponse(BaseModel):
    response: str