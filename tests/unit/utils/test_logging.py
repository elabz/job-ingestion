from __future__ import annotations

from job_ingestion.utils.logging import get_logger


def test_get_logger_returns_object_with_info() -> None:
    logger = get_logger("tests.utils.logging")
    assert hasattr(logger, "info") and callable(logger.info)

    # Calling .info should not raise
    logger.info("test_event", test_key=123)
