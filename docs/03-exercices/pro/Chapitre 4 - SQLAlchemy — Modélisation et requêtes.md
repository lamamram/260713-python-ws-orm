## Exercice 1 — Modéliser un domaine avec SQLAlchemy

Vous devez modéliser le schéma de données d'une plateforme de cours en ligne.

**Entités à modéliser :**

- `Formateur` : id, nom, email (unique), specialite, date_inscription
- `Cours` : id, titre, description, prix (décimal exact 10,2), duree_heures, publie (bool), date_creation, formateur_id (FK)
- `Stagiaire` : id, nom, email (unique), date_inscription
- `Inscription` : table d'association n-à-n entre Cours et Stagiaire, avec `date_inscription` et `note` (entier 0-20, optionnel)

**Travail à réaliser :**

1. Créer `models.py` avec les quatre modèles SQLAlchemy 2.0
2. Configurer `database.py` avec un Engine SQLite et une Session
3. Créer les tables avec `Base.metadata.create_all()`
4. Initialiser Alembic et générer la migration initiale
5. Vérifier le schéma créé avec un outil SQLite (DB Browser for SQLite ou la commande `sqlite3`)

**Critères de validation :**

- `alembic upgrade head` s'exécute sans erreur
- Toutes les relations `relationship()` sont définies et accessibles des deux côtés
- `Numeric(10, 2)` est utilisé pour le prix
- La table `Inscription` est une table d'association avec des colonnes supplémentaires (`date_inscription`, `note`)

## Exercice 2 — Requêtes CRUD

Écrivez un script Python `seed.py` qui peuple la base et effectue des requêtes.

**Opérations à implémenter :**

1. Créer 2 formateurs, 3 cours, 4 stagiaires
2. Inscrire 3 stagiaires au cours 1 et 2 stagiaires au cours 2
3. Lister tous les cours publiés triés par prix croissant
4. Compter le nombre d'inscrits par cours
5. Trouver tous les stagiaires inscrits à un cours donné

**Critères de validation :**

- Le script `python seed.py` s'exécute sans erreur
- Chaque opération utilise la syntaxe SQLAlchemy ORM 2.0 (`select(...)`)
- La requête de comptage utilise `func.count()`
