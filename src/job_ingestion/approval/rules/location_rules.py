from __future__ import annotations

from typing import Any

from .base import ApprovalRule

# Simple configuration knobs for later tuning
REQUIRE_LOCATION: bool = True
ALLOWED_COUNTRIES = {"USA", "US", "United States", "Canada", "CA"}
ALLOWED_COUNTRY_CODES = {"US", "USA", "CA", "CAN"}


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


def _extract_country_from_location(location: Any) -> str | None:
    """
    Extract country information from location data.

    Args:
        location: Can be a dict with country field or a string to parse

    Returns:
        Country string if found, None otherwise
    """
    if isinstance(location, dict):
        return location.get("country")

    if isinstance(location, str):
        # Parse string location formats like "New York, NY, USA" or "Toronto, ON, Canada"
        parts = [part.strip() for part in location.split(",")]
        if len(parts) >= 3:
            return parts[-1]  # Last part is usually the country
        elif len(parts) == 2:
            # Check if second part looks like a country
            second_part = parts[-1].upper()
            if second_part in ALLOWED_COUNTRY_CODES or second_part in ALLOWED_COUNTRIES:
                return parts[-1]

    return None


def is_geographical_location_approved(job: dict[str, Any]) -> tuple[bool, str | None]:
    """
    Approve if job is either remote or located in US/Canada.

    Rule: Job must be either remote (anywhere) or in-person located within
    the United States or Canada.

    Args:
        job: Job data dictionary

    Returns:
        Tuple of (is_approved, rejection_reason)

    Examples:
        >>> is_geographical_location_approved({"remote": True, "location": "London, UK"})
        (True, None)
        >>> is_geographical_location_approved({"location": {"country": "USA"}, "remote": False})
        (True, None)
        >>> is_geographical_location_approved({"location": "Paris, France", "remote": False})
        (False, 'Job location must be in US/Canada or remote')
    """
    # Check if job is remote - if so, approve regardless of location
    is_remote = job.get("remote", False) or job.get("is_remote", False)
    if is_remote:
        return True, None

    # Extract location information
    location = job.get("location")
    if not location:
        return False, "Missing location information"

    # Extract country from location data
    country = _extract_country_from_location(location)
    if not country:
        return False, "Unable to determine country from location"

    # Normalize country for comparison
    country_normalized = country.strip().upper()

    # Check if country is in allowed list
    allowed_normalized = {c.upper() for c in ALLOWED_COUNTRIES} | {
        c.upper() for c in ALLOWED_COUNTRY_CODES
    }

    if country_normalized in allowed_normalized:
        return True, None

    return False, "Job location must be in US/Canada or remote"


def get_rules() -> list[ApprovalRule]:
    """Return a list of location-related approval rules."""
    return [has_location_info, is_geographical_location_approved]
