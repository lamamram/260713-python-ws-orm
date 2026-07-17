# Chapitre 1 — Quiz : Découverte de FastAPI et des Web Services

1. Quel style architectural a été décrit par Roy Fielding dans sa thèse de doctorat en 2000 et est aujourd'hui la base de la grande majorité des API publiques ?
   - A) SOAP
   - B) GraphQL
   - C) REST
   - D) RPC

2. Parmi les propositions suivantes, laquelle décrit correctement une opération **idempotente** ?
   - A) `POST /articles` — crée un nouvel article à chaque appel
   - B) `DELETE /articles/42` — supprime l'article 42, résultat identique peu importe le nombre d'appels
   - C) `PATCH /articles/42` — met à jour partiellement l'article 42, résultat variable
   - D) `POST /paiements` — débite le compte client à chaque appel

3. Quel code de statut HTTP FastAPI retourne-t-il automatiquement quand la validation Pydantic d'un paramètre d'entrée échoue ?
   - A) 400 Bad Request
   - B) 404 Not Found
   - C) 422 Unprocessable Entity
   - D) 500 Internal Server Error

4. Sur quelle URL Swagger UI est-il disponible par défaut dans une application FastAPI démarrée sur `localhost:8000` ?
   - A) `http://localhost:8000/swagger`
   - B) `http://localhost:8000/api-docs`
   - C) `http://localhost:8000/docs`
   - D) `http://localhost:8000/openapi`

5. Quelle bibliothèque Python est responsable de la validation automatique des données d'entrée dans FastAPI ?
   - A) Marshmallow
   - B) WTForms
   - C) Cerberus
   - D) Pydantic

6. Quelle commande installe FastAPI avec le serveur Uvicorn et les dépendances standard de développement ?
   - A) `pip install fastapi`
   - B) `pip install "fastapi[standard]"`
   - C) `pip install fastapi uvicorn --extras`
   - D) `pip install fastapi-full`

7. Quelle est la différence fondamentale entre `401 Unauthorized` et `403 Forbidden` ?
   - A) `401` est pour les erreurs de syntaxe JSON, `403` pour les erreurs de validation
   - B) `401` indique que l'utilisateur n'est pas authentifié, `403` qu'il est authentifié mais non autorisé
   - C) `401` est retourné par le client, `403` par le serveur
   - D) Ils sont interchangeables selon le framework

8. Dans FastAPI, que représente l'annotation `: int` dans `def get_article(article_id: int)` ?
   - A) Un commentaire Python sans effet sur le comportement
   - B) Une indication qui force FastAPI à extraire et convertir `article_id` depuis l'URL, et à retourner 422 si la conversion échoue
   - C) Une restriction qui empêche le déploiement si le type ne correspond pas
   - D) Une métadonnée de documentation sans validation

9. Quel serveur ASGI est recommandé et installé par défaut avec `fastapi[standard]` ?
   - A) Gunicorn
   - B) Waitress
   - C) Uvicorn
   - D) Hypercorn

10. Dans le contexte FastAPI, que signifie le sigle **ASGI** ?
    - A) Asynchronous Server Gateway Interface
    - B) Advanced Server Group Interface
    - C) Application Service Gateway Integration
    - D) Asynchronous Standard General Interface

## Corrections

1. **C) REST** — Roy Fielding a décrit REST (Representational State Transfer) dans sa thèse en 2000. SOAP est une norme W3C née en 1998, GraphQL a été créé par Facebook en 2012 (section "Web Services — du SOAP au REST").
2. **B) `DELETE /articles/42`** — L'idempotence signifie que répéter l'opération donne le même résultat : l'article 42 est absent, que l'appel soit fait une ou dix fois. `POST` crée à chaque appel — il n'est pas idempotent (section "Les méthodes HTTP et leur sémantique").
3. **C) 422 Unprocessable Entity** — FastAPI retourne automatiquement un `422` avec un corps JSON détaillé quand la validation Pydantic échoue sur les paramètres d'entrée, sans que le développeur n'écrive de code de gestion d'erreur (section "Explorer la documentation Swagger").
4. **C) `http://localhost:8000/docs`** — FastAPI expose Swagger UI sur `/docs` et ReDoc sur `/redoc` par défaut (section "Swagger UI et ReDoc").
5. **D) Pydantic** — Pydantic (v2 depuis FastAPI 0.100) est la bibliothèque de validation et de sérialisation de données intégrée à FastAPI (section "Architecture interne de FastAPI").
6. **B) `pip install "fastapi[standard]"`** — Les guillemets sont nécessaires dans la plupart des shells ; l'extra `[standard]` installe Uvicorn, httpx et les autres dépendances recommandées (section "Prérequis et installation").
7. **B) `401` indique que l'utilisateur n'est pas authentifié, `403` qu'il est authentifié mais non autorisé** — `401` concerne l'authentification (jeton absent ou invalide) ; `403` concerne l'autorisation (identité connue, mais permission refusée) (section "Les codes de statut HTTP essentiels").
8. **B) Une indication qui force FastAPI à extraire et convertir `article_id` depuis l'URL, et à retourner 422 si la conversion échoue** — FastAPI utilise les annotations de type Python pour la validation automatique des paramètres (section "Premier fichier main.py").
9. **C) Uvicorn** — Uvicorn est le serveur ASGI recommandé, fondé sur `uvloop` et `httptools`, installé via `fastapi[standard]` (section "Architecture interne de FastAPI").
10. **A) Asynchronous Server Gateway Interface** — ASGI est le successeur asynchrone de WSGI, permettant aux frameworks Python de gérer des connexions concurrentes efficacement (section "Architecture interne de FastAPI").
