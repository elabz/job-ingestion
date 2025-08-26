# T21: Implement POST /api/v1/jobs/ingest endpoint

## Summary
Implement the ingestion endpoint defined in the PRD to accept a single job or a batch of jobs and return 202 Accepted with a `processing_id` so normalization/approval can proceed asynchronously.

## API contract (from PRD)
- Method/Path: `POST /api/v1/jobs/ingest`
- Request: `oneOf` SingleJobPosting | JobPostingBatch, where batch contains `jobs: JobPosting[]`.
- Response (202): `{ processing_id: UUID, message: str, estimated_completion?: datetime }`.

## Implementation details
- Files:
  - `src/job_ingestion/api/models.py`
    - Define request models compatible with Pydantic v1. Options:
      - Preferred: `Union[JobPosting, JobPostingBatch]` with a small validator that distinguishes batch if `jobs` key exists.
      - Alternative: A single wrapper model `{ jobs?: list[JobPosting], ... }` and treat presence of `jobs` as batch.
  - `src/job_ingestion/api/routes.py`
    - Add route `POST /api/v1/jobs/ingest` to `api_router`.
    - Parse request payload (single vs batch), normalize shapes to a list of jobs for the service.
    - Call `IngestionService.ingest_batch(jobs_data: list[dict], source_platform: str = "api")`.
    - Return `202` JSON with `processing_id` and a short `message`.
    - Error handling: 422 on validation errors (FastAPI default), 500 with generic message on unexpected errors.
  - `src/job_ingestion/ingestion/service.py`
    - Ensure method signature exists (from T06). For MVP stub:
      - Generate a UUID `processing_id`.
      - Optionally store basic in-memory status for future `GET /api/v1/jobs/status/{processing_id}`.
      - Return `processing_id`.
  - Tests: `tests/integration/test_ingest_api.py`.
    - Test single payload returns 202 and `processing_id`.
    - Test batch payload returns 202 and `processing_id`.

### Request model notes (Pydantic v1)
- Keep compatibility with current pin (see T19). Pydantic v1 supports `Union[...]` and discriminated unions (>=1.8). If discriminators become cumbersome, use a field-presence heuristic (presence of `jobs`) to branch.

## Checklist
- [ ] Define request models for single and batch ingestion in `api/models.py`.
- [ ] Implement `POST /api/v1/jobs/ingest` in `api/routes.py` and wire to `api_router`.
- [ ] Call `IngestionService.ingest_batch()` with a normalized list of job dicts.
- [ ] Return `202` JSON with `processing_id`.
- [ ] Add integration tests for single and batch requests.
- [ ] Update `README.md` Quickstart with curl examples.
- [ ] Run `make quality-check` and fix any issues (Black, Ruff, MyPy).

## Acceptance criteria
- `POST /api/v1/jobs/ingest` returns HTTP 202 with a JSON body containing a valid UUID in `processing_id` for both single and batch payloads.
- OpenAPI docs render the endpoint and schemas (leveraging T11 scaffolding).
- Integration tests in `tests/integration/test_ingest_api.py` pass.

## Verification
```bash
# Start the dev server
conda run -n job-ingestion-service uvicorn src.job_ingestion.api.main:app --reload

# Single payload
curl -i -s -X POST http://127.0.0.1:8000/api/v1/jobs/ingest \
  -H 'Content-Type: application/json' \
  -d '{
    "title":"Data Engineer",
    "description":"Build pipelines",
    "employment_type":"full-time",
    "hiring_organization":{"name":"Acme Inc"},
    "date_posted":"2024-01-01T00:00:00Z"
  }'

# Batch payload
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

# Tests
conda run -n job-ingestion-service pytest -q tests/integration/test_ingest_api.py
```

## Docs
- Update `README.md` Quickstart with example `curl` commands and a note about 202 + `processing_id`.

## Risks/Notes
- OpenAPI `oneOf` vs Pydantic v1: discriminated union by `type` field is cleanest; if avoiding schema changes, use heuristic on `jobs` key.
- Authentication, rate limiting, and idempotency are not covered in this MVP task; add follow-up tasks as needed.
- Consider payload size constraints and basic request timeouts.

## Dependencies
- `T04` Basic API routing scaffold (router wiring).
- `T06` Ingestion service interfaces (stubs).
- `T11` API contract scaffolding (models in place and docs render).
- `T17` Integration test framework for API endpoints.
- `T19` Version pinning (ensure Pydantic v1 compatibility).
- Optional: `T16` Sample fixtures for future pipeline tests.

## Effort
- M: ~2–3h.
