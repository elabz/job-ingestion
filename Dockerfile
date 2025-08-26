# syntax=docker/dockerfile:1
FROM python:3.10-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=1

# System deps for psycopg2 and build tools
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps separately for better caching
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy source (will be bind-mounted in dev for live reload)
COPY src ./src

ENV PYTHONPATH=/app/src

EXPOSE 8000

# Default command runs FastAPI with reload for development
CMD ["uvicorn", "src.job_ingestion.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
