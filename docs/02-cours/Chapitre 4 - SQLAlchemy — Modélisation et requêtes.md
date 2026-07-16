---
formation: Python Avancé - FastAPI + ORM
numero: "04"
titre: SQLAlchemy — Modélisation et requêtes
sous_titre: ORM, Engine, Session, modèles déclaratifs, relations et requêtes de base
duree: 7h30
objectifs:
  - Expliquer le principe des ORM et le positionnement de SQLAlchemy dans l'écosystème Python
  - Configurer un Engine et une Session SQLAlchemy pour se connecter à une base de données
  - Définir des modèles ORM déclaratifs avec colonnes, types, contraintes et clés étrangères
  - Modéliser les trois types de relations (1-à-n, 1-à-1, n-à-n) avec SQLAlchemy
  - Gérer les migrations de schéma avec Alembic
  - Écrire des requêtes CRUD de base avec la Session SQLAlchemy ORM
---

# Chapitre 4 — SQLAlchemy — Modélisation et requêtes

## Objectifs du chapitre

À l'issue de ce chapitre, chaque stagiaire est capable de :

- Expliquer ce qu'est un ORM et en quoi SQLAlchemy diffère de SQLObject, Peewee ou Django ORM
- Distinguer SQLAlchemy Core (SQL Expression Language) et SQLAlchemy ORM et choisir le bon niveau d'abstraction
- Configurer un `Engine` et une `Session` SQLAlchemy pour SQLite, PostgreSQL et MySQL
- Créer des modèles ORM avec la base déclarative moderne (`DeclarativeBase`)
- Définir des colonnes avec les types SQLAlchemy, des contraintes et des valeurs par défaut
- Créer des relations `relationship()` avec `ForeignKey` pour les trois types d'associations
- Initialiser et exécuter des migrations de schéma avec Alembic
- Écrire des requêtes de base (select, insert, update, delete, filtres) avec la Session 2.0

## Principe des ORM et positionnement de SQLAlchemy

### Le problème de l'impedance objet-relationnel

Les bases de données relationnelles stockent des données dans des tables avec des lignes et des colonnes. Les programmes Python travaillent avec des objets, des attributs et des méthodes. Ce décalage entre les deux paradigmes — le modèle relationnel et le modèle objet — est appelé **impedance objet-relationnel** (Object-Relational Impedance Mismatch).

Sans ORM, accéder à une base de données en Python implique d'écrire du SQL brut, de gérer manuellement les connexions, de convertir les lignes de résultats (`tuples`) en objets Python, et de reconstruire les relations entre tables à la main. Pour des opérations ponctuelles, le SQL brut est parfait. Pour une application qui manipule des centaines de tables avec des relations complexes, cette approche devient rapidement source d'erreurs et de duplication.

Un ORM (Object-Relational Mapper) est une bibliothèque qui établit une correspondance (mapping) entre les classes Python et les tables de la base de données, et entre les instances de ces classes et les lignes. L'ORM génère et exécute le SQL à la place du développeur, offre une API orientée objet pour les requêtes, et gère les relations entre entités comme des associations entre objets Python.

> [!NOTE] Analogie
> L'ORM est un traducteur simultané entre deux langues : le Python côté programme, et le SQL côté base de données. Vous parlez Python, il traduit en SQL — et vous retranscrit les résultats SQL sous forme d'objets Python.

### L'écosystème ORM Python

Plusieurs ORMs coexistent dans l'écosystème Python. Le programme officiel Dawan cite SQLObject, SQLAlchemy, Peewee et PonyORM. Voici une comparaison rapide :

| ORM | Points forts | Points faibles | Cas d'usage typique |
|-----|-------------|----------------|---------------------|
| **SQLAlchemy** | Complet, flexible, SQL expressif, async, Alembic | Courbe d'apprentissage steep | Applications d'entreprise, FastAPI |
| **Peewee** | Simple, léger, batteries incluses | Moins performant sur de gros volumes | Projets petits/moyens, prototypes |
| **Django ORM** | Intégré à Django, admin automatique | Couplé à Django | Applications Django uniquement |
| **PonyORM** | Syntaxe Python naturelle (générateurs) | Communauté plus petite | Projets qui préfèrent la syntaxe objet |
| **Tortoise ORM** | Async natif, API proche Django | Moins mature | FastAPI avec full-async |

