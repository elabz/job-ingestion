from __future__ import annotations

from typing import Any

from .base import ApprovalRule

# Salary thresholds
MIN_ANNUAL_SALARY_USD: float = 100_000.0
MIN_HOURLY_RATE_USD: float = 45.0

# Currency conversion rates (approximate, could be made dynamic)
CURRENCY_TO_USD_RATES = {
    "USD": 1.0,
    "CAD": 0.74,  # 1 CAD = 0.74 USD (approximate)
    "EUR": 1.08,  # 1 EUR = 1.08 USD (approximate)
    "GBP": 1.27,  # 1 GBP = 1.27 USD (approximate)
}


def salary_meets_requirements(job: dict[str, Any]) -> tuple[bool, str | None]:
    """
    Approve if the job's salary meets minimum requirements:
    - Annual salary: $100,000+ USD
    - Hourly rate: $45+ USD per hour

    Handles various salary formats and currencies with conversion to USD.

    Examples:
        >>> ok, reason = salary_meets_requirements({"salary_min": 150000, "salary_currency": "USD"})
        >>> ok, reason
        (True, None)
        >>> ok, reason = salary_meets_requirements({
        ...     "salary_min": 65, "salary_unit": "hourly", "salary_currency": "USD"
        ... })
        >>> ok, reason
        (True, None)
        >>> ok, reason = salary_meets_requirements({"salary_min": 80000, "salary_currency": "USD"})
        >>> ok, reason
        (False, 'Annual salary below $100,000 USD (found: $80,000 USD)')
    """
    # Extract salary information from various possible fields
    salary_value = None
    currency = "USD"  # Default to USD
    unit = "annual"  # Default to annual

    # Try to get salary from min_salary (mapped from job data)
    if "salary_min" in job and job["salary_min"] is not None:
        try:
            salary_value = float(job["salary_min"])
        except (TypeError, ValueError):
            pass

    # Get currency and unit information
    if "salary_currency" in job and job["salary_currency"]:
        currency = str(job["salary_currency"]).upper()

    if "salary_unit" in job and job["salary_unit"]:
        unit = str(job["salary_unit"]).lower()
        if unit in ["hourly", "hour", "per hour"]:
            unit = "hourly"
        else:
            unit = "annual"

    # If no salary found, reject
    if salary_value is None or salary_value <= 0:
        return False, "No valid salary information found"

    # Convert to USD if needed
    usd_rate = CURRENCY_TO_USD_RATES.get(currency, 1.0)
    salary_usd = salary_value * usd_rate

    # Determine if salary meets requirements based on unit
    if unit == "hourly":
        # Check hourly rate requirement
        if salary_usd >= MIN_HOURLY_RATE_USD:
            return True, None
        else:
            return (
                False,
                f"Hourly rate below ${MIN_HOURLY_RATE_USD}/hour USD "
                f"(found: ${salary_usd:.2f}/hour USD)",
            )
    else:
        # Check annual salary requirement
        if salary_usd >= MIN_ANNUAL_SALARY_USD:
            return True, None
        else:
            return (
                False,
                f"Annual salary below ${MIN_ANNUAL_SALARY_USD:,.0f} USD "
                f"(found: ${salary_usd:,.0f} USD)",
            )


def get_rules() -> list[ApprovalRule]:
    """Return a list of salary-related approval rules.

    The returned callables conform to the `ApprovalRule` protocol.
    """
    return [salary_meets_requirements]
