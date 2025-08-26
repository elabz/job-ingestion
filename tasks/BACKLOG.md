# Job Ingestion Service — Developer Backlog (Independent Tasks)

Each task is small, independently implementable, and includes steps, docs, verification, and test requirements. Use Conda env `job-ingestion-service` and pre-commit for all work.

---

## T01: Bootstrap FastAPI app and health endpoint
- Summary: Implement minimal API app with `/health` and project wiring.
- Affected paths: `src/job_ingestion/api/main.py`, `tests/unit/test_health.py`
- Steps:
  1) Create FastAPI app with title and version.
  2) Add GET `/health` returning `{ "status": "ok" }`.
  3) Ensure importable via `src.job_ingestion.api.main:app`.
- Docs: Update `README.md` Quickstart and `CONTRIBUTING.md`.
- Verification:
  - `conda run -n job-ingestion-service uvicorn src.job_ingestion.api.main:app --reload` starts.
  - `GET /health` returns 200 `{"status":"ok"}`.
- Tests: `tests/unit/test_health.py` asserting response code and payload.

## T02: Project configuration and tooling
- Summary: Configure Black, Ruff, MyPy, pytest.
- Affected paths: `pyproject.toml`, `.pre-commit-config.yaml`, `Makefile`.
- Steps:
  1) Ensure `black`, `ruff`, `mypy`, `pytest` configs are present.
  2) Enable pre-commit hooks for format, lint, type-check.
- Docs: `CONTRIBUTING.md` (code quality workflow).
- Verification:
  - `make quality-check` succeeds.
  - `pre-commit run --all-files` passes.
- Tests: No logic tests; CI check is passing hooks locally.

## T03: Configuration management via Pydantic Settings (v1)
- Summary: Centralize env config with `.env` support using `pydantic.BaseSettings`.
- Affected: `src/job_ingestion/utils/config.py`, `.env.example`.
- Steps:
  1) Provide `Settings` reading `DATABASE_URL`, `REDIS_URL`, `ENVIRONMENT`.
  2) Load `.env` automatically.
- Docs: Add env table to `README.md`.
- Verification: Unit test loads defaults and `.env` overrides.
- Tests: `tests/unit/test_settings.py` to verify values from env.

## T04: Basic API routing scaffold
- Summary: Create `routes.py` and include into app for future endpoints.
- Affected: `src/job_ingestion/api/routes.py`, `src/job_ingestion/api/main.py`.
- Steps: Define `api_router` with placeholder routes; include in app.
- Docs: N/A
- Verification: `/health` still works; `/api/v1/ping` returns 200.
- Tests: `tests/unit/api/test_ping.py`.

## T05: Storage models and DB connection interface (stubs)
- Summary: Define SQLAlchemy models and session factory (no migrations yet).
- Affected: `src/job_ingestion/storage/models.py`, `src/job_ingestion/storage/repositories.py`.
- Steps:
  1) Define `Job` table per PRD subset (id, external_id, title, approval_status, created_at).
  2) Create `get_session()` and base repository pattern.
- Docs: Add section in `README.md` (development DB).
- Verification: Importing models and creating metadata works against SQLite.
- Tests: `tests/unit/storage/test_models.py` creates in-memory SQLite and checks tables.

## T06: Ingestion service interfaces (stubs)
- Summary: Define `IngestionService` signatures from PRD and no-op impl.
- Affected: `src/job_ingestion/ingestion/service.py`.
- Steps: Create methods `ingest_batch()`, `get_processing_status()`, `register_source_schema()` with TODOs.
- Docs: Inline docstrings.
- Verification: Import without runtime errors.
- Tests: `tests/unit/ingestion/test_service_signatures.py` validates default behaviors/exceptions.

## T07: Schema detector (stub)
- Summary: Add JSON schema detection module with simple heuristic placeholder.
- Affected: `src/job_ingestion/ingestion/schema_detector.py`.
- Steps: Provide `detect_schema(jobs_data)` returning a named variant.
- Verification: Simple detection by key presence.
- Tests: `tests/unit/ingestion/test_schema_detector.py`.

## T08: Transformation normalizers (stubs)
- Summary: Create `LocationNormalizer`, `SalaryNormalizer`, `CompanyValidator` classes with method stubs.
- Affected: `src/job_ingestion/transformation/normalizers.py`.
- Steps: Implement signatures from PRD with basic placeholder logic.
- Verification: Methods return expected datatypes or None.
- Tests: `tests/unit/transformation/test_normalizers.py`.

