# T02: Project configuration and tooling

- [ ] Task complete

## Summary
Configure Black, Ruff, MyPy (strict), pytest, and pre-commit hooks.

## Implementation details
- `pyproject.toml`: sections for `tool.black`, `tool.ruff`, `tool.mypy`, `tool.pytest.ini_options`.
- `.pre-commit-config.yaml`: hooks for Black, Ruff (lint+format optional), MyPy, end-of-file-fixer, trailing-whitespace.
- `Makefile`: targets `format`, `lint`, `type-check`, `test`, `quality-check` using Conda env with `conda run -n job-ingestion-service ...`.
- Ensure `environment.yml` contains tooling.

## Checklist
- [ ] Black config with line-length 100 and py310.
- [ ] Ruff select rule sets (e.g., E,F,I,UP,B). Exclude `tests/fixtures/*` as needed.
- [ ] MyPy strict: `warn-redundant-casts`, `warn-unused-ignores`, `disallow-any-generics`, etc.
- [ ] pytest config: `testpaths=["tests"]`, `addopts=-q`.
- [ ] Pre-commit hooks wired and passing.

## Acceptance criteria
- [ ] `make quality-check` succeeds.
- [ ] `pre-commit run --all-files` passes.

## Verification
```bash
conda run -n job-ingestion-service pre-commit install
conda run -n job-ingestion-service pre-commit run --all-files
conda run -n job-ingestion-service make quality-check
```

## Docs
- `CONTRIBUTING.md`: document quality workflow and commands.

## Risks/Notes
- MyPy strict may require adding precise types and `typing_extensions`.

## Dependencies
- None.

## Effort
- S: ~1–2h.
