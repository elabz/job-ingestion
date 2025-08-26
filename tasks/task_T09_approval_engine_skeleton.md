# T09: Approval engine skeleton

- [x] Task complete

## Summary
Implement `ApprovalEngine` class with rule registry and `evaluate_job()` stub returning `ApprovalDecision` dataclass.

## Implementation details
- `src/job_ingestion/approval/engine.py`:
  - `@dataclass` `ApprovalDecision { approved: bool, reasons: list[str] }`.
  - `class ApprovalEngine:` with `register_rule(callable)`, `evaluate_job(job: dict) -> ApprovalDecision`.
- `src/job_ingestion/approval/rules/base.py`:
  - Protocol/ABC for rules: `def __call__(self, job: dict) -> tuple[bool, str|None]`.

## Checklist
- [x] Implement dataclass and engine with registry list.
- [x] Support both callables and objects implementing the protocol.
- [x] Unit tests covering registration and evaluation aggregation.

## Acceptance criteria
- [x] Able to register a rule and evaluate a job to produce decision with reasons.

## Verification
```bash
conda run -n job-ingestion-service pytest -q tests/unit/approval/test_engine.py
```

## Docs
- Inline docstrings and quick usage example.

## Risks/Notes
- Keep API stable for T10 rule modules.

## Dependencies
- None.

## Effort
- M: ~2h.
