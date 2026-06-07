from dataclasses import dataclass
from scipy.spatial.distance import cosine



TAGS = [
    "technology",
    "music",
    "fitness",
    "books",
    "ai"
]


@dataclass
class UserProfile:
    id: int
    name: str
    interests: list[str]


@dataclass
class ContentItem:
    title: str
    tags: list[str]



users = [
    UserProfile(
        1,
        "Alice",
        ["technology", "music"]
    ),

    UserProfile(
        2,
        "Bob",
        ["fitness", "books"]
    ),

    UserProfile(
        3,
        "Claire",
        ["fitness"]
    ),

    UserProfile(
        4,
        "David",
        ["music"]
    ),

    UserProfile(
        5,
        "Emma",
        ["technology", "books", "fitness"]
    )
]



catalog = [

    ContentItem(
        "Deep Learning with Python",
        ["technology", "ai"]
    ),

    ContentItem(
        "Rock Essentials",
        ["music"]
    ),

    ContentItem(
        "Morning Yoga Flow",
        ["fitness"]
    ),

    ContentItem(
        "Atomic Habits",
        ["books"]
    ),

    ContentItem(
        "AI Revolution Blog",
        ["technology", "ai"]
    )
]




def vectorize_interests(interests):

    vector = []

    for tag in TAGS:

        if tag in interests:
            vector.append(1)
        else:
            vector.append(0)

    return vector



def similarity(user1, user2):

    v1 = vectorize_interests(user1.interests)
    v2 = vectorize_interests(user2.interests)

    if sum(v1) == 0 or sum(v2) == 0:
        return 0

    return 1 - cosine(v1, v2)



def find_similar_users(target_user, users):

    results = []

    for user in users:

        if user.id == target_user.id:
            continue

        score = similarity(
            target_user,
            user
        )

        results.append(
            (user, score)
        )

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return results



def recommend_content(
        target_user,
        users,
        catalog,
        top_n=3
):

    similar_users = find_similar_users(
        target_user,
        users
    )

    recommendations = []

    for item in catalog:

        score = 0

        for similar_user, similarity_score in similar_users:

            common_tags = set(
                similar_user.interests
            ).intersection(
                item.tags
            )

            score += (
                len(common_tags)
                * similarity_score
            )

        recommendations.append(
            (item, score)
        )

    recommendations.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return recommendations[:top_n]




target_user = users[0]  # Alice

print("\nUtilisateur :", target_user.name)

print("\nUtilisateurs similaires :")

similar = find_similar_users(
    target_user,
    users
)

for user, score in similar:

    print(
        user.name,
        "->",
        round(score, 2)
    )

print("\nRecommandations :")

recommendations = recommend_content(
    target_user,
    users,
    catalog
)

for item, score in recommendations:

    print(
        item.title,
        "- score:",
        round(score, 2)
    )