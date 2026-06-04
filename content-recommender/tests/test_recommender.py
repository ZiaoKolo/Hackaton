from src.models import ContentItem, UserProfile
from src.recommender import recommend_content, score_content


def test_score_content_rewards_category_and_tags():
    user = UserProfile(user_id="u1", preferences=["tech", "design"])
    item = ContentItem(content_id="c1", title="Intro to AI", category="tech", tags=["data", "tech"])

    assert score_content(user, item) == 3.0


def test_recommend_content_sorts_by_score():
    user = UserProfile(user_id="u1", preferences=["tech"])
    catalog = [
        ContentItem(content_id="c1", title="Design", category="design", tags=[]),
        ContentItem(content_id="c2", title="AI", category="tech", tags=["tech"]),
    ]

    recommendations = recommend_content(user, catalog, top_n=2)

    assert [item.content_id for item in recommendations] == ["c2", "c1"]
