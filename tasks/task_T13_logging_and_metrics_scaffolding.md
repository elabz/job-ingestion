# T13: Logging and metrics scaffolding

- [x] Task complete

## Summary
Create structured logging with `structlog` and metrics placeholders.

## Implementation details
- `src/job_ingestion/utils/logging.py` sets up structlog processors and returns a logger via `get_logger()`.
- `src/job_ingestion/utils/metrics.py` exposes no-op counters (increment/get/reset) to avoid external deps for now.
- Logger integrated into app startup with a simple `app.startup` info event in `src/job_ingestion/api/main.py`.

## Checklist
- [x] Implement logging config and export `get_logger`.
- [x] Implement metrics placeholders.
- [x] Unit tests ensure logger is usable.

## Acceptance criteria
- [x] Importing `get_logger()` returns an object with `.info()`.

## Verification
```bash
conda run -n job-ingestion-service pytest -q tests/unit/utils/test_logging.py
```

## Docs
- Brief logging guidance in README.

## Risks/Notes
- Avoid global state; allow injecting logger for testing.

## Dependencies
- None.

## Effort
- S: ~1h.
