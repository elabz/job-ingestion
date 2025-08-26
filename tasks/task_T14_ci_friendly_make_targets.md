# T14: CI-friendly Make targets

- [x] Task complete

## Summary
Complete Makefile with `format`, `lint`, `type-check`, `test`, `quality-check`, `run-dev` using Conda.

## Implementation details
- Use `conda run -n job-ingestion-service` prefix for all commands.
- `run-dev`: uvicorn run of FastAPI app.
- Ensure phony targets and helpful echo.

## Checklist
- [x] Implement Make targets and verify.
- [x] Works on macOS with Conda.

## Acceptance criteria
- [x] All targets run successfully locally.

## Verification
```bash
make format
make lint
make type-check
make test
make quality-check
make run-dev
```

## Docs
- Document in README and CONTRIBUTING.

## Risks/Notes
- Ensure Makefile portable for CI runner later.

## Dependencies
- T01, T02.

## Effort
- S: ~0.5h.
