ENV_NAME=job-ingestion-service

.PHONY: init conda-create pre-commit-install format lint type-check test test-unit test-integration run-dev quality-check

init: conda-create pre-commit-install

conda-create:
	conda env create -f environment.yml || echo "Environment may already exist"

pre-commit-install:
	conda run -n $(ENV_NAME) pre-commit install

format:
	conda run -n $(ENV_NAME) black src tests

lint:
	conda run -n $(ENV_NAME) ruff check --fix src tests

type-check:
	conda run -n $(ENV_NAME) mypy src

quality-check: format lint type-check test

test:
	conda run -n $(ENV_NAME) env DISABLE_DOTENV=1 PYTHONPATH=src python -m pytest -q

test-unit:
	conda run -n $(ENV_NAME) env DISABLE_DOTENV=1 PYTHONPATH=src python -m pytest -q tests/unit

test-integration:
	conda run -n $(ENV_NAME) env DISABLE_DOTENV=1 PYTHONPATH=src python -m pytest -q tests/integration -s

run-dev:
	conda run -n $(ENV_NAME) env PYTHONPATH=src python -m uvicorn src.job_ingestion.api.main:app --reload --host 127.0.0.1 --port 8000
