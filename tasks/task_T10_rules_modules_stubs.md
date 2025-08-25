# T10: Rules modules (stubs)

- [ ] Task complete

## Summary
Implement placeholder `location_rules.py`, `salary_rules.py`, `content_rules.py` with simple pass/fail.

## Implementation details
- `src/job_ingestion/approval/rules/location_rules.py`
- `src/job_ingestion/approval/rules/salary_rules.py`
- `src/job_ingestion/approval/rules/content_rules.py`
- Each exposes a `get_rules()` returning a list of callables compatible with base rule protocol.
- Example: salary min threshold rule approving if min >= THRESHOLD.

## Checklist
- [ ] Implement three rule modules with at least one rule each.
- [ ] Unit tests in `tests/unit/approval/test_rules.py` covering pass/fail.

## Acceptance criteria
- [ ] Engine can load rules and evaluate decisions as expected.

## Verification
```bash
conda run -n job-ingestion-service pytest -q tests/unit/approval/test_rules.py
```

## Docs
- Docstrings for each rule with examples.

## Risks/Notes
- Keep thresholds and constants easy to configure for later tuning.

## Dependencies
- T09.

## Effort
- M: ~1–2h.
