from src.models import ContentItem, UserProfile
from src.recommender import recommend_content, score_content


def test_score_content_rewards_activity_matches():
    user = UserProfile(
        user_id="u1",
        interests=["tech", "design"],
        activity_log=["watched ai talk", "bought headphones"],
    )
    item = ContentItem(
        content_id="c1",
        title="Intro to AI",
        category="tech",
        tags=["data", "tech"],
    )

    assert score_content(user, item) > 1.0


def test_generate_returns_top_five_sorted_recommendations():
    catalog = [
        ContentItem(content_id="c1", title="AI Basics", category="tech", tags=["ai", "technology"]),
        ContentItem(content_id="c2", title="Music Theory", category="playlist", tags=["music"]),
        ContentItem(content_id="c3", title="Morning Fitness", category="fitness", tags=["fitness", "health"]),
        ContentItem(content_id="c4", title="Reading List", category="book", tags=["books"]),
        ContentItem(content_id="c5", title="Rock Energy", category="playlist", tags=["rock", "music"]),
        ContentItem(content_id="c6", title="Health Tech", category="book", tags=["health", "technology"]),
    ]

    profiles = [
        UserProfile(
            user_id="young_active",
            name="Lina",
            age=24,
            interests=["technology", "music"],
            activity_log=["watched ai talk", "listened to rock music", "bought headphones"],
        ),
        UserProfile(
            user_id="young_passive",
            name="Noah",
            age=22,
            interests=["music"],
            activity_log=[],
        ),
        UserProfile(
            user_id="senior_active",
            name="Marie",
            age=64,
            interests=["health", "fitness"],
            activity_log=["walked 5km", "read health article", "tracked workout"],
        ),
        UserProfile(
            user_id="senior_passive",
            name="Paul",
            age=68,
            interests=["book", "history"],
            activity_log=[],
        ),
        UserProfile(
            user_id="mixed_profile",
            name="Sara",
            age=38,
            interests=["technology", "health"],
            activity_log=["read ai article", "saved fitness routine"],
        ),
    ]

    for profile in profiles:
        recommendations = recommend_content(profile, catalog, top_n=5)

        assert len(recommendations) == 5
        assert [item.score for item in recommendations] == sorted(
            [item.score for item in recommendations], reverse=True
        )


def test_activity_boost_changes_top_pick_for_active_user():
    catalog = [
        ContentItem(content_id="c1", title="AI Basics", category="tech", tags=["ai", "technology"]),
        ContentItem(content_id="c2", title="Music Theory", category="playlist", tags=["music"]),
        ContentItem(content_id="c3", title="Morning Fitness", category="fitness", tags=["fitness", "health"]),
    ]
    active_user = UserProfile(
        user_id="u_active",
        interests=["technology", "music"],
        activity_log=["watched ai talk", "bought headphones", "listened to rock music"],
    )

    recommendations = recommend_content(active_user, catalog, top_n=3)

    assert recommendations[0].content_id == "c1"
