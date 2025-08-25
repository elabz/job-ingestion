# T15: Pre-commit in CI and local

- [ ] Task complete

## Summary
Ensure `pre-commit` installed and `pre-commit run --all-files` clean.

## Implementation details
- `.pre-commit-config.yaml` includes required hooks.
- Add installation note and `pre-commit install` in onboarding.
- Optional: pre-commit.ci config later.

## Checklist
- [ ] Hooks present and versions pinned.
- [ ] Local run passes on a clean checkout.

## Acceptance criteria
- [ ] `pre-commit run --all-files` returns 0.

## Verification
```bash
conda run -n job-ingestion-service pre-commit run --all-files
```

## Docs
- CONTRIBUTING update.

## Risks/Notes
- Keep hook versions aligned with `environment.yml`.

## Dependencies
- T02.

## Effort
- S: ~0.5h.