**SQLAlchemy** est le choix de cette formation car c'est la bibliothèque la plus utilisée et la plus puissante de l'écosystème Python, et celle qui s'intègre le mieux avec FastAPI via son mode asynchrone.

### SQLAlchemy Core vs SQLAlchemy ORM

SQLAlchemy offre deux niveaux d'abstraction distincts qui peuvent coexister dans le même projet.

**SQLAlchemy Core** (SQL Expression Language) permet de construire des expressions SQL en Python sous forme d'objets. Il génère du SQL portable (fonctionne avec SQLite, PostgreSQL, MySQL, Oracle…) mais reste proche du SQL — on manipule des tables et des colonnes, pas des classes et des attributs.

**SQLAlchemy ORM** ajoute au-dessus de Core la couche de mapping objet-relationnel : les classes Python correspondent à des tables, les instances à des lignes, les attributs à des colonnes. La Session gère le cycle de vie des objets (nouveau, persistant, détaché, supprimé) et le suivi des modifications (Unit of Work).

```python
# SQLAlchemy Core — proche du SQL
from sqlalchemy import select, text
result = conn.execute(select(articles_table).where(articles_table.c.publie == True))

# SQLAlchemy ORM — orienté objet
session.query(Article).filter(Article.publie == True).all()  # Style 1.x (legacy)
session.execute(select(Article).where(Article.publie == True)).scalars().all()  # Style 2.0
```

Cette formation utilise **SQLAlchemy ORM avec la syntaxe 2.0** — la syntaxe moderne depuis SQLAlchemy 2.0 (2023), plus cohérente entre les versions synchrone et asynchrone.

## Installation et configuration

### Installation

```bash
pip install "sqlalchemy[asyncio]" alembic psycopg2-binary
# sqlalchemy[asyncio] inclut greenlet pour le support async
# alembic pour les migrations
# psycopg2-binary pour PostgreSQL (en production, utiliser psycopg2 sans -binary)

# Pour SQLite (inclus dans Python) : aucune dépendance supplémentaire
# Pour MySQL : pip install pymysql
```

### Engine — connexion à la base de données

L'`Engine` est le point d'entrée de SQLAlchemy. Il encapsule la chaîne de connexion (connection string) et gère un pool de connexions.

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# SQLite (développement)
DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Requis pour SQLite + multi-thread
)

# PostgreSQL (production)
# DATABASE_URL = "postgresql://user:password@localhost:5432/db_name"
# engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)

# MySQL
# DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/db_name"
# engine = create_engine(DATABASE_URL)
```

> [!NOTE] Format de l'URL de connexion SQLAlchemy
> `dialect+driver://username:password@host:port/database`
> - SQLite : `sqlite:///./app.db` (relatif) ou `sqlite:////abs/path/app.db`
> - PostgreSQL : `postgresql://user:pwd@localhost:5432/dbname`
> - PostgreSQL (async) : `postgresql+asyncpg://user:pwd@localhost:5432/dbname`

### Session — cycle de vie des objets

La `Session` est l'objet central de SQLAlchemy ORM. Elle représente une "conversation" avec la base de données — un périmètre transactionnel dans lequel les objets sont suivis, les modifications détectées et les requêtes exécutées.

```python
# database.py (suite)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Utilisation manuelle de la session
def get_db():
    db = SessionLocal()
    try:
        yield db          # Fournit la session
    finally:
        db.close()        # Toujours fermer même en cas d'exception
```

> [!WARN] Ne jamais partager une Session entre threads
> Une `Session` n'est pas thread-safe. Chaque requête HTTP doit avoir sa propre instance de Session, créée en début de requête et fermée à la fin. La session par requête est implémentée dans FastAPI via `Depends(get_db)` au Chapitre 5.

### Base déclarative

La `DeclarativeBase` est la classe de base dont héritent tous les modèles ORM. Elle maintient le registre des classes mappées et génère les métadonnées de tables.

```python
# database.py (suite)
class Base(DeclarativeBase):
    pass
```

Depuis SQLAlchemy 2.0, `DeclarativeBase` remplace l'ancien `declarative_base()` (toujours supporté mais considéré legacy). `Base.metadata` contient toutes les informations sur les tables définies dans les modèles.

## Définir des modèles ORM

### Premier modèle — Utilisateur

```python
# models.py
from sqlalchemy import String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime

class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=False)
    est_actif: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    est_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    date_creation: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Utilisateur(id={self.id}, username='{self.username}')>"
```

