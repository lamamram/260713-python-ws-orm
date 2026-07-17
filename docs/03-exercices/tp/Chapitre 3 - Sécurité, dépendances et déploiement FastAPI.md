## Exercice 1 — Sécuriser une API avec JWT

**Étape 1 — Installer les dépendances**

```bash
pip install "python-jose[cryptography]" "passlib[bcrypt]" "pydantic-settings"
pip freeze > requirements.txt
```

**Étape 2 — Créer `auth.py`**

```python
# auth.py
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

SECRET_KEY = "formation-dawan-clé-de-développement-seulement"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class TokenReponse(BaseModel):
    access_token: str
    token_type: str

class UtilisateurDansToken(BaseModel):
    username: str
    est_admin: bool = False

UTILISATEURS_DB = {
    "alice": {"username": "alice", "hashed_password": pwd_context.hash("secret"), "est_admin": False},
    "bob":   {"username": "bob",   "hashed_password": pwd_context.hash("admin123"), "est_admin": True},
}

def authentifier(username: str, password: str) -> Optional[dict]:
    user = UTILISATEURS_DB.get(username)
    if not user or not pwd_context.verify(password, user["hashed_password"]):
        return None
    return user

def creer_jeton(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UtilisateurDansToken:
    exc = HTTPException(status_code=401, detail="Jeton invalide",
                        headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise exc
    except JWTError:
        raise exc
    user = UTILISATEURS_DB.get(username)
    if not user:
        raise exc
    return UtilisateurDansToken(**user)

async def require_admin(user: UtilisateurDansToken = Depends(get_current_user)) -> UtilisateurDansToken:
    if not user.est_admin:
        raise HTTPException(status_code=403, detail="Droits admin requis")
    return user
```

**Étape 3 — Ajouter le routeur d'authentification**

Créez `routers/auth.py` :

```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth import authentifier, creer_jeton, TokenReponse

router = APIRouter(prefix="/auth", tags=["Authentification"])

@router.post("/token", response_model=TokenReponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authentifier(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Identifiants incorrects",
                            headers={"WWW-Authenticate": "Bearer"})
    return {"access_token": creer_jeton({"sub": user["username"]}), "token_type": "bearer"}
```

**Étape 4 — Protéger les routes de tâches**

Dans `routers/taches.py`, importez les dépendances et ajoutez-les :

```python
from auth import get_current_user, require_admin, UtilisateurDansToken

@router.get("/", response_model=List[TacheReponse])
def list_taches(..., user: UtilisateurDansToken = Depends(get_current_user)):
    ...

@router.post("/", response_model=TacheReponse, status_code=201)
def create_tache(tache: TacheCreation, user: UtilisateurDansToken = Depends(get_current_user)):
    ...

@router.delete("/{tache_id}", status_code=204)
def delete_tache(tache_id: int, admin: UtilisateurDansToken = Depends(require_admin)):
    ...
```

**Étape 5 — Inclure le routeur dans `main.py`**

```python
from routers import auth, taches
app.include_router(auth.router)
app.include_router(taches.router)
```

**Étape 6 — Tester dans Swagger UI**

1. `fastapi dev main.py` → ouvrir `/docs`
2. Cliquer **Authorize** → saisir `alice` / `secret` → `Authorize`
3. Tester `GET /taches/` → `200`
4. Tester `DELETE /taches/1` → `403` (alice n'est pas admin)
5. Se déconnecter → **Authorize** avec `bob` / `admin123`
6. Tester `DELETE /taches/1` → `204`

---

## Exercice 2 — Tests pytest de l'API sécurisée

**Étape 1 — Installer pytest et httpx**

```bash
pip install pytest httpx pytest-cov
```

**Étape 2 — Créer `tests/conftest.py`**

```python
import pytest
from fastapi.testclient import TestClient
from main import app
from auth import get_current_user, UtilisateurDansToken

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def token_alice(client):
    r = client.post("/auth/token", data={"username": "alice", "password": "secret"})
    return r.json()["access_token"]

@pytest.fixture
def token_bob(client):
    r = client.post("/auth/token", data={"username": "bob", "password": "admin123"})
    return r.json()["access_token"]

@pytest.fixture
def alice_headers(token_alice):
    return {"Authorization": f"Bearer {token_alice}"}

@pytest.fixture
def bob_headers(token_bob):
    return {"Authorization": f"Bearer {token_bob}"}
```

**Étape 3 — Créer `tests/test_taches.py`**

```python
def test_creation_avec_jeton(client, alice_headers):
    r = client.post("/taches/", json={"titre": "Tâche test"}, headers=alice_headers)
    assert r.status_code == 201
    assert r.json()["titre"] == "Tâche test"

def test_creation_sans_jeton(client):
    r = client.post("/taches/", json={"titre": "Tâche test"})
    assert r.status_code == 401

def test_suppression_non_admin(client, alice_headers):
    # Créer d'abord une tâche
    r = client.post("/taches/", json={"titre": "À supprimer"}, headers=alice_headers)
    tache_id = r.json()["id"]
    # Tenter de supprimer en tant que non-admin
    r = client.delete(f"/taches/{tache_id}", headers=alice_headers)
    assert r.status_code == 403

def test_suppression_admin(client, alice_headers, bob_headers):
    r = client.post("/taches/", json={"titre": "À supprimer admin"}, headers=alice_headers)
    tache_id = r.json()["id"]
    r = client.delete(f"/taches/{tache_id}", headers=bob_headers)
    assert r.status_code == 204

def test_tache_inexistante(client, alice_headers):
    r = client.get("/taches/99999", headers=alice_headers)
    assert r.status_code == 404

def test_validation_titre_trop_court(client, alice_headers):
    r = client.post("/taches/", json={"titre": "AB"}, headers=alice_headers)
    assert r.status_code == 422
```

**Étape 4 — Lancer les tests**

```bash
# Tests simples
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=routers --cov-report=term-missing
```

Résultat attendu : 6 tests PASSED, couverture ≥ 80 % sur `routers/taches.py`.
