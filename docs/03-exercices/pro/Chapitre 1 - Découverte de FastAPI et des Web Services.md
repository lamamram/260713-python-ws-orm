## Exercice 1 — Analyser une API publique avec Postman

Vous disposez d'un accès à l'API publique JSONPlaceholder (`https://jsonplaceholder.typicode.com`), une fausse API REST de test qui expose des ressources `posts`, `users` et `comments`.

**Travail à réaliser :**

Créez dans Postman une collection nommée **"Formation FastAPI — Chapitre 1"** contenant quatre requêtes :

1. `GET /posts` — récupérer la liste des 100 posts
2. `GET /posts/1` — récupérer le post d'identifiant 1
3. `GET /users/1` — récupérer le profil de l'utilisateur 1
4. `POST /posts` avec un corps JSON `{"title": "Test", "body": "Contenu de test", "userId": 1}`

**Critères de validation :**

- Chaque requête retourne un code de statut HTTP correct (200 ou 201)
- La variable d'environnement `{{base_url}}` = `https://jsonplaceholder.typicode.com` est définie et utilisée dans toutes les URLs
- Vous pouvez identifier, dans la réponse de `GET /posts/1`, les champs retournés et leur type JSON (chaîne, entier, etc.)
- Vous expliquez pourquoi la requête `POST /posts` retourne un `201` et non un `200`

## Exercice 2 — Premier projet FastAPI

Créez un projet FastAPI nommé `api-bibliotheque` qui expose les routes suivantes :

- `GET /` — retourne `{"service": "API Bibliothèque", "version": "0.1.0"}`
- `GET /livres/{livre_id}` — retourne `{"id": livre_id, "titre": "Livre fictif", "auteur": "Auteur inconnu"}`
- `GET /auteurs/{auteur_id}/livres` — retourne `{"auteur_id": auteur_id, "livres": []}`

**Critères de validation :**

- Le projet est dans un dossier dédié avec un environnement virtuel activé et `requirements.txt` à jour
- Le serveur démarre sans erreur avec `fastapi dev main.py`
- Les trois routes répondent avec les codes et corps attendus
- Swagger UI sur `/docs` affiche les trois routes avec leurs paramètres de chemin
- Envoyer `GET /livres/abc` retourne un `422` (validation automatique du type `int`)
