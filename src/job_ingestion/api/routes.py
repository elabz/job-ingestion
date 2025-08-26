from collections.abc import Callable
from typing import Any, TypeVar

from fastapi import APIRouter

from job_ingestion.api.models import JobPosting, PingResponse

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
