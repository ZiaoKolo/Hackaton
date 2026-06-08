from __future__ import annotations

import json
import random
from dataclasses import asdict
from pathlib import Path
from typing import Any

from src.models import ContentItem, UserProfile


def _rand_age() -> Any:
    """Return ages with realistic dirty data."""
    roll = random.random()
    if roll < 0.78:
        return random.randint(15, 70)
    if roll < 0.85:
        return None
    if roll < 0.90:
        return random.choice(["", "N/A", "unknown"])
    if roll < 0.95:
        return random.choice([160, 200, -55, -2, 0])
    # string numeric sometimes
    return str(random.randint(15, 70))


def _rand_interests(pool: list[str]) -> Any:
    roll = random.random()
    k = random.randint(1, 3)
    picked = random.sample(pool, k)

    if roll < 0.80:
        return picked
    if roll < 0.90:
        # comma-separated string (dirty)
        return ", ".join(picked)
    if roll < 0.95:
        return [p.upper() if random.random() < 0.5 else p for p in picked]
    # missing
    return None


def _rand_activity_log(pool: list[str]) -> Any:
    roll = random.random()
    k = random.randint(1, 3)
    picked = random.sample(pool, k)

    if roll < 0.75:
        return picked
    if roll < 0.85:
        # sometimes use alternative field names / typoes
        return [p.replace("watched", "viewed") if random.random() < 0.4 else p for p in picked]
    if roll < 0.90:
        # underscore variant
        return [p.replace("listened_to", "listened to").replace("listened to", "listened_to") for p in picked]
    if roll < 0.95:
        # wrong type
        return ", ".join(picked)
    return None


def _rand_name() -> str:
    prenoms = ["Alice", "Ali", "Charlie", "Diana", "Eva", "Frank", "Marie", "Noah", "Sara", "Paul", "Lina"]
    noms = ["Kouakou", "Bamba", "Koffi", "Yao", "Ouattara", "Oulaï", "Doe", "Smith", "Lee", "Koffi"]
    name = f"{random.choice(prenoms)} {random.choice(noms)}"
    if random.random() < 0.20:
        # dirty spacing
        name = "  " + name + "  "
    return name


