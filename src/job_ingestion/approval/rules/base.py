from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ApprovalRule(Protocol):
    """
    Protocol for approval rules used by the ApprovalEngine.

    A rule is any callable that accepts a job dict and returns a tuple of:
    - bool indicating approval
    - optional string reason if not approved

    Example:
        >>> def has_title(job: dict[str, Any]) -> tuple[bool, Optional[str]]:
        ...     ok = bool(job.get("title"))
        ...     return ok, None if ok else "Missing title"
    """

    def __call__(
        self, job: dict[str, Any]
    ) -> tuple[bool, str | None]:  # pragma: no cover - signature only
        ...


__all__ = ["ApprovalRule"]