La syntaxe `Mapped[type] = mapped_column(...)` est la syntaxe moderne SQLAlchemy 2.0. Elle combine l'annotation de type Python (utilisée pour la vérification statique et la documentation) avec la définition de colonne SQLAlchemy.

**Attributs clés de `mapped_column` :**

| Attribut | Description | Exemple |
|---------|-------------|---------|
| `primary_key=True` | Clé primaire | `id` auto-incrémenté |
| `unique=True` | Contrainte d'unicité | `username`, `email` |
| `nullable=False` | Valeur obligatoire (NOT NULL) | Champs requis |
| `index=True` | Index sur la colonne | Colonnes souvent filtrées |
| `default=...` | Valeur par défaut Python | `default=True` |
| `server_default=...` | Valeur par défaut SQL | `server_default="NOW()"` |

### Types de colonnes SQLAlchemy

```python
from sqlalchemy import (
    Integer,          # Entier 32 bits
    BigInteger,       # Entier 64 bits
    Float,            # Flottant
    Numeric,          # Décimal précis (argent)
    String,           # VARCHAR(n)
    Text,             # TEXT illimité
    Boolean,          # BOOLEAN
    Date,             # DATE
    DateTime,         # DATETIME / TIMESTAMP
    JSON,             # JSON (PostgreSQL, MySQL 5.7+)
    Enum,             # ENUM (valeurs prédéfinies)
    ForeignKey,       # Clé étrangère
)
```

> [!TIP] Utiliser `Numeric` pour les montants monétaires
> `Float` accumule des erreurs d'arrondi liées à la représentation binaire des flottants. Pour les montants en euros ou dollars, toujours utiliser `Numeric(precision=10, scale=2)` — stocké en décimal exact dans la base.

### Modèle Article avec clé étrangère

```python
# models.py (suite)
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship

class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titre: Mapped[str] = mapped_column(String(200), nullable=False)
    contenu: Mapped[str] = mapped_column(Text, nullable=False)
    publie: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    date_creation: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    auteur_id: Mapped[int] = mapped_column(Integer, ForeignKey("utilisateurs.id"), nullable=False)

    # Relation vers l'auteur (côté "many" de la relation 1-à-n)
    auteur: Mapped["Utilisateur"] = relationship("Utilisateur", back_populates="articles")

    def __repr__(self) -> str:
        return f"<Article(id={self.id}, titre='{self.titre[:30]}')>"
```

La `ForeignKey("utilisateurs.id")` est une contrainte SQL qui référence la colonne `id` de la table `utilisateurs`. La `relationship("Utilisateur", back_populates="articles")` est une définition côté ORM — elle ne crée pas de colonne supplémentaire, mais permet d'accéder à l'auteur d'un article via `article.auteur` (un objet Python `Utilisateur`).

## Relations entre modèles

### Relation 1-à-n (One-to-Many)

La relation la plus courante : un utilisateur peut avoir plusieurs articles, un article appartient à un seul utilisateur.

```python
# Dans Utilisateur : ajouter le côté "one"
class Utilisateur(Base):
    ...
    articles: Mapped[list["Article"]] = relationship(
        "Article",
        back_populates="auteur",
        cascade="all, delete-orphan",  # Supprime les articles quand l'auteur est supprimé
    )
```

```python
# Dans Article : côté "many" déjà défini ci-dessus
class Article(Base):
    ...
    auteur_id: Mapped[int] = mapped_column(ForeignKey("utilisateurs.id"))
    auteur: Mapped["Utilisateur"] = relationship("Utilisateur", back_populates="articles")
```

```python
# Utilisation
user = session.get(Utilisateur, 1)
print(user.articles)       # Liste des articles de cet utilisateur
article = user.articles[0]
print(article.auteur)      # Retourne l'objet Utilisateur correspondant
```

### Relation 1-à-1 (One-to-One)

Un utilisateur possède un et un seul profil, un profil appartient à un et un seul utilisateur.

```python
class ProfilUtilisateur(Base):
    __tablename__ = "profils_utilisateurs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    utilisateur_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("utilisateurs.id"),
        unique=True,       # unique=True garantit le 1-à-1
        nullable=False,
    )
    bio: Mapped[str] = mapped_column(Text, default="")
    avatar_url: Mapped[str] = mapped_column(String(500), default="")

    utilisateur: Mapped["Utilisateur"] = relationship(
        "Utilisateur", back_populates="profil"
    )

# Dans Utilisateur
class Utilisateur(Base):
    ...
    profil: Mapped[Optional["ProfilUtilisateur"]] = relationship(
        "ProfilUtilisateur",
        back_populates="utilisateur",
        uselist=False,      # uselist=False → attribut unique, pas une liste
    )
```

