from __future__ import annotations

from typing import Any

from .base import ApprovalRule

# Simple configuration knobs for later tuning
REQUIRE_LOCATION: bool = True


def has_location_info(job: dict[str, Any]) -> tuple[bool, str | None]:
    """
    Approve if job contains sufficient location information.

    Current criteria (stub):
    - Non-empty string field "location", OR
    - Boolean flag "is_remote" set to True.

    Examples:
        >>> has_location_info({"location": "NYC, USA"})
        (True, None)
        >>> has_location_info({"is_remote": True})
        (True, None)
        >>> has_location_info({})
        (False, 'Missing location information')
    """
    if not REQUIRE_LOCATION:
        return True, None

    location = job.get("location")
    is_remote = bool(job.get("is_remote", False))

    ok = (isinstance(location, str) and location.strip() != "") or is_remote
    return (ok, None) if ok else (False, "Missing location information")


def get_rules() -> list[ApprovalRule]:
    """Return a list of location-related approval rules (stubs)."""
    return [has_location_info]
