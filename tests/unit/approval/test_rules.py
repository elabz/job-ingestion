from __future__ import annotations

from typing import Any

from job_ingestion.approval.engine import ApprovalEngine
from job_ingestion.approval.rules import content_rules, location_rules, salary_rules
from job_ingestion.approval.rules.base import ApprovalRule


def test_salary_rules_pass_fail() -> None:
    rules = salary_rules.get_rules()
    # mypy/type-check: ensure protocol compatibility
    for r in rules:
        assert callable(r)

    min_rule: ApprovalRule = rules[0]

    ok, reason = min_rule({"min_salary": salary_rules.MIN_SALARY_THRESHOLD})
    assert ok is True and reason is None

    ok, reason = min_rule({"min_salary": salary_rules.MIN_SALARY_THRESHOLD - 1})
    assert ok is False and "Min salary below" in (reason or "")

    ok, reason = min_rule({"min_salary": "not-a-number"})
    assert ok is False and "Min salary below" in (reason or "")


def test_location_rules_pass_fail() -> None:
    rules = location_rules.get_rules()
    loc_rule: ApprovalRule = rules[0]

    ok, reason = loc_rule({"location": "NYC, USA"})
    assert ok is True and reason is None

    ok, reason = loc_rule({"is_remote": True})
    assert ok is True and reason is None

    ok, reason = loc_rule({})
    assert ok is False and (reason or "").lower().startswith("missing location")


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


def test_engine_with_all_rules() -> None:
    engine = ApprovalEngine(
        [
            *salary_rules.get_rules(),
            *location_rules.get_rules(),
            *content_rules.get_rules(),
        ]
    )

    passing_job: dict[str, Any] = {
        "min_salary": salary_rules.MIN_SALARY_THRESHOLD + 5_000,
        "location": "Berlin, DE",
        "title": "Backend Engineer",
        "description": "This is a long enough description to pass the content rule.",
    }
    decision_ok = engine.evaluate_job(passing_job)
    assert decision_ok.approved is True
    assert decision_ok.reasons == []

    failing_job: dict[str, Any] = {
        "min_salary": 10_000,  # below threshold
        # missing location and remote flag
        "title": "",
        "description": "short",
    }
    decision_bad = engine.evaluate_job(failing_job)
    assert decision_bad.approved is False
    # At least two distinct reasons should be present
    assert len(decision_bad.reasons) >= 2
