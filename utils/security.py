"""
Fonctions de sécurité pour l'application AGIB
"""
import bcrypt


def hash_password(password):
    """
    Hacher un mot de passe avec bcrypt

    Args:
        password (str): Mot de passe en clair

    Returns:
        str: Mot de passe haché
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(password, hashed_password):
    """
    Vérifier un mot de passe contre son hash

    Args:
        password (str): Mot de passe en clair
        hashed_password (str): Mot de passe haché

    Returns:
        bool: True si le mot de passe correspond, False sinon
    """
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