## T09: Approval engine skeleton
- Summary: Implement `ApprovalEngine` class with registry and `evaluate_job()` stub.
- Affected: `src/job_ingestion/approval/engine.py`, `src/job_ingestion/approval/rules/base.py`.
- Steps: Create base rule interface and registry.
- Verification: Can register rule and call evaluate_job producing `ApprovalDecision` dataclass.
- Tests: `tests/unit/approval/test_engine.py`.

## T10: Rules modules (stubs)
- Summary: Implement placeholder `location_rules.py`, `salary_rules.py`, `content_rules.py` with simple pass/fail.
- Affected: `src/job_ingestion/approval/rules/*.py`.
- Verification: Salary rule passes for >= threshold.
- Tests: `tests/unit/approval/test_rules.py` incl. min examples from PRD.

## T11: API contract scaffolding (OpenAPI)
- Summary: Add OpenAPI schemas for JobPosting and basic endpoints.
- Affected: `src/job_ingestion/api/models.py`, `src/job_ingestion/api/routes.py`.
- Steps: Define Pydantic models reflecting PRD `JobPosting` subset.
- Verification: `/docs` renders models.
- Tests: `tests/integration/test_api_docs.py` checks OpenAPI contains components.

## T12: Docker compose for local DB/Redis (dev only)
- Summary: Add `docker-compose.yml` per PRD dev section.
- Affected: `docker-compose.yml`.
- Steps: Services for postgres, redis; env vars from `.env`.
- Verification: `docker-compose up -d db redis` succeeds.
- Tests: Not applicable; add smoke check script `scripts/wait_for_services.sh` (optional).

## T13: Logging and metrics scaffolding
- Summary: Create structured logging with `structlog` and metrics placeholders.
- Affected: `src/job_ingestion/utils/logging.py`, `src/job_ingestion/utils/metrics.py`.
- Verification: Logger available; metrics no-op counters.
- Tests: `tests/unit/utils/test_logging.py` ensures logger returns.

## T14: CI-friendly Make targets
- Summary: Complete Makefile with `format`, `lint`, `type-check`, `test`, `run-dev`.
- Affected: `Makefile`.
- Verification: All targets run under Conda.
- Tests: N/A.

## T15: Pre-commit in CI and local
- Summary: Ensure `pre-commit` installed and `pre-commit run --all-files` clean.
- Affected: `.pre-commit-config.yaml`.
- Verification: All hooks pass locally.
- Tests: N/A.

## T16: Sample fixtures and test data
- Summary: Add sample job JSON fixtures to support tests.
- Affected: `tests/fixtures/sample_jobs.json`.
- Verification: File parsable; used in integration tests.
- Tests: Reference in integration test later.

## T17: Integration test — API health and docs
- Summary: Add `tests/integration/test_api_endpoints.py` to validate `/health` and docs.
- Verification: 200 responses.
- Tests: As described.

## T18: Documentation — CONTRIBUTING and Quickstart
- Summary: Write `CONTRIBUTING.md` (Conda, quality checks, test strategy) and expand `README.md`.
- Verification: Steps work end-to-end locally.
- Tests: N/A.

## T19: Version pinning and compatibility
- Summary: Pin FastAPI/Pydantic versions compatible with current code (Pydantic v1). Add a follow-up task to migrate to Pydantic v2.
- Verification: `pip check` clean in Conda env; imports succeed.
- Tests: Existing tests pass.

## T20: Follow-up — Migrate to Pydantic v2
- Summary: Replace `BaseSettings` with `pydantic-settings`, update models and FastAPI compatibility.
- Verification: All tests still pass; run mypy.
- Tests: Update tests accordingly.

## T21: Implement POST /api/v1/jobs/ingest endpoint
- Summary: Implement ingestion endpoint accepting a single job or batch payload and returning 202 with a `processing_id`.
- Affected: `src/job_ingestion/api/routes.py`, `src/job_ingestion/api/models.py`, `src/job_ingestion/ingestion/service.py`, `tests/integration/test_ingest_api.py`.
- Steps:
  1) Define request models per PRD OpenAPI (oneOf `SingleJobPosting` or `JobPostingBatch`) reusing the `JobPosting` schema.
  2) Implement POST `/api/v1/jobs/ingest` that validates payload and invokes `IngestionService.ingest_batch()`; respond 202 with `processing_id` and message.
  3) Wire the route into `api_router` in `src/job_ingestion/api/routes.py`.
  4) Add basic error handling for invalid payloads (422) and unexpected errors (500).
