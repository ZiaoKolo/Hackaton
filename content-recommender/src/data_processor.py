"""Helpers for loading and cleaning user data."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).strip().lower().split())


def clean_user_record(record: dict[str, Any]) -> dict[str, Any]:
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
    return [clean_user_record(record) for record in records]
