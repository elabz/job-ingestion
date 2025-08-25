from typing import Any

import pytest
from job_ingestion.storage.models import ApprovalStatus, Base, Job
from job_ingestion.storage.repositories import get_engine, get_session, get_sessionmaker
from sqlalchemy import inspect, select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker


@pytest.fixture()  # type: ignore[misc]
def engine() -> Engine:
    eng = get_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(bind=eng)
    return eng


@pytest.fixture()  # type: ignore[misc]
def session_maker(engine: Engine) -> sessionmaker:
    return get_sessionmaker(engine)


def test_create_all_and_reflection(engine: Any) -> None:
    insp = inspect(engine)

    # Table exists
    assert "jobs" in insp.get_table_names()

    # Columns present
    cols = insp.get_columns("jobs")
    col_names = {c["name"] for c in cols}
    assert {"id", "external_id", "title", "approval_status", "created_at"}.issubset(col_names)

    # Primary key
    pk_cols: list[str] = insp.get_pk_constraint("jobs").get("constrained_columns", [])
    assert pk_cols == ["id"]

    # Unique constraint or index on external_id
    # Some dialects (e.g., SQLite) may reflect a unique index instead of a
    # table-level UNIQUE constraint
    uniques = insp.get_unique_constraints("jobs")
    has_unique_constraint = any("external_id" in (u.get("column_names") or []) for u in uniques)
    if not has_unique_constraint:
        indexes = insp.get_indexes("jobs")
        has_unique_index = any(
            idx.get("unique") and ["external_id"] == (idx.get("column_names") or [])
            for idx in indexes
        )
        assert has_unique_index, "external_id should be uniquely constrained/indexed"
    else:
        assert has_unique_constraint


def test_unique_constraint_enforced(session_maker: Any) -> None:
    with get_session(session_maker) as s:
        s.add(Job(external_id="ext-1", title="Title 1", approval_status=ApprovalStatus.PENDING))

    with pytest.raises(IntegrityError):
        with get_session(session_maker) as s:
            s.add(
                Job(external_id="ext-1", title="Duplicate", approval_status=ApprovalStatus.PENDING)
            )
            # commit happens on context exit, which should raise


def test_session_commit_and_rollback(session_maker: Any) -> None:
    # Commit path
    with get_session(session_maker) as s:
        s.add(Job(external_id="ok-1", title="OK 1", approval_status=ApprovalStatus.APPROVED))

    # Verify committed
    with get_session(session_maker) as s:
        count1 = s.execute(select(Job)).all()
        assert len(count1) == 1

    # Rollback path
    with pytest.raises(RuntimeError):
        with get_session(session_maker) as s:
            s.add(
                Job(
                    external_id="will-rollback", title="RB", approval_status=ApprovalStatus.REJECTED
                )
            )
            raise RuntimeError("force error")

    # Verify rolled back (still 1 row)
    with get_session(session_maker) as s:
        count2 = s.execute(select(Job)).all()
        assert len(count2) == 1
