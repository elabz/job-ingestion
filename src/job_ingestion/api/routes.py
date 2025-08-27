from collections.abc import Callable
from typing import Any, TypeVar
from uuid import UUID, uuid4

from fastapi import APIRouter, Body, HTTPException

from job_ingestion.api.models import (
    IngestBatchRequest,
    IngestResponse,
    JobPosting,
    PingResponse,
    ProcessingStatusResponse,
    SingleJobPostingRequest,
)
from job_ingestion.ingestion.service import IngestionService
from job_ingestion.utils.logging import get_logger

logger = get_logger("api.routes")

api_router = APIRouter(prefix="/api/v1")

# Module-level request body examples for Swagger (/docs)
INGEST_BODY_EXAMPLES: Any = {
    "single": {
        "summary": "Single job",
        "value": {
            "title": "Data Engineer",
            "description": "Build data pipelines",
            "location": "NYC, USA",
            "min_salary": 120000,
        },
    },
    "batch": {
        "summary": "Batch jobs",
        "value": {
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
        },
    },
}

# Module-level Body specification referencing examples (mypy-safe via Any)
INGEST_REQUEST_BODY: Any = Body(..., examples=INGEST_BODY_EXAMPLES)

F = TypeVar("F", bound=Callable[..., Any])


def route_get(path: str, *, response_model: type[Any] | None = None) -> Callable[[F], F]:
    """Typed decorator to register GET routes on api_router.

    Returns the original function to keep its type for MyPy strict mode.
    """

    def decorator(func: F) -> F:
        if response_model is None:
            api_router.get(path)(func)
        else:
            api_router.get(path, response_model=response_model)(func)
        return func

    return decorator


def route_post(
    path: str, *, response_model: type[Any] | None = None, status_code: int | None = None
) -> Callable[[F], F]:
    """Typed decorator to register POST routes on api_router."""

    def decorator(func: F) -> F:
        if response_model is None and status_code is None:
            api_router.post(path)(func)
        elif response_model is None and status_code is not None:
            api_router.post(path, status_code=status_code)(func)
        elif response_model is not None and status_code is None:
            api_router.post(path, response_model=response_model)(func)
        else:
            api_router.post(path, response_model=response_model, status_code=status_code)(func)
        return func

    return decorator


@route_get("/ping", response_model=PingResponse)
def ping() -> PingResponse:
    return PingResponse(message="pong")


@route_get("/jobposting/example", response_model=JobPosting)
def jobposting_example() -> JobPosting:
    """Return an example JobPosting to expose schema in OpenAPI."""
    return JobPosting(
        title="Senior Data Engineer",
        company="Acme Corp",
        location="San Francisco, CA",
        salary_min=140000,
        salary_max=180000,
        description="We are seeking a Senior Data Engineer to join our team...",
    )


@route_post(
    "/jobs/ingest",
    response_model=IngestResponse,
    status_code=202,
)
def ingest(
    payload: dict[str, Any] = INGEST_REQUEST_BODY,
) -> IngestResponse:
    """Accept a single job or a batch and return a processing id.

    The ingestion service orchestrates schema detection, normalization, approval
    evaluation, and persistence. A UUID `processing_id` is returned immediately
    upon acceptance.

    See /docs for request body examples (single and batch) included via the
    endpoint's requestBody examples.
    """

    try:
        # Manually discriminate between batch and single job based on presence of 'jobs' key
        if "jobs" in payload:
            # Batch request
            batch_payload = IngestBatchRequest(**payload)
            jobs: list[dict[str, Any]] = batch_payload.jobs
        else:
            # Single job request
            single_payload = SingleJobPostingRequest(**payload)
            jobs = [single_payload.dict()]

        logger.info("api.ingest_request", job_count=len(jobs))
        service = IngestionService()
        batch_id = service.ingest_batch(jobs)
        logger.info("api.ingest_completed", processing_id=batch_id)
        # Best effort to coerce into UUID; fallback to new UUID if invalid
        processing_id: UUID
        try:
            processing_id = UUID(str(batch_id))
        except Exception:
            processing_id = uuid4()

        return IngestResponse(
            processing_id=processing_id,
            message="Batch accepted for processing",
            estimated_completion=None,
        )
    except Exception as exc:  # pragma: no cover - generic safety net
        logger.exception("api.ingest_error", error=str(exc))
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc


@route_get("/jobs/status/{processing_id}", response_model=ProcessingStatusResponse)
def get_status(processing_id: UUID) -> ProcessingStatusResponse:
    """Return processing status snapshot for a batch processing id.

    Returns 404 if the processing id is unknown to the in-memory tracker.
    """

    service = IngestionService()
    status = service.get_processing_status(str(processing_id))
    if not status:
        raise HTTPException(status_code=404, detail="Processing id not found")

    return ProcessingStatusResponse(
        processing_id=processing_id,
        total=int(status.get("total", 0)),
        processed=int(status.get("processed", 0)),
        approved=int(status.get("approved", 0)),
        rejected=int(status.get("rejected", 0)),
        errors=int(status.get("errors", 0)),
        started_at=status.get("started_at"),
        finished_at=status.get("finished_at"),
    )
