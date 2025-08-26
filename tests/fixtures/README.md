# Test fixtures: sample_jobs.json

This folder contains small, realistic sample job payloads used by tests and local experiments.

File: `sample_jobs.json`
- Purpose: provide varied inputs for ingestion to exercise schema detection and approval rules.
- Size: a handful of entries to avoid repo bloat.

Coverage highlights:
- Schema detection (`src/job_ingestion/ingestion/schema_detector.py`):
  - Records containing `company_name` are treated as "schema_a" candidates.
  - Records containing `employer` are treated as "schema_b" candidates.
  - Records without either reflect the "unknown" path.
- Approval rules (`src/job_ingestion/approval/rules/`):
  - Content: requires non-empty `title` and a `description` length >= 20 chars.
  - Location: requires non-empty `location` (after normalization) or `is_remote=true`.
  - Salary: requires `min_salary` >= 30000, or parsed from a text field like `salary`, `salary_text`, or `compensation` via the `SalaryNormalizer`.

Notes:
- Values are anonymized but realistic.
- Use these fixtures in integration or e2e tests; unit tests can inline smaller dicts.
- If editing this file, keep it valid JSON and small.

Validation:
- You can validate with jq:

```bash
jq . tests/fixtures/sample_jobs.json
```
