# Manuel d'Utilisation - Application AGIB

## Table des matières
1. [Installation](#installation)
2. [Première utilisation](#première-utilisation)
3. [Connexion](#connexion)
4. [Tableau de bord](#tableau-de-bord)
5. [Gestion des utilisateurs](#gestion-des-utilisateurs)
6. [Gestion des produits](#gestion-des-produits)
7. [Gestion des ventes](#gestion-des-ventes)
8. [Gestion des achats](#gestion-des-achats)
9. [Rapports et exports](#rapports-et-exports)
10. [Conseils et bonnes pratiques](#conseils-et-bonnes-pratiques)
11. [Dépannage](#dépannage)

---

## Installation

### Prérequis
- Python 3.7 ou supérieur
- Windows 10 ou supérieur

### Étapes d'installation

1. **Installer Python** (si ce n'est pas déjà fait)
   - Télécharger depuis https://www.python.org/downloads/
   - Cocher "Add Python to PATH" lors de l'installation

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application**
   ```bash
   python main.py
   ```

---

## Première utilisation

### Compte administrateur par défaut
Lors du premier lancement, un compte administrateur est créé automatiquement :
- **Identifiant** : `admin`
- **Mot de passe** : `admin123`

⚠️ **IMPORTANT** : Changez ce mot de passe dès la première connexion pour des raisons de sécurité !

---

## Connexion

### Se connecter
1. Entrez votre nom d'utilisateur
2. Entrez votre mot de passe
3. Cliquez sur "Se connecter" ou appuyez sur Entrée

### Rôles utilisateurs
- **Administrateur** : Accès complet à toutes les fonctionnalités
- **Vendeur** : Accès aux ventes et consultation du stock

---

## Tableau de bord

Le tableau de bord affiche :
- **Total produits** : Nombre total de produits en stock
- **Ventes du jour** : Montant total des ventes de la journée
- **Produits en rupture** : Nombre de produits avec un stock faible (≤ 10)
- **Valeur du stock** : Valeur totale du stock (quantité × prix d'achat)

### Navigation
Cliquez sur les boutons pour accéder aux différentes sections :
- **Gestion des Produits** : Ajouter, modifier, supprimer des produits
- **Gestion des Ventes** : Enregistrer des ventes
- **Gestion des Achats** : Enregistrer des achats (entrées de stock)
- **Rapports & Exports** : Générer et exporter des rapports
- **Gestion des Utilisateurs** : Créer et gérer les comptes (Administrateur uniquement)

---

## Gestion des utilisateurs

⚠️ **Cette section est accessible uniquement aux Administrateurs**

### Créer un nouvel utilisateur
1. Cliquez sur "Gestion des Utilisateurs" dans le tableau de bord
2. Cliquez sur "Ajouter Utilisateur"
3. Remplissez les informations :
   - **Nom d'utilisateur** : Identifiant unique (obligatoire)
   - **Rôle** : Administrateur ou Vendeur
   - **Mot de passe** : Minimum 4 caractères (obligatoire)
   - **Confirmer mot de passe** : Doit correspondre au mot de passe
4. Cliquez sur "Créer"

### Changer le mot de passe d'un utilisateur
1. Dans la liste des utilisateurs, trouvez l'utilisateur concerné
2. Cliquez sur "Changer mot de passe"
3. Entrez le nouveau mot de passe (minimum 4 caractères)
4. Confirmez le nouveau mot de passe
5. Cliquez sur "Modifier"

**Note** : Vous pouvez changer votre propre mot de passe ou celui de n'importe quel utilisateur si vous êtes administrateur.

### Supprimer un utilisateur
1. Dans la liste des utilisateurs, trouvez l'utilisateur à supprimer
2. Cliquez sur "Supprimer"
3. Confirmez la suppression

⚠️ **Attention** :
- Vous ne pouvez pas supprimer votre propre compte
- La suppression est définitive et irréversible

### Différences entre les rôles

#### Administrateur
- Accès complet à toutes les fonctionnalités
- Peut gérer les utilisateurs (créer, modifier, supprimer)
- Peut gérer les produits
- Peut enregistrer des ventes et des achats
- Peut générer des rapports

#### Vendeur
- Peut consulter les produits
- Peut enregistrer des ventes
- Peut consulter les ventes
- **Ne peut pas** gérer les utilisateurs
- **Ne peut pas** modifier les produits
- **Ne peut pas** enregistrer des achats

---

## Gestion des produits

### Ajouter un produit
1. Cliquez sur "Ajouter Produit"
2. Remplissez les informations :
   - **Nom** : Nom du produit (obligatoire)
   - **Code** : Code unique du produit (obligatoire)
   - **Prix d'achat** : Prix d'achat unitaire
   - **Prix de vente** : Prix de vente unitaire
   - **Quantité** : Quantité initiale en stock
   - **Catégorie** : Catégorie du produit (optionnel)
   - **Date d'expiration** : Format YYYY-MM-DD (optionnel)
3. Cliquez sur "Sauvegarder"

### Modifier un produit
1. Trouvez le produit dans la liste
2. Cliquez sur "Modifier"
3. Modifiez les informations souhaitées
4. Cliquez sur "Sauvegarder"

### Supprimer un produit
1. Trouvez le produit dans la liste
2. Cliquez sur "Supprimer"
3. Confirmez la suppression

### Rechercher un produit
Utilisez la barre de recherche pour trouver un produit par nom ou code.

---

## Gestion des ventes

### Enregistrer une vente
1. Cliquez sur "Nouvelle Vente"
2. Sélectionnez le produit dans la liste déroulante
3. Entrez la quantité vendue
4. Le prix unitaire est automatiquement rempli (modifiable si nécessaire)
5. Le total est calculé automatiquement
6. Cliquez sur "Valider la vente"
7. Vous pouvez ensuite exporter le ticket de vente

### Consulter les ventes
- L'écran affiche toutes les ventes du jour
- Chaque vente montre : produit, quantité, prix, total, vendeur, heure
- Les statistiques du jour sont affichées en haut

### Exporter un ticket de vente
Cliquez sur "Ticket" à côté d'une vente pour générer un fichier .txt du ticket.

---

## Gestion des achats

### Enregistrer un achat
1. Cliquez sur "Nouvel Achat"
2. Sélectionnez le produit
3. Entrez la quantité achetée
4. Entrez le nom du fournisseur (optionnel)
5. Le nouveau stock est calculé automatiquement
6. Cliquez sur "Valider l'achat"

Le stock du produit est automatiquement mis à jour.

### Consulter les achats
L'écran affiche tous les achats enregistrés avec :
- Produit
- Quantité
- Fournisseur
- Date et heure
- Utilisateur ayant enregistré l'achat

---

## Rapports et exports

### Exports rapides

#### Inventaire complet
- Exporte tous les produits avec leurs informations
- Fichier : `INVENTAIRE_YYYYMMDD_HHMMSS.txt`
- Contient : code, nom, quantité, prix, catégorie, date d'expiration

#### Ventes du jour
- Exporte toutes les ventes de la journée
- Fichier : `VENTES_YYYYMMDD.txt`
- Contient : heure, produit, quantité, prix, total, vendeur

#### Produits en rupture
- Exporte les produits avec un stock ≤ 10
- Fichier : `RUPTURE_STOCK_YYYYMMDD_HHMMSS.txt`
- Utile pour planifier les commandes

#### Journal des opérations
- Exporte toutes les opérations effectuées
- Fichier : `JOURNAL_YYYYMMDD_HHMMSS.txt`
- Contient : date, heure, action, utilisateur, détails

### Export personnalisé

#### Ventes par date
1. Entrez une date au format YYYY-MM-DD
2. Cliquez sur "Exporter"
3. Le fichier contient toutes les ventes de cette date

### Localisation des fichiers
Tous les fichiers exportés sont sauvegardés dans le dossier `exports/` à la racine de l'application.

---

## Conseils et bonnes pratiques

### Sécurité
- Changez le mot de passe par défaut immédiatement
- Créez des comptes séparés pour chaque vendeur
- Ne partagez jamais vos identifiants

### Gestion du stock
- Vérifiez régulièrement les produits en rupture
- Exportez l'inventaire quotidiennement pour archivage
- Utilisez des codes produits uniques et cohérents

### Sauvegardes
- Exportez l'inventaire au format .txt chaque jour
- Sauvegardez le fichier `agib.db` régulièrement
- Conservez les exports dans un lieu sûr (clé USB, cloud, etc.)

### Performance
- L'application peut gérer plusieurs milliers de produits
- Nettoyez périodiquement les anciennes données si nécessaire
- Fermez l'application correctement (ne pas forcer la fermeture)

---

## Dépannage

### L'application ne démarre pas
- Vérifiez que Python est installé : `python --version`
- Vérifiez que les dépendances sont installées : `pip install -r requirements.txt`
- Vérifiez les messages d'erreur dans la console

### Impossible de se connecter
- Vérifiez que vous utilisez les bons identifiants
- Utilisez le compte par défaut : admin / admin123
- Vérifiez que le fichier `agib.db` existe

### Erreur lors d'une vente
- Vérifiez que le stock est suffisant
- Vérifiez que la quantité et le prix sont valides
- Assurez-vous d'être connecté

### Erreur lors d'un export
- Vérifiez que le dossier `exports/` existe
- Vérifiez les permissions d'écriture
- Fermez les fichiers .txt s'ils sont ouverts

### Le stock ne se met pas à jour
- Vérifiez que la vente/achat a bien été validé
- Actualisez la liste des produits
- Redémarrez l'application si nécessaire

### Problèmes d'affichage
- Redimensionnez la fenêtre
- Redémarrez l'application
- Vérifiez la résolution de votre écran

---

## Support

Pour toute question ou problème non résolu :
1. Consultez le fichier README.md
2. Vérifiez le cahier des charges
3. Contactez l'administrateur système

---

## Raccourcis clavier

- **Entrée** : Valider la connexion (écran de connexion)
- **Échap** : Fermer les popups
- **Tab** : Naviguer entre les champs

---

## Formats de fichiers

### Format des exports .txt
- **Encodage** : UTF-8
- **Séparateur** : Tabulation (TAB)
- **Format de date** : YYYY-MM-DD
- **Format d'heure** : HH:MM:SS

### Exemple de ligne d'inventaire
```
CODE001	Produit Test	50	15.99	12.50	Catégorie A	2025-12-31
```

---

**Version** : 1.0
**Date** : 2025
**Application** : AGIB - Gestion d'Inventaire pour Boutique
