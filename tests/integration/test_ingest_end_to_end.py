from __future__ import annotations

import os
from typing import Any

from job_ingestion.storage.models import ApprovalStatus, Base, Job
from job_ingestion.storage.repositories import get_engine, get_session, get_sessionmaker
from job_ingestion.utils.config import get_settings
from sqlalchemy import select


def test_ingest_persists_jobs_and_statuses(client: Any) -> None:
    # Point service to a test database and reset cached settings
    os.environ["DATABASE_URL"] = "sqlite:///./db_integration_e2e.sqlite3"
    get_settings.cache_clear()

    payload = {
        "jobs": [
            {
                "title": "OK",
                "description": "Approved job description long enough",
                "location": "NYC, USA",
                "min_salary": 50000,
            },
            {
                "title": "Too Low",
                "description": "This will be rejected due to low salary threshold",
                "location": "Remote",
                "min_salary": 20000,
            },
        ]
    }

    resp = client.post("/api/v1/jobs/ingest", json=payload)
    assert resp.status_code == 202

    # Open a session to the same DB and verify rows
    engine = get_engine(os.environ["DATABASE_URL"])
    Base.metadata.create_all(bind=engine)
    sm = get_sessionmaker(engine)
    with get_session(sm) as s:
        rows = s.execute(select(Job)).scalars().all()
        # Expect exactly two jobs inserted
        assert len(rows) >= 2  # allow other tests to have inserted rows as well
        # Find our titles
        by_title = {j.title: j for j in rows}
        assert by_title["OK"].approval_status == ApprovalStatus.APPROVED
        assert by_title["Too Low"].approval_status == ApprovalStatus.REJECTED
