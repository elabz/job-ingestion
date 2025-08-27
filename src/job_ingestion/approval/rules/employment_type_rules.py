from __future__ import annotations

from typing import Any

from .base import ApprovalRule

# Accepted employment types for approval
ACCEPTED_EMPLOYMENT_TYPES = {"Full-Time", "full-time", "FULL-TIME", "Full Time", "full time"}


def is_full_time_position(job: dict[str, Any]) -> tuple[bool, str | None]:
    """
    Approve if the job is a full-time position.

    A job is expected to provide an "employment_type" field that indicates
    it's a full-time position (case-insensitive variations accepted).

    Examples:
        >>> ok, reason = is_full_time_position({"employment_type": "Full-Time"})
        >>> ok, reason
        (True, None)
        >>> ok, reason = is_full_time_position({"employment_type": "Internship"})
        >>> ok, reason
        (False, 'Job must be a full-time position, got: Internship')
        >>> ok, reason = is_full_time_position({})
        >>> ok, reason
        (False, 'Job must be a full-time position, got: None')
    """
    employment_type = job.get("employment_type")

    if employment_type is None:
        return False, "Job must be a full-time position, got: None"

    # Convert to string and check against accepted variants
    employment_type_str = str(employment_type).strip()

    if employment_type_str in ACCEPTED_EMPLOYMENT_TYPES:
        return True, None

    return False, f"Job must be a full-time position, got: {employment_type_str}"


def get_rules() -> list[ApprovalRule]:
    """Return a list of employment type related approval rules.

    The returned callables conform to the `ApprovalRule` protocol.
    """
    return [is_full_time_position]
