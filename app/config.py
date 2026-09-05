from dotenv import load_dotenv
import os


load_dotenv()


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./jobs.db",
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2",
)

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434",
)
OLLAMA_TIMEOUT = int(
    os.getenv(
        "OLLAMA_TIMEOUT",
        "120",
    )
)

MAX_LLM_INPUT_LENGTH = int(
    os.getenv(
        "MAX_LLM_INPUT_LENGTH",
        "12000",
    )
)

MAX_LLM_OUTPUT_LENGTH = int(
    os.getenv(
        "MAX_LLM_OUTPUT_LENGTH",
        "12000",
    )
)

ENVIRONMENT = os.getenv(
    "ENVIRONMENT",
    "development",
).lower()

API_KEY = os.getenv(
    "API_KEY",
    "",
)

MAX_UPLOAD_SIZE = int(
    os.getenv(
        "MAX_UPLOAD_SIZE",
        str(5 * 1024 * 1024),
    )
)

ALLOWED_CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_CORS_ORIGINS",
        "http://localhost:8501,http://127.0.0.1:8501",
    ).split(",")
    if origin.strip()
]


# External hosts that the application is allowed to contact.
#
# These are intentionally restrictive.
# Add another host only when the application genuinely needs it.
ALLOWED_EXTERNAL_HOSTS = {
    "boards-api.greenhouse.io",
    "api.lever.co",
    "jobs.lever.co",
    "boards.greenhouse.io",
}


# Maximum amount of text extracted from a resume.
# This prevents unexpectedly huge PDFs from producing enormous
# prompts or consuming excessive memory.
MAX_RESUME_TEXT_LENGTH = int(
    os.getenv(
        "MAX_RESUME_TEXT_LENGTH",
        "200000",
    )
)


# Maximum number of pages processed from a PDF resume.
MAX_RESUME_PAGES = int(
    os.getenv(
        "MAX_RESUME_PAGES",
        "10",
    )
)