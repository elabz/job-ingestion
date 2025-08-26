# T16: Sample fixtures and test data

- [x] Task complete

## Summary
Add sample job JSON fixtures to support tests.

## Implementation details
- Create `tests/fixtures/sample_jobs.json` with a few entries covering schema detection and rules cases.
- Keep values realistic but anonymized.

## Checklist
- [x] Add fixture file and ensure JSON valid.
- [x] Reference in future tests where applicable.

## Acceptance criteria
- [x] File parsable and used in at least one integration test later.

## Verification
```bash
jq . tests/fixtures/sample_jobs.json
```

## Docs
- Inline comments (if using `.jsonc` temporarily) or README note.

## Risks/Notes
- Keep size small to avoid repo bloat.

## Dependencies
- None.

## Effort
- S: ~0.5h.