def generate_users_raw(n: int = 50, seed: int | None = 42) -> list[dict[str, Any]]:
    """Generate a raw users dataset (dirty on purpose) compatible with data_loader.cleaning.

    Schema (ideal): {user_id, name, age, preferences, activity_log}
    We will inject realistic issues:
    - invalid ages (None, strings, out-of-range)
    - interests as list OR comma-separated string OR None
    - activity logs list OR wrong separators OR None
    - occasional key renames (preferences<->interests, activity_log variants)
    """
    if seed is not None:
        random.seed(seed)

    interests_pool = [
        "technology",
        "fitness",
        "music",
        "sports",
        "travel",
        "photography",
        "gaming",
        "cooking",
        "fashion",
        "finance",
        "business",
        "entrepreneurship",
        "art",
        "movies",
        "books",
        "science",
        "health",
        "education",
        "automotive",
        "real_estate",
        "cryptocurrency",
        "artificial_intelligence",
        "sustainability",
        "gardening",
        "pets",
        "vlog",
        "politics",
        "comedy",
        "Racing",
    ]

    activity_pool = [
        "viewed_page",
        "viewed_product",
        "viewed_video",
        "viewed_article",
        "searched_query",
        "searched_product",
        "searched_ai_tools",
        "liked_post",
        "liked_video",
        "liked_comment",
        "shared_post",
        "shared_video",
        "commented_post",
        "saved_post",
        "followed_user",
        "watched_video",
        "watched_ai_talk",
        "watched_webinar",
        "watched_tutorial",
        "watched_movie",
        "listened_to_music",
        "listened_to_rock_music",
        "listened_to_podcast",
        "liked_song",
        "followed_artist",
        "added_to_cart",
        "removed_from_cart",
        "added_to_wishlist",
        "started_checkout",
        "completed_purchase",
        "bought_headphones",
        "bought_laptop",
        "bought_book",
        "reviewed_product",
        "rated_product",
        "installed_app",
        "opened_app",
        "upgraded_subscription",
        "renewed_subscription",
        "signed_up",
        "logged_in",
        "updated_profile",
        "sent_message",
        "joined_group",
        "downloaded_file",
        "uploaded_file",
        "completed_course",
        "attended_ai_talk",
        "booked_hotel",
        "booked_flight",
        "visited_restaurant",
        "attended_event",
        "played_game",
        "earned_achievement",
        "bought_stock",
        "sold_stock",
        "started_workout",
        "completed_workout",
        "tracked_steps",
        "watched AI talk",
        "listened to rock music",
        "listened to a podcast",
        "searched for headphones",
        "viewed a product",
        "added headphones to cart",
        "bought headphones",
        "reviewed headphones",
        "followed an artist",
        "shared a video",
        "commented on a post",
        "completed a course",
        "attended an AI conference",
        "booked a hotel",
        "played a game",
        "completed a workout",
    ]

    users: list[dict[str, Any]] = []
    for i in range(1, n + 1):
        user_id = f"u{i}"
        rec: dict[str, Any] = {
            "user_id": user_id if random.random() > 0.12 else f" {user_id} ",
            "name": _rand_name(),
            "age": _rand_age(),
        }

        preferences_value = _rand_interests(interests_pool)
        activity_value = _rand_activity_log(activity_pool)

        # Inject field-name variations
        if random.random() < 0.12:
            rec["interests"] = preferences_value
        else:
            rec["preferences"] = preferences_value

        if random.random() < 0.12:
            rec["activity_logs"] = activity_value
        else:
            rec["activity_log"] = activity_value

        # Sometimes drop one field entirely
        if random.random() < 0.06:
            rec.pop("age", None)
        if random.random() < 0.06:
            rec.pop("preferences", None)
        if random.random() < 0.06:
            rec.pop("activity_log", None)

        # Ensure JSON-serializable None/list/str
        users.append(rec)

    return users


def write_users_raw_and_clean(
    users_raw_path: str | Path,
    users_clean_path: str | Path,
    n: int = 50,
    seed: int = 42,
) -> None:
    """Write users_raw.json and users_clean.csv.

    users_clean.csv is expected by users_clean_to_profiles:
    columns: Name,Age,Interests,Activity Logs
    where interests/activity are stringified python lists.
    """
    from src.data_processor import clean_user_record

    users_raw = generate_users_raw(n=n, seed=seed)

    users_clean_rows: list[dict[str, Any]] = []
    for r in users_raw:
        cleaned = clean_user_record(r)
        users_clean_rows.append(
            {
                "Name": cleaned.get("name", ""),
                "Age": cleaned.get("age", ""),
                "Interests": str(cleaned.get("preferences", [])),
                "Activity Logs": str(cleaned.get("activity_log", [])),
            }
        )

    users_raw_path = Path(users_raw_path)
    users_clean_path = Path(users_clean_path)
    users_raw_path.parent.mkdir(parents=True, exist_ok=True)
    users_clean_path.parent.mkdir(parents=True, exist_ok=True)

    users_raw_path.write_text(json.dumps(users_raw, ensure_ascii=False, indent=2), encoding="utf-8")

    # Write CSV without requiring pandas
    headers = ["Name", "Age", "Interests", "Activity Logs"]
    lines = [",".join(headers)]
    for row in users_clean_rows:
        # csv escaping: wrap fields containing commas/brackets in quotes
        def esc(v: Any) -> str:
            s = "" if v is None else str(v)
            if any(ch in s for ch in [",", "[", "]", "\"", "\n"]):
                s = s.replace('"', '""')
                return f'"{s}"'
            return s

        lines.append(",".join([esc(row[h]) for h in headers]))

    users_clean_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    write_users_raw_and_clean(
        root / "data" / "users_raw.json",
        root / "data" / "users_clean.csv",
        n=50,
        seed=42,
    )

