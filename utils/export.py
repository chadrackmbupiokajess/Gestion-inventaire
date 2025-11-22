"""
Fonctions d'export en format .txt pour l'application AGIB
"""
import os
from datetime import datetime
from config import EXPORT_DIR, EXPORT_ENCODING, EXPORT_SEPARATOR, BOUTIQUE_NOM
from models.produit import Produit
from models.vente import Vente
from models.achat import Achat
from database.db_manager import db


class ExportManager:
    """Classe pour gérer les exports en format .txt"""

    @staticmethod
    def _generer_nom_fichier(prefix):
        """
        Générer un nom de fichier avec timestamp

        Args:
            prefix (str): Préfixe du nom de fichier

        Returns:
            str: Nom de fichier complet
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.txt"

    @staticmethod
    def _ecrire_entete(f, titre):
        """
        Écrire l'en-tête du fichier

        Args:
            f: Fichier ouvert
            titre (str): Titre du rapport
        """
        f.write("=" * 80 + "\n")
        f.write(f"{BOUTIQUE_NOM} - {titre}\n")
        f.write(f"Date de génération: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")

    @staticmethod
    def exporter_inventaire():
        """
        Exporter l'inventaire complet en format .txt

        Returns:
            str: Chemin du fichier exporté
        """
        nom_fichier = ExportManager._generer_nom_fichier("INVENTAIRE")
        chemin_fichier = os.path.join(EXPORT_DIR, nom_fichier)

        produits = Produit.obtenir_tous()

        with open(chemin_fichier, 'w', encoding=EXPORT_ENCODING) as f:
            ExportManager._ecrire_entete(f, "INVENTAIRE COMPLET")

            # En-tête des colonnes
            colonnes = ["CODE", "NOM", "QTE", "PRIX_VENTE", "PRIX_ACHAT", "CATEGORIE", "DATE_EXP"]
            f.write(EXPORT_SEPARATOR.join(colonnes) + "\n")
            f.write("-" * 80 + "\n")

            # Données des produits
            for produit in produits:
                ligne = [
                    produit['code'],
                    produit['nom'],
                    str(produit['quantite']),
                    f"{produit['prix_vente']:.2f}",
                    f"{produit['prix_achat']:.2f}",
                    produit['categorie_nom'] if produit['categorie_nom'] else "N/A",
                    produit['date_expiration'] if produit['date_expiration'] else "N/A"
                ]
                f.write(EXPORT_SEPARATOR.join(ligne) + "\n")

            # Statistiques
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"TOTAL PRODUITS: {len(produits)}\n")
            valeur_stock = sum(p['quantite'] * p['prix_achat'] for p in produits)
            f.write(f"VALEUR TOTALE DU STOCK: {valeur_stock:.2f}\n")

        return chemin_fichier

    @staticmethod
    def exporter_ventes_journalieres(date=None):
        """
        Exporter les ventes journalières en format .txt

        Args:
            date (str, optional): Date au format YYYY-MM-DD. Si None, utilise la date du jour

        Returns:
            str: Chemin du fichier exporté
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        nom_fichier = f"VENTES_{date.replace('-', '')}.txt"
        chemin_fichier = os.path.join(EXPORT_DIR, nom_fichier)

        ventes = Vente.obtenir_par_jour(date)
        total = Vente.calculer_total_jour(date)

        with open(chemin_fichier, 'w', encoding=EXPORT_ENCODING) as f:
            ExportManager._ecrire_entete(f, f"VENTES DU {date}")

            # En-tête des colonnes
            colonnes = ["HEURE", "CODE", "PRODUIT", "QTE", "PRIX_UNIT", "TOTAL", "VENDEUR"]
            f.write(EXPORT_SEPARATOR.join(colonnes) + "\n")
            f.write("-" * 80 + "\n")

            # Données des ventes
            for vente in ventes:
                heure = datetime.fromisoformat(vente['date']).strftime("%H:%M:%S")
                ligne = [
                    heure,
                    vente['produit_code'],
                    vente['produit_nom'],
                    str(vente['quantite']),
                    f"{vente['prix_unitaire']:.2f}",
                    f"{vente['montant_total']:.2f}",
                    vente['utilisateur_nom']
                ]
                f.write(EXPORT_SEPARATOR.join(ligne) + "\n")

            # Total
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"NOMBRE DE VENTES: {len(ventes)}\n")
            f.write(f"TOTAL DES VENTES: {total:.2f}\n")

        return chemin_fichier

    @staticmethod
    def exporter_produits_rupture(seuil):
        """
        Exporter les produits en rupture de stock

        Args:
            seuil (int): Seuil de stock faible

        Returns:
            str: Chemin du fichier exporté
        """
        nom_fichier = ExportManager._generer_nom_fichier("RUPTURE_STOCK")
        chemin_fichier = os.path.join(EXPORT_DIR, nom_fichier)

        produits = Produit.obtenir_stock_faible(seuil)

        with open(chemin_fichier, 'w', encoding=EXPORT_ENCODING) as f:
            ExportManager._ecrire_entete(f, f"PRODUITS EN RUPTURE (Seuil: {seuil})")

            # En-tête des colonnes
            colonnes = ["CODE", "NOM", "QTE_ACTUELLE", "CATEGORIE"]
            f.write(EXPORT_SEPARATOR.join(colonnes) + "\n")
            f.write("-" * 80 + "\n")

            # Données des produits
            for produit in produits:
                ligne = [
                    produit['code'],
                    produit['nom'],
                    str(produit['quantite']),
                    produit['categorie_nom'] if produit['categorie_nom'] else "N/A"
                ]
                f.write(EXPORT_SEPARATOR.join(ligne) + "\n")

            # Total
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"TOTAL PRODUITS EN RUPTURE: {len(produits)}\n")

        return chemin_fichier

    @staticmethod
    def exporter_journal(date_debut=None, date_fin=None):
        """
        Exporter le journal des opérations

        Args:
            date_debut (str, optional): Date de début (ISO format)
            date_fin (str, optional): Date de fin (ISO format)

        Returns:
            str: Chemin du fichier exporté
        """
        nom_fichier = ExportManager._generer_nom_fichier("JOURNAL")
        chemin_fichier = os.path.join(EXPORT_DIR, nom_fichier)

        # Requête pour obtenir le journal
        if date_debut and date_fin:
            query = """
                SELECT j.*, u.nom as utilisateur_nom
                FROM journal j
                LEFT JOIN utilisateurs u ON j.utilisateur_id = u.id
                WHERE j.date BETWEEN ? AND ?
                ORDER BY j.date DESC
            """
            journal = db.fetch_all(query, (date_debut, date_fin))
        else:
            query = """
                SELECT j.*, u.nom as utilisateur_nom
                FROM journal j
                LEFT JOIN utilisateurs u ON j.utilisateur_id = u.id
                ORDER BY j.date DESC
            """
            journal = db.fetch_all(query)

        with open(chemin_fichier, 'w', encoding=EXPORT_ENCODING) as f:
            ExportManager._ecrire_entete(f, "JOURNAL DES OPERATIONS")

            # En-tête des colonnes
            colonnes = ["DATE", "HEURE", "ACTION", "UTILISATEUR", "DETAILS"]
            f.write(EXPORT_SEPARATOR.join(colonnes) + "\n")
            f.write("-" * 80 + "\n")

            # Données du journal
            for entry in journal:
                dt = datetime.fromisoformat(entry['date'])
                ligne = [
                    dt.strftime("%Y-%m-%d"),
                    dt.strftime("%H:%M:%S"),
                    entry['action'],
                    entry['utilisateur_nom'] if entry['utilisateur_nom'] else "N/A",
                    entry['details'] if entry['details'] else ""
                ]
                f.write(EXPORT_SEPARATOR.join(ligne) + "\n")

            # Total
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"TOTAL OPERATIONS: {len(journal)}\n")

        return chemin_fichier

    @staticmethod
    def generer_ticket_vente(vente_id):
        """
        Générer un ticket de vente en format .txt

        Args:
            vente_id (int): ID de la vente

        Returns:
            str: Chemin du fichier exporté
        """
        nom_fichier = f"TICKET_{vente_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        chemin_fichier = os.path.join(EXPORT_DIR, nom_fichier)

        # Obtenir les détails de la vente
        query = """
            SELECT v.*, p.nom as produit_nom, p.code as produit_code, u.nom as utilisateur_nom
            FROM ventes v
            JOIN produits p ON v.produit_id = p.id
            JOIN utilisateurs u ON v.utilisateur_id = u.id
            WHERE v.id = ?
        """
        vente = db.fetch_one(query, (vente_id,))

        if not vente:
            raise ValueError("Vente introuvable")

        with open(chemin_fichier, 'w', encoding=EXPORT_ENCODING) as f:
            # En-tête du ticket
            f.write("=" * 50 + "\n")
            f.write(f"{BOUTIQUE_NOM}\n")
            f.write("TICKET DE VENTE\n")
            f.write("=" * 50 + "\n\n")

            # Informations de la vente
            dt = datetime.fromisoformat(vente['date'])
            f.write(f"Date: {dt.strftime('%d/%m/%Y')}\n")
            f.write(f"Heure: {dt.strftime('%H:%M:%S')}\n")
            f.write(f"Vendeur: {vente['utilisateur_nom']}\n")
            f.write(f"Ticket N°: {vente_id}\n\n")

            # Détails du produit
            f.write("-" * 50 + "\n")
            f.write(f"Produit: {vente['produit_nom']}\n")
            f.write(f"Code: {vente['produit_code']}\n")
            f.write(f"Quantité: {vente['quantite']}\n")
            f.write(f"Prix unitaire: {vente['prix_unitaire']:.2f}\n")
            f.write("-" * 50 + "\n\n")

            # Total
            f.write(f"TOTAL: {vente['montant_total']:.2f}\n\n")
            f.write("=" * 50 + "\n")
            f.write("Merci de votre visite!\n")
            f.write("=" * 50 + "\n")

        return chemin_fichier

    @staticmethod
    def generer_ticket_panier(ventes_ids):
        """
        Générer un ticket pour plusieurs ventes (panier)

        Args:
            ventes_ids (list): Liste des IDs de ventes

        Returns:
            str: Chemin du fichier exporté
        """
        nom_fichier = f"TICKET_PANIER_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        chemin_fichier = os.path.join(EXPORT_DIR, nom_fichier)

        # Obtenir les détails de toutes les ventes
        placeholders = ','.join('?' * len(ventes_ids))
        query = f"""
            SELECT v.*, p.nom as produit_nom, p.code as produit_code, u.nom as utilisateur_nom
            FROM ventes v
            JOIN produits p ON v.produit_id = p.id
            JOIN utilisateurs u ON v.utilisateur_id = u.id
            WHERE v.id IN ({placeholders})
            ORDER BY v.id
        """
        ventes = db.fetch_all(query, ventes_ids)

        if not ventes:
            raise ValueError("Ventes introuvables")

        with open(chemin_fichier, 'w', encoding=EXPORT_ENCODING) as f:
            # En-tête du ticket
            f.write("=" * 50 + "\n")
            f.write(f"{BOUTIQUE_NOM}\n")
            f.write("TICKET DE VENTE\n")
            f.write("=" * 50 + "\n\n")

            # Informations générales
            dt = datetime.fromisoformat(ventes[0]['date'])
            f.write(f"Date: {dt.strftime('%d/%m/%Y')}\n")
            f.write(f"Heure: {dt.strftime('%H:%M:%S')}\n")
            f.write(f"Vendeur: {ventes[0]['utilisateur_nom']}\n")
            f.write(f"Ticket N°: {ventes[0]['id']}\n\n")

            # Détails des produits
            f.write("-" * 50 + "\n")
            f.write("ARTICLES:\n")
            f.write("-" * 50 + "\n")

            total_general = 0
            for vente in ventes:
                f.write(f"\n{vente['produit_nom']} ({vente['produit_code']})\n")
                f.write(f"  Quantité: {vente['quantite']} x {vente['prix_unitaire']:.2f}\n")
                f.write(f"  Sous-total: {vente['montant_total']:.2f}\n")
                total_general += vente['montant_total']

            f.write("\n" + "-" * 50 + "\n")

            # Total
            f.write(f"\nNOMBRE D'ARTICLES: {len(ventes)}\n")
            f.write(f"TOTAL A PAYER: {total_general:.2f}\n\n")
            f.write("=" * 50 + "\n")
            f.write("Merci de votre visite!\n")
            f.write("=" * 50 + "\n")

        return chemin_fichier
