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
import io

class ExportManager:
    """Classe pour gérer les exports en format .txt"""

    @staticmethod
    def _generer_nom_fichier(prefix):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.txt"

    @staticmethod
    def _ecrire_entete(f, titre):
        f.write("=" * 80 + "\n")
        f.write(f"{BOUTIQUE_NOM} - {titre}\n")
        f.write(f"Date de génération: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")

    # --- Fonctions de génération de contenu ---

    @staticmethod
    def generer_contenu_inventaire():
        produits = Produit.obtenir_tous()
        output = io.StringIO()
        ExportManager._ecrire_entete(output, "INVENTAIRE COMPLET")
        colonnes = ["CODE", "NOM", "QTE", "PRIX_VENTE", "PRIX_ACHAT", "CATEGORIE", "DATE_EXP"]
        output.write(EXPORT_SEPARATOR.join(colonnes) + "\n")
        output.write("-" * 80 + "\n")
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
            output.write(EXPORT_SEPARATOR.join(ligne) + "\n")
        output.write("\n" + "=" * 80 + "\n")
        output.write(f"TOTAL PRODUITS: {len(produits)}\n")
        valeur_stock = sum(p['quantite'] * p['prix_achat'] for p in produits)
        output.write(f"VALEUR TOTALE DU STOCK: {valeur_stock:.2f}\n")
        return output.getvalue()

    @staticmethod
    def generer_contenu_ventes_journalieres(date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        ventes = Vente.obtenir_par_jour(date)
        total = Vente.calculer_total_jour(date)
        output = io.StringIO()
        ExportManager._ecrire_entete(output, f"VENTES DU {date}")
        colonnes = ["HEURE", "CODE", "PRODUIT", "QTE", "PRIX_UNIT", "TOTAL", "VENDEUR"]
        output.write(EXPORT_SEPARATOR.join(colonnes) + "\n")
        output.write("-" * 80 + "\n")
        for vente in ventes:
            heure = datetime.fromisoformat(vente['date']).strftime("%H:%M:%S")
            ligne = [heure, vente['produit_code'], vente['produit_nom'], str(vente['quantite']), f"{vente['prix_unitaire']:.2f}", f"{vente['montant_total']:.2f}", vente['utilisateur_nom']]
            output.write(EXPORT_SEPARATOR.join(ligne) + "\n")
        output.write("\n" + "=" * 80 + "\n")
        output.write(f"NOMBRE DE VENTES: {len(ventes)}\n")
        output.write(f"TOTAL DES VENTES: {total:.2f}\n")
        return output.getvalue()

    @staticmethod
    def generer_contenu_produits_rupture(seuil):
        produits = Produit.obtenir_stock_faible(seuil)
        output = io.StringIO()
        ExportManager._ecrire_entete(output, f"PRODUITS EN RUPTURE (Seuil: {seuil})")
        colonnes = ["CODE", "NOM", "QTE_ACTUELLE", "CATEGORIE"]
        output.write(EXPORT_SEPARATOR.join(colonnes) + "\n")
        output.write("-" * 80 + "\n")
        for produit in produits:
            ligne = [produit['code'], produit['nom'], str(produit['quantite']), produit['categorie_nom'] if produit['categorie_nom'] else "N/A"]
            output.write(EXPORT_SEPARATOR.join(ligne) + "\n")
        output.write("\n" + "=" * 80 + "\n")
        output.write(f"TOTAL PRODUITS EN RUPTURE: {len(produits)}\n")
        return output.getvalue()

    @staticmethod
    def generer_contenu_journal(date_debut=None, date_fin=None):
        if date_debut and date_fin:
            query = "SELECT j.*, u.nom as utilisateur_nom FROM journal j LEFT JOIN utilisateurs u ON j.utilisateur_id = u.id WHERE j.date BETWEEN ? AND ? ORDER BY j.date DESC"
            journal = db.fetch_all(query, (date_debut, date_fin))
        else:
            query = "SELECT j.*, u.nom as utilisateur_nom FROM journal j LEFT JOIN utilisateurs u ON j.utilisateur_id = u.id ORDER BY j.date DESC"
            journal = db.fetch_all(query)
        output = io.StringIO()
        ExportManager._ecrire_entete(output, "JOURNAL DES OPERATIONS")
        colonnes = ["DATE", "HEURE", "ACTION", "UTILISATEUR", "DETAILS"]
        output.write(EXPORT_SEPARATOR.join(colonnes) + "\n")
        output.write("-" * 80 + "\n")
        for entry in journal:
            dt = datetime.fromisoformat(entry['date'])
            ligne = [dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S"), entry['action'], entry['utilisateur_nom'] if entry['utilisateur_nom'] else "N/A", entry['details'] if entry['details'] else ""]
            output.write(EXPORT_SEPARATOR.join(ligne) + "\n")
        output.write("\n" + "=" * 80 + "\n")
        output.write(f"TOTAL OPERATIONS: {len(journal)}\n")
        return output.getvalue()

    # --- Fonctions d'export de fichier ---

    @staticmethod
    def exporter_inventaire():
        contenu = ExportManager.generer_contenu_inventaire()
        nom_fichier = ExportManager._generer_nom_fichier("INVENTAIRE")
        chemin_fichier = os.path.join(EXPORT_DIR, nom_fichier)
        with open(chemin_fichier, 'w', encoding=EXPORT_ENCODING) as f:
            f.write(contenu)
        return chemin_fichier

    @staticmethod
    def exporter_ventes_journalieres(date=None):
        contenu = ExportManager.generer_contenu_ventes_journalieres(date)
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        nom_fichier = f"VENTES_{date.replace('-', '')}.txt"
        chemin_fichier = os.path.join(EXPORT_DIR, nom_fichier)
        with open(chemin_fichier, 'w', encoding=EXPORT_ENCODING) as f:
            f.write(contenu)
        return chemin_fichier

    @staticmethod
    def exporter_produits_rupture(seuil):
        contenu = ExportManager.generer_contenu_produits_rupture(seuil)
        nom_fichier = ExportManager._generer_nom_fichier("RUPTURE_STOCK")
        chemin_fichier = os.path.join(EXPORT_DIR, nom_fichier)
        with open(chemin_fichier, 'w', encoding=EXPORT_ENCODING) as f:
            f.write(contenu)
        return chemin_fichier

    @staticmethod
    def exporter_journal(date_debut=None, date_fin=None):
        contenu = ExportManager.generer_contenu_journal(date_debut, date_fin)
        nom_fichier = ExportManager._generer_nom_fichier("JOURNAL")
        chemin_fichier = os.path.join(EXPORT_DIR, nom_fichier)
        with open(chemin_fichier, 'w', encoding=EXPORT_ENCODING) as f:
            f.write(contenu)
        return chemin_fichier

    @staticmethod
    def generer_ticket_vente(vente_id):
        # Cette fonction reste inchangée car elle est spécifique à un ticket
        nom_fichier = f"TICKET_{vente_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        chemin_fichier = os.path.join(EXPORT_DIR, nom_fichier)
        query = "SELECT v.*, p.nom as produit_nom, p.code as produit_code, u.nom as utilisateur_nom FROM ventes v JOIN produits p ON v.produit_id = p.id JOIN utilisateurs u ON v.utilisateur_id = u.id WHERE v.id = ?"
        vente = db.fetch_one(query, (vente_id,))
        if not vente:
            raise ValueError("Vente introuvable")
        with open(chemin_fichier, 'w', encoding=EXPORT_ENCODING) as f:
            f.write("=" * 50 + "\n")
            f.write(f"{BOUTIQUE_NOM}\n")
            f.write("TICKET DE VENTE\n")
            f.write("=" * 50 + "\n\n")
            dt = datetime.fromisoformat(vente['date'])
            f.write(f"Date: {dt.strftime('%d/%m/%Y')}\n")
            f.write(f"Heure: {dt.strftime('%H:%M:%S')}\n")
            f.write(f"Vendeur: {vente['utilisateur_nom']}\n")
            f.write(f"Ticket N°: {vente_id}\n\n")
            f.write("-" * 50 + "\n")
            f.write(f"Produit: {vente['produit_nom']}\n")
            f.write(f"Code: {vente['produit_code']}\n")
            f.write(f"Quantité: {vente['quantite']}\n")
            f.write(f"Prix unitaire: {vente['prix_unitaire']:.2f}\n")
            f.write("-" * 50 + "\n\n")
            f.write(f"TOTAL: {vente['montant_total']:.2f}\n\n")
            f.write("=" * 50 + "\n")
            f.write("Merci de votre visite!\n")
            f.write("=" * 50 + "\n")
        return chemin_fichier

    @staticmethod
    def generer_ticket_panier(ventes_ids):
        # Cette fonction reste inchangée
        nom_fichier = f"TICKET_PANIER_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        chemin_fichier = os.path.join(EXPORT_DIR, nom_fichier)
        placeholders = ','.join('?' * len(ventes_ids))
        query = f"SELECT v.*, p.nom as produit_nom, p.code as produit_code, u.nom as utilisateur_nom FROM ventes v JOIN produits p ON v.produit_id = p.id JOIN utilisateurs u ON v.utilisateur_id = u.id WHERE v.id IN ({placeholders}) ORDER BY v.id"
        ventes = db.fetch_all(query, ventes_ids)
        if not ventes:
            raise ValueError("Ventes introuvables")
        with open(chemin_fichier, 'w', encoding=EXPORT_ENCODING) as f:
            f.write("=" * 50 + "\n")
            f.write(f"{BOUTIQUE_NOM}\n")
            f.write("TICKET DE VENTE\n")
            f.write("=" * 50 + "\n\n")
            dt = datetime.fromisoformat(ventes[0]['date'])
            f.write(f"Date: {dt.strftime('%d/%m/%Y')}\n")
            f.write(f"Heure: {dt.strftime('%H:%M:%S')}\n")
            f.write(f"Vendeur: {ventes[0]['utilisateur_nom']}\n")
            f.write(f"Ticket N°: {ventes[0]['id']}\n\n")
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
            f.write(f"\nNOMBRE D'ARTICLES: {len(ventes)}\n")
            f.write(f"TOTAL A PAYER: {total_general:.2f}\n\n")
            f.write("=" * 50 + "\n")
            f.write("Merci de votre visite!\n")
            f.write("=" * 50 + "\n")
        return chemin_fichier
