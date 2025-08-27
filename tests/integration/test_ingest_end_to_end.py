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
                "title": "Senior Python Developer",
                "description": "We are looking for a Senior Python Developer to join our team. "
                "This is a full-time position requiring Python expertise.",
                "location": "New York, NY, USA",
                "min_salary": 120000,
                "employment_type": "Full-Time",
                "language": "English",
            },
            {
                "title": "Junior Data Analyst",
                "description": "Entry level data analyst position with competitive salary and "
                "benefits package.",
                "location": "San Francisco, CA, USA",
                "min_salary": 105000,
                "employment_type": "Full-Time",
                "language": "English",
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
        assert by_title["Senior Python Developer"].approval_status == ApprovalStatus.APPROVED
        assert by_title["Junior Data Analyst"].approval_status == ApprovalStatus.APPROVED
