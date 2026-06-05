from math import sqrt
from models import TAGS

class Recommender:

    def __init__(self, catalog):
        self.catalog = catalog
        
    def vectorize_user(self, user):
        vector = []

        for tag in TAGS:
            if tag in user.interests:
                vector.append(1)
            else:
                vector.append(0)

        return vector

    def vectorize_item(self, item):
        vector = []

        for tag in TAGS:
            if tag in item.tags:
                vector.append(1)
            else:
                vector.append(0)

        return vector
   

    def cosine_similarity(self, v1, v2):

        # Produit scalaire
        dot_product = 0
        for i in range(len(v1)):
            dot_product += v1[i] * v2[i]

        # Norme du premier vecteur
        sum_v1 = 0
        for x in v1:
            sum_v1 += x * x
        norm_v1 = sqrt(sum_v1)

        # Norme du deuxième vecteur
        sum_v2 = 0
        for x in v2:
            sum_v2 += x * x
        norm_v2 = sqrt(sum_v2)

        # Éviter la division par zéro
        if norm_v1 == 0 or norm_v2 == 0:
            return 0

        return dot_product / (norm_v1 * norm_v2)
    
    def generate(self, user):

        user_vector = self.vectorize_user(user)

        recommendations = []

        for item in self.catalog:

            item_vector = self.vectorize_item(item)

            score = self.cosine_similarity(user_vector, item_vector)

            if score > 0:
                recommendations.append(item)

        return recommendations