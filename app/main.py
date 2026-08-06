from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.jobs import router as job_router
from app.database.init_db import init_db
from app.api.search import router as search_router
from app.api.score import router as score_router
from app.api.candidate import router as candidate_router
from app.api.resume import router as resume_router
from app.api.ats import router as ats_router
from app.api.resume_advisor import router as advisor_router
from app.api.ai import router as ai_router
from app.api.system import router as system_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="AI Job Hunter",
    lifespan=lifespan,
)

app.include_router(job_router)
app.include_router(search_router)
app.include_router(score_router)
app.include_router(candidate_router)
app.include_router(resume_router)
app.include_router(ats_router)
app.include_router(advisor_router)
app.include_router(ai_router)
app.include_router(system_router)


@app.get("/")
def home():
    return {"message": "AI Job Hunter API"}


@app.get("/health")
def health():
    return {"status": "healthy"}