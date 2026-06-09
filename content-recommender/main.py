"""Fichier principal du projet : Moteur de Recommandation.

Ce fichier Python s'occupe de la logique logicielle (Programmation Orientee Objet).
Il charge les donnees prealablement nettoyees par notre Notebook (Pandas/Numpy),
puis il applique une logique conditionnelle pour recommander du contenu.
"""

import csv
import os

from src.models import (
    UserProfile, ContentItem, BookRecommendation, MusicRecommendation,
    FitnessRecommendation, TechRecommendation
)

# ============================================================================
# Catalogue de contenu (Simule une base de donnees)
# ============================================================================

CATALOGUE_BRUT = [
    {"content_id": "b1", "title": "Bases de l'IA", "category": "Book", "tags": ["ai", "technology", "books"]},
    {"content_id": "b2", "title": "Apprendre Python", "category": "Book", "tags": ["technology", "science"]},
    {"content_id": "b3", "title": "Histoire de Rome", "category": "Book", "tags": ["books", "history"]},
    {"content_id": "p1", "title": "Classiques Rock", "category": "Playlist", "tags": ["music", "rock"]},
    {"content_id": "p2", "title": "Mix Motivation", "category": "Playlist", "tags": ["music", "fitness", "sports"]},
    {"content_id": "f1", "title": "Cardio Matinal", "category": "Fitness", "tags": ["fitness", "health", "sports"]},
    {"content_id": "t1", "title": "News Tech Hebdo", "category": "Tech", "tags": ["technology", "business"]},
    {"content_id": "t2", "title": "Podcast IA", "category": "Tech", "tags": ["technology", "ai"]}
]

def charger_catalogue():
    """Convertit les dictionnaires bruts en objets POO (Heritage)."""
    objets_contenu = []
    
    for item in CATALOGUE_BRUT:
        cat = item["category"]
        c_id = item["content_id"]
        titre = item["title"]
        tags = item["tags"]
        
        # Demontre l'utilisation des classes enfants (Polymorphisme & Heritage)
        if cat == "Book":
            obj = BookRecommendation(c_id, titre, cat, tags)
        elif cat == "Playlist":
            obj = MusicRecommendation(c_id, titre, cat, tags)
        elif cat == "Fitness":
            obj = FitnessRecommendation(c_id, titre, cat, tags)
        elif cat == "Tech":
            obj = TechRecommendation(c_id, titre, cat, tags)
        else:
            obj = ContentItem(c_id, titre, cat, tags)
            
        objets_contenu.append(obj)
        
    return objets_contenu


# ============================================================================
# Logique de Recommandation
# ============================================================================

def calculer_score(user, item):
    """Calcule une note de recommandation (Logique conditionnelle simple)."""
    # 1. Base = mots-cles en commun
    interets = user.get_interests()
    score_base = item.matches_interests(interets)
    
    # 2. Bonus = Activite recente
    historique_complet = " ".join(user.get_activity_log())
    bonus = 0.0
    
    # Si le sujet du contenu apparait dans l'historique
    for tag in item.tags:
        if tag in historique_complet:
            bonus += 1.0
            
    # Condition speciale pour l'IA (Hackathon IA)
    if "ai" in historique_complet or "intelligence" in historique_complet:
        if "ai" in item.tags or "technology" in item.tags:
            bonus += 1.0
            
    return score_base + bonus

def recommander_contenu(user, catalogue, top_n=3):
    """Trouve les meilleurs contenus pour un utilisateur."""
    resultats = []
    
    for item in catalogue:
        score = calculer_score(user, item)
        if score > 0:
            # On ajoute un tuple (score, objet) pour pouvoir trier facilement
            resultats.append((score, item))
            
    # Tri decroissant selon le score (le score est l'element 0 du tuple)
    resultats.sort(key=lambda x: x[0], reverse=True)
    
    # On recupere seulement les 'top_n' meilleurs objets
    meilleurs_contenus = []
    for i in range(min(top_n, len(resultats))):
        meilleurs_contenus.append(resultats[i][1])
        
    return meilleurs_contenus


# ============================================================================
# Fonction Principale
# ============================================================================

def main():
    print("=== Generateur de Contenu Personnalise (Hackathon IA) ===\n")
    
    # 1. Verification des donnees du Notebook
    fichier_donnees = "data/users_clean.csv"
    if not os.path.exists(fichier_donnees):
        print(f"ERREUR: Fichier introuvable '{fichier_donnees}'.")
        print("Veuillez d'abord executer le notebook 'analyse_donnees.ipynb' pour generer et nettoyer les donnees.")
        return
        
    # 2. Chargement des utilisateurs (depuis le CSV propre cree par Pandas)
    utilisateurs = []
    with open(fichier_donnees, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # On cree nos objets POO
            u = UserProfile(
                user_id=row["user_id"],
                name=row["Name"],
                age=row["Age"],
                interests=row["Interests"],
                activity_log=row["Activity Logs"]
            )
            utilisateurs.append(u)
            
    print(f"-> {len(utilisateurs)} profils utilisateurs charges avec succes.\n")
    
    # 3. Chargement du catalogue
    catalogue = charger_catalogue()
    
    # 4. Affichage des recommandations pour les 3 premiers utilisateurs
    print("--- RECOMMANDATIONS ---\n")
    for i in range(min(3, len(utilisateurs))):
        user = utilisateurs[i]
        recos = recommander_contenu(user, catalogue, top_n=2)
        
        print(f"Utilisateur : {user.get_name().title()} ({user.get_age()} ans)")
        print(f"Interets    : {', '.join(user.get_interests())}")
        print("Suggestions :")
        
        if not recos:
            print("  - Aucune recommandation correspondante.")
        else:
            for reco in recos:
                # Utilisation de la methode describe() qui differe selon la classe (Polymorphisme)
                print(f"  - {reco.describe()}")
        print("-" * 30)

if __name__ == "__main__":
    main()
