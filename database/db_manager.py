"""
Gestionnaire de base de données SQLite pour l'application AGIB
"""
import sqlite3
import os
from datetime import datetime
from config import DB_PATH


class DatabaseManager:
    """Classe pour gérer toutes les opérations de base de données"""

    def __init__(self):
        self.db_path = DB_PATH
        self.init_database()

    def get_connection(self):
        """Créer une connexion à la base de données"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
        return conn

    def init_database(self):
        """Initialiser la base de données avec le schéma"""
        # Lire le schéma SQL
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')

        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        # Créer les tables
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.executescript(schema_sql)
        conn.commit()

        # Vérifier si un utilisateur admin existe, sinon le créer
        cursor.execute("SELECT COUNT(*) as count FROM utilisateurs WHERE role = 'Administrateur'")
        result = cursor.fetchone()

        if result['count'] == 0:
            # Créer un utilisateur admin par défaut
            from utils.security import hash_password
            hashed_pwd = hash_password('admin123')
            cursor.execute(
                "INSERT INTO utilisateurs (nom, role, mot_de_passe, date_creation) VALUES (?, ?, ?, ?)",
                ('admin', 'Administrateur', hashed_pwd, datetime.now().isoformat())
            )
            conn.commit()
            print("Utilisateur administrateur par défaut créé (admin/admin123)")

        conn.close()

    def execute_query(self, query, params=None):
        """Exécuter une requête SQL (INSERT, UPDATE, DELETE)"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            last_id = cursor.lastrowid
            conn.close()
            return last_id
        except sqlite3.Error as e:
            conn.close()
            raise e

    def fetch_all(self, query, params=None):
        """Récupérer tous les résultats d'une requête SELECT"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            conn.close()
            return results
        except sqlite3.Error as e:
            conn.close()
            raise e

    def fetch_one(self, query, params=None):
        """Récupérer un seul résultat d'une requête SELECT"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            return result
        except sqlite3.Error as e:
            conn.close()
            raise e

    def log_action(self, action, utilisateur_id, details=""):
        """Enregistrer une action dans le journal"""
        query = """
            INSERT INTO journal (action, date, utilisateur_id, details)
            VALUES (?, ?, ?, ?)
        """
        self.execute_query(query, (action, datetime.now().isoformat(), utilisateur_id, details))


# Instance globale du gestionnaire de base de données
db = DatabaseManager()
