# Contributing

This project uses a Conda environment and pre-commit hooks. Always develop inside the Conda env and ensure hooks pass before committing.

## Prerequisites
- Conda (Miniconda/Anaconda)
- Git

## Environment Setup
```bash
conda env create -f environment.yml
conda activate job-ingestion-service
# Install dev extras (if not already installed via conda)
pre-commit install
```

## Common Tasks
- Code format: `make format`
- Lint: `make lint`
- Type-check: `make type-check`
- Tests: `make test`
- All checks: `make quality-check`

## Pre-Commit
Run hooks locally before committing:
```bash
pre-commit run --all-files
```

## Code Style
- Python 3.10+
- Black (line length 100)
- Ruff for linting
- MyPy in strict mode

## Testing
- Unit tests go under `tests/unit/`
- Integration tests under `tests/integration/`
- Add fixtures to `tests/fixtures/`

## FastAPI Dev Server
```bash
conda run -n job-ingestion-service uvicorn src.job_ingestion.api.main:app --reload --port 8000
```
