## Exercice 1 — Analyser une API publique avec Postman

Vous allez explorer l'API publique JSONPlaceholder pour vous familiariser avec Postman et avec le format des réponses HTTP REST.

**Étape 1 — Créer l'environnement Postman**

1. Ouvrez Postman et cliquez sur **Environments** (icône d'œil en haut à droite)
2. Cliquez **Add** → nommez l'environnement `Formation FastAPI`
3. Ajoutez une variable : `base_url` = `https://jsonplaceholder.typicode.com`
4. Cliquez **Save** puis sélectionnez cet environnement dans le sélecteur en haut à droite

**Étape 2 — Créer la collection**

1. Cliquez **Collections** → **New Collection** → nommez-la `Formation FastAPI — Chapitre 1`
2. Pour chaque requête ci-dessous, cliquez **Add a request** dans la collection

**Étape 3 — Requête GET /posts**

1. Méthode : `GET`, URL : `{{base_url}}/posts`
2. Cliquez **Send**
3. Observez : code de statut `200 OK`, onglet **Body** affiche un tableau JSON de 100 objets, onglet **Headers** montre `Content-Type: application/json`
4. Sauvegardez la requête (Ctrl+S) avec le nom `Lister tous les posts`

**Étape 4 — Requête GET /posts/1**

1. Méthode : `GET`, URL : `{{base_url}}/posts/1`
2. Cliquez **Send** → observez le corps JSON :
   ```json
   { "userId": 1, "id": 1, "title": "...", "body": "..." }
   ```
3. Identifiez les types : `userId` et `id` sont des entiers, `title` et `body` sont des chaînes
4. Sauvegardez sous `Récupérer le post 1`

**Étape 5 — Requête GET /users/1**

1. Méthode : `GET`, URL : `{{base_url}}/users/1`
2. Cliquez **Send** → observez la structure imbriquée (objet `address` dans la réponse)
3. Sauvegardez sous `Récupérer l'utilisateur 1`

**Étape 6 — Requête POST /posts**

1. Méthode : `POST`, URL : `{{base_url}}/posts`
2. Onglet **Body** → sélectionnez **raw** → dans le menu déroulant, choisissez **JSON**
3. Saisissez le corps :
   ```json
   {
     "title": "Test",
     "body": "Contenu de test",
     "userId": 1
   }
   ```
4. Cliquez **Send** → observez le code `201 Created` (JSONPlaceholder simule la création)
5. La différence avec `200 OK` : `201` indique que la ressource a été **créée**, pas seulement lue
6. Sauvegardez sous `Créer un post`

---

## Exercice 2 — Premier projet FastAPI

Vous allez créer un projet FastAPI complet avec trois routes.

**Étape 1 — Mettre en place le projet**

```bash
# Créer le dossier et l'environnement virtuel
mkdir api-bibliotheque
cd api-bibliotheque
python -m venv .venv

# Activer (Windows PowerShell)
.venv\Scripts\Activate.ps1
# Activer (Linux/macOS)
# source .venv/bin/activate

# Installer FastAPI
pip install "fastapi[standard]"

# Créer requirements.txt
pip freeze > requirements.txt
```

**Étape 2 — Créer le fichier `.gitignore`**

```
.venv/
__pycache__/
*.pyc
```

**Étape 3 — Écrire `main.py`**

```python
# main.py
from fastapi import FastAPI

app = FastAPI(
    title="API Bibliothèque",
    description="Gestion de livres et d'auteurs — Formation FastAPI Dawan",
    version="0.1.0",
)


@app.get("/")
def read_root():
    """Point d'entrée — informations sur l'API."""
    return {"service": "API Bibliothèque", "version": "0.1.0"}


@app.get("/livres/{livre_id}")
def get_livre(livre_id: int):
    """Retourne un livre fictif par son identifiant entier."""
    return {"id": livre_id, "titre": "Livre fictif", "auteur": "Auteur inconnu"}


@app.get("/auteurs/{auteur_id}/livres")
def get_livres_auteur(auteur_id: int):
    """Retourne les livres d'un auteur (liste vide pour l'instant)."""
    return {"auteur_id": auteur_id, "livres": []}
```

**Étape 4 — Démarrer le serveur**

```bash
fastapi dev main.py
# → INFO: Application startup complete.
# → INFO: Uvicorn running on http://127.0.0.1:8000
```

**Étape 5 — Tester les routes**

Ouvrez un navigateur ou Postman et vérifiez :

| URL | Résultat attendu |
|-----|-----------------|
| `http://localhost:8000/` | `{"service": "API Bibliothèque", "version": "0.1.0"}` |
| `http://localhost:8000/livres/7` | `{"id": 7, "titre": "Livre fictif", "auteur": "Auteur inconnu"}` |
| `http://localhost:8000/auteurs/3/livres` | `{"auteur_id": 3, "livres": []}` |
| `http://localhost:8000/livres/abc` | Code `422` avec message d'erreur Pydantic |

**Étape 6 — Explorer Swagger UI**

1. Ouvrez `http://localhost:8000/docs`
2. Vérifiez que les trois routes apparaissent avec leurs paramètres
3. Utilisez **Try it out** sur `GET /livres/{livre_id}` → saisissez `7` → **Execute**
4. Observez la requête `curl` générée par Swagger UI
