from __future__ import annotations

from typing import Any

from .base import ApprovalRule

# Thresholds/constants kept simple for now; easy to tune later.
MIN_SALARY_THRESHOLD: int = 30_000


def min_salary_at_least_threshold(job: dict[str, Any]) -> tuple[bool, str | None]:
    """
    Approve if the job's minimum salary meets or exceeds MIN_SALARY_THRESHOLD.

    A job is expected to provide a numeric "min_salary" field.

    Examples:
        >>> ok, reason = min_salary_at_least_threshold({"min_salary": 50000})
        >>> ok, reason
        (True, None)
        >>> ok, reason = min_salary_at_least_threshold({"min_salary": 25000})
        >>> ok, reason
        (False, 'Min salary below 30000')
        >>> ok, reason = min_salary_at_least_threshold({})
        >>> ok, reason
        (False, 'Min salary below 30000')
    """
    raw = job.get("min_salary", 0)
    try:
        value = float(raw)
    except (TypeError, ValueError):
        value = 0.0

    ok = value >= float(MIN_SALARY_THRESHOLD)
    return (ok, None) if ok else (False, f"Min salary below {MIN_SALARY_THRESHOLD}")


def get_rules() -> list[ApprovalRule]:
    """Return a list of salary-related approval rules.

    The returned callables conform to the `ApprovalRule` protocol.
    """
    return [min_salary_at_least_threshold]
