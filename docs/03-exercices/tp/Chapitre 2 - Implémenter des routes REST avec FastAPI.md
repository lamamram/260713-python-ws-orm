## Exercice 1 — API CRUD d'une ressource `taches`

Vous allez construire pas à pas une API de gestion de tâches (to-do list) avec FastAPI.

**Étape 1 — Préparer la structure du projet**

Réutilisez ou créez un projet `api-taches` avec la structure :

```
api-taches/
├── main.py
├── routers/
│   ├── __init__.py
│   └── taches.py
├── schemas/
│   ├── __init__.py
│   └── tache.py
└── requirements.txt
```

**Étape 2 — Définir les schémas Pydantic (`schemas/tache.py`)**

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TacheCreation(BaseModel):
    titre: str = Field(min_length=3, max_length=100)
    description: Optional[str] = None
    terminee: bool = False
    priorite: int = Field(default=3, ge=1, le=5)

class TacheMiseAJour(BaseModel):
    titre: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = None
    terminee: Optional[bool] = None
    priorite: Optional[int] = Field(default=None, ge=1, le=5)

class TacheReponse(BaseModel):
    id: int
    titre: str
    description: Optional[str]
    terminee: bool
    priorite: int
    date_creation: datetime
```

**Étape 3 — Écrire le routeur (`routers/taches.py`)**

```python
from fastapi import APIRouter, HTTPException, Path, Query
from schemas.tache import TacheCreation, TacheMiseAJour, TacheReponse
from datetime import datetime
from typing import Optional, List

router = APIRouter(prefix="/taches", tags=["Tâches"])

# Stockage en mémoire
_id_counter = 0
taches_db: dict[int, dict] = {}

def _nouvel_id() -> int:
    global _id_counter
    _id_counter += 1
    return _id_counter


@router.get("/", response_model=List[TacheReponse])
def list_taches(
    page: int = Query(default=1, ge=1),
    taille: int = Query(default=10, ge=1, le=100),
    terminee: Optional[bool] = None,
):
    taches = list(taches_db.values())
    if terminee is not None:
        taches = [t for t in taches if t["terminee"] == terminee]
    debut = (page - 1) * taille
    return taches[debut:debut + taille]


@router.post("/", response_model=TacheReponse, status_code=201)
def create_tache(tache: TacheCreation):
    nid = _nouvel_id()
    nouvelle = {"id": nid, **tache.model_dump(), "date_creation": datetime.utcnow()}
    taches_db[nid] = nouvelle
    return nouvelle


@router.get("/{tache_id}", response_model=TacheReponse)
def get_tache(tache_id: int = Path(gt=0)):
    if tache_id not in taches_db:
        raise HTTPException(status_code=404, detail=f"Tâche {tache_id} introuvable")
    return taches_db[tache_id]


@router.patch("/{tache_id}", response_model=TacheReponse)
def update_tache(tache_id: int, tache: TacheMiseAJour):
    if tache_id not in taches_db:
        raise HTTPException(status_code=404, detail=f"Tâche {tache_id} introuvable")
    maj = tache.model_dump(exclude_none=True)
    taches_db[tache_id].update(maj)
    return taches_db[tache_id]


@router.delete("/{tache_id}", status_code=204)
def delete_tache(tache_id: int = Path(gt=0)):
    if tache_id not in taches_db:
        raise HTTPException(status_code=404, detail=f"Tâche {tache_id} introuvable")
    del taches_db[tache_id]
```

**Étape 4 — Écrire `main.py`**

```python
from fastapi import FastAPI
from routers import taches

app = FastAPI(title="API Tâches", version="1.0.0")
app.include_router(taches.router)
```

**Étape 5 — Tester via Swagger UI**

1. `fastapi dev main.py`
2. Ouvrir `http://localhost:8000/docs`
3. Créer deux tâches avec `POST /taches`
4. Lister avec `GET /taches`
5. Filtrer les tâches terminées : `GET /taches?terminee=false`
6. Mettre à jour une tâche : `PATCH /taches/1` avec `{"terminee": true}`
7. Supprimer une tâche : `DELETE /taches/1`
8. Tester `GET /taches/abc` → vérifier le `422`
9. Tester `GET /taches/999` → vérifier le `404`

---

## Exercice 2 — Gestionnaire d'erreurs uniforme

**Étape 1 — Définir l'exception personnalisée**

Dans `main.py` (ou dans un fichier `exceptions.py`), ajoutez :

```python
class TacheIntrouvable(Exception):
    def __init__(self, tache_id: int):
        self.tache_id = tache_id
```

**Étape 2 — Enregistrer le handler**

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="API Tâches", version="1.0.0")

@app.exception_handler(TacheIntrouvable)
async def tache_not_found_handler(request: Request, exc: TacheIntrouvable):
    return JSONResponse(
        status_code=404,
        content={
            "erreur": "RESSOURCE_INTROUVABLE",
            "message": f"La tâche {exc.tache_id} n'existe pas",
            "code": 404,
            "chemin": str(request.url.path),
        },
    )
```

**Étape 3 — Modifier le routeur**

Remplacez les `HTTPException` des routes `GET /{id}` et `DELETE /{id}` :

```python
# Avant
raise HTTPException(status_code=404, detail=f"Tâche {tache_id} introuvable")

# Après
raise TacheIntrouvable(tache_id=tache_id)
```

**Étape 4 — Vérification**

1. Relancez le serveur
2. Testez `GET /taches/999` via Swagger UI ou Postman
3. Vérifiez que le corps de réponse correspond au format attendu :
   ```json
   {"erreur": "RESSOURCE_INTROUVABLE", "message": "La tâche 999 n'existe pas", "code": 404, "chemin": "/taches/999"}
   ```
