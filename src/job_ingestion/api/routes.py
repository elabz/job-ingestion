from collections.abc import Callable
from typing import Any, TypeVar
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException

from job_ingestion.api.models import (
    IngestBatchRequest,
    IngestResponse,
    JobPosting,
    PingResponse,
    SingleJobPostingRequest,
)
from job_ingestion.ingestion.service import IngestionService

api_router = APIRouter(prefix="/api/v1")

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
def ingest(payload: IngestBatchRequest | SingleJobPostingRequest) -> IngestResponse:
    """Accept a single job or a batch and return a processing id.

    The service layer is not implemented yet; we gracefully fall back to a
    generated UUID when ingest_batch raises NotImplementedError.
    """

    try:
        if isinstance(payload, IngestBatchRequest):
            jobs: list[dict[str, Any]] = payload.jobs
        else:
            # Single payload -> normalize to a one-item list
            jobs = [payload.dict()]

        service = IngestionService()
        try:
            batch_id = service.ingest_batch(jobs)
            # Best effort to coerce into UUID; fallback to new UUID if invalid
            processing_id: UUID
            try:
                processing_id = UUID(str(batch_id))
            except Exception:
                processing_id = uuid4()
        except NotImplementedError:
            processing_id = uuid4()

        return IngestResponse(
            processing_id=processing_id,
            message="Batch accepted for processing",
            estimated_completion=None,
        )
    except Exception as exc:  # pragma: no cover - generic safety net
        raise HTTPException(status_code=500, detail="Internal Server Error") from exc
