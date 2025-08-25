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
