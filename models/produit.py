"""
Modèle Produit
"""
from datetime import datetime
from database.db_manager import db


class Produit:
    """Classe pour gérer les produits"""

    @staticmethod
    def creer(nom, code, prix_achat, prix_vente, quantite, categorie_id=None, date_expiration=None):
        """
        Créer un nouveau produit

        Args:
            nom (str): Nom du produit
            code (str): Code unique du produit
            prix_achat (float): Prix d'achat
            prix_vente (float): Prix de vente
            quantite (int): Quantité en stock
            categorie_id (int, optional): ID de la catégorie
            date_expiration (str, optional): Date d'expiration

        Returns:
            int: ID du nouveau produit
        """
        query = """
            INSERT INTO produits (nom, code, prix_achat, prix_vente, quantite,
                                 categorie_id, date_expiration, date_creation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        return db.execute_query(query, (nom, code, prix_achat, prix_vente, quantite,
                                        categorie_id, date_expiration, datetime.now().isoformat()))

    @staticmethod
    def modifier(produit_id, nom, code, prix_achat, prix_vente, quantite, categorie_id=None, date_expiration=None):
        """
        Modifier un produit

        Args:
            produit_id (int): ID du produit
            nom (str): Nom du produit
            code (str): Code unique du produit
            prix_achat (float): Prix d'achat
            prix_vente (float): Prix de vente
            quantite (int): Quantité en stock
            categorie_id (int, optional): ID de la catégorie
            date_expiration (str, optional): Date d'expiration

        Returns:
            int: ID du produit
        """
        query = """
            UPDATE produits
            SET nom = ?, code = ?, prix_achat = ?, prix_vente = ?,
                quantite = ?, categorie_id = ?, date_expiration = ?
            WHERE id = ?
        """
        return db.execute_query(query, (nom, code, prix_achat, prix_vente, quantite,
                                        categorie_id, date_expiration, produit_id))

    @staticmethod
    def supprimer(produit_id):
        """
        Supprimer un produit

        Args:
            produit_id (int): ID du produit

        Returns:
            int: ID du produit supprimé
        """
        query = "DELETE FROM produits WHERE id = ?"
        return db.execute_query(query, (produit_id,))

    @staticmethod
    def obtenir_tous():
        """
        Obtenir tous les produits avec leurs catégories

        Returns:
            list: Liste des produits
        """
        query = """
            SELECT p.*, c.nom as categorie_nom
            FROM produits p
            LEFT JOIN categories c ON p.categorie_id = c.id
            ORDER BY p.nom
        """
        return [dict(row) for row in db.fetch_all(query)]

    @staticmethod
    def obtenir_par_id(produit_id):
        """
        Obtenir un produit par son ID

        Args:
            produit_id (int): ID du produit

        Returns:
            dict: Informations du produit
        """
        query = """
            SELECT p.*, c.nom as categorie_nom
            FROM produits p
            LEFT JOIN categories c ON p.categorie_id = c.id
            WHERE p.id = ?
        """
        result = db.fetch_one(query, (produit_id,))
        return dict(result) if result else None

    @staticmethod
    def rechercher(terme):
        """
        Rechercher des produits par nom ou code

        Args:
            terme (str): Terme de recherche

        Returns:
            list: Liste des produits correspondants
        """
        query = """
            SELECT p.*, c.nom as categorie_nom
            FROM produits p
            LEFT JOIN categories c ON p.categorie_id = c.id
            WHERE p.nom LIKE ? OR p.code LIKE ?
            ORDER BY p.nom
        """
        terme_like = f"%{terme}%"
        return [dict(row) for row in db.fetch_all(query, (terme_like, terme_like))]

    @staticmethod
    def obtenir_stock_faible(seuil):
        """
        Obtenir les produits avec un stock faible

        Args:
            seuil (int): Seuil de stock

        Returns:
            list: Liste des produits en stock faible
        """
        query = """
            SELECT p.*, c.nom as categorie_nom
            FROM produits p
            LEFT JOIN categories c ON p.categorie_id = c.id
            WHERE p.quantite <= ?
            ORDER BY p.quantite ASC
        """
        return [dict(row) for row in db.fetch_all(query, (seuil,))]

    @staticmethod
    def mettre_a_jour_quantite(produit_id, nouvelle_quantite):
        """
        Mettre à jour la quantité d'un produit

        Args:
            produit_id (int): ID du produit
            nouvelle_quantite (int): Nouvelle quantité

        Returns:
            int: ID du produit
        """
        query = "UPDATE produits SET quantite = ? WHERE id = ?"
        return db.execute_query(query, (nouvelle_quantite, produit_id))

    @staticmethod
    def ajuster_quantite(produit_id, delta):
        """
        Ajuster la quantité d'un produit (ajouter ou retirer)

        Args:
            produit_id (int): ID du produit
            delta (int): Quantité à ajouter (positif) ou retirer (négatif)

        Returns:
            int: ID du produit
        """
        query = "UPDATE produits SET quantite = quantite + ? WHERE id = ?"
        return db.execute_query(query, (delta, produit_id))
