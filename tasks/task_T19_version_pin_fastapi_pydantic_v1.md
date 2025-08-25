# T19: Version pinning and compatibility

- [ ] Task complete

## Summary
Pin FastAPI/Pydantic versions compatible with current code (Pydantic v1). Add a follow-up task to migrate to Pydantic v2.

## Implementation details
- `environment.yml` and/or `pyproject.toml` pins:
  - fastapi ~= 0.111
  - pydantic ~= 1.10
  - starlette compatible with fastapi pin
- `pip check` clean in Conda env.

## Checklist
- [ ] Update pins and lock if applicable.
- [ ] Imports succeed and app runs.

## Acceptance criteria
- [ ] All existing tests pass under pinned versions.

## Verification
```bash
conda run -n job-ingestion-service python -c "import fastapi, pydantic; print(fastapi.__version__, pydantic.__version__)"
conda run -n job-ingestion-service pytest -q
```

## Docs
- Note in README about v1 vs v2.

## Risks/Notes
- Track transitive deps (typing-extensions, annotated-types).

## Dependencies
- None (but before T20).

## Effort
- S: ~0.5h.
