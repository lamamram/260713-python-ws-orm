# Chapitre 5 — Quiz : SQLAlchemy avancé et intégration avec FastAPI

1. En quoi consiste le problème des **N+1 requêtes** avec un ORM ?
   - A) Une requête retourne N résultats au lieu du résultat attendu
   - B) Une première requête charge N entités, puis N requêtes supplémentaires chargent les relations de chacune
   - C) L'ORM exécute la même requête N fois à cause d'un bug de cache
   - D) La session limite à N+1 le nombre de connexions simultanées

2. Quelle stratégie d'eager loading est la plus adaptée pour charger une relation **to-one** (ex. `article.auteur`) ?
   - A) `selectinload()`
   - B) `lazyload()`
   - C) `joinedload()`
   - D) `subqueryload()`

3. Pourquoi utiliser `.unique()` après un `joinedload()` sur une relation to-many avant `.scalars().all()` ?
   - A) Pour éliminer les doublons de l'objet parent générés par le JOIN
   - B) Pour forcer SQLAlchemy à utiliser un index
   - C) Pour limiter le résultat à un seul objet
   - D) `.unique()` est requis pour toutes les requêtes SQLAlchemy 2.0

4. Dans la dépendance `get_db()`, pourquoi placer `db.close()` dans un bloc `finally` ?
   - A) Pour améliorer les performances du pool de connexions
   - B) Pour s'assurer que la session est fermée même si une exception est levée pendant le traitement de la requête
   - C) `finally` est requis par le protocole `yield` de FastAPI
   - D) Pour committer automatiquement les transactions en attente

5. Que fait `model_config = ConfigDict(from_attributes=True)` dans un modèle Pydantic utilisé avec SQLAlchemy ?
   - A) Permet à Pydantic de lire les attributs d'un objet Python quelconque (pas seulement un dict)
   - B) Active la validation stricte des types SQLAlchemy
   - C) Configure Pydantic pour se connecter directement à la base de données
   - D) Remplace SQLAlchemy pour la sérialisation JSON

6. Pourquoi est-il préférable d'encoder l'`id` de l'utilisateur (et non le `username`) dans le payload JWT ?
   - A) L'`id` est plus court et réduit la taille du jeton
   - B) L'`id` ne change jamais, contrairement au `username` qui peut être modifié
   - C) Le `username` ne peut pas être encodé en JSON
   - D) FastAPI impose d'utiliser l'`id` dans les jetons JWT

7. Dans `crud/articles.py`, pourquoi extraire les fonctions CRUD des gestionnaires FastAPI dans un module séparé ?
   - A) FastAPI l'impose pour les projets avec SQLAlchemy
   - B) Pour respecter la séparation des responsabilités et faciliter les tests unitaires
   - C) Pour améliorer les performances des requêtes SQL
   - D) Pour éviter d'importer SQLAlchemy dans les routeurs

8. Quelle configuration de la base de données de test est recommandée pour les tests pytest avec FastAPI et SQLAlchemy ?
   - A) Utiliser la même base de données que la production pour des tests réalistes
   - B) Utiliser une base SQLite en mémoire (`sqlite:///:memory:`) réinitialisée pour chaque test
   - C) Mocker entièrement SQLAlchemy avec `unittest.mock`
   - D) Utiliser une base PostgreSQL dédiée aux tests

9. Dans Docker Compose, à quoi sert la condition `service_healthy` dans le bloc `depends_on` du service `api` ?
   - A) À vérifier que l'image Docker de l'API est à jour
   - B) À attendre que PostgreSQL soit prêt à accepter des connexions avant de démarrer l'API
   - C) À redémarrer automatiquement l'API si elle plante
   - D) À limiter les ressources CPU du service

10. Quel est l'avantage principal de `selectinload()` sur `joinedload()` pour charger une collection (relation to-many) ?
    - A) `selectinload` est plus rapide car il utilise un cache interne
    - B) `selectinload` génère un `IN` propre sur les IDs, évitant la duplication de lignes du parent que le JOIN produit
    - C) `selectinload` supporte les transactions distribuées
    - D) `joinedload` ne fonctionne pas avec PostgreSQL

## Corrections

1. **B) Une première requête charge N entités, puis N requêtes supplémentaires chargent les relations** — Le problème N+1 est la conséquence du lazy loading dans une boucle : 1 requête pour la liste + N requêtes individuelles pour les relations de chaque entité (section "Le syndrome des N+1 requêtes").
2. **C) `joinedload()`** — Pour une relation to-one, le JOIN est efficace : il ajoute des colonnes à chaque ligne mais ne multiplie pas le nombre de lignes. `selectinload` est préférable pour les collections (section "Eager loading — charger les relations en avance").
3. **A) Pour éliminer les doublons de l'objet parent générés par le JOIN** — Un JOIN avec une relation to-many duplique les lignes du parent (1 ligne par enfant). `unique()` déduplique les objets Python résultants (section "Eager loading").
4. **B) Pour s'assurer que la session est fermée même si une exception est levée** — `try/finally` garantit la fermeture de la session dans tous les cas de figure, évitant les fuites de connexions (section "Session par requête avec Depends").
5. **A) Permet à Pydantic de lire les attributs d'un objet Python quelconque** — Sans `from_attributes=True`, Pydantic ne sait lire que des dictionnaires. Cette option lui permet de lire les attributs d'instances SQLAlchemy (section "Schémas Pydantic compatibles avec SQLAlchemy").
6. **B) L'`id` ne change jamais, contrairement au `username`** — Encoder un identifiant immuable dans le JWT garantit que le jeton reste valide si l'utilisateur change son `username` (section "Authentification avec base de données").
7. **B) Pour respecter la séparation des responsabilités et faciliter les tests unitaires** — Les fonctions CRUD dans `crud/` peuvent être testées indépendamment des routes HTTP, en passant directement une session de test (section "Couche de données — CRUD functions").
8. **B) Utiliser une base SQLite en mémoire réinitialisée pour chaque test** — `sqlite:///:memory:` crée une base éphémère ultra-rapide, réinitialisée entre les tests, sans impact sur les données de développement (section "Tests d'intégration avec base de données").
9. **B) À attendre que PostgreSQL soit prêt avant de démarrer l'API** — `service_healthy` attend que le `healthcheck` (`pg_isready`) passe, évitant que l'API tente de se connecter à une base qui n'est pas encore prête (section "Déploiement avec Docker Compose").
10. **B) `selectinload` génère un `IN` propre évitant la duplication de lignes** — Avec `joinedload` sur une collection, chaque ligne parente est dupliquée pour chaque enfant dans le résultat SQL, nécessitant `unique()`. `selectinload` fait deux requêtes propres et SQLAlchemy assemble les objets en mémoire (section "Eager loading").
