# T11: API contract scaffolding (OpenAPI)

- [x] Task complete

## Summary
Add OpenAPI schemas for JobPosting and basic endpoints.

## Implementation details
- `src/job_ingestion/api/models.py`:
  - Pydantic v1 models: `JobPosting`, minimal fields from PRD subset (title, company, location, salary_min/max optional, description optional).
- `src/job_ingestion/api/routes.py` uses response_model for `/api/v1/ping` or future endpoints.
- Confirm `/docs` renders components.

## Checklist
- [x] Define models with field types and examples.
- [x] Wire into routes where applicable.

## Acceptance criteria
- [x] OpenAPI schema includes `JobPosting` component.

## Verification
```bash
conda run -n job-ingestion-service pytest -q tests/integration/test_api_docs.py
```

## Docs
- None beyond OpenAPI.

## Risks/Notes
- Ensure compatibility with Pydantic v1 (T19/T20 awareness).

## Dependencies
- T04.

## Effort
- S: ~1h.
