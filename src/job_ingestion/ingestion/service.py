from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from typing import Any
from uuid import uuid4

from job_ingestion.approval.engine import ApprovalEngine
from job_ingestion.approval.rules.content_rules import get_rules as content_rules
from job_ingestion.approval.rules.location_rules import get_rules as location_rules
from job_ingestion.approval.rules.salary_rules import get_rules as salary_rules
from job_ingestion.ingestion import schema_detector
from job_ingestion.ingestion.job_mapper import JobDataMapper
from job_ingestion.storage.models import ApprovalStatus, Base, Job, RejectedJob
from job_ingestion.storage.repositories import get_engine, get_session, get_sessionmaker
from job_ingestion.transformation.normalizers import LocationNormalizer, SalaryNormalizer
from job_ingestion.utils import metrics
from job_ingestion.utils.config import get_settings
from job_ingestion.utils.logging import get_logger

logger = get_logger("ingestion.service")


class IngestionService:
    """
    Public interface and implementation for the ingestion service.

    Orchestrates:
    - Schema detection
    - Field normalization
    - Approval rule evaluation
    - Persistence
    - In-memory processing status tracking
    """

    # Lightweight in-memory status store; to be moved to Redis/DB in later tasks
    _batches: dict[str, dict[str, Any]] = {}

    def ingest_batch(self, jobs_data: Sequence[dict[str, Any]]) -> str:
        """
        Submit a batch of job records for ingestion.

        Args:
            jobs_data: A sequence of dictionaries representing raw job data
                from an external source.

        Returns:
            processing_id (str): Identifier for the processed batch.
        """

        processing_id = str(uuid4())
        started_at = datetime.utcnow()

        # Initialize status tracking
        self._batches[processing_id] = {
            "total": len(jobs_data),
            "processed": 0,
            "approved": 0,
            "rejected": 0,
            "errors": 0,
            "started_at": started_at,
            "finished_at": None,
        }

        logger.info("ingest.batch_started", processing_id=processing_id, total=len(jobs_data))
        metrics.increment("ingest.batch_started")

        # Detect schema (heuristic placeholder)
        try:
            schema_name = schema_detector.detect_schema(jobs_data)
        except Exception:  # pragma: no cover - defensive
            logger.exception("schema detection failed; defaulting to 'unknown'")
            schema_name = "unknown"

        # Build dependencies
        settings = get_settings()
        engine = get_engine(settings.database_url)
        # Ensure tables exist (dev/test convenience)
        Base.metadata.create_all(bind=engine)
        session_maker = get_sessionmaker(engine)

        rules = [*content_rules(), *location_rules(), *salary_rules()]
        approval_engine = ApprovalEngine(rules=rules)

        job_mapper = JobDataMapper()

        status = self._batches[processing_id]

        for idx, raw in enumerate(jobs_data):
            try:
                # Map all job data to database fields
                mapped_data = job_mapper.map_job_data(raw)

                # Create canonical job for approval engine (backward compatibility)
                canonical_job: dict[str, Any] = {
                    "title": mapped_data.get("title", "(untitled)"),
                    "description": mapped_data.get("short_description")
                    or mapped_data.get("full_description", ""),
                    "min_salary": mapped_data.get("salary_min"),
                    "location": mapped_data.get("primary_location"),
                    "external_id": mapped_data.get("external_id"),
                    "_schema": schema_name,
                }

                decision = approval_engine.evaluate_job(canonical_job)

                # Persist with comprehensive fields
                with get_session(session_maker) as s:
                    if decision.approved:
                        # Create approved job with all mapped fields
                        job = Job(approval_status=ApprovalStatus.APPROVED, **mapped_data)
                        s.add(job)
                        status["approved"] += 1
                        metrics.increment("ingest.item_approved")
                    else:
                        # Create rejected job with rejection reasons
                        rejection_reasons = (
                            "; ".join(decision.reasons)
                            if decision.reasons
                            else "Failed approval rules"
                        )
                        rejected_job = RejectedJob(
                            rejection_reasons=rejection_reasons, **mapped_data
                        )
                        s.add(rejected_job)
                        status["rejected"] += 1
                        metrics.increment("ingest.item_rejected")

                # Update counters
                status["processed"] += 1

                logger.info(
                    "ingest.item",
                    processing_id=processing_id,
                    index=idx,
                    external_id=mapped_data.get("external_id"),
                    approved=decision.approved,
                    reasons=decision.reasons,
                )
            except Exception as exc:  # keep processing on errors
                status["errors"] += 1
                metrics.increment("ingest.item_error")
                logger.exception(
                    "ingest.item_error", processing_id=processing_id, index=idx, error=str(exc)
                )

        status["finished_at"] = datetime.utcnow()
        metrics.increment("ingest.batch_finished")
        logger.info(
            "ingest.batch_finished",
            processing_id=processing_id,
            processed=status["processed"],
            approved=status["approved"],
            rejected=status["rejected"],
            errors=status["errors"],
        )

        return processing_id

    def get_processing_status(self, batch_id: str) -> dict[str, Any]:
        """
        Retrieve processing status for a previously submitted batch.

        Returns a dict with counts and timestamps, or an empty dict if unknown.
        """
        return dict(self._batches.get(batch_id, {}))

    # --- Helpers ---
    @staticmethod
    def _get_title(raw: dict[str, Any]) -> str:
        title = raw.get("title") or raw.get("job_title") or raw.get("position")
        if isinstance(title, str) and title.strip():
            return title
        return "(untitled)"

    @staticmethod
    def _get_description(raw: dict[str, Any]) -> str:
        desc = raw.get("description") or raw.get("details") or raw.get("summary")
        return desc if isinstance(desc, str) else ""

    @staticmethod
    def _get_external_id(raw: dict[str, Any], processing_id: str, idx: int) -> str:
        ext = raw.get("external_id") or raw.get("id")
        if isinstance(ext, str | int):
            return str(ext)
        # Fallback to a generated ID that is unique within the batch
        return f"proc-{processing_id}-{idx + 1}"

    @staticmethod
    def _extract_location(raw: dict[str, Any], loc_norm: LocationNormalizer) -> str | None:
        loc = raw.get("location") or raw.get("city") or raw.get("region")
        if isinstance(loc, str):
            return loc_norm.normalize(loc)
        return None

    @staticmethod
    def _extract_min_salary(raw: dict[str, Any], sal_norm: SalaryNormalizer) -> int | None:
        # Look for common fields; prefer explicit numeric min
        if "min_salary" in raw and isinstance(raw["min_salary"], int | float):
            return int(raw["min_salary"])
        salary_text = raw.get("salary") or raw.get("salary_text") or raw.get("compensation")
        if isinstance(salary_text, str):
            low, _ = sal_norm.parse_range(salary_text)
            return low
        return None

    # Placeholder for future schema registration API
    def register_source_schema(self, name: str, schema: dict[str, Any]) -> None:  # pragma: no cover
        raise NotImplementedError("register_source_schema is not yet implemented")
