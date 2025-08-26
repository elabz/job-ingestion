# T09 (supporting): Unit test for ApprovalEngine

- [x] Task complete

## Summary
Add `tests/unit/approval/test_engine.py` covering registry and decision aggregation.

## Implementation details
- Create dummy rules that return pass/fail and reasons.

## Checklist
- [x] Implement tests.

## Acceptance criteria
- [x] Engine aggregates reasons and boolean outcome.

## Verification
```bash
conda run -n job-ingestion-service pytest -q tests/unit/approval/test_engine.py
```

## Dependencies
- T09.

## Effort
- S: ~0.5h.
