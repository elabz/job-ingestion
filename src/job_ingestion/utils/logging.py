from __future__ import annotations

import logging
import sys
from collections.abc import Callable, Mapping, MutableMapping
from typing import Any, Protocol, cast

import structlog

from job_ingestion.utils.config import get_settings


class LoggerProtocol(Protocol):
    def debug(self, event: str, *args: Any, **kwargs: Any) -> Any: ...

    def info(self, event: str, *args: Any, **kwargs: Any) -> Any: ...

    def warning(self, event: str, *args: Any, **kwargs: Any) -> Any: ...

    def error(self, event: str, *args: Any, **kwargs: Any) -> Any: ...

    def exception(self, event: str, *args: Any, **kwargs: Any) -> Any: ...

    def bind(self, **kwargs: Any) -> LoggerProtocol: ...


# Local alias compatible with structlog "Processor" call signature
Processor = Callable[
    [Any, str, MutableMapping[str, Any]],
    Mapping[str, Any] | str | bytes | bytearray | tuple[Any, ...],
]

_CONFIGURED = False


def configure_logging() -> None:
    """Configure structlog and standard logging once (idempotent).

    - Development: human-friendly console renderer
    - Production (ENVIRONMENT == "production"): JSON renderer
    """
    global _CONFIGURED
    if _CONFIGURED:
        return

    settings = get_settings()
    is_production = settings.environment.lower() == "production"

    # Basic stdlib logging to stdout
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(message)s",
    )

    shared_processors: list[Processor] = [
        cast(Processor, structlog.processors.TimeStamper(fmt="iso", key="timestamp")),
        cast(Processor, structlog.stdlib.add_log_level),
        cast(Processor, structlog.processors.StackInfoRenderer()),
        cast(Processor, structlog.processors.format_exc_info),
    ]

    if is_production:
        final_processor: Processor = cast(Processor, structlog.processors.JSONRenderer())
    else:
        final_processor = cast(Processor, structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            *shared_processors,
            final_processor,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    _CONFIGURED = True


def get_logger(name: str | None = None) -> LoggerProtocol:
    """Return a structlog logger; ensures logging is configured.

    Args:
        name: Optional logger name to bind as a field.
    """
    configure_logging()
    if name:
        return cast(LoggerProtocol, structlog.get_logger(name))
    return cast(LoggerProtocol, structlog.get_logger())


__all__ = ["get_logger", "configure_logging", "LoggerProtocol"]
