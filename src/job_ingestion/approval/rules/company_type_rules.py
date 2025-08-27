from __future__ import annotations

from typing import Any

from .base import ApprovalRule

# Company types that should be rejected
REJECTED_COMPANY_TYPES = {
    "Staffing Firm",
    "staffing firm",
    "STAFFING FIRM",
    "Staffing Agency",
    "staffing agency",
    "STAFFING AGENCY",
    "Recruiting Firm",
    "recruiting firm",
    "RECRUITING FIRM",
    "Recruitment Agency",
    "recruitment agency",
    "RECRUITMENT AGENCY",
}


def is_not_staffing_firm(job: dict[str, Any]) -> tuple[bool, str | None]:
    """
    Approve if the job is not from a staffing firm.

    A job is rejected if its "company_type" field indicates it's from a staffing firm,
    recruiting firm, or similar intermediary (case-insensitive variations accepted).

    Examples:
        >>> ok, reason = is_not_staffing_firm({"company_type": "Direct Employer"})
        >>> ok, reason
        (True, None)
        >>> ok, reason = is_not_staffing_firm({"company_type": "Staffing Firm"})
        >>> ok, reason
        (False, 'Job must not be from a staffing firm, got: Staffing Firm')
        >>> ok, reason = is_not_staffing_firm({})
        >>> ok, reason
        (True, None)
    """
    company_type = job.get("company_type")

    # If no company_type is provided, we don't reject based on this rule
    if company_type is None:
        return True, None

    # Convert to string and check against rejected variants
    company_type_str = str(company_type).strip()

    if company_type_str in REJECTED_COMPANY_TYPES:
        return False, f"Job must not be from a staffing firm, got: {company_type_str}"

    return True, None


def get_rules() -> list[ApprovalRule]:
    """Return a list of company type related approval rules.

    The returned callables conform to the `ApprovalRule` protocol.
    """
    return [is_not_staffing_firm]
