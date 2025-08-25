import pytest
from job_ingestion.ingestion.service import IngestionService


def test_ingest_batch_raises_not_implemented() -> None:
    service = IngestionService()
    with pytest.raises(NotImplementedError):
        service.ingest_batch([{}])


def test_get_processing_status_raises_not_implemented() -> None:
    service = IngestionService()
    with pytest.raises(NotImplementedError):
        service.get_processing_status("batch-123")


def test_register_source_schema_raises_not_implemented() -> None:
    service = IngestionService()
    with pytest.raises(NotImplementedError):
        service.register_source_schema("source-x", {})
