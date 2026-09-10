from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.ai import router as ai_router
from app.api.ats import router as ats_router
from app.api.candidate import router as candidate_router
from app.api.jobs import router as job_router
from app.api.resume import router as resume_router
from app.api.resume_advisor import router as advisor_router
from app.api.score import router as score_router
from app.api.search import router as search_router
from app.api.system import router as system_router
from app.config import (
    ALLOWED_CORS_ORIGINS,
    API_KEY,
    ENVIRONMENT,
)
from app.database.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):

    if ENVIRONMENT == "production" and not API_KEY:
        raise RuntimeError(
            "API_KEY must be configured when "
            "ENVIRONMENT=production"
        )

    init_db()

    yield


if ENVIRONMENT == "production":
    app = FastAPI(
        title="AI Job Hunter",
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )
else:
    app = FastAPI(
        title="AI Job Hunter",
        lifespan=lifespan,
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=[
        "GET",
        "POST",
        "OPTIONS",
    ],
    allow_headers=[
        "Content-Type",
        "Accept",
        "X-API-Key",
    ],
)


@app.middleware("http")
async def security_headers(
    request: Request,
    call_next,
):
    response = await call_next(request)

    response.headers[
        "X-Content-Type-Options"
    ] = "nosniff"

    response.headers[
        "X-Frame-Options"
    ] = "DENY"

    response.headers[
        "Referrer-Policy"
    ] = "strict-origin-when-cross-origin"

    response.headers[
        "Permissions-Policy"
    ] = (
        "camera=(), microphone=(), "
        "geolocation=()"
    )

    if ENVIRONMENT == "production":
        response.headers[
            "Strict-Transport-Security"
        ] = (
            "max-age=31536000; "
            "includeSubDomains"
        )

    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        },
    )
    
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(
    request: Request,
    exc: SQLAlchemyError,
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "A database error occurred."
        },
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
    return {
        "message": "AI Job Hunter API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }