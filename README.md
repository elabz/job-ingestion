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

## Developer Docs

- Quickstart: `docs/QUICKSTART.md`
- Contributing guide: `CONTRIBUTING.md`
- Task backlog: `tasks/BACKLOG.md`

## Notes

- Python 3.10, FastAPI, pytest. Code style via Black, lint via Ruff, types via MyPy (strict).
- Always develop inside the Conda env or use `conda run -n job-ingestion-service ...`.
