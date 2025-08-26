import os
from uuid import UUID

import pytest
from job_ingestion.ingestion.service import IngestionService
from job_ingestion.utils.config import get_settings


def test_ingest_batch_returns_processing_id_and_status() -> None:
    # Use a file-based sqlite DB so we can verify persistence in other tests if needed
    os.environ["DATABASE_URL"] = "sqlite:///./db_unit_signatures.sqlite3"
    get_settings.cache_clear()  # ensure settings reflect env

    service = IngestionService()
    pid = service.ingest_batch([{"title": "X", "description": "d" * 25, "location": "NY"}])
    # processing id is UUID-like
    UUID(str(pid))
    status = service.get_processing_status(str(pid))
    assert status.get("total") == 1
    assert status.get("processed") == 1


def test_register_source_schema_raises_not_implemented() -> None:
    service = IngestionService()
    with pytest.raises(NotImplementedError):
        service.register_source_schema("source-x", {})
