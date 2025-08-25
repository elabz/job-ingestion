# T04: Basic API routing scaffold

- [x] Task complete

## Summary
Create `routes.py` and include into app for future endpoints.

## Implementation details
- `src/job_ingestion/api/routes.py` exporting `api_router = APIRouter(prefix="/api/v1")`.
- Add placeholder route `GET /api/v1/ping` -> `{ "message": "pong" }`.
- In `src/job_ingestion/api/main.py`, include router: `app.include_router(api_router)`.

## Checklist
- [x] Create `routes.py` with `APIRouter`.
- [x] Implement `/api/v1/ping` handler.
- [x] Wire router into `app`.
- [x] Add unit test `tests/unit/api/test_ping.py`.

## Acceptance criteria
- [x] `/health` still works.
- [x] `/api/v1/ping` returns 200 and expected payload.

## Verification
```bash
conda run -n job-ingestion-service uvicorn src.job_ingestion.api.main:app --reload
curl -sS http://127.0.0.1:8000/api/v1/ping | jq .
```

## Docs
- Optional mention in `README.md`.

## Risks/Notes
- Keep response models minimal until T11.

## Dependencies
- T01 must be complete.

## Effort
- S: ~0.5–1h.
