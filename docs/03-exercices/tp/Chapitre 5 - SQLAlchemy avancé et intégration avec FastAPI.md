## Exercice 1 — Projet fil rouge : API Catalogue complet

Vous allez assembler les briques des chapitres précédents en un projet complet.

**Étape 1 — Préparer la structure**

```bash
mkdir api-catalogue && cd api-catalogue
python -m venv .venv && .venv\Scripts\Activate.ps1
pip install "fastapi[standard]" "sqlalchemy[asyncio]" alembic "python-jose[cryptography]" "passlib[bcrypt]" "pydantic-settings" psycopg2-binary gunicorn
pip freeze > requirements.txt
mkdir routers schemas crud tests
touch routers/__init__.py schemas/__init__.py crud/__init__.py tests/__init__.py
```

**Étape 2 — `database.py`**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Generator
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Étape 3 — `models.py`** (reprendre les modèles du Chapitre 4 et ajouter Tag)

```python
from sqlalchemy import String, Boolean, Integer, Text, DateTime, ForeignKey, Table, Column, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from datetime import datetime
from typing import Optional

articles_tags = Table(
    "articles_tags", Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=False)
    est_actif: Mapped[bool] = mapped_column(Boolean, default=True)
    est_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    date_creation: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    articles: Mapped[list["Article"]] = relationship("Article", back_populates="auteur",
                                                      cascade="all, delete-orphan")

class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    articles: Mapped[list["Article"]] = relationship("Article", secondary=articles_tags,
                                                      back_populates="tags")

class Article(Base):
    __tablename__ = "articles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titre: Mapped[str] = mapped_column(String(200), nullable=False)
    contenu: Mapped[str] = mapped_column(Text, nullable=False)
    publie: Mapped[bool] = mapped_column(Boolean, default=False)
    date_creation: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    auteur_id: Mapped[int] = mapped_column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    auteur: Mapped["Utilisateur"] = relationship("Utilisateur", back_populates="articles")
    tags: Mapped[list["Tag"]] = relationship("Tag", secondary=articles_tags, back_populates="articles")
```

**Étape 4 — `crud/articles.py`** (reprendre le code de la section "Couche de données")

**Étape 5 — `auth.py`** (reprendre la version base de données de la section "Authentification")

**Étape 6 — `main.py`**

```python
from fastapi import FastAPI
from database import Base, engine
from routers import auth, utilisateurs, articles, tags
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Catalogue",
    description="Formation Dawan — Python Avancé FastAPI + ORM",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(utilisateurs.router)
app.include_router(articles.router)
app.include_router(tags.router)
```

**Étape 7 — Tester le flux complet via Swagger UI**

1. `fastapi dev main.py`
2. Ouvrir `http://localhost:8000/docs`
3. `POST /utilisateurs/` → créer alice et bob
4. **Authorize** avec alice
5. `POST /tags/` → créer le tag "python"
6. `POST /articles/` → créer un article
7. `PUT /articles/1/tags/1` → assigner le tag python à l'article
8. `GET /articles/1` → vérifier que `auteur.username` et `tags` apparaissent dans la réponse

---

## Exercice 2 — Corriger le N+1

**Étape 1 — Reproduire le problème**

Dans `crud/articles.py`, écrire temporairement la version naïve :

```python
# Version N+1 (à corriger)
def list_articles_naive(db: Session) -> list[Article]:
    return db.execute(select(Article)).scalars().all()
```

Activer les logs SQL dans `database.py` :

```python
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
```

Créer 5 articles avec des auteurs différents, appeler `GET /articles/` et compter les lignes SQL dans le terminal.

**Étape 2 — Corriger avec eager loading**

```python
from sqlalchemy.orm import joinedload, selectinload

def list_articles(db: Session, skip: int = 0, limit: int = 10) -> list[Article]:
    stmt = (
        select(Article)
        .options(
            joinedload(Article.auteur),       # to-one : auteur de l'article
            selectinload(Article.tags),        # to-many : liste de tags
        )
        .order_by(Article.date_creation.desc())
        .offset(skip)
        .limit(limit)
    )
    return db.execute(stmt).unique().scalars().all()
```

**Étape 3 — Comparer**

Relancer `GET /articles/` avec les logs SQL activés.

| Stratégie | Requêtes pour 5 articles |
|-----------|------------------------|
| Lazy loading (avant) | 11 (1 + 5 auteurs + 5 tags) |
| Eager loading (après) | 2 (1 SELECT articles+auteurs JOIN, 1 SELECT tags IN) |

Désactiver `echo=True` avant le déploiement.
