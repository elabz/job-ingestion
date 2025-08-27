from __future__ import annotations

from typing import Any

from job_ingestion.approval.engine import ApprovalEngine
from job_ingestion.approval.rules import (
    company_type_rules,
    content_rules,
    employment_type_rules,
    language_rules,
    location_rules,
    salary_rules,
)
from job_ingestion.approval.rules.base import ApprovalRule


def test_salary_rules_pass_fail() -> None:
    rules = salary_rules.get_rules()
    # mypy/type-check: ensure protocol compatibility
    for r in rules:
        assert callable(r)

    min_rule: ApprovalRule = rules[0]

    ok, reason = min_rule({"salary_min": salary_rules.MIN_SALARY_THRESHOLD})
    assert ok is True and reason is None

    ok, reason = min_rule({"salary_min": salary_rules.MIN_SALARY_THRESHOLD - 1})
    assert ok is False and "Annual salary below" in (reason or "")

    ok, reason = min_rule({"salary_min": "not-a-number"})
    assert ok is False and "No valid salary information found" in (reason or "")


def test_location_rules_pass_fail() -> None:
    rules = location_rules.get_rules()
    loc_rule: ApprovalRule = rules[0]

    ok, reason = loc_rule({"location": "NYC, USA"})
    assert ok is True and reason is None

    ok, reason = loc_rule({"is_remote": True})
    assert ok is True and reason is None

    ok, reason = loc_rule({})
    assert ok is False and (reason or "").lower().startswith("missing location")


def test_geographical_location_rule() -> None:
    """Test the geographical location approval rule."""
    rules = location_rules.get_rules()
    geo_rule: ApprovalRule = rules[1]  # geographical location rule is second

    # Test remote jobs (should always pass)
    ok, reason = geo_rule({"remote": True, "location": {"country": "France"}})
    assert ok is True and reason is None

    ok, reason = geo_rule({"is_remote": True, "location": "London, UK"})
    assert ok is True and reason is None

    # Test US locations (object format)
    ok, reason = geo_rule(
        {"location": {"city": "Austin", "state": "TX", "country": "USA"}, "remote": False}
    )
    assert ok is True and reason is None

    ok, reason = geo_rule(
        {"location": {"city": "Seattle", "state": "WA", "country": "US"}, "remote": False}
    )
    assert ok is True and reason is None

    # Test Canada locations (object format)
    ok, reason = geo_rule(
        {"location": {"city": "Vancouver", "state": "BC", "country": "Canada"}, "remote": False}
    )
    assert ok is True and reason is None

    # Test US locations (string format)
    ok, reason = geo_rule({"location": "New York, NY, USA", "remote": False})
    assert ok is True and reason is None

    ok, reason = geo_rule({"location": "Seattle, WA, US", "remote": False})
    assert ok is True and reason is None

    # Test Canada locations (string format)
    ok, reason = geo_rule({"location": "Toronto, ON, Canada", "remote": False})
    assert ok is True and reason is None

    ok, reason = geo_rule({"location": "Montreal, QC, Canada", "remote": False})
    assert ok is True and reason is None

    # Test non-US/Canada locations (should fail)
    ok, reason = geo_rule({"location": {"city": "Paris", "country": "France"}, "remote": False})
    assert ok is False and "Job location must be in US/Canada or remote" in (reason or "")

    ok, reason = geo_rule({"location": "London, UK", "remote": False})
    assert ok is False and "Unable to determine country from location" in (reason or "")

    ok, reason = geo_rule({"location": {"city": "Manchester", "country": "UK"}, "remote": False})
    assert ok is False and "Job location must be in US/Canada or remote" in (reason or "")

    # Test missing location
    ok, reason = geo_rule({"remote": False})
    assert ok is False and "Missing location information" in (reason or "")

    # Test unparseable location
    ok, reason = geo_rule({"location": "Unknown Format", "remote": False})
    assert ok is False and "Unable to determine country from location" in (reason or "")


def test_content_rules_pass_fail() -> None:
    rules = content_rules.get_rules()
    content_rule: ApprovalRule = rules[0]

    ok, reason = content_rule(
        {"title": "SWE", "description": "x" * content_rules.MIN_DESCRIPTION_LENGTH}
    )
    assert ok is True and reason is None

    ok, reason = content_rule({"title": "", "description": "A decent role"})
    assert ok is False and (reason or "").lower().startswith("missing or empty title")

    ok, reason = content_rule({"title": "SWE", "description": "too short"})
    assert ok is False and "Description too short" in (reason or "")


def test_employment_type_rules_pass_fail() -> None:
    """Test employment type approval rules."""
    rules = employment_type_rules.get_rules()
    # mypy/type-check: ensure protocol compatibility
    for r in rules:
        assert callable(r)

    employment_rule: ApprovalRule = rules[0]

    # Test valid full-time variations
    ok, reason = employment_rule({"employment_type": "Full-Time"})
    assert ok is True and reason is None

    ok, reason = employment_rule({"employment_type": "full-time"})
    assert ok is True and reason is None

    ok, reason = employment_rule({"employment_type": "FULL-TIME"})
    assert ok is True and reason is None

    ok, reason = employment_rule({"employment_type": "Full Time"})
    assert ok is True and reason is None

    ok, reason = employment_rule({"employment_type": "full time"})
    assert ok is True and reason is None

    # Test invalid employment types
    ok, reason = employment_rule({"employment_type": "Internship"})
    assert ok is False and "Job must be a full-time position, got: Internship" in (reason or "")

    ok, reason = employment_rule({"employment_type": "Contract"})
    assert ok is False and "Job must be a full-time position, got: Contract" in (reason or "")

    ok, reason = employment_rule({"employment_type": "Part-Time"})
    assert ok is False and "Job must be a full-time position, got: Part-Time" in (reason or "")

    # Test missing employment type
    ok, reason = employment_rule({})
    assert ok is False and "Job must be a full-time position, got: None" in (reason or "")