### Relation n-à-n (Many-to-Many)

Un article peut avoir plusieurs tags, un tag peut être associé à plusieurs articles. La relation n-à-n nécessite une **table d'association** (table pivot).

```python
from sqlalchemy import Table, Column

# Table d'association — définie avec Table() car elle n'a pas de modèle ORM propre
articles_tags = Table(
    "articles_tags",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    articles: Mapped[list["Article"]] = relationship(
        "Article", secondary=articles_tags, back_populates="tags"
    )

# Dans Article : ajouter la relation
class Article(Base):
    ...
    tags: Mapped[list["Tag"]] = relationship(
        "Tag", secondary=articles_tags, back_populates="articles"
    )
```

```python
# Utilisation
article = session.get(Article, 1)
print(article.tags)       # Liste de Tag
tag = session.get(Tag, 1)
print(tag.articles)       # Liste d'Article
```

![Relations entre modèles SQLAlchemy — 1-à-n, 1-à-1 et n-à-n](../08-images/ch04-orm-relations.svg)

Le schéma ci-dessus représente les trois types de relations avec leurs clés étrangères et tables d'association : Utilisateur ↔ Article (1-à-n), Utilisateur ↔ Profil (1-à-1), Article ↔ Tag via la table articles_tags (n-à-n).

## Créer les tables — Base.metadata

```python
# Créer toutes les tables définies dans les modèles importés
from database import engine, Base
import models  # Nécessaire pour que les modèles soient enregistrés dans Base.metadata

Base.metadata.create_all(bind=engine)
```

> [!WARN] `create_all` en développement seulement
> `Base.metadata.create_all()` est pratique pour créer les tables au démarrage lors d'un prototype ou d'un test. En production, utiliser exclusivement Alembic pour gérer les migrations — `create_all` ne gère pas les modifications de schéma (ajout de colonne, modification de contrainte).

## Migrations avec Alembic

### Initialiser Alembic

```bash
# Dans le dossier du projet
alembic init alembic
```

Alembic crée :
```
alembic/
├── env.py           ← Point d'entrée des migrations
├── script.py.mako   ← Template des fichiers de migration
└── versions/        ← Fichiers de migration générés
alembic.ini          ← Configuration Alembic
```

```python
# alembic/env.py — modifications à apporter
from database import Base
from models import Utilisateur, Article, Tag  # Importer tous les modèles

target_metadata = Base.metadata  # Pointer vers les métadonnées des modèles
```

```ini
# alembic.ini — configurer l'URL de la base de données
sqlalchemy.url = sqlite:///./app.db
```

### Créer et appliquer une migration

```bash
# Générer une migration automatiquement (compare les modèles au schéma actuel)
alembic revision --autogenerate -m "Création des tables initiales"
# Crée alembic/versions/xxxx_création_des_tables_initiales.py

# Appliquer les migrations en attente
alembic upgrade head

# Voir l'historique des migrations
alembic history

# Revenir à la migration précédente
alembic downgrade -1
```

```python
# Exemple de fichier de migration généré par --autogenerate
def upgrade() -> None:
    op.create_table(
        "utilisateurs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(50), nullable=False, unique=True),
        sa.Column("email", sa.String(200), nullable=False, unique=True),
        # ...
    )

def downgrade() -> None:
    op.drop_table("utilisateurs")
```

> [!TIP] Versionner les migrations
> Les fichiers de migration dans `alembic/versions/` doivent être versionnés avec Git — ce sont les contrats de schéma de l'application. Les revues de code incluent la lecture des migrations pour s'assurer qu'elles sont réversibles.

## Requêtes CRUD avec SQLAlchemy ORM 2.0

### Créer des enregistrements (INSERT)

```python
from sqlalchemy.orm import Session
from models import Utilisateur, Article
from database import SessionLocal

db = SessionLocal()

# Créer un utilisateur
nouvel_utilisateur = Utilisateur(
    username="charlie",
    email="charlie@exemple.com",
    hashed_password="$2b$12$...",
    est_admin=False,
)
db.add(nouvel_utilisateur)
db.commit()
db.refresh(nouvel_utilisateur)  # Recharge l'objet depuis la DB (id assigné)
print(nouvel_utilisateur.id)    # 1 (ou l'ID auto-généré)
```

