# Chapitre 3 — Quiz : Sécurité, dépendances et déploiement FastAPI

1. Dans FastAPI, que fait `Depends(get_token)` passé comme valeur par défaut d'un paramètre ?
   - A) Il documente que le paramètre vient de l'en-tête HTTP `Token`
   - B) Il demande à FastAPI d'appeler `get_token()` avant le gestionnaire et d'injecter son résultat
   - C) Il rend le paramètre optionnel dans Swagger UI
   - D) Il désactive la validation Pydantic pour ce paramètre

2. Quelle partie d'un JWT peut être lue par n'importe qui sans la clé secrète ?
   - A) Aucune — tout le JWT est chiffré avec la clé secrète
   - B) Uniquement le header
   - C) Le header et le payload — ils sont seulement encodés en Base64
   - D) Uniquement la signature

3. Quelle commande génère une clé secrète aléatoire sécurisée pour `SECRET_KEY` ?
   - A) `python -c "import uuid; print(uuid.uuid4())"`
   - B) `openssl rand -hex 32`
   - C) `fastapi generate-key`
   - D) `python -m secrets`

4. Quel middleware FastAPI permet d'autoriser les appels cross-origin depuis un frontend sur un domaine différent ?
   - A) `AuthMiddleware`
   - B) `CORSMiddleware`
   - C) `ProxyMiddleware`
   - D) `SecurityMiddleware`

5. Quand doit-on utiliser `BackgroundTasks` au lieu d'une file de messages (Celery) ?
   - A) Toujours — BackgroundTasks est plus performant que Celery
   - B) Pour des tâches courtes, non critiques, exécutées dans le même processus FastAPI
   - C) Pour des tâches qui doivent être rejouées en cas d'échec du serveur
   - D) Uniquement pour l'envoi de métriques

6. Dans `pytest`, quel objet FastAPI permet d'appeler l'application directement en mémoire, sans serveur HTTP ?
   - A) `FastAPIClient`
   - B) `RequestsMock`
   - C) `TestClient`
   - D) `MockApp`

7. Comment remplacer une dépendance FastAPI par un mock dans les tests ?
   - A) `app.mock_dependency(dep, mock_func)`
   - B) `app.dependency_overrides[dep] = mock_func`
   - C) `pytest.mock.patch(dep, mock_func)`
   - D) `app.replace_depends(dep, mock_func)`

8. Pourquoi utiliser Gunicorn avec Uvicorn en production plutôt qu'Uvicorn seul ?
   - A) Gunicorn gère le HTTPS, Uvicorn non
   - B) Uvicorn seul est limité à HTTP/1.1, Gunicorn ajoute HTTP/2
   - C) Uvicorn seul est monoprocessus ; Gunicorn lance plusieurs workers Uvicorn pour utiliser tous les CPU
   - D) Gunicorn est requis pour que les middlewares FastAPI fonctionnent

9. Quelle est la différence entre `401 Unauthorized` et `403 Forbidden` dans le contexte de l'authentification JWT ?
   - A) `401` : jeton absent ou invalide (non authentifié) ; `403` : jeton valide mais permissions insuffisantes
   - B) `401` : mot de passe incorrect ; `403` : compte suspendu
   - C) `401` : erreur côté serveur ; `403` : erreur côté client
   - D) Ils sont équivalents dans FastAPI

10. Quel outil de FastAPI permet de charger la configuration (`SECRET_KEY`, `DATABASE_URL`) depuis des variables d'environnement ou un fichier `.env` ?
    - A) `fastapi.Config`
    - B) `os.environ` directement dans le code
    - C) `pydantic_settings.BaseSettings`
    - D) `dotenv.load_env()`

## Corrections

1. **B) Il demande à FastAPI d'appeler `get_token()` avant le gestionnaire et d'injecter son résultat** — `Depends()` est le mécanisme d'injection de dépendances de FastAPI. La fonction dépendance est appelée automatiquement, son résultat est injecté dans le paramètre (section "Principe de l'injection de dépendances").
2. **C) Le header et le payload — ils sont seulement encodés en Base64** — Un JWT n'est pas chiffré, seulement signé. Le header et le payload sont encodés en Base64 URL et lisibles par n'importe qui. Seule la signature nécessite la clé secrète pour être vérifiée (section "JWT — JSON Web Token").
3. **B) `openssl rand -hex 32`** — Génère 32 octets aléatoires cryptographiquement forts en hexadécimal. Python `uuid4` est aléatoire mais pas conçu pour les secrets cryptographiques (section "Implémentation complète — OAuth2 Password Flow").
4. **B) `CORSMiddleware`** — `from fastapi.middleware.cors import CORSMiddleware` est le middleware fourni par FastAPI/Starlette pour gérer les en-têtes CORS (section "CORS — Cross-Origin Resource Sharing").
5. **B) Pour des tâches courtes, non critiques, exécutées dans le même processus FastAPI** — `BackgroundTasks` est léger et simple mais les tâches sont perdues si le processus redémarre. Pour des tâches critiques ou longues, utiliser Celery (section "Tâches de fond — BackgroundTasks").
6. **C) `TestClient`** — `from fastapi.testclient import TestClient` est le client de test fourni par FastAPI, fondé sur `httpx`, qui appelle l'application directement en mémoire (section "Tests avec pytest et TestClient").
7. **B) `app.dependency_overrides[dep] = mock_func`** — `dependency_overrides` est un dictionnaire sur l'instance `FastAPI` qui permet de substituer n'importe quelle dépendance par une version de test (section "Remplacer des dépendances dans les tests").
8. **C) Uvicorn seul est monoprocessus ; Gunicorn lance plusieurs workers Uvicorn pour utiliser tous les CPU** — Uvicorn est un excellent serveur ASGI mais monoprocessus. Gunicorn le lance en plusieurs instances parallèles (section "Dockerfile pour FastAPI").
9. **A) `401` : jeton absent ou invalide (non authentifié) ; `403` : jeton valide mais permissions insuffisantes** — `401` signifie "je ne sais pas qui vous êtes" ; `403` signifie "je sais qui vous êtes mais vous n'avez pas le droit" (section "Authentification OAuth2 et JWT").
10. **C) `pydantic_settings.BaseSettings`** — `pydantic-settings` (package séparé depuis Pydantic v2) fournit `BaseSettings` qui charge les champs depuis les variables d'environnement ou un fichier `.env` (section "Variables d'environnement et configuration").
