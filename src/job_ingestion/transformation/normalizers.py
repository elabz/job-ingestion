"""Normalizers and validators for basic transformation layer.

This module provides minimal, well-typed stubs for:
- LocationNormalizer.normalize: trims and collapses whitespace; returns None for blank strings
- SalaryNormalizer.parse_range: parses numeric ranges; supports optional k/m suffixes
- CompanyValidator.validate: checks basic plausibility of a company name

Note: Detailed normalization rules will be implemented in task T10.
"""

from __future__ import annotations

import re

__all__ = [
    "LocationNormalizer",
    "SalaryNormalizer",
    "CompanyValidator",
]


class LocationNormalizer:
    """Basic location normalizer.

    Placeholder behavior:
    - Strip leading/trailing spaces
    - Collapse internal whitespace to single spaces
    - Return None if the input is empty/whitespace-only
    """

    _ws_re = re.compile(r"\s+")

    def normalize(self, raw: str) -> str | None:
        """Normalize a location string.

        Args:
            raw: The raw location text.

        Returns:
            A cleaned string or None if input is blank.
        """
        s = raw.strip()
        if not s:
            return None
        s = self._ws_re.sub(" ", s)
        return s


class SalaryNormalizer:
    """Parse salary-like strings into a numeric range.

    Placeholder behavior:
    - Extract up to two numeric values, allowing optional k/m suffixes (e.g., 50k, 1.2M)
    - If one value is found, return (value, value)
    - If two values are found, return them as (low, high) with ordering enforced
    - If no numeric values are found, return (None, None)

    Values are returned as integers; suffix multipliers are applied and truncated to int.
    """

    # Capture number with optional decimal part and an optional [k|m] suffix
    _num_re = re.compile(r"(?i)(\d+(?:\.\d+)?)([km]?)")

    @staticmethod
    def _apply_suffix(num_str: str, suffix: str) -> int:
        num = float(num_str)
        factor = 1.0
        if suffix.lower() == "k":
            factor = 1_000.0
        elif suffix.lower() == "m":
            factor = 1_000_000.0
        return int(num * factor)

    def parse_range(self, raw: str) -> tuple[int | None, int | None]:
        """Parse a salary string and return a numeric range.

        Examples:
            "1200 - 3400" -> (1200, 3400)
            "50k–70k"     -> (50000, 70000)
            "5000"        -> (5000, 5000)
            "n/a"         -> (None, None)
        """
        matches = self._num_re.findall(raw)
        values: list[int] = [self._apply_suffix(n, s) for (n, s) in matches]

        if not values:
            return (None, None)
        if len(values) == 1:
            v = values[0]
            return (v, v)
        low, high = values[0], values[1]
        if high < low:
            low, high = high, low
        return (low, high)


class CompanyValidator:
    """Basic company name validator.

    Placeholder behavior:
    - Must not be blank after trimming
    - Must contain at least one alphabetic character
    """

    def validate(self, raw: str) -> bool:
        s = raw.strip()
        if not s:
            return False
        if not any(ch.isalpha() for ch in s):
            return False
        return True
