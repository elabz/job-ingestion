# T05: Storage models and DB connection interface (stubs)

- [ ] Task complete

## Summary
Define SQLAlchemy models and session factory (no migrations yet).

## Implementation details
- Use SQLAlchemy 1.4/2.x style declarative base.
- `src/job_ingestion/storage/models.py`:
  - `Base = declarative_base()`
  - `class Job(Base)` with cols: `id (PK, int, autoincrement)`, `external_id (str, unique)`, `title (str)`, `approval_status (enum: PENDING/APPROVED/REJECTED)`, `created_at (datetime, server_default=func.now())`.
- `src/job_ingestion/storage/repositories.py`:
  - `get_engine(url)` and `get_sessionmaker(engine)`; convenience `get_session()` for contextmanager.
- Target dev DB: SQLite for now.

## Checklist
- [ ] Define `Job` model and metadata.
- [ ] Provide session utilities.
- [ ] Unit tests create in-memory SQLite and reflect tables.

## Acceptance criteria
- [ ] Importing and creating `Base.metadata.create_all(bind=engine)` works.
- [ ] Unique constraint on `external_id` present.

## Verification
```bash
conda run -n job-ingestion-service pytest -q tests/unit/storage/test_models.py
```

## Docs
- `README.md`: development DB notes.

## Risks/Notes
- Migrations intentionally deferred; Alembic later.

## Dependencies
- None, but aligns with T09/T10 requirements.

## Effort
- M: ~2–3h.
