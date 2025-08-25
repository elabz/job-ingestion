# T01: Bootstrap FastAPI app and health endpoint

- [x] Task complete

## Summary
Implement minimal FastAPI app with `/health` and proper project wiring.

## Implementation details
- Create `src/job_ingestion/api/main.py` exporting `app: FastAPI` with title, version.
- Define `GET /health` returning `{ "status": "ok" }` and 200.
- Ensure import path `src.job_ingestion.api.main:app` works for Uvicorn.
- Keep code lint/type-check clean (Black line-length 100, Ruff, MyPy strict).
- Add `__all__ = ["app"]` to avoid unused-import issues if required.

## Checklist
- [x] Create module `src/job_ingestion/api/main.py` and FastAPI app instance.
- [x] Implement `/health` route and return JSON literal dict.
- [x] Ensure `if __name__ == "__main__"` block is absent (use Uvicorn CLI instead).
- [x] Update `README.md` Quickstart with run command.
- [x] Add/verify `tests/unit/test_health.py` assertions.

## Acceptance criteria
- [x] `GET /health` returns 200 and `{"status": "ok"}`.
- [x] `src.job_ingestion.api.main:app` importable without side effects.
- [x] `pre-commit run --all-files` passes.

## Verification
```bash
conda run -n job-ingestion-service uvicorn src.job_ingestion.api.main:app --reload
# In another shell
curl -sS http://127.0.0.1:8000/health | jq .
```

## Tests
- File: `tests/unit/test_health.py`
- Validate status code and payload equality, no extra keys.

## Docs
- Update `README.md` run instructions.
- Update `CONTRIBUTING.md` basic dev loop.

## Risks/Notes
- Pin FastAPI/Pydantic versions consistent with Pydantic v1 (see T19).

## Dependencies
- None.

## Effort
- S: ~0.5–1h.
