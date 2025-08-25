# T05 (supporting): Unit test for models metadata

- [x] Task complete

## Summary
Add `tests/unit/storage/test_models.py` ensuring tables can be created in-memory and constraints exist.

## Implementation details
- Use SQLite `sqlite+pysqlite:///:memory:` and `Base.metadata.create_all`.
- Assert unique constraint on `external_id` by attempting insert duplicates.

## Checklist
- [x] Add test file and scenarios.

## Acceptance criteria
- [x] Tests pass and validate model shape.

## Verification
```bash
conda run -n job-ingestion-service pytest -q tests/unit/storage/test_models.py
```

## Dependencies
- T05.

## Effort
- S: ~0.5h.
