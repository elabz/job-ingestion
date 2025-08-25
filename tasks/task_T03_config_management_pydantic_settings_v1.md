# T03: Configuration management via Pydantic Settings (v1)

- [ ] Task complete

## Summary
Centralize env config with `.env` support using `pydantic.BaseSettings` (Pydantic v1).

## Implementation details
- File `src/job_ingestion/utils/config.py`:
  - `class Settings(BaseSettings)` with fields: `DATABASE_URL: AnyUrl | str`, `REDIS_URL: AnyUrl | str`, `ENVIRONMENT: Literal["local","dev","prod"] = "local"`.
  - `Config` inner class: `env_file = ".env"`, `case_sensitive = True`.
  - Provide `get_settings()` singleton with `lru_cache()`.
- `.env.example`: include keys with placeholder values and comments.
- Ensure imports: `from pydantic import BaseSettings` (v1) not pydantic-settings.

## Checklist
- [ ] Implement `Settings` with correct types and defaults.
- [ ] Add `.env.example` with variables and guidance.
- [ ] Add `get_settings()` cached accessor.
- [ ] Unit tests for default and override behaviors.

## Acceptance criteria
- [ ] Importing `get_settings()` returns a `Settings` instance and reads `.env` if present.
- [ ] `tests/unit/test_settings.py` passes.

## Verification
```bash
conda run -n job-ingestion-service pytest -q tests/unit/test_settings.py
```

## Docs
- `README.md`: env var table and examples.

## Risks/Notes
- Pydantic v1 syntax only; Pydantic v2 migration in T20.

## Dependencies
- None (but coordinate with T19 for versions).

## Effort
- S: ~1h.
