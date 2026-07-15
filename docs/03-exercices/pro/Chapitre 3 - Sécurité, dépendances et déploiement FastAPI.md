## Exercice 1 — Sécuriser une API avec JWT

Reprenez l'API de tâches du Chapitre 2 et ajoutez une couche d'authentification JWT complète.

**Travail à réaliser :**

1. Installez `python-jose[cryptography]`, `passlib[bcrypt]` et `pydantic-settings`
2. Créez un module `auth.py` avec :
   - Deux utilisateurs en mémoire (`alice`/`secret` non-admin, `bob`/`admin123` admin)
   - Un endpoint `POST /auth/token` retournant un JWT
   - Une dépendance `get_current_user` qui valide le JWT
   - Une dépendance `require_admin` qui vérifie le rôle admin
3. Protégez les routes :
   - `GET /taches` et `GET /taches/{id}` — utilisateur authentifié uniquement
   - `DELETE /taches/{id}` — administrateur uniquement
   - `POST /taches` et `PATCH /taches/{id}` — utilisateur authentifié

**Critères de validation :**

- `POST /auth/token` avec les bons credentials retourne un JWT
- `GET /taches` sans jeton retourne `401`
- `GET /taches` avec le jeton d'alice retourne `200`
- `DELETE /taches/1` avec le jeton d'alice retourne `403`
- `DELETE /taches/1` avec le jeton de bob retourne `204`
- Swagger UI affiche le bouton **Authorize** et permet de s'authentifier

## Exercice 2 — Tests pytest de l'API sécurisée

Écrivez une suite de tests `pytest` couvrant les routes sécurisées.

**Tests à écrire (au minimum 6) :**

1. Création réussie d'une tâche avec jeton valide (`201`)
2. Création refusée sans jeton (`401`)
3. Suppression refusée par un non-admin (`403`)
4. Suppression réussie par un admin (`204`)
5. Route inexistante retourne `404` avec le bon format
6. Validation Pydantic retourne `422` avec un titre trop court

**Critères de validation :**

- Tous les tests passent avec `pytest tests/ -v`
- Les routes protégées utilisent `dependency_overrides` pour injecter un utilisateur de test
- Le coverage de `routers/taches.py` atteint au moins 80 % (mesuré avec `pytest --cov`)
