-- Schéma de base de données pour l'application AGIB
-- Base de données SQLite

-- Table des catégories
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE
);

-- Table des produits
CREATE TABLE IF NOT EXISTS produits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    prix_achat REAL NOT NULL,
    prix_vente REAL NOT NULL,
    quantite INTEGER NOT NULL DEFAULT 0,
    categorie_id INTEGER,
    date_expiration TEXT,
    date_creation TEXT NOT NULL,
    FOREIGN KEY (categorie_id) REFERENCES categories(id)
);

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL CHECK(role IN ('Administrateur', 'Vendeur')),
    mot_de_passe TEXT NOT NULL,
    date_creation TEXT NOT NULL
);

-- Table des achats (entrées de stock)
CREATE TABLE IF NOT EXISTS achats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produit_id INTEGER NOT NULL,
    quantite INTEGER NOT NULL,
    date TEXT NOT NULL,
    fournisseur TEXT,
    utilisateur_id INTEGER NOT NULL,
    FOREIGN KEY (produit_id) REFERENCES produits(id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
);

-- Table des ventes (sorties de stock)
CREATE TABLE IF NOT EXISTS ventes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produit_id INTEGER NOT NULL,
    quantite INTEGER NOT NULL,
    prix_unitaire REAL NOT NULL,
    montant_total REAL NOT NULL,
    date TEXT NOT NULL,
    utilisateur_id INTEGER NOT NULL,
    FOREIGN KEY (produit_id) REFERENCES produits(id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
);

-- Table du journal des opérations
CREATE TABLE IF NOT EXISTS journal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    date TEXT NOT NULL,
    utilisateur_id INTEGER,
    details TEXT,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
);

-- Index pour améliorer les performances
CREATE INDEX IF NOT EXISTS idx_produits_code ON produits(code);
CREATE INDEX IF NOT EXISTS idx_produits_categorie ON produits(categorie_id);
CREATE INDEX IF NOT EXISTS idx_ventes_date ON ventes(date);
CREATE INDEX IF NOT EXISTS idx_achats_date ON achats(date);
CREATE INDEX IF NOT EXISTS idx_journal_date ON journal(date);
