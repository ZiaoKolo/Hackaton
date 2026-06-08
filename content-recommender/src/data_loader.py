"""Load datasets used by the dashboard.

The dashboard must use the real dataset files:
- data/users_raw.json
- data/users_clean.csv
- data/content_catalog.json

No heavy work should happen at import time.
"""

from __future__ import annotations

import json

from pathlib import Path
from typing import Any

import pandas as pd


from src.models import ContentItem, UserProfile
from src.data_processor import clean_user_record


def _ensure_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    # Sometimes the generator may output comma-separated strings
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return [value]



def _data_path(filename: str) -> Path:
    # content-recommender/src -> content-recommender
    root = Path(__file__).resolve().parent.parent
    return root / "data" / filename


def load_users_raw(limit: int | None = None) -> list[dict[str, Any]]:
    path = _data_path("users_raw.json")
    records: list[dict[str, Any]] = json.loads(path.read_text(encoding="utf-8"))
    if limit is not None:
        records = records[:limit]
    return records


def users_raw_to_profiles(limit: int | None = None) -> list[UserProfile]:
    records = load_users_raw(limit=limit)

    profiles: list[UserProfile] = []
    for rec in records:
        cleaned = clean_user_record(rec)
        profiles.append(
            UserProfile(
                user_id=str(cleaned.get("user_id", "")),
                name=str(cleaned.get("name", "")),
                age=cleaned.get("age"),
                interests=_ensure_list(cleaned.get("preferences", []))
                if "preferences" in cleaned
                else _ensure_list(cleaned.get("interests", []))
                if "interests" in cleaned
                else [],

                activity_log=_ensure_list(cleaned.get("activity_log", []))
                if "activity_log" in cleaned
                else _ensure_list(cleaned.get("activity_logs", []))
                if "activity_logs" in cleaned
                else _ensure_list(cleaned.get("activity", []))
                if "activity" in cleaned
                else _ensure_list(cleaned.get("Activity Logs", []))
                if "Activity Logs" in cleaned
                else [],

            )
        )
    return profiles


def load_users_clean(limit: int | None = None) -> pd.DataFrame:
    path = _data_path("users_clean.csv")
    df = pd.read_csv(path)
    if limit is not None:
        df = df.head(limit)
    return df


def users_clean_to_profiles(limit: int | None = None) -> list[UserProfile]:
    df = load_users_clean(limit=limit)

    profiles: list[UserProfile] = []
    # Expected columns per notebook: Name, Age, Interests, Activity Logs
    for _, row in df.iterrows():
        name = str(row.get("Name", ""))
        age = row.get("Age", None)

        # Interests & Activity Logs are stored like "['a', 'b']" in CSV
        interests_raw = row.get("Interests", [])
        if pd.isna(interests_raw):
            interests_list: list[str] = []
        else:
            interests_text = str(interests_raw)
            interests_text = interests_text.strip().lstrip("[").rstrip("]")
            interests_list = [
                part.strip()
                for part in interests_text.split(",")
                if part.strip() and part.strip().lower() != "nan"
            ]
            interests_list = [s.strip("'\"") for s in interests_list]

        activity_raw = row.get("Activity Logs", [])
        if pd.isna(activity_raw):
            activity_list: list[str] = []
        else:
            activity_text = str(activity_raw)
            activity_text = activity_text.strip().lstrip("[").rstrip("]")
            activity_parts = [
                part.strip()
                for part in activity_text.split(",")
                if part.strip() and part.strip().lower() != "nan"
            ]
            activity_list = [s.strip("'\"") for s in activity_parts]

        # For dashboard scoring, user_id can be the row index.
        profiles.append(
            UserProfile(
                user_id=str(_),
                name=name,
                age=int(age) if age is not None and str(age).strip().lower() != "nan" else None,
                interests=[i.lower() for i in interests_list],
                activity_log=[a.lower() for a in activity_list],
            )
        )

    return profiles


def load_content_catalog(limit: int | None = None) -> list[ContentItem]:
    path = _data_path("content_catalog.json")
    raw = json.loads(path.read_text(encoding="utf-8"))
    if limit is not None:
        raw = raw[:limit]

    items: list[ContentItem] = []
    for rec in raw:
        items.append(
            ContentItem(
                content_id=str(rec.get("content_id", rec.get("id", ""))),
                title=str(rec.get("title", "")),
                category=str(rec.get("category", "")),
                tags=[str(t).lower() for t in rec.get("tags", [])],
            )
        )
    return items

