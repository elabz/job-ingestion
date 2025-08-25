# T20: Follow-up — Migrate to Pydantic v2

- [ ] Task complete

## Summary
Replace `BaseSettings` with `pydantic-settings`, update models and FastAPI compatibility.

## Implementation details
- Swap imports to `from pydantic_settings import BaseSettings` and `from pydantic import BaseModel` (v2 semantics).
- Update settings and models for v2 (field validators, `model_config`, etc.).
- Validate FastAPI compatibility with pinned versions for v2.

## Checklist
- [ ] Update config settings module and `.env.example` if needed.
- [ ] Update API models to v2 syntax.
- [ ] Update tests to reflect behavior changes.
- [ ] Run MyPy and fix types.

## Acceptance criteria
- [ ] All tests pass under v2.

## Verification
```bash
conda run -n job-ingestion-service pytest -q
conda run -n job-ingestion-service mypy --strict src
```

## Docs
- README/CONTRIBUTING update for v2 notes.

## Risks/Notes
- Breaking changes in validation/serialization semantics between v1 and v2.

## Dependencies
- T19.

## Effort
- M: ~2–3h.
