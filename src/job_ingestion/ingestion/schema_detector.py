from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Literal

SchemaName = Literal["unknown", "schema_a", "schema_b"]


def detect_schema(jobs_data: Sequence[dict[str, Any]]) -> SchemaName:
    """
    Detect a simple source schema for a batch of job records using key presence.

    Heuristic (placeholder):
    - If any record contains "company_name" -> return "schema_a".
    - Else if any record contains "employer" -> return "schema_b".
    - If both key patterns appear in the batch, choose the one with higher count;
      if tied, return "unknown".
    - If no indicative keys are present or the input is empty -> "unknown".

    This function is intentionally simple and deterministic. It will be replaced by
    a more sophisticated detector in later tasks.

    Args:
        jobs_data: A sequence of raw job dicts.

    Returns:
        One of the literal schema identifiers: "unknown", "schema_a", or "schema_b".
    """
    if not jobs_data:
        return "unknown"

    count_a = 0
    count_b = 0

    for record in jobs_data:
        # Guard: only dict[str, Any] are expected; ignore non-dicts defensively
        if not isinstance(record, dict):
            continue
        if "company_name" in record:
            count_a += 1
        if "employer" in record:
            count_b += 1

    if count_a and not count_b:
        return "schema_a"
    if count_b and not count_a:
        return "schema_b"
    if count_a and count_b:
        if count_a > count_b:
            return "schema_a"
        if count_b > count_a:
            return "schema_b"
        return "unknown"

    return "unknown"
