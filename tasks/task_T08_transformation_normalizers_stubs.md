# T08: Transformation normalizers (stubs)

- [x] Task complete

## Summary
Create `LocationNormalizer`, `SalaryNormalizer`, `CompanyValidator` classes with method stubs.

## Implementation details
- `src/job_ingestion/transformation/normalizers.py`:
  - `class LocationNormalizer: def normalize(self, raw: str) -> str | None`
  - `class SalaryNormalizer: def parse_range(self, raw: str) -> tuple[int|None, int|None]`
  - `class CompanyValidator: def validate(self, raw: str) -> bool`
- Provide basic placeholder logic and type hints.

## Checklist
- [x] Implement classes and methods.
- [x] Unit tests for expected datatypes and basic behavior.

## Acceptance criteria
- [x] Functions return expected types and sentinel Nones where needed.

## Verification
```bash
conda run -n job-ingestion-service pytest -q tests/unit/transformation/test_normalizers.py
```

## Docs
- Docstrings describing assumptions.

## Risks/Notes
- Keep logic minimal; detailed rules in T10.

## Dependencies
- None.

## Effort
- S: ~1–2h.
