# job-ingestion
Job Ingestion Service MVP

## Quickstart

1) Create and activate Conda environment

```bash
conda env create -f environment.yml
conda activate job-ingestion-service
```

2) Install and run pre-commit hooks

```bash
pre-commit install
pre-commit run --all-files
```

3) Run quality checks and tests

```bash
make quality-check
```

4) Start the API locally

```bash
conda run -n job-ingestion-service uvicorn src.job_ingestion.api.main:app --reload --port 8000
# Open http://localhost:8000/health and http://localhost:8000/docs
```

## Make targets

- __format__: `make format` — Black format `src` and `tests`.
- __lint__: `make lint` — Ruff lint (non-mutating, CI-friendly).
- __type-check__: `make type-check` — MyPy strict type checks over `src`.
- __test__: `make test` — Run full pytest suite.
- __quality-check__: `make quality-check` — Runs format, lint, type-check, and tests.
- __run-dev__: `make run-dev` — Start FastAPI via Uvicorn with reload.

### Ingest jobs (returns 202 with processing_id)

Single payload:

```bash
curl -i -s -X POST http://127.0.0.1:8000/api/v1/jobs/ingest \
  -H 'Content-Type: application/json' \
  -d '{
    "title":"Data Engineer",
    "description":"Build pipelines",
    "employment_type":"full-time",
    "hiring_organization":{"name":"Acme Inc"},
    "date_posted":"2024-01-01T00:00:00Z"
  }'
```

Batch payload:

```bash
curl -i -s -X POST http://127.0.0.1:8000/api/v1/jobs/ingest \
  -H 'Content-Type: application/json' \
  -d '{
    "jobs":[{
      "title":"Data Engineer",
      "description":"Build pipelines",
      "employment_type":"full-time",
      "hiring_organization":{"name":"Acme Inc"},
      "date_posted":"2024-01-01T00:00:00Z"
    }]
  }'
```

## Configuration

The service uses Pydantic BaseSettings (v1) for configuration.

- __Env vars__
  - `DATABASE_URL` (str). Default: `sqlite:///./db.sqlite3`
  - `REDIS_URL` (str). Default: `redis://localhost:6379`
  - `ENVIRONMENT` (str). Default: `development`

- __.env support__
  - Values are loaded from `.env` if present. Variable names are case-sensitive.
  - Copy `.env.example` to `.env` and adjust as needed.

- __Example .env__

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/job_ingestion
REDIS_URL=redis://localhost:6379
ENVIRONMENT=development
```

- __Access in code__

```python
from job_ingestion.utils.config import get_settings

settings = get_settings()
print(settings.database_url)
```

## Development database

- The default `DATABASE_URL` is SQLite: `sqlite:///./db.sqlite3`.
- SQLAlchemy 2.x ORM is used for models and sessions.
- To create tables locally:

```python
from job_ingestion.storage.models import Base
from job_ingestion.storage.repositories import get_engine

engine = get_engine("sqlite:///./db.sqlite3")
Base.metadata.create_all(bind=engine)
```

Models live in `src/job_ingestion/storage/models.py` and session helpers in `src/job_ingestion/storage/repositories.py`.

## Developer Docs

- Quickstart: `docs/QUICKSTART.md`
- Contributing guide: `CONTRIBUTING.md`
- Task backlog: `tasks/BACKLOG.md`

## Notes

- Python 3.10, FastAPI, pytest. Code style via Black, lint via Ruff, types via MyPy (strict).
- Always develop inside the Conda env or use `conda run -n job-ingestion-service ...`.

## Logging

- The project uses `structlog` for structured logs via `job_ingestion.utils.logging.get_logger()`.
- Environment-aware output:
  - `ENVIRONMENT=production` -> JSON logs
  - otherwise -> human-friendly console logs

Example:

```python
from job_ingestion.utils.logging import get_logger

logger = get_logger("example")
logger.info("job.ingested", job_id="123", approved=True)
```

Tips:
- Prefer binding a module/service name (e.g. `get_logger("api.main")`).
- Inject a logger into components for easier testing.

## Local services with Docker Compose (Postgres + Redis)

- Copy `.env.example` to `.env` and adjust if needed. The example `DATABASE_URL` points to local Postgres.
- `.env` also includes `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` used by Compose for the `db` service.

Start services and check health:

```bash
docker compose up -d db redis
docker compose ps
# Optional: wait until services are ready
./scripts/wait_for_services.sh
```

Stop services:

```bash
docker compose down
```

Verify API still runs locally and responds (separate terminal):

```bash
conda run -n job-ingestion-service uvicorn src.job_ingestion.api.main:app --reload --port 8000 &
sleep 2
curl -sS http://127.0.0.1:8000/health | jq .
```

## Run the API in Docker (live reload)

- Ensure Docker is installed and running.
- Copy `.env.example` to `.env` if not already done.
- Optionally change `APP_HOST_PORT` (default 8000) or `REDIS_HOST_PORT` in `.env` to avoid port conflicts.

Start the app alongside Postgres and Redis:

```bash
docker compose up -d db redis app
docker compose ps
```

Verify the health endpoint (curl):

```bash
curl -sS http://127.0.0.1:${APP_HOST_PORT:-8000}/health | jq .
```

Live reload: edits under `./src/` are bind-mounted into the container and auto-reloaded by Uvicorn.

Stop services:

```bash
docker compose down
```
