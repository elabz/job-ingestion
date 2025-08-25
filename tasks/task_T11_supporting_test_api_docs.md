# T11 (supporting): Integration test for OpenAPI docs

- [ ] Task complete

## Summary
Add `tests/integration/test_api_docs.py` checking OpenAPI contains components.

## Implementation details
- Implement test to fetch `/openapi.json` and assert presence of `components.schemas.JobPosting`.

## Checklist
- [ ] Add integration test file and assertions.

## Acceptance criteria
- [ ] Test passes when models are wired.

## Verification
```bash
conda run -n job-ingestion-service pytest -q tests/integration/test_api_docs.py
```

## Dependencies
- T11.

## Effort
- S: ~0.25h.
