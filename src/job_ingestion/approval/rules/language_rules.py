from __future__ import annotations

from typing import Any

from .base import ApprovalRule

# Accepted languages for job postings
ACCEPTED_LANGUAGES = {"English", "english", "ENGLISH", "en", "EN"}
ACCEPTED_LANGUAGES_CANADA = ACCEPTED_LANGUAGES | {"French", "french", "FRENCH", "fr", "FR"}


def is_acceptable_language(job: dict[str, Any]) -> tuple[bool, str | None]:
    """
    Approve if the job description is in an acceptable language.

    Language requirements:
    - English is always accepted
    - French is accepted only if the job is in Canada
    - Empty/missing language field is rejected

    Examples:
        >>> ok, reason = is_acceptable_language({
        ...     "language": "English", "location": {"country": "USA"}
        ... })
        >>> ok, reason
        (True, None)
        >>> ok, reason = is_acceptable_language({
        ...     "language": "French", "location": {"country": "Canada"}
        ... })
        >>> ok, reason
        (True, None)
        >>> ok, reason = is_acceptable_language({
        ...     "language": "French", "location": {"country": "USA"}
        ... })
        >>> ok, reason
        (False, 'French language is only accepted for jobs in Canada, job location: USA')
        >>> ok, reason = is_acceptable_language({
        ...     "language": "Spanish", "location": {"country": "USA"}
        ... })
        >>> ok, reason
        (False, 'Job must be in English (or French if in Canada), got: Spanish')
        >>> ok, reason = is_acceptable_language({
        ...     "language": "", "location": {"country": "USA"}
        ... })
        >>> ok, reason
        (False, 'Job must specify a language')
    """
    language = job.get("language")

    # Handle missing or empty language
    if not language or (isinstance(language, str) and not language.strip()):
        return False, "Job must specify a language"

    language_str = str(language).strip()

    # Get job location country
    location = job.get("location", {})
    if isinstance(location, str):
        # Handle string location format like "Toronto, ON, Canada"
        country = location.split(",")[-1].strip() if "," in location else location
    else:
        # Handle dict location format
        country = location.get("country", "") if isinstance(location, dict) else ""

    # Normalize country name
    country = country.strip()
    is_canada = country.lower() in {"canada", "ca"}

    # Check if language is acceptable
    if is_canada:
        # In Canada, both English and French are acceptable
        if language_str in ACCEPTED_LANGUAGES_CANADA:
            return True, None
    else:
        # Outside Canada, only English is acceptable
        if language_str in ACCEPTED_LANGUAGES:
            return True, None
        elif language_str in {"French", "french", "FRENCH", "fr", "FR"}:
            return (
                False,
                f"French language is only accepted for jobs in Canada, job location: {country}",
            )

    return False, f"Job must be in English (or French if in Canada), got: {language_str}"


def get_rules() -> list[ApprovalRule]:
    """Return a list of language related approval rules.

    The returned callables conform to the `ApprovalRule` protocol.
    """
    return [is_acceptable_language]
