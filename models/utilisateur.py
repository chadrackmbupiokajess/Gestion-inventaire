"""
Modèle Utilisateur
"""
from datetime import datetime
from database.db_manager import db
from utils.security import hash_password, verify_password


class Utilisateur:
    """Classe pour gérer les utilisateurs"""

    @staticmethod
    def authentifier(nom, mot_de_passe):
        """
        Authentifier un utilisateur

        Args:
            nom (str): Nom d'utilisateur
            mot_de_passe (str): Mot de passe

        Returns:
            dict: Informations utilisateur si authentification réussie, None sinon
        """
        query = "SELECT * FROM utilisateurs WHERE nom = ?"
        user = db.fetch_one(query, (nom,))

        if user and verify_password(mot_de_passe, user['mot_de_passe']):
            return dict(user)
        return None

    @staticmethod
    def creer(nom, role, mot_de_passe):
        """
        Créer un nouvel utilisateur

        Args:
            nom (str): Nom d'utilisateur
            role (str): Rôle (Administrateur ou Vendeur)
            mot_de_passe (str): Mot de passe

        Returns:
            int: ID du nouvel utilisateur
        """
        hashed_pwd = hash_password(mot_de_passe)
        query = """
            INSERT INTO utilisateurs (nom, role, mot_de_passe, date_creation)
            VALUES (?, ?, ?, ?)
        """
        return db.execute_query(query, (nom, role, hashed_pwd, datetime.now().isoformat()))

    @staticmethod
    def modifier_mot_de_passe(utilisateur_id, nouveau_mot_de_passe):
        """
        Modifier le mot de passe d'un utilisateur

        Args:
            utilisateur_id (int): ID de l'utilisateur
            nouveau_mot_de_passe (str): Nouveau mot de passe

        Returns:
            int: ID de l'utilisateur
        """
        hashed_pwd = hash_password(nouveau_mot_de_passe)
        query = "UPDATE utilisateurs SET mot_de_passe = ? WHERE id = ?"
        return db.execute_query(query, (hashed_pwd, utilisateur_id))

    @staticmethod
    def obtenir_tous():
        """
        Obtenir tous les utilisateurs

        Returns:
            list: Liste des utilisateurs
        """
        query = "SELECT id, nom, role, date_creation FROM utilisateurs ORDER BY nom"
        return [dict(row) for row in db.fetch_all(query)]

    @staticmethod
    def obtenir_par_id(utilisateur_id):
        """
        Obtenir un utilisateur par son ID

        Args:
            utilisateur_id (int): ID de l'utilisateur

        Returns:
            dict: Informations de l'utilisateur
        """
        query = "SELECT id, nom, role, date_creation FROM utilisateurs WHERE id = ?"
        result = db.fetch_one(query, (utilisateur_id,))
        return dict(result) if result else None

    @staticmethod
    def supprimer(utilisateur_id):
        """
        Supprimer un utilisateur

        Args:
            utilisateur_id (int): ID de l'utilisateur

        Returns:
            int: ID de l'utilisateur supprimé
        """
        query = "DELETE FROM utilisateurs WHERE id = ?"
        return db.execute_query(query, (utilisateur_id,))