def test_company_type_rules_pass_fail() -> None:
    """Test company type approval rules."""
    rules = company_type_rules.get_rules()
    # mypy/type-check: ensure protocol compatibility
    for r in rules:
        assert callable(r)

    company_type_rule: ApprovalRule = rules[0]

    # Test valid company types (should pass)
    ok, reason = company_type_rule({"company_type": "Direct Employer"})
    assert ok is True and reason is None

    ok, reason = company_type_rule({"company_type": "Consulting Agency"})
    assert ok is True and reason is None

    ok, reason = company_type_rule({"company_type": "Startup"})
    assert ok is True and reason is None

    # Test missing company type (should pass - not rejected)
    ok, reason = company_type_rule({})
    assert ok is True and reason is None

    # Test rejected company types (should fail)
    ok, reason = company_type_rule({"company_type": "Staffing Firm"})
    assert ok is False and "Job must not be from a staffing firm, got: Staffing Firm" in (
        reason or ""
    )

    ok, reason = company_type_rule({"company_type": "staffing firm"})
    assert ok is False and "Job must not be from a staffing firm, got: staffing firm" in (
        reason or ""
    )

    ok, reason = company_type_rule({"company_type": "STAFFING FIRM"})
    assert ok is False and "Job must not be from a staffing firm, got: STAFFING FIRM" in (
        reason or ""
    )

    ok, reason = company_type_rule({"company_type": "Staffing Agency"})
    assert ok is False and "Job must not be from a staffing firm, got: Staffing Agency" in (
        reason or ""
    )

    ok, reason = company_type_rule({"company_type": "Recruiting Firm"})
    assert ok is False and "Job must not be from a staffing firm, got: Recruiting Firm" in (
        reason or ""
    )

    ok, reason = company_type_rule({"company_type": "Recruitment Agency"})
    assert ok is False and "Job must not be from a staffing firm, got: Recruitment Agency" in (
        reason or ""
    )


def test_language_rules_pass_fail() -> None:
    """Test language approval rules."""
    rules = language_rules.get_rules()
    # mypy/type-check: ensure protocol compatibility
    for r in rules:
        assert callable(r)

    language_rule: ApprovalRule = rules[0]

    # Test English in various countries (should pass)
    ok, reason = language_rule({"language": "English", "location": {"country": "USA"}})
    assert ok is True and reason is None

    ok, reason = language_rule({"language": "english", "location": {"country": "Canada"}})
    assert ok is True and reason is None

    ok, reason = language_rule({"language": "ENGLISH", "location": {"country": "UK"}})
    assert ok is True and reason is None

    ok, reason = language_rule({"language": "en", "location": "New York, NY, USA"})
    assert ok is True and reason is None

    # Test French in Canada (should pass)
    ok, reason = language_rule({"language": "French", "location": {"country": "Canada"}})
    assert ok is True and reason is None

    ok, reason = language_rule({"language": "french", "location": "Montreal, QC, Canada"})
    assert ok is True and reason is None

    ok, reason = language_rule({"language": "fr", "location": {"country": "Canada"}})
    assert ok is True and reason is None

    # Test French outside Canada (should fail)
    ok, reason = language_rule({"language": "French", "location": {"country": "USA"}})
    assert ok is False and "French language is only accepted for jobs in Canada" in (reason or "")

    ok, reason = language_rule({"language": "French", "location": "Paris, France"})
    assert ok is False and "French language is only accepted for jobs in Canada" in (reason or "")

    # Test unsupported languages (should fail)
    ok, reason = language_rule({"language": "Spanish", "location": {"country": "USA"}})
    assert ok is False and "Job must be in English (or French if in Canada), got: Spanish" in (
        reason or ""
    )

    ok, reason = language_rule({"language": "German", "location": {"country": "Canada"}})
    assert ok is False and "Job must be in English (or French if in Canada), got: German" in (
        reason or ""
    )

    # Test missing language (should fail)
    ok, reason = language_rule({"location": {"country": "USA"}})
    assert ok is False and "Job must specify a language" in (reason or "")

    # Test empty language (should fail)
    ok, reason = language_rule({"language": "", "location": {"country": "USA"}})
    assert ok is False and "Job must specify a language" in (reason or "")

    ok, reason = language_rule({"language": "   ", "location": {"country": "USA"}})
    assert ok is False and "Job must specify a language" in (reason or "")


def test_engine_with_all_rules() -> None:
    engine = ApprovalEngine(
        [
            *salary_rules.get_rules(),
            *location_rules.get_rules(),
            *content_rules.get_rules(),
            *employment_type_rules.get_rules(),
            *company_type_rules.get_rules(),
            *language_rules.get_rules(),
        ]
    )

    passing_job: dict[str, Any] = {
        "salary_min": salary_rules.MIN_SALARY_THRESHOLD + 5_000,
        "location": "New York, NY, USA",
        "title": "Backend Engineer",
        "description": "This is a long enough description to pass the content rule.",
        "employment_type": "Full-Time",
        "language": "English",
    }
    decision_ok = engine.evaluate_job(passing_job)
    assert decision_ok.approved is True
    assert decision_ok.reasons == []

    failing_job: dict[str, Any] = {
        "salary_min": 10_000,  # below threshold
        # missing location and remote flag
        "title": "",
        "description": "short",
    }
    decision_bad = engine.evaluate_job(failing_job)
    assert decision_bad.approved is False
    # At least two distinct reasons should be present
    assert len(decision_bad.reasons) >= 2
