# src/visualizer.py

import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs("outputs", exist_ok=True)


class Visualizer:

    def plot_categories(self):
        categories = ["Book", "Playlist", "Fitness"]
        counts = [10, 7, 5]

        plt.bar(categories, counts)
        plt.title("Contenus par catégorie")
        plt.savefig("outputs/categories.png")
        plt.close()

    def plot_tags(self):
        tags = ["technology", "music", "ai", "fitness"]
        counts = [8, 6, 5, 3]

        sns.barplot(x=tags, y=counts)
        plt.title("Distribution des tags")
        plt.savefig("outputs/tags.png")
        plt.close()

    def plot_scores(self):
        scores = [0.9, 0.7, 0.5, 0.3]

        plt.plot(scores)
        plt.title("Scores de recommandation")
        plt.savefig("outputs/scores.png")
        plt.close()