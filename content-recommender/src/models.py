"""Modeles de donnees pour le Generateur de Contenu Personnalise.

Ce fichier montre comment utiliser la Programmation Orientee Objet (POO) en Python.
Concepts demontres :
- Encapsulation : cacher les donnees avec '_' et utiliser des methodes get/set.
- Heritage : creer des classes filles a partir d'une classe parente (ContentItem).
- Polymorphisme : chaque classe fille modifie la methode describe() a sa facon.
"""

# Constantes du projet
CATEGORIES = ("Book", "Playlist", "Fitness", "Tech")

ALL_INTERESTS = (
    "technology", "music", "fitness", "health", "ai", "business", 
    "science", "sports", "art", "movies", "books"
)

# ============================================================================
# Fonctions Utilitaires (Pour demontrer lambda, map, filter, reduce)
# ============================================================================

def normalize_interests(interests):
    """Nettoie une liste de mots en utilisant map() et une fonction lambda."""
    if not interests:
        return []
    
    # map() applique la fonction lambda a chaque element de la liste
    result = map(lambda x: str(x).strip().lower(), interests)
    return list(result)

def filter_valid_ages(ages):
    """Garde uniquement les ages valides en utilisant filter() et une fonction lambda."""
    # filter() garde seulement les elements pour lesquels la condition est Vraie (True)
    result = filter(lambda a: isinstance(a, int) and 1 <= a <= 120, ages)
    return list(result)

def count_total_activities(users):
    """Calcule le nombre total d'activites pour tous les utilisateurs avec reduce()."""
    from functools import reduce
    
    if not users:
        return 0
        
    # reduce() accumule les resultats
    return reduce(lambda acc, u: acc + len(u.get_activity_log()), users, 0)


# ============================================================================
# Classes Modeles (Pour demontrer la POO)
# ============================================================================

class UserProfile:
    """Represente le profil d'un utilisateur de notre application.
    Demontre le principe d'Encapsulation.
    """
    
    def __init__(self, user_id, name="", age=None, interests=None, activity_log=None):
        """Constructeur : appele lors de la creation d'un nouvel utilisateur."""
        # Attributs publics
        self.user_id = user_id
        
        # Attributs prives (Encapsulation)
        self._name = ""
        self._age = None
        self._interests = []
        self._activity_log = []
        
        # Initialisation via les setters
        self.set_name(name)
        self.set_age(age)
        self.set_interests(interests)
        self.set_activity_log(activity_log)

    # --- Methodes Getter et Setter (Encapsulation) ---
    
    def get_name(self):
        """Retourne le nom de l'utilisateur."""
        return self._name
        
    def set_name(self, value):
        """Modifie le nom de l'utilisateur."""
        self._name = str(value).strip().lower()

    def get_age(self):
        """Retourne l'age de l'utilisateur."""
        return self._age

    def set_age(self, value):
        """Definit l'age avec une validation pour eviter les erreurs."""
        if value is None or str(value) == "nan":
            self._age = None
            return
            
        try:
            parsed_age = int(value)
            if 1 <= parsed_age <= 120:
                self._age = parsed_age
            else:
                self._age = None
        except (ValueError, TypeError):
            self._age = None

    def get_interests(self):
        """Retourne la liste des centres d'interet."""
        return self._interests
        
    def set_interests(self, value):
        """Definit les centres d'interet en les nettoyant."""
        if value:
            if isinstance(value, str):
                # Si c'est une chaine de caracteres, on la separe
                value = value.replace("[", "").replace("]", "").replace("'", "").split(",")
            self._interests = normalize_interests(value)
        else:
            self._interests = []

    def get_activity_log(self):
        """Retourne l'historique des activites de l'utilisateur."""
        return self._activity_log
        
    def set_activity_log(self, value):
        """Definit l'historique des activites."""
        self._activity_log = []
        if value:
            if isinstance(value, str):
                value = value.replace("[", "").replace("]", "").replace("'", "").split(",")
            for activity in value:
                cleaned_activity = str(activity).strip().lower()
                if cleaned_activity:
                    self._activity_log.append(cleaned_activity)

    # --- Autres methodes ---
    
    def dominant_interest(self):
        """Retourne le centre d'interet principal."""
        if len(self._interests) == 0:
            return "Aucun"
        return self._interests[0]

    def has_interest(self, interest):
        """Verifie si l'utilisateur possede un centre d'interet specifique."""
        return str(interest).lower().strip() in self._interests


class ContentItem:
    """Classe parente (Classe de base) pour les contenus recommandes."""
    
    def __init__(self, content_id, title, category, tags):
        """Constructeur du contenu."""
        self.content_id = content_id
        self.title = str(title).strip()
        self.category = str(category).strip()
        self.score = 0.0  # Le score sera calcule par notre moteur
        
        self.tags = []
        for tag in tags:
            self.tags.append(str(tag).lower().strip())

    def matches_interests(self, user_interests):
        """Compte combien de tags de ce contenu correspondent aux interets de l'utilisateur."""
        match_count = 0
        for tag in self.tags:
            if tag in user_interests:
                match_count += 1
        return match_count

    def describe(self):
        """Description par defaut du contenu (Polymorphisme)."""
        tags_str = ", ".join(self.tags)
        return "[" + self.category + "] " + self.title + " (Tags: " + tags_str + ")"


# ============================================================================
# Classes Filles (Pour demontrer l'Heritage et le Polymorphisme)
# ============================================================================

class BookRecommendation(ContentItem):
    """Specialisation pour les livres (Heritage)."""
    def describe(self):
        return "Livre a lire : " + self.title

class MusicRecommendation(ContentItem):
    """Specialisation pour la musique (Heritage)."""
    def describe(self):
        return "A ecouter : " + self.title

class FitnessRecommendation(ContentItem):
    """Specialisation pour le sport (Heritage)."""
    def describe(self):
        return "Entrainement suggere : " + self.title

class TechRecommendation(ContentItem):
    """Specialisation pour la technologie et l'IA (Heritage)."""
    def describe(self):
        return "Decouverte Tech/IA : " + self.title
