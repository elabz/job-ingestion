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

## 3) Run tests and quality checks
```bash
make quality-check
```

## 4) Start the API locally
```bash
uvicorn src.job_ingestion.api.main:app --reload --port 8000
# Open http://localhost:8000/health
# Open http://localhost:8000/docs
```
