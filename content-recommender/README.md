# 🚀 Présentation : Générateur de Contenu Personnalisé (IA)

Bienvenue dans mon projet pour le **Hackathon IA**. Ce document sert de plan de présentation pour démontrer au jury comment toutes les exigences techniques ont été remplies avec brio.

---

## 🎯 1. L'Objectif du Projet
L'objectif est de créer un système intelligent capable de générer des suggestions (livres, playlists, fitness, tech) basées sur les préférences et l'historique des utilisateurs.

Mon approche a été de simuler un **environnement Data Science / Développement réaliste** :
1. Un Notebook pour le travail de la donnée (Data Engineer / Data Analyst).
2. Un code Python "pur" pour l'algorithme (Software Engineer).

---

## 📊 2. Démonstration Data (Notebook)
*Ouvrez le fichier `notebooks/analyse_donnees.ipynb` pour cette partie de la présentation.*

1. **Génération de données bruitées (NumPy)** : Je montre comment j'ai généré 50 utilisateurs avec des âges distribués normalement (Moyenne 35 ans, Ecart-type 12). Surtout, j'ai injecté **volontairement des erreurs** (âges négatifs, valeurs `NaN`) pour rendre l'exercice intéressant.
2. **Nettoyage (Pandas)** : Je démontre l'utilisation de `dropna()` et `astype()` pour nettoyer ce fichier brut et le préparer pour notre moteur.
3. **Visualisation (Matplotlib & Seaborn)** : 
   - Histogramme des âges.
   - **Carte Thermique (Heatmap)** croisant les Heures et l'Activité (100% consigne).
   - Graphique en Barres des catégories recommandées par notre algorithme (100% consigne).
4. **Statistiques Mathématiques (SciPy)** :
   - Application du **Test du Chi-Carré** pour prouver que les intérêts de mes utilisateurs ne sont pas répartis uniformément.
   - Calcul de la **Similarité Cosinus** (`scipy.spatial.distance`) pour quantifier mathématiquement à quel point l'Utilisateur 1 et l'Utilisateur 2 se ressemblent.

---

## 💻 3. Démonstration Logique & POO (Code Python)
*Ouvrez le fichier `src/models.py`.*

Ici, je prouve ma maîtrise des fondamentaux du langage Python :
- **Encapsulation** : J'ai créé la classe `UserProfile` avec des attributs privés (`_age`) et des méthodes strictes (`get_age()`, `set_age()`).
- **Héritage & Polymorphisme** : Les classes `BookRecommendation`, `TechRecommendation` héritent toutes de `ContentItem` et réécrivent la méthode `describe()`.
- **Fonctions Avancées** : Les fonctions utilitaires démontrent l'utilisation de `lambda`, `map` (pour nettoyer du texte), `filter` (pour trier les âges) et `reduce` (pour compter l'activité totale).

---

## ⚙️ 4. Démonstration Algorithmique (Terminal)
*Lancez `python main.py`.*

L'algorithme de recommandation (le "Moteur") est basé sur une logique conditionnelle :
1. Il lit le fichier CSV propre que nous avons généré via Pandas.
2. Il convertit ces lignes en Objets (POO).
3. **Logique métier** : Il compare les "mots-clés" (tags) et applique un bonus conditionnel (ex: si l'utilisateur a le mot "ai" dans son historique d'activité, on booste les contenus Tech).
4. Il imprime de manière élégante le Top 2 des recommandations pour chaque utilisateur cible.

---

## 💡 Conclusion pour le Jury
Le projet respecte **intégralement toutes les contraintes techniques** du hackathon, tout en offrant une structure académique claire et professionnelle. Le code est robuste, commenté pédagogiquement, et les données sont traitées de bout en bout !
