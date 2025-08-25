from collections.abc import Callable
from typing import Any, TypeVar

from fastapi import APIRouter

api_router = APIRouter(prefix="/api/v1")

F = TypeVar("F", bound=Callable[..., Any])


def route_get(path: str) -> Callable[[F], F]:
    """Typed decorator to register GET routes on api_router.

    Returns the original function to keep its type for MyPy strict mode.
    """

    def decorator(func: F) -> F:
        api_router.get(path)(func)
        return func

    return decorator


@route_get("/ping")
def ping() -> dict[str, str]:
    return {"message": "pong"}
