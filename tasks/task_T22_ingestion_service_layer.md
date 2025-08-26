# T22: Implement Ingestion Service Layer (Full Implementation)

## Summary
Implement the full ingestion pipeline in `IngestionService` to process single or batch job payloads: detect source schema, normalize/transform fields, evaluate approval rules, persist to storage, and expose processing status via `get_processing_status()`. Replace the NotImplementedError fallback in the API by returning a real `processing_id` produced by the service.

## Affected Paths
- `src/job_ingestion/ingestion/service.py`
- `src/job_ingestion/ingestion/schema_detector.py`
- `src/job_ingestion/transformation/normalizers.py`
- `src/job_ingestion/approval/engine.py` (usage)
- `src/job_ingestion/storage/models.py`, `src/job_ingestion/storage/repositories.py`
- Tests under `tests/unit/ingestion/` and `tests/integration/`

## Deliverables
- Concrete implementation of `IngestionService.ingest_batch(jobs: list[dict[str, Any]]) -> str` returning a durable `processing_id`.
- Implementation of `IngestionService.get_processing_status(processing_id: str)` returning structure with counts by status (processed, approved, rejected, errors).
- Orchestration across schema detection, normalization, rules engine, and persistence.
- Robust logging, metrics counters, and strict typing.

## Implementation Details
1) Orchestration
- Generate a `processing_id` (UUID4 string).
- For each job dict:
  - Detect schema with `schema_detector.detect_schema()`.
  - Transform/normalize fields via `normalizers` utilities to a canonical shape the `Job` model expects.
  - Evaluate approval via `ApprovalEngine` and set `approval_status` accordingly.
  - Persist a `Job` row using SQLAlchemy session (repository pattern).
- Track per-item outcomes for status reporting.

2) Persistence and Status Tracking
- Use existing `Job` SQLAlchemy model. Persist minimally: `external_id` (if present), `title`, `approval_status`. Add optional-safe handling for missing fields.
- Maintain a lightweight processing record in-memory for now (a class-level dict keyed by `processing_id`) with counts. Structure:
  ```python
  {
    processing_id: {
      "total": int,
      "processed": int,
      "approved": int,
      "rejected": int,
      "errors": int,
      "started_at": datetime,
      "finished_at": Optional[datetime],
    }
  }
  ```
- Mark `finished_at` when batch is done. This will be replaced by Redis or DB table in a later task.

3) Error Handling
- Catch and log per-item exceptions; increment `errors` but continue processing the batch.
- If all items fail, still return `processing_id` with error counts.

4) Logging and Metrics
- Add structured logs at batch start/end and per-item with decision outcome.
- Expose simple counters in `utils/metrics.py` (no-op allowed) for batch processed, approved, rejected, errors.

5) Type Safety
- Add precise type hints and docstrings. Run mypy in strict mode cleanly.

## Docs
- Update `README.md` to note that the ingestion endpoint now returns a real processing_id and that the service processes and persists jobs synchronously (interim).
- Add a short section describing the processing stages and where to find logs.

## Verification
- `conda run -n job-ingestion-service make quality-check` passes.
- Manual smoke: start the dev server and POST to `/api/v1/jobs/ingest` (single and batch) using the existing curl examples. Then verify rows are written by running a short sqlite script in tests or a temporary CLI snippet to query the in-memory dev DB (or adapt to local DB if configured).

## Tests
- Unit: `tests/unit/ingestion/test_service_impl.py`
  - Mocks `schema_detector`, `normalizers`, and `ApprovalEngine` to ensure orchestration order, error handling, and status counts.
  - Asserts `processing_id` format and status dict shape.
- Integration: `tests/integration/test_ingest_end_to_end.py`
  - POST single and batch payloads via API; verify 202.
  - Open a SQLAlchemy session to check that `Job` rows were inserted with the expected `approval_status` values.

## Acceptance Criteria
- `IngestionService.ingest_batch` returns a real `processing_id` and persists jobs.
- `get_processing_status(processing_id)` returns accurate counts and timestamps.
- All quality checks and tests pass locally.
- Logs and metrics for batch and items are produced without raising errors.

## Follow-ups (separate tasks)
- T23: Add `GET /api/v1/ingest/{processing_id}` to expose processing status via API.
- T24: Move status tracking to Redis (use `REDIS_URL`) and implement async job processing.
- T25: Idempotency keys and deduplication for `external_id`.
- T26: Dead-letter handling for invalid payloads; error reporting route.
- T27: Observability enhancements (structured logging fields, metrics labels).
