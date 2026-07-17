# Glossaire — Python Avancé : FastAPI + ORM

> Glossaire vivant enrichi au fil des chapitres. Version actuelle : couvre les Chapitres 1 à 5.

**Alembic** — Outil de migration de schéma de base de données pour SQLAlchemy. Génère des fichiers de migration versionnés et permet d'appliquer (`upgrade`) ou d'annuler (`downgrade`) les changements de schéma.

**ASGI (Asynchronous Server Gateway Interface)** — Interface Python pour les serveurs web asynchrones, successeur de WSGI. Permet la gestion concurrente des connexions via `async`/`await`.

**Authentification** — Processus vérifiant l'identité d'un appelant ("Qui êtes-vous ?"). Distinct de l'autorisation. Dans cette formation : vérification du jeton JWT.

**Autorisation** — Processus vérifiant qu'une identité authentifiée possède les droits nécessaires ("Avez-vous le droit ?"). Distinct de l'authentification. Codes HTTP : 403 Forbidden.

**BackgroundTasks** — Mécanisme FastAPI pour exécuter des fonctions après que la réponse HTTP a été envoyée au client, dans le même processus. Adapté aux tâches légères non critiques.

**Base déclarative (`DeclarativeBase`)** — Classe de base SQLAlchemy dont héritent les modèles ORM. Maintient le registre des tables et génère les métadonnées.

**CORS (Cross-Origin Resource Sharing)** — Mécanisme de sécurité des navigateurs contrôlant les requêtes vers des domaines différents. Configuré dans FastAPI via `CORSMiddleware`.

**Dépendance (`Depends`)** — Mécanisme FastAPI d'injection de dépendances. Une fonction déclarée avec `Depends()` est appelée automatiquement avant le gestionnaire et son résultat lui est injecté.

**Eager loading** — Stratégie de chargement des relations SQLAlchemy qui charge les objets liés en même temps que l'objet principal, évitant le N+1. Deux variantes : `joinedload()` et `selectinload()`.

**Engine** — Objet SQLAlchemy représentant la connexion à la base de données. Encapsule la chaîne de connexion et gère le pool de connexions.

**FastAPI** — Framework web Python asynchrone (ASGI) créé en 2018. Fondé sur Starlette (routage, middleware) et Pydantic (validation). Génère automatiquement la documentation OpenAPI.

**ForeignKey** — Contrainte SQL référençant la colonne d'une autre table. Définit le côté "many" d'une relation dans SQLAlchemy.

**Gestionnaire (handler)** — Fonction Python associée à une route FastAPI via un décorateur d'opération (`@app.get`, `@app.post`…). Contient la logique métier de l'endpoint.

**GraphQL** — Langage de requête pour API permettant au client de choisir les champs retournés. Alternative à REST pour les interfaces riches.

**Gunicorn** — Gestionnaire de processus Python qui lance plusieurs workers Uvicorn en production pour utiliser tous les CPU disponibles.

**HTTPException** — Exception FastAPI à lever pour retourner une réponse HTTP d'erreur structurée (`{"detail": "..."}`) avec le code de statut approprié.

**Idempotence** — Propriété d'une opération dont le résultat est identique qu'elle soit exécutée une ou plusieurs fois. GET, PUT et DELETE sont idempotents ; POST ne l'est pas.

**Impedance objet-relationnel** — Décalage conceptuel entre le modèle objet (classes, attributs, méthodes) et le modèle relationnel (tables, lignes, colonnes). Les ORM réduisent ce décalage.

**JWT (JSON Web Token)** — Jeton signé numériquement encodant un payload JSON. Composé de trois parties : header + payload + signature. Le payload est encodé en Base64 (pas chiffré).

**joinedload()** — Stratégie SQLAlchemy d'eager loading qui charge une relation via un JOIN dans la requête principale. Efficace pour les relations to-one.

**Lazy loading** — Comportement par défaut des relations SQLAlchemy : les objets liés ne sont chargés que lors de l'accès à l'attribut de relation, déclenchant une requête SQL supplémentaire.

**mapped_column** — Syntaxe SQLAlchemy 2.0 pour définir une colonne de modèle avec annotation de type Python. Remplace `Column()` dans la syntaxe héritée.

**Middleware** — Couche de traitement interposée entre la réception d'une requête et le gestionnaire. Gère les préoccupations transversales : CORS, logging, authentification globale.

**Mapped[type]** — Annotation SQLAlchemy 2.0 indiquant le type Python d'un attribut mappé sur une colonne ou une relation.

**Migration** — Script versionné décrivant une modification du schéma de base de données (ajout de colonne, création de table…). Géré par Alembic.

**N+1 (syndrome des N+1 requêtes)** — Problème de performance ORM : 1 requête pour charger N entités + N requêtes pour charger les relations de chacune = N+1 requêtes au total. Résolu par l'eager loading.

**OAuth2 Password Flow** — Flux d'authentification OAuth2 où le client envoie directement l'identifiant et le mot de passe pour obtenir un jeton d'accès. Implémenté avec `OAuth2PasswordBearer` dans FastAPI.

**OpenAPI** — Spécification ouverte pour décrire des API REST (anciennement Swagger). FastAPI génère automatiquement une spécification OpenAPI 3.0 à partir des annotations de type.

**ORM (Object-Relational Mapper)** — Bibliothèque qui établit une correspondance entre classes Python et tables de base de données, gérant la conversion et les requêtes SQL.

**Pydantic** — Bibliothèque Python de validation de données par annotation de type. Utilisée par FastAPI pour valider les entrées et sérialiser les sorties des endpoints.

**relationship()** — Directive SQLAlchemy ORM définissant une association navigable entre deux modèles. Ne crée pas de colonne — utilise la `ForeignKey` existante.

**REST (Representational State Transfer)** — Style architectural pour les API HTTP défini par Roy Fielding en 2000. Caractérisé par : interface uniforme, sans état, ressources identifiées par URL.

**response_model** — Paramètre des décorateurs FastAPI définissant le modèle Pydantic utilisé pour sérialiser et filtrer la réponse. Garantit qu'aucun champ non autorisé n'est exposé.

**secondary** — Paramètre de `relationship()` indiquant la table d'association pour une relation n-à-n.

**selectinload()** — Stratégie SQLAlchemy d'eager loading qui charge une collection via une requête `IN` séparée. Efficace pour les relations to-many.

**Session** — Objet SQLAlchemy représentant une "conversation" avec la base de données. Gère le cycle de vie des objets (transient, pending, persistent, detached) et les transactions.

**SOAP (Simple Object Access Protocol)** — Protocole de Web Services basé sur XML, défini par le W3C en 1998. Rigoureux et formel, utilisé dans les systèmes d'entreprise legacy.

**Starlette** — Framework ASGI Python sur lequel FastAPI est fondé. Fournit le routage, le middleware, les WebSockets et le TestClient.

**TestClient** — Client HTTP de test fourni par FastAPI (fondé sur `httpx`) qui appelle l'application directement en mémoire sans ouvrir de port TCP.

**Unit of Work** — Patron de conception implémenté par la Session SQLAlchemy : les modifications des objets persistants sont trackées et envoyées à la base en une seule transaction au `commit()`.

**Uvicorn** — Serveur ASGI Python hautes performances fondé sur `uvloop` et `httptools`. Serveur de référence pour FastAPI en développement et en production.

**WSGI (Web Server Gateway Interface)** — Interface Python historique pour les serveurs web synchrones. Flask et Django (mode classique) utilisent WSGI. Remplacé par ASGI pour les applications asynchrones.
