from __future__ import annotations

from typing import Any

from job_ingestion.approval.engine import ApprovalEngine
from job_ingestion.approval.rules.base import ApprovalRule


def test_empty_registry_approves_by_default() -> None:
    engine = ApprovalEngine()
    decision = engine.evaluate_job({"title": "Software Engineer"})
    assert decision.approved is True
    assert decision.reasons == []


def test_register_callable_and_aggregate_results() -> None:
    def always_pass(job: dict[str, Any]) -> tuple[bool, str | None]:
        return True, None

    def fail_if_missing_title(job: dict[str, Any]) -> tuple[bool, str | None]:
        ok = bool(job.get("title"))
        return (ok, None) if ok else (False, "Missing title")

    engine = ApprovalEngine()
    engine.register_rule(always_pass)
    engine.register_rule(fail_if_missing_title)

    decision1 = engine.evaluate_job({"title": "SWE"})
    assert decision1.approved is True
    assert decision1.reasons == []

    decision2 = engine.evaluate_job({})
    assert decision2.approved is False
    assert decision2.reasons == ["Missing title"]


def test_support_object_implementing_protocol() -> None:
    class MinSalaryRule:
        def __init__(self, threshold: int) -> None:
            self.threshold = threshold

        # Matches ApprovalRule protocol
        def __call__(self, job: dict[str, Any]) -> tuple[bool, str | None]:
            min_salary = job.get("min_salary", 0)
            ok = isinstance(min_salary, int | float) and min_salary >= self.threshold
            return (ok, None) if ok else (False, f"Min salary below {self.threshold}")

    rule_obj: ApprovalRule = MinSalaryRule(100_000)
    engine = ApprovalEngine([rule_obj])

    ok_decision = engine.evaluate_job({"min_salary": 120_000})
    assert ok_decision.approved is True
    assert ok_decision.reasons == []

    bad_decision = engine.evaluate_job({"min_salary": 90_000})
    assert bad_decision.approved is False
    assert bad_decision.reasons == ["Min salary below 100000"]


def test_init_with_rules_sequence() -> None:
    def rule_true(job: dict[str, Any]) -> tuple[bool, str | None]:
        return True, None

    def rule_false(job: dict[str, Any]) -> tuple[bool, str | None]:
        return False, "nope"

    engine = ApprovalEngine([rule_true, rule_false])
    decision = engine.evaluate_job({})
    assert decision.approved is False
    assert decision.reasons == ["nope"]
