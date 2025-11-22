"""
Modèle Vente (sorties de stock)
"""
from datetime import datetime
from database.db_manager import db
from models.produit import Produit


class Vente:
    """Classe pour gérer les ventes (sorties de stock)"""

    @staticmethod
    def creer(produit_id, quantite, prix_unitaire, utilisateur_id):
        """
        Enregistrer une vente et mettre à jour le stock

        Args:
            produit_id (int): ID du produit
            quantite (int): Quantité vendue
            prix_unitaire (float): Prix unitaire de vente
            utilisateur_id (int): ID de l'utilisateur

        Returns:
            int: ID de la nouvelle vente
        """
        # Vérifier le stock disponible
        produit = Produit.obtenir_par_id(produit_id)
        if not produit:
            raise ValueError("Produit introuvable")

        if produit['quantite'] < quantite:
            raise ValueError(f"Stock insuffisant. Disponible: {produit['quantite']}")

        # Calculer le montant total
        montant_total = quantite * prix_unitaire

        # Enregistrer la vente
        query = """
            INSERT INTO ventes (produit_id, quantite, prix_unitaire, montant_total, date, utilisateur_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        vente_id = db.execute_query(query, (produit_id, quantite, prix_unitaire, montant_total,
                                            datetime.now().isoformat(), utilisateur_id))

        # Mettre à jour le stock (retirer la quantité)
        Produit.ajuster_quantite(produit_id, -quantite)

        # Logger l'action
        details = f"Vente: {produit['nom']} - Quantité: {quantite} - Montant: {montant_total}"
        db.log_action("VENTE", utilisateur_id, details)

        return vente_id

    @staticmethod
    def obtenir_toutes():
        """
        Obtenir toutes les ventes

        Returns:
            list: Liste des ventes
        """
        query = """
            SELECT v.*, p.nom as produit_nom, p.code as produit_code, u.nom as utilisateur_nom
            FROM ventes v
            JOIN produits p ON v.produit_id = p.id
            JOIN utilisateurs u ON v.utilisateur_id = u.id
            ORDER BY v.date DESC
        """
        return [dict(row) for row in db.fetch_all(query)]

    @staticmethod
    def obtenir_par_periode(date_debut, date_fin):
        """
        Obtenir les ventes pour une période donnée

        Args:
            date_debut (str): Date de début (ISO format)
            date_fin (str): Date de fin (ISO format)

        Returns:
            list: Liste des ventes
        """
        query = """
            SELECT v.*, p.nom as produit_nom, p.code as produit_code, u.nom as utilisateur_nom
            FROM ventes v
            JOIN produits p ON v.produit_id = p.id
            JOIN utilisateurs u ON v.utilisateur_id = u.id
            WHERE v.date BETWEEN ? AND ?
            ORDER BY v.date DESC
        """
        return [dict(row) for row in db.fetch_all(query, (date_debut, date_fin))]

    @staticmethod
    def obtenir_par_jour(date):
        """
        Obtenir les ventes pour un jour spécifique

        Args:
            date (str): Date (format YYYY-MM-DD)

        Returns:
            list: Liste des ventes
        """
        date_debut = f"{date}T00:00:00"
        date_fin = f"{date}T23:59:59"
        return Vente.obtenir_par_periode(date_debut, date_fin)

    @staticmethod
    def calculer_total_jour(date):
        """
        Calculer le total des ventes pour un jour

        Args:
            date (str): Date (format YYYY-MM-DD)

        Returns:
            float: Total des ventes
        """
        date_debut = f"{date}T00:00:00"
        date_fin = f"{date}T23:59:59"
        query = """
            SELECT SUM(montant_total) as total
            FROM ventes
            WHERE date BETWEEN ? AND ?
        """
        result = db.fetch_one(query, (date_debut, date_fin))
        return result['total'] if result['total'] else 0.0

    @staticmethod
    def obtenir_par_produit(produit_id):
        """
        Obtenir les ventes pour un produit spécifique

        Args:
            produit_id (int): ID du produit

        Returns:
            list: Liste des ventes
        """
        query = """
            SELECT v.*, p.nom as produit_nom, p.code as produit_code, u.nom as utilisateur_nom
            FROM ventes v
            JOIN produits p ON v.produit_id = p.id
            JOIN utilisateurs u ON v.utilisateur_id = u.id
            WHERE v.produit_id = ?
            ORDER BY v.date DESC
        """
        return [dict(row) for row in db.fetch_all(query, (produit_id,))]
