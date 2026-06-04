"""Data models for the content recommender."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class UserProfile:
    user_id: str
    name: str = ""
    age: int | None = None
    preferences: List[str] = field(default_factory=list)


@dataclass
class ContentItem:
    content_id: str
    title: str
    category: str = ""
    tags: List[str] = field(default_factory=list)


@dataclass
class Recommendation:
    content_id: str
    title: str
    score: float
