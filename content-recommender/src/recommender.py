"""Simple content recommendation helpers."""

from __future__ import annotations

from collections.abc import Iterable

from .models import ContentItem, Recommendation, UserProfile


def score_content(user: UserProfile, item: ContentItem) -> float:
    preference_set = {value.lower() for value in user.preferences}
    tag_set = {value.lower() for value in item.tags}
    score = 0.0
    if item.category.lower() in preference_set:
        score += 2.0
    score += float(len(preference_set & tag_set))
    return score


def recommend_content(user: UserProfile, catalog: Iterable[ContentItem], top_n: int = 5) -> list[Recommendation]:
    ranked = [
        Recommendation(content_id=item.content_id, title=item.title, score=score_content(user, item))
        for item in catalog
    ]
    ranked.sort(key=lambda recommendation: recommendation.score, reverse=True)
    return ranked[:top_n]
