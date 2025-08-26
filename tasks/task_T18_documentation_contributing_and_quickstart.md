# T18: Documentation — CONTRIBUTING and Quickstart

- [x] Task complete

## Summary
Write `CONTRIBUTING.md` (Conda, quality checks, test strategy) and expand `README.md`.

## Implementation details
- CONTRIBUTING: environment setup, pre-commit, make targets, coding standards, PR checklist.
- README: Quickstart, run commands, directory structure, version notes (Pydantic v1).

## Checklist
- [x] Add sections and verify correctness.

## Acceptance criteria
- [x] Steps work end-to-end locally.

## Verification
```bash
conda run -n job-ingestion-service make quality-check
conda run -n job-ingestion-service pytest -q
```

## Risks/Notes
- Keep docs accurate as code evolves.

## Dependencies
- T01–T02.

## Effort
- S: ~1h.
