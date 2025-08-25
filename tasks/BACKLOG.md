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

---

Notes:
- Always activate Conda env or use `conda run -n job-ingestion-service ...` in Makefile.
- All new code must include unit tests and docstrings.
- Use `pre-commit` locally before commits.
