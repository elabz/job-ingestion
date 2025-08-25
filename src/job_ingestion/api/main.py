from collections.abc import Callable
from typing import Any, TypeVar

from fastapi import FastAPI

from job_ingestion.api.routes import api_router

app = FastAPI(title="Job Ingestion Service API", version="0.1.0")

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
