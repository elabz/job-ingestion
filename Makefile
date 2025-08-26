ENV_NAME=job-ingestion-service

.PHONY: init conda-create pre-commit-install pre-commit-all format lint type-check test test-unit test-integration run-dev quality-check

init: conda-create pre-commit-install
	@echo "==> Initialized development environment"

conda-create:
	@echo "==> Creating Conda env '$(ENV_NAME)' (if needed)"
	conda env create -f environment.yml || echo "Environment may already exist"

pre-commit-install:
	@echo "==> Installing pre-commit hooks"
	conda run -n $(ENV_NAME) pre-commit install

pre-commit-all:
	@echo "==> Running pre-commit on all files"
	conda run -n $(ENV_NAME) pre-commit run --all-files

format:
	@echo "==> Formatting with Black"
	conda run -n $(ENV_NAME) black src tests
	@echo "==> Sorting imports with Ruff (I rules)"
	conda run -n $(ENV_NAME) ruff check --select I --fix src tests

lint:
	@echo "==> Linting with Ruff"
	conda run -n $(ENV_NAME) ruff check src tests

type-check:
	@echo "==> Type-checking with MyPy"
	conda run -n $(ENV_NAME) mypy src

quality-check: format lint type-check test
	@echo "==> Quality check complete (format, lint, type-check, test)"

test:
	@echo "==> Running tests"
	conda run -n $(ENV_NAME) env DISABLE_DOTENV=1 PYTHONPATH=src python -m pytest -q

test-unit:
	@echo "==> Running unit tests"
	conda run -n $(ENV_NAME) env DISABLE_DOTENV=1 PYTHONPATH=src python -m pytest -q tests/unit

test-integration:
	@echo "==> Running integration tests"
	conda run -n $(ENV_NAME) env DISABLE_DOTENV=1 PYTHONPATH=src python -m pytest -q tests/integration -s

run-dev:
	@echo "==> Starting dev server at http://127.0.0.1:8000 ..."
	conda run -n $(ENV_NAME) env PYTHONPATH=src python -m uvicorn src.job_ingestion.api.main:app --reload --host 127.0.0.1 --port 8000
