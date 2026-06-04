"""Basic dataset statistics helpers."""

from __future__ import annotations

from collections.abc import Iterable


def summarize_values(values: Iterable[str]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for value in values:
        summary[value] = summary.get(value, 0) + 1
    return summary
