# Contributing

This project uses a Conda environment and pre-commit hooks. Always develop inside the Conda env and ensure hooks pass before committing.

## Prerequisites
- Conda (Miniconda/Anaconda)
- Git

## Environment Setup
```bash
conda env create -f environment.yml
conda activate job-ingestion-service
# Install dev hooks
pre-commit install
```

## Common Tasks
- Code format: `make format`
- Lint: `make lint`
- Type-check: `make type-check`
- Tests: `make test`
- All checks: `make quality-check`
- Dev server: `make run-dev`

## Pre-Commit
Run hooks locally before committing:
```bash
pre-commit run --all-files
```

Or via Make (uses Conda automatically):
```bash
make pre-commit-all
```

## Code Style
- Python 3.10+
- Black (line length 100)
- Ruff for linting (includes import sort with `ruff check --select I --fix`)
- MyPy in strict mode over `src`
- Keep functions small and typed. Add docstrings for public APIs.

## Testing Strategy
- Unit tests under `tests/unit/`
- Integration tests under `tests/integration/`
- Shared fixtures under `tests/fixtures/`
- Run all tests quickly:
  ```bash
  conda run -n job-ingestion-service env DISABLE_DOTENV=1 PYTHONPATH=src python -m pytest -q
  ```
- Run only unit or integration:
  ```bash
  make test-unit
  make test-integration
  ```
- CI and local dev use the same checks via `make quality-check`.

## Running the API Locally
```bash
conda run -n job-ingestion-service uvicorn src.job_ingestion.api.main:app --reload --port 8000
# Visit http://localhost:8000/health and http://localhost:8000/docs
```

## Git Workflow
- Create feature branches from `main` (e.g., `feature/T18-docs`, `fix/ingest-500`)
- Keep PRs small and focused.
- Rebase over `main` when needed; prefer linear history.

## Pull Request Checklist
- [ ] Updated/added tests as necessary
- [ ] `make quality-check` passes locally
- [ ] `pre-commit run --all-files` passes (Black, Ruff, MyPy)
- [ ] Docs updated (README, QUICKSTART, or in `tasks/` as appropriate)
- [ ] Verified critical endpoints via curl when relevant (e.g., `/health`, `/docs`)
- [ ] Self-reviewed code (naming, typing, logs)

## Version Notes
- Pydantic v1.x (`pydantic<2`) is used; refer to Pydantic v1 docs.
- FastAPI is pinned `<0.100` to remain compatible with Pydantic v1.
