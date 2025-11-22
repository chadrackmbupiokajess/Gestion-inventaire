"""
Modèle Catégorie
"""
from database.db_manager import db


class Categorie:
    """Classe pour gérer les catégories de produits"""

    @staticmethod
    def creer(nom):
        """
        Créer une nouvelle catégorie

        Args:
            nom (str): Nom de la catégorie

        Returns:
            int: ID de la nouvelle catégorie
        """
        query = "INSERT INTO categories (nom) VALUES (?)"
        return db.execute_query(query, (nom,))

    @staticmethod
    def modifier(categorie_id, nom):
        """
        Modifier une catégorie

        Args:
            categorie_id (int): ID de la catégorie
            nom (str): Nouveau nom

        Returns:
            int: ID de la catégorie
        """
        query = "UPDATE categories SET nom = ? WHERE id = ?"
        return db.execute_query(query, (nom, categorie_id))

    @staticmethod
    def supprimer(categorie_id):
        """
        Supprimer une catégorie

        Args:
            categorie_id (int): ID de la catégorie

        Returns:
            int: ID de la catégorie supprimée
        """
        query = "DELETE FROM categories WHERE id = ?"
        return db.execute_query(query, (categorie_id,))

    @staticmethod
    def obtenir_toutes():
        """
        Obtenir toutes les catégories

        Returns:
            list: Liste des catégories
        """
        query = "SELECT * FROM categories ORDER BY nom"
        return [dict(row) for row in db.fetch_all(query)]

    @staticmethod
    def obtenir_par_id(categorie_id):
        """
        Obtenir une catégorie par son ID

        Args:
            categorie_id (int): ID de la catégorie

        Returns:
            dict: Informations de la catégorie
        """
        query = "SELECT * FROM categories WHERE id = ?"
        result = db.fetch_one(query, (categorie_id,))
        return dict(result) if result else None
