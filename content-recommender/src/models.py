"""Models for the content recommender project.

The unit tests expect:
- UserProfile(user_id, name, age, interests, activity_log)
- ContentItem(content_id, title, category, tags)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

CATEGORIES: List[str] = ["Book", "Playlist", "Fitness"]

TAGS: List[str] = ["technology", "music", "rock", "ai", "fitness", "health"]


@dataclass
class UserProfile:
    user_id: str
    name: str = ""
    age: Optional[int] = None
    interests: List[str] = None  # type: ignore[assignment]
    activity_log: List[str] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.interests is None:
            self.interests = []
        if self.activity_log is None:
            self.activity_log = []


@dataclass
class ContentItem:
    content_id: str
    title: str
    category: str
    tags: List[str]

