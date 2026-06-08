"""Helpers for loading and cleaning user data.

This module is intentionally small to support unit tests.

Unit tests expect:
- clean_user_record(record)
- clean_user_records(records)

No dataset should be loaded at import time.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def normalize_text(value: Any) -> str:
    """Lowercase + trim + collapse multiple spaces."""
    if value is None:
        return ""
    return " ".join(str(value).strip().lower().split())


def clean_user_record(record: dict[str, Any]) -> dict[str, Any]:
    """Clean a single user record."""
    cleaned = dict(record)

    cleaned["user_id"] = normalize_text(record.get("user_id"))
    cleaned["name"] = normalize_text(record.get("name"))

    age = record.get("age")
    try:
        cleaned["age"] = int(age) if age not in (None, "") else None
    except (TypeError, ValueError):
        cleaned["age"] = None

    preferences = record.get("preferences", [])
    if isinstance(preferences, str):
        preferences = [item.strip() for item in preferences.split(",") if item.strip()]

    cleaned["preferences"] = [normalize_text(item) for item in preferences]
    return cleaned


def clean_user_records(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Clean multiple user records."""
    return [clean_user_record(record) for record in records]

