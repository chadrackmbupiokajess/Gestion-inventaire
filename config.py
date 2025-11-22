# Configuration de l'application AGIB
import os

# Chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'agib.db')
EXPORT_DIR = os.path.join(BASE_DIR, 'exports')

# Créer le dossier d'export s'il n'existe pas
if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)

# Informations boutique
BOUTIQUE_NOM = "AGIB"
BOUTIQUE_ADRESSE = "Votre adresse"

# Paramètres de sécurité
MIN_PASSWORD_LENGTH = 4

# Paramètres d'alerte stock
SEUIL_STOCK_FAIBLE = 10

# Format d'export
EXPORT_ENCODING = 'utf-8'
EXPORT_SEPARATOR = '\t'
