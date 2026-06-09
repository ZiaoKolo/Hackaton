"""Tests pour le projet de Hackathon."""

from src.models import (
    UserProfile, ContentItem, BookRecommendation, MusicRecommendation,
    FitnessRecommendation, TechRecommendation, normalize_interests,
    filter_valid_ages, count_total_activities
)

def test_user_profile_encapsulation():
    """Verifie l'encapsulation: getters/setters explicites."""
    user = UserProfile(user_id="u1", name="Test", age=25)
    assert user.get_name() == "test"
    
    user.set_age(30)
    assert user.get_age() == 30
    
    user.set_age(None)
    assert user.get_age() is None
    
    # Age invalide
    user.set_age(-5)
    assert user.get_age() is None

def test_content_inheritance():
    """Verifie que les classes specialisees heritent de ContentItem."""
    book = BookRecommendation(content_id="b1", title="Test Book", category="Book", tags=["ai"])
    assert isinstance(book, ContentItem)

def test_polymorphism_describe():
    """Verifie le polymorphisme: describe() renvoie des messages differents."""
    book = BookRecommendation(content_id="b1", title="AI Book", category="Book", tags=["ai"])
    music = MusicRecommendation(content_id="m1", title="Rock Mix", category="Playlist", tags=["rock"])
    
    assert book.describe() != music.describe()
    assert "AI Book" in book.describe()
    assert "Rock Mix" in music.describe()

def test_lambda_map_filter():
    """Verifie les fonctions utilitaires."""
    result = normalize_interests([" TECH ", "  Music", "AI"])
    assert result == ["tech", "music", "ai"]
    
    ages = [25, -1, 200, 30, None, "abc", 0, 45]
    valid = filter_valid_ages(ages)
    assert valid == [25, 30, 45]
