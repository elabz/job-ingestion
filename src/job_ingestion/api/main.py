from collections.abc import Callable
from typing import Any, TypeVar

from fastapi import FastAPI

from job_ingestion.api.routes import api_router
from job_ingestion.utils.logging import get_logger

app = FastAPI(title="Job Ingestion Service API", version="0.1.0")
logger = get_logger("api.main")

__all__ = ["app"]


app.include_router(api_router)


F = TypeVar("F", bound=Callable[..., Any])


def route_get(path: str) -> Callable[[F], F]:
    """Typed decorator that registers a GET route and preserves function type.

    This avoids MyPy's "untyped decorator" error by returning the original
    function unchanged while ensuring FastAPI registers the route.
    """

    def decorator(func: F) -> F:
        app.get(path)(func)
        return func

    return decorator


@route_get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def on_startup() -> None:
    # Minimal startup log to verify logging is configured
    logger.info("app.startup")


# Register startup event handler without using untyped decorator
app.add_event_handler("startup", on_startup)
