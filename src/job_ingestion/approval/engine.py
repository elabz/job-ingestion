from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

from .rules.base import ApprovalRule

RuleResult = tuple[bool, str | None]
RuleCallable = Callable[[dict[str, Any]], RuleResult]


@dataclass(frozen=True)
class ApprovalDecision:
    """
    Result of evaluating a job against registered approval rules.

    Attributes:
        approved: Overall approval status. True only if all rules approve.
        reasons: Collected reasons from failed rules (empty if approved).

    Example:
        >>> engine = ApprovalEngine()
        >>> def has_title(job: dict[str, Any]) -> tuple[bool, str | None]:
        ...     ok = bool(job.get("title"))
        ...     return ok, None if ok else "Missing title"
        >>> engine.register_rule(has_title)
        >>> decision = engine.evaluate_job({"title": "Software Engineer"})
        >>> decision.approved
        True
        >>> decision.reasons
        []
    """

    approved: bool
    reasons: list[str]


class ApprovalEngine:
    """
    Approval engine that holds a registry of rules and evaluates jobs against them.

    Rules can be registered as callables or objects implementing the `ApprovalRule` protocol
    (i.e., any callable that accepts a `dict` job and returns `(bool, str | None)`).
    """

    def __init__(self, rules: Sequence[ApprovalRule] | None = None) -> None:
        self._rules: list[ApprovalRule] = []
        if rules:
            for r in rules:
                self.register_rule(r)

    def register_rule(self, rule: ApprovalRule) -> None:
        """Register a rule. Accepts plain callables or objects implementing the protocol."""
        # Anything callable with the correct signature will be accepted at runtime.
        if not callable(rule):  # pragma: no cover - defensive guard
            raise TypeError("rule must be callable")
        # Store as protocol type; plain callables are structurally compatible.
        self._rules.append(rule)

    def evaluate_job(self, job: dict[str, Any]) -> ApprovalDecision:
        """
        Evaluate the job against all registered rules.

        - Overall approval is True only if all rules return True.
        - Reasons are aggregated from rules that returned False and provided a reason.
        """
        results: list[RuleResult] = []
        for rule in self._rules:
            approved, reason = rule(job)
            results.append((approved, reason))

        overall_approved = all(ok for ok, _ in results) if results else True
        reasons = [reason for ok, reason in results if not ok and reason]
        return ApprovalDecision(approved=overall_approved, reasons=reasons)
