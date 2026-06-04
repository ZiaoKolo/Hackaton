"""Entry point for the content recommender project."""

from src.data_generator import generate_sample_catalog, generate_sample_users
from src.models import ContentItem, UserProfile
from src.recommender import recommend_content


def main() -> None:
    users = generate_sample_users()
    catalog = [ContentItem(**item) for item in generate_sample_catalog()]
    user = UserProfile(**users[0])
    recommendations = recommend_content(user, catalog)
    for recommendation in recommendations:
        print(f"{recommendation.title}: {recommendation.score}")


if __name__ == "__main__":
    main()
