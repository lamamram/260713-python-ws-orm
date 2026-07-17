# Cheat-Sheet — Python Avancé : FastAPI + ORM

## FastAPI — Démarrage rapide

```bash
pip install "fastapi[standard]"       # Installe FastAPI + Uvicorn
fastapi dev main.py                   # Serveur de développement (--reload)
uvicorn main:app --reload             # Equivalent Uvicorn direct
# Swagger UI  → http://localhost:8000/docs
# ReDoc       → http://localhost:8000/redoc
# OpenAPI JSON→ http://localhost:8000/openapi.json
```

## FastAPI — Routes et paramètres

```python
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Path, Query
from typing import Optional

app = FastAPI(title="Mon API")
router = APIRouter(prefix="/articles", tags=["Articles"])

# Paramètre de chemin
@router.get("/{id}")
def get(id: int = Path(gt=0)): ...

# Paramètre de requête
@router.get("/")
def list(page: int = Query(1, ge=1), taille: int = Query(10, le=100),
         q: Optional[str] = None): ...

# Corps JSON (modèle Pydantic)
@router.post("/", status_code=201)
def create(article: ArticleCreation): ...

app.include_router(router)
```

## Codes de statut courants

| Code | Signification | Usage |
|------|--------------|-------|
| 200 | OK | GET, PATCH, PUT réussis |
| 201 | Created | POST réussi |
| 204 | No Content | DELETE réussi |
| 400 | Bad Request | Requête malformée |
| 401 | Unauthorized | Non authentifié (jeton manquant/invalide) |
| 403 | Forbidden | Authentifié mais non autorisé |
| 404 | Not Found | Ressource inexistante |
| 409 | Conflict | Conflit (doublon email, etc.) |
| 422 | Unprocessable Entity | Validation Pydantic échouée |
| 500 | Internal Server Error | Exception non gérée |

## Pydantic v2

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class ArticleCreation(BaseModel):
    titre: str = Field(min_length=3, max_length=200)
    contenu: str = Field(min_length=10)
    tags: List[str] = Field(default_factory=list)

class ArticleReponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Pour SQLAlchemy
    id: int
    titre: str
    auteur: AuteurSchema

# Sérialisation
obj.model_dump()                    # → dict
obj.model_dump(exclude_none=True)   # → dict sans les None (pour PATCH)
ArticleReponse.model_validate(orm_obj)  # Depuis un objet SQLAlchemy
```

## Gestion des erreurs

```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Introuvable")
raise HTTPException(status_code=401, detail="Jeton invalide",
                    headers={"WWW-Authenticate": "Bearer"})

# Handler global
@app.exception_handler(MonException)
async def handler(request, exc):
    return JSONResponse(status_code=422, content={"erreur": str(exc)})
```

## Injection de dépendances

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    ...

@router.get("/profil")
def profil(user = Depends(get_current_user)):
    return user
```

## JWT (python-jose + passlib)

```python
from jose import jwt, JWTError
from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"])
pwd.hash("secret")                         # Hacher un mot de passe
pwd.verify("secret", "$2b$12$...")         # Vérifier

jwt.encode({"sub": "1", "exp": ...}, KEY, algorithm="HS256")  # Créer un jeton
jwt.decode(token, KEY, algorithms=["HS256"])                   # Décoder/vérifier
```

## SQLAlchemy 2.0 — Démarrage

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

engine = create_engine("sqlite:///./app.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase): pass
Base.metadata.create_all(bind=engine)  # Créer toutes les tables (dev seulement)
```

## SQLAlchemy 2.0 — Modèles

```python
from sqlalchemy import String, Integer, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    est_actif: Mapped[bool] = mapped_column(Boolean, default=True)
    date_creation: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    articles: Mapped[list["Article"]] = relationship("Article", back_populates="auteur")

class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(primary_key=True)
    auteur_id: Mapped[int] = mapped_column(ForeignKey("utilisateurs.id"))
    auteur: Mapped["Utilisateur"] = relationship("Utilisateur", back_populates="articles")
```

## SQLAlchemy 2.0 — CRUD

```python
from sqlalchemy import select, update, delete

# CREATE
obj = Utilisateur(username="alice", ...); db.add(obj); db.commit(); db.refresh(obj)

# READ
user = db.get(Utilisateur, 1)                                  # Par PK
user = db.execute(select(Utilisateur).where(...)).scalar_one_or_none()
users = db.execute(select(Utilisateur).limit(10)).scalars().all()

# UPDATE
user.email = "new@ex.com"; db.commit()
db.execute(update(Utilisateur).where(...).values(est_actif=False)); db.commit()

# DELETE
db.delete(user); db.commit()
```

## SQLAlchemy — Eager loading

```python
from sqlalchemy.orm import joinedload, selectinload

# to-one (auteur d'un article) → JOIN
stmt = select(Article).options(joinedload(Article.auteur))
articles = db.execute(stmt).unique().scalars().all()

# to-many (tags d'un article) → IN
stmt = select(Article).options(selectinload(Article.tags))
articles = db.execute(stmt).scalars().all()

# Combiner
stmt = select(Article).options(
    joinedload(Article.auteur),
    selectinload(Article.tags),
)
```

## SQLAlchemy — Relations n-à-n

```python
from sqlalchemy import Table, Column

# Table d'association
articles_tags = Table(
    "articles_tags", Base.metadata,
    Column("article_id", ForeignKey("articles.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)
# Dans Article : tags = relationship("Tag", secondary=articles_tags, ...)
# Dans Tag     : articles = relationship("Article", secondary=articles_tags, ...)
```

## Alembic

```bash
alembic init alembic               # Initialiser
alembic revision --autogenerate -m "description"  # Générer une migration
alembic upgrade head               # Appliquer toutes les migrations
alembic downgrade -1               # Revenir à la précédente
alembic history                    # Historique des migrations
```

## Tests pytest + TestClient

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create():
    r = client.post("/articles/", json={"titre": "Test", "contenu": "..."})
    assert r.status_code == 201

# Remplacer une dépendance
app.dependency_overrides[get_db] = lambda: test_db
app.dependency_overrides.clear()  # Nettoyer après les tests
```

## Docker

```bash
docker compose up --build          # Construire et démarrer
docker compose exec api alembic upgrade head  # Migrations en conteneur
docker compose logs -f api         # Logs en temps réel
docker compose down                # Arrêter et supprimer les conteneurs
docker compose down -v             # Arrêter ET supprimer les volumes
```
