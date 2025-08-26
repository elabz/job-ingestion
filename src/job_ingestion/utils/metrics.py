"""Minimal metrics utility (no-op counters).

Provides a typed increment() function used by the ingestion service. In this MVP,
metrics are collected in-memory and are safe no-ops in production runs.
"""

from __future__ import annotations

from collections import defaultdict

__all__ = ["increment", "get_counters", "reset_counters"]

# Simple in-memory counters for observability in tests/dev
_counters: defaultdict[str, int] = defaultdict(int)


def increment(name: str, value: int = 1) -> None:
    """Increment a named counter by value (default 1)."""
    try:
        _counters[name] += int(value)
    except Exception:
        # Defensive no-op on unexpected input
        pass


def get_counters() -> dict[str, int]:
    """Return a snapshot of current counters (for tests/dev)."""
    return dict(_counters)


def reset_counters() -> None:
    """Reset all counters to zero (for tests/dev)."""
    _counters.clear()
