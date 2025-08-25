from __future__ import annotations

from collections.abc import Sequence
from typing import Any


class IngestionService:
    """
    Public interface for the ingestion service.

    This service is responsible for accepting job data payloads, tracking
    processing status for submitted batches, and registering source schemas
    that describe incoming data formats. Implementations will be provided in
    later tasks; this module defines the stable API surface.
    """

    def ingest_batch(self, jobs_data: Sequence[dict[str, Any]]) -> str:
        """
        Submit a batch of job records for ingestion.

        Args:
            jobs_data: A sequence of dictionaries representing raw job data
                from an external source. Each dict should conform to a
                registered source schema or a default schema.

        Returns:
            A string identifier for the created batch. This ID can be used to
            query processing status via `get_processing_status()`.

        Raises:
            NotImplementedError: This is a stub implementation.
        """
        # TODO(T06): Implement ingestion coordination and persistence logic.
        raise NotImplementedError("ingest_batch is not yet implemented")

    def get_processing_status(self, batch_id: str) -> dict[str, Any]:
        """
        Retrieve processing status for a previously submitted batch.

        Args:
            batch_id: The identifier returned from `ingest_batch()`.

        Returns:
            A dictionary describing the current processing status, e.g.,
            {"batch_id": str, "status": str, "processed": int, "total": int}.

        Raises:
            NotImplementedError: This is a stub implementation.
        """
        # TODO(T06): Implement status retrieval from storage/queue/worker layer.
        raise NotImplementedError("get_processing_status is not yet implemented")

    def register_source_schema(self, name: str, schema: dict[str, Any]) -> None:
        """
        Register or update a named source schema for incoming job data.

        Args:
            name: A unique name for the source schema (e.g., provider or feed).
            schema: A JSON-schema-like dictionary describing the expected
                structure of input job records for this source.

        Returns:
            None

        Raises:
            NotImplementedError: This is a stub implementation.
        """
        # TODO(T06): Persist schema and validate incoming payloads against it.
        raise NotImplementedError("register_source_schema is not yet implemented")
