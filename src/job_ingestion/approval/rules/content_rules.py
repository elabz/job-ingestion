from __future__ import annotations

from typing import Any

from .base import ApprovalRule

# Simple, configurable content requirements
REQUIRE_TITLE: bool = True
MIN_DESCRIPTION_LENGTH: int = 20


def has_basic_content(job: dict[str, Any]) -> tuple[bool, str | None]:
    """
    Approve if basic content fields are present and sufficiently informative.

    Current criteria (stub):
    - Non-empty "title" (if REQUIRE_TITLE is True)
    - "description" present and at least MIN_DESCRIPTION_LENGTH characters (after stripping)

    Examples:
        >>> has_basic_content({"title": "SWE", "description": "x" * 25})
        (True, None)
        >>> has_basic_content({"title": "", "description": "Great job"})
        (False, 'Missing or empty title')
        >>> has_basic_content({"title": "SWE", "description": "Too short"})
        (False, 'Description too short (< 20)')
    """
    title = job.get("title")
    description = job.get("description", "")

    if REQUIRE_TITLE and not (isinstance(title, str) and title.strip() != ""):
        return False, "Missing or empty title"

    desc_text = description if isinstance(description, str) else ""
    if len(desc_text.strip()) < MIN_DESCRIPTION_LENGTH:
        return False, f"Description too short (< {MIN_DESCRIPTION_LENGTH})"

    return True, None


def get_rules() -> list[ApprovalRule]:
    """Return a list of content-related approval rules (stubs)."""
    return [has_basic_content]
