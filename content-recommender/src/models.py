"""Créer classes OOP :
User, ContentItem,
Recommender
Définir catalogue contenu
(livres, playlists, fitness)

Exemples :
{
    "name": "John Doe",
    "age": 28,
    "interests": ["technology", "music"],
    "activity_log": ["watched AI talk", "listened to rock music", "bought headphones"]
}
    """

# Constantes du catalogue

CATEGORIES = [
    "Book",
    "Playlist",
    "Fitness"
]

TAGS = [
    "technology",
    "music",
    "rock",
    "ai",
    "fitness",
    "health"
]


class User:
    def __init__(self, name, age, interests, activity_log):
        self.name = name
        self.age = age
        self.interests = interests
        self.activity_log = activity_log


class ContentItem:
    def __init__(self, content_id, title, category, tags):
        self.content_id = content_id
        self.title = title
        self.category = category
        self.tags = tags