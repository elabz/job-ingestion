# T07: Schema detector (stub)

- [x] Task complete

## Summary
Add JSON schema detection module with simple heuristic placeholder.

## Implementation details
- `src/job_ingestion/ingestion/schema_detector.py` with function
  - `def detect_schema(jobs_data: Sequence[dict]) -> Literal["unknown","schema_a","schema_b"]:`
  - Heuristic: presence of key sets (e.g., if `company_name` -> schema_a, if `employer` -> schema_b, else unknown).
- Keep logic simple and typed.

## Checklist
- [x] Implement function with deterministic mapping.
- [x] Unit tests cover key presence branches.

## Acceptance criteria
- [x] Returns expected literal values given fixtures.

## Verification
```bash
conda run -n job-ingestion-service env PYTHONPATH=src python -m pytest -q tests/unit/ingestion/test_schema_detector.py
```

## Docs
- Inline docstrings.

## Risks/Notes
- This is a placeholder; real detection later.

## Dependencies
- None.

## Effort
- S: ~1h.
