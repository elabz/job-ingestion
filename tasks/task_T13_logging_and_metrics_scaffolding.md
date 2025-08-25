# T13: Logging and metrics scaffolding

- [ ] Task complete

## Summary
Create structured logging with `structlog` and metrics placeholders.

## Implementation details
- `src/job_ingestion/utils/logging.py` sets up structlog processors and returns a logger via `get_logger()`.
- `src/job_ingestion/utils/metrics.py` exposes `Counter`-like no-op wrappers (functions/classes) to avoid external deps for now.
- Integrate logger into app startup minimally.

## Checklist
- [ ] Implement logging config and export `get_logger`.
- [ ] Implement metrics placeholders.
- [ ] Unit tests ensure logger is usable.

## Acceptance criteria
- [ ] Importing `get_logger()` returns an object with `.info()`.

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
