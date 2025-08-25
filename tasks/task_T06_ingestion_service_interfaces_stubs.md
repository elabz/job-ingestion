# T06: Ingestion service interfaces (stubs)

- [ ] Task complete

## Summary
Define `IngestionService` signatures from PRD and no-op implementation.

## Implementation details
- `src/job_ingestion/ingestion/service.py`:
  - `class IngestionService:` with methods
    - `ingest_batch(self, jobs_data: Sequence[dict]) -> str` (returns batch_id)
    - `get_processing_status(self, batch_id: str) -> dict`
    - `register_source_schema(self, name: str, schema: dict) -> None`
  - Methods raise `NotImplementedError` or provide minimal pass-through impl.
- Include docstrings describing expected behavior.

## Checklist
- [ ] Create module and class with signatures.
- [ ] Add TODOs for implementations.
- [ ] Minimal unit tests check default behavior/raises.

## Acceptance criteria
- [ ] Module imports without runtime errors.

## Verification
```bash
conda run -n job-ingestion-service pytest -q tests/unit/ingestion/test_service_signatures.py
```

## Docs
- Inline docstrings.

## Risks/Notes
- Keep public API stable for later tasks.

## Dependencies
- None.

## Effort
- S: ~1h.
