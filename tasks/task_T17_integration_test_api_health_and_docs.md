# T17: Integration test — API health and docs

- [x] Task complete

## Summary
Add `tests/integration/test_api_endpoints.py` to validate `/health` and docs availability.

## Implementation details
- Use FastAPI TestClient (starlette) for in-process testing.
- Tests:
  - `/health` returns 200 and payload.
  - `/docs` and `/openapi.json` return 200.

## Checklist
- [x] Implement integration tests.

## Acceptance criteria
- [x] Both endpoints respond with 200.

## Verification
```bash
conda run -n job-ingestion-service pytest -q tests/integration/test_api_endpoints.py
```

## Docs
- None.

## Risks/Notes
- Ensure app import path is correct.

## Dependencies
- T01.

## Effort
- S: ~0.5h.
