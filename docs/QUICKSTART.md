# Quickstart

## 1) Create and activate Conda environment
```bash
conda env create -f environment.yml
conda activate job-ingestion-service
```

## 2) Install pre-commit hooks
```bash
pre-commit install
pre-commit run --all-files
```

## 3) Start local Postgres and Redis (Docker Compose)
- Copy `.env.example` to `.env` if you haven't already.
- Ensure `DATABASE_URL` points to your desired DB (defaults to local Postgres in example).

```bash
docker compose up -d db redis
docker compose ps
# Optional: wait until services are ready
./scripts/wait_for_services.sh
```

## 4) Run tests and quality checks
```bash
make quality-check
```

## 5) Start the API locally
```bash
uvicorn src.job_ingestion.api.main:app --reload --port 8000
# Open http://localhost:8000/health
# Open http://localhost:8000/docs
```