> [!NOTE] `db.commit()` puis `db.refresh()`
> Après `commit()`, les champs générés par la base (id auto-incrémenté, `default=func.now()`) sont assignés dans la DB mais pas encore mis à jour dans l'objet Python. `db.refresh(objet)` recharge l'objet depuis la DB pour synchroniser les valeurs générées.

### Lire des enregistrements (SELECT)

```python
from sqlalchemy import select

# Lecture par clé primaire — retourne None si inexistant
user = db.get(Utilisateur, 1)

# SELECT avec filtre (SQLAlchemy 2.0)
stmt = select(Utilisateur).where(Utilisateur.username == "charlie")
user = db.execute(stmt).scalars().first()

# Lister tous les utilisateurs actifs, triés par username
stmt = (
    select(Utilisateur)
    .where(Utilisateur.est_actif == True)
    .order_by(Utilisateur.username)
    .limit(10)
    .offset(0)
)
utilisateurs = db.execute(stmt).scalars().all()

# Compter
from sqlalchemy import func
stmt = select(func.count()).select_from(Utilisateur).where(Utilisateur.est_actif == True)
nb = db.execute(stmt).scalar()
```

### Modifier des enregistrements (UPDATE)

```python
# Charger l'objet, modifier ses attributs, commit
user = db.get(Utilisateur, 1)
if user:
    user.email = "nouvel_email@exemple.com"
    user.est_actif = False
    db.commit()
    db.refresh(user)

# UPDATE en masse avec SQLAlchemy 2.0
from sqlalchemy import update
stmt = (
    update(Utilisateur)
    .where(Utilisateur.est_actif == False)
    .values(est_admin=False)
)
db.execute(stmt)
db.commit()
```

### Supprimer des enregistrements (DELETE)

```python
# Supprimer un objet chargé
user = db.get(Utilisateur, 1)
if user:
    db.delete(user)
    db.commit()

# DELETE en masse
from sqlalchemy import delete
stmt = delete(Utilisateur).where(Utilisateur.est_actif == False)
db.execute(stmt)
db.commit()
```

### Filtres courants

```python
from sqlalchemy import and_, or_, not_, like, in_

# AND implicite (plusieurs where enchaînés)
stmt = select(Article).where(Article.publie == True).where(Article.auteur_id == 1)

# OR explicite
stmt = select(Utilisateur).where(
    or_(Utilisateur.username == "alice", Utilisateur.est_admin == True)
)

# LIKE (recherche textuelle)
stmt = select(Article).where(Article.titre.like("%FastAPI%"))

# IN
stmt = select(Article).where(Article.auteur_id.in_([1, 2, 3]))

# IS NULL
stmt = select(Article).where(Article.date_publication.is_(None))
```

![Cycle de vie d'un objet SQLAlchemy dans la Session](../08-images/ch04-session-lifecycle.svg)

Le schéma ci-dessus illustre les quatre états d'un objet SQLAlchemy dans une Session : **transient** (créé mais pas ajouté), **pending** (ajouté mais pas encore commité), **persistent** (commité, suivi par la session), **detached** (session fermée, l'objet existe mais n'est plus suivi). Les transitions entre ces états correspondent aux opérations `add()`, `commit()`, `close()`, `expunge()`.

## Patterns de requête courants

### Requête avec jointure

```python
# Récupérer les articles avec les informations de leur auteur
stmt = (
    select(Article, Utilisateur)
    .join(Utilisateur, Article.auteur_id == Utilisateur.id)
    .where(Article.publie == True)
    .order_by(Article.date_creation.desc())
)
resultats = db.execute(stmt).all()
for article, auteur in resultats:
    print(f"{article.titre} — par {auteur.username}")
```

### Requête avec agrégation

```python
from sqlalchemy import func

# Nombre d'articles par auteur
stmt = (
    select(Utilisateur.username, func.count(Article.id).label("nb_articles"))
    .join(Article, Article.auteur_id == Utilisateur.id)
    .group_by(Utilisateur.username)
    .order_by(func.count(Article.id).desc())
)
resultats = db.execute(stmt).all()
```

### Accéder aux relations chargées

```python
user = db.get(Utilisateur, 1)
# Attention : accéder à user.articles déclenche un SELECT supplémentaire (lazy loading)
# Ce comportement est détaillé au Chapitre 5
for article in user.articles:
    print(article.titre)
```