- Docs: Update `README.md` Quickstart with curl examples.
- Verification:
  - Start: `conda run -n job-ingestion-service uvicorn src.job_ingestion.api.main:app --reload`.
  - Single example:
    curl -s -X POST http://127.0.0.1:8000/api/v1/jobs/ingest -H 'Content-Type: application/json' -d '{"title":"Data Engineer","description":"Build pipelines","employment_type":"full-time","hiring_organization":{"name":"Acme Inc"},"date_posted":"2024-01-01T00:00:00Z"}'
    Expect 202 with JSON containing `processing_id` (UUID).
  - Batch example:
    curl -s -X POST http://127.0.0.1:8000/api/v1/jobs/ingest -H 'Content-Type: application/json' -d '{"jobs":[{"title":"Data Engineer","description":"Build pipelines","employment_type":"full-time","hiring_organization":{"name":"Acme Inc"},"date_posted":"2024-01-01T00:00:00Z"}]}'
    Expect 202 with `processing_id`.
- Tests: Implement `tests/integration/test_ingest_api.py` asserting 202 response and presence of `processing_id` for single and batch payloads.

## T22: Implement Ingestion Service Layer (Full Implementation)
- Summary: Implement the full `IngestionService` pipeline to process batch jobs end-to-end: schema detection, normalization, approval evaluation, persistence, and processing status tracking. Replace API fallback UUID with a real `processing_id` returned from the service.
- Affected: `src/job_ingestion/ingestion/service.py`, `src/job_ingestion/ingestion/schema_detector.py`, `src/job_ingestion/transformation/normalizers.py`, `src/job_ingestion/approval/engine.py`, `src/job_ingestion/storage/models.py`, `src/job_ingestion/storage/repositories.py`, tests under `tests/unit/ingestion/` and `tests/integration/`.
- Steps:
  1) Implement `ingest_batch(jobs: list[dict[str, Any]]) -> str` to orchestrate: detect schema, normalize to canonical shape, evaluate approval via `ApprovalEngine`, and persist `Job` rows via SQLAlchemy repository.
  2) Generate and return a UUID4 `processing_id`. Track per-batch status in-memory (counts: total, processed, approved, rejected, errors; timestamps start/finish). Mark finished when all items processed.
  3) Implement `get_processing_status(processing_id: str)` returning a dict with the above counts and timestamps.
  4) Add structured logging at batch start/end and per item; increment simple metrics counters. Ensure strict typing and docstrings.
  5) Update the API route to rely on the service’s `processing_id` (no fallback when service implemented).
- Docs: Update `README.md` to describe processing stages and note that `processing_id` is now produced by the service. Cross-check FastAPI/Pydantic/SQLAlchemy usage against latest docs.
- Verification:
  - `conda run -n job-ingestion-service make quality-check` passes.
  - Manual: POST single and batch to `/api/v1/jobs/ingest` using curl examples; verify 202 and that rows are written (query dev DB via a short SQLAlchemy snippet or test helper).
- Tests:
  - Unit: `tests/unit/ingestion/test_service_impl.py` mocking collaborators to assert orchestration order, error handling, and accurate status counts.
  - Integration: `tests/integration/test_ingest_end_to_end.py` posting via API and verifying `Job` persistence and approval statuses.

## T23: Dockerize application container with live reload
- Summary: Add Dockerfile and compose `app` service to run FastAPI with reload and source bind mount for active development.
- Affected: `Dockerfile`, `docker-compose.yml`, `.env.example`, `.dockerignore`, `requirements.txt`.
- Steps:
  1) Create `Dockerfile` using `python:3.10-slim`, install `requirements.txt`, set `PYTHONPATH`, and run uvicorn with `--reload`.
  2) Add `app` service to `docker-compose.yml` exposing `${APP_HOST_PORT:-8000}` and mounting `./src:/app/src`.
  3) Default `DATABASE_URL` to Postgres service (`db`) and `REDIS_URL` to Redis service (`redis`) inside container.
  4) Add `.dockerignore` and `APP_HOST_PORT` to `.env.example`.
  5) Optional healthcheck on `/health` for the app service.
- Docs: Update `README.md`/`docs/QUICKSTART.md` with instructions to run the app via compose and verify with curl.
- Verification:
  - `docker compose up -d db redis app` completes; `docker compose ps` shows healthy services.
  - `curl -sSf http://127.0.0.1:${APP_HOST_PORT:-8000}/health` returns `{ "status": "ok" }`.
- Tests: Not applicable; smoke verification via curl only.

---

Notes:
- Always activate Conda env or use `conda run -n job-ingestion-service ...` in Makefile.
- All new code must include unit tests and docstrings.
- Use `pre-commit` locally before commits.
