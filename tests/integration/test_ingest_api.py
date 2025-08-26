from typing import Any
from uuid import UUID


def test_ingest_single_returns_202_and_processing_id(client: Any) -> None:
    payload = {
        "title": "Data Engineer",
        "description": "Build pipelines",
        "employment_type": "full-time",
        "hiring_organization": {"name": "Acme Inc"},
        "date_posted": "2024-01-01T00:00:00Z",
    }
    resp = client.post("/api/v1/jobs/ingest", json=payload)
    assert resp.status_code == 202
    body = resp.json()
    assert "processing_id" in body and isinstance(body["processing_id"], str)
    # Validate UUID format
    UUID(body["processing_id"])  # will raise if invalid
    assert body.get("message")


def test_ingest_batch_returns_202_and_processing_id(client: Any) -> None:
    payload = {
        "jobs": [
            {
                "title": "Data Engineer",
                "description": "Build pipelines",
                "employment_type": "full-time",
                "hiring_organization": {"name": "Acme Inc"},
                "date_posted": "2024-01-01T00:00:00Z",
            }
        ]
    }
    resp = client.post("/api/v1/jobs/ingest", json=payload)
    assert resp.status_code == 202
    body = resp.json()
    assert "processing_id" in body and isinstance(body["processing_id"], str)
    UUID(body["processing_id"])  # format check
    assert body.get("message")
