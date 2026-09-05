FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Create an unprivileged application user.
RUN groupadd --system appuser \
    && useradd --system --gid appuser --create-home appuser

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application files.
COPY app ./app
COPY frontend ./frontend
COPY uploads ./uploads

# Make runtime directories writable by the application user.
RUN mkdir -p /app/uploads /app/data \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s \
    --timeout=5s \
    --start-period=20s \
    --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]