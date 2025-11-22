"""
Modèle Achat (entrées de stock)
"""
from datetime import datetime
from database.db_manager import db
from models.produit import Produit


class Achat:
    """Classe pour gérer les achats (entrées de stock)"""

    @staticmethod
    def creer(produit_id, quantite, fournisseur, utilisateur_id):
        """
        Enregistrer un achat et mettre à jour le stock

        Args:
            produit_id (int): ID du produit
            quantite (int): Quantité achetée
            fournisseur (str): Nom du fournisseur
            utilisateur_id (int): ID de l'utilisateur

        Returns:
            int: ID du nouvel achat
        """
        # Enregistrer l'achat
        query = """
            INSERT INTO achats (produit_id, quantite, date, fournisseur, utilisateur_id)
            VALUES (?, ?, ?, ?, ?)
        """
        achat_id = db.execute_query(query, (produit_id, quantite, datetime.now().isoformat(),
                                            fournisseur, utilisateur_id))

        # Mettre à jour le stock
        Produit.ajuster_quantite(produit_id, quantite)

        # Logger l'action
        produit = Produit.obtenir_par_id(produit_id)
        details = f"Achat: {produit['nom']} - Quantité: {quantite} - Fournisseur: {fournisseur}"
        db.log_action("ACHAT", utilisateur_id, details)

        return achat_id

    @staticmethod
    def obtenir_tous():
        """
        Obtenir tous les achats

        Returns:
            list: Liste des achats
        """
        query = """
            SELECT a.*, p.nom as produit_nom, p.code as produit_code, u.nom as utilisateur_nom
            FROM achats a
            JOIN produits p ON a.produit_id = p.id
            JOIN utilisateurs u ON a.utilisateur_id = u.id
            ORDER BY a.date DESC
        """
        return [dict(row) for row in db.fetch_all(query)]

    @staticmethod
    def obtenir_par_periode(date_debut, date_fin):
        """
        Obtenir les achats pour une période donnée

        Args:
            date_debut (str): Date de début (ISO format)
            date_fin (str): Date de fin (ISO format)

        Returns:
            list: Liste des achats
        """
        query = """
            SELECT a.*, p.nom as produit_nom, p.code as produit_code, u.nom as utilisateur_nom
            FROM achats a
            JOIN produits p ON a.produit_id = p.id
            JOIN utilisateurs u ON a.utilisateur_id = u.id
            WHERE a.date BETWEEN ? AND ?
            ORDER BY a.date DESC
        """
        return [dict(row) for row in db.fetch_all(query, (date_debut, date_fin))]

    @staticmethod
    def obtenir_par_produit(produit_id):
        """
        Obtenir les achats pour un produit spécifique

        Args:
            produit_id (int): ID du produit

        Returns:
            list: Liste des achats
        """
        query = """
            SELECT a.*, p.nom as produit_nom, p.code as produit_code, u.nom as utilisateur_nom
            FROM achats a
            JOIN produits p ON a.produit_id = p.id
            JOIN utilisateurs u ON a.utilisateur_id = u.id
            WHERE a.produit_id = ?
            ORDER BY a.date DESC
        """
        return [dict(row) for row in db.fetch_all(query, (produit_id,))]
