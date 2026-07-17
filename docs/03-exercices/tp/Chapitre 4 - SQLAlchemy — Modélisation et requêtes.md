## Exercice 1 — Modéliser un domaine avec SQLAlchemy

**Étape 1 — Créer le projet et installer les dépendances**

```bash
mkdir plateforme-cours ; cd plateforme-cours
python -m venv .venv ; .venv\Scripts\Activate.ps1
pip install "sqlalchemy[asyncio]" alembic
pip freeze > requirements.txt
```

**Étape 2 — Créer `database.py`**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./cours.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass
```

**Étape 3 — Créer `models.py`**

```python
from sqlalchemy import String, Boolean, Integer, Numeric, Text, DateTime, ForeignKey, Table, Column, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from datetime import datetime
from typing import Optional

# Table d'association n-à-n avec colonnes supplémentaires
class Inscription(Base):
    __tablename__ = "inscriptions"

    cours_id: Mapped[int] = mapped_column(Integer, ForeignKey("cours.id"), primary_key=True)
    stagiaire_id: Mapped[int] = mapped_column(Integer, ForeignKey("stagiaires.id"), primary_key=True)
    date_inscription: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    note: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Accès aux objets liés
    cours: Mapped["Cours"] = relationship("Cours", back_populates="inscriptions")
    stagiaire: Mapped["Stagiaire"] = relationship("Stagiaire", back_populates="inscriptions")


class Formateur(Base):
    __tablename__ = "formateurs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    specialite: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    date_inscription: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    cours: Mapped[list["Cours"]] = relationship("Cours", back_populates="formateur",
                                                 cascade="all, delete-orphan")


class Cours(Base):
    __tablename__ = "cours"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titre: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    prix: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    duree_heures: Mapped[int] = mapped_column(Integer, nullable=False)
    publie: Mapped[bool] = mapped_column(Boolean, default=False)
    date_creation: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    formateur_id: Mapped[int] = mapped_column(Integer, ForeignKey("formateurs.id"), nullable=False)

    formateur: Mapped["Formateur"] = relationship("Formateur", back_populates="cours")
    inscriptions: Mapped[list["Inscription"]] = relationship("Inscription", back_populates="cours")


class Stagiaire(Base):
    __tablename__ = "stagiaires"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    date_inscription: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    inscriptions: Mapped[list["Inscription"]] = relationship("Inscription", back_populates="stagiaire")
```

**Étape 4 — Créer les tables**

```python
# create_tables.py
from database import engine, Base
import models  # Importer pour enregistrer les modèles

Base.metadata.create_all(bind=engine)
print("Tables créées !")
```

```bash
python create_tables.py
```

**Étape 5 — Initialiser Alembic**

```bash
alembic init alembic
```

Modifier `alembic/env.py` :
```python
from database import Base
import models  # Charge tous les modèles
target_metadata = Base.metadata
```

Modifier `alembic.ini` :
```ini
sqlalchemy.url = sqlite:///./cours.db
```

```bash
alembic revision --autogenerate -m "schema_initial"
alembic upgrade head
alembic history  # Vérifier que la migration est appliquée
```

---

## Exercice 2 — Requêtes CRUD

**Créer `seed.py`**

```python
# seed.py
from sqlalchemy import select, func
from database import SessionLocal, engine, Base
import models
from models import Formateur, Cours, Stagiaire, Inscription
from datetime import datetime

Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    # 1. Créer 2 formateurs
    f1 = Formateur(nom="Alice Martin", email="alice@dawan.fr", specialite="Python")
    f2 = Formateur(nom="Bob Dupont",   email="bob@dawan.fr",   specialite="DevOps")
    db.add_all([f1, f2])
    db.commit()
    db.refresh(f1) ; db.refresh(f2)

    # 2. Créer 3 cours
    c1 = Cours(titre="Python Initiation", prix=975, duree_heures=35, publie=True, formateur_id=f1.id)
    c2 = Cours(titre="FastAPI + ORM",    prix=975, duree_heures=35, publie=True, formateur_id=f1.id)
    c3 = Cours(titre="Docker",           prix=975, duree_heures=21, publie=False, formateur_id=f2.id)
    db.add_all([c1, c2, c3])
    db.commit()
    db.refresh(c1) ; db.refresh(c2) ; db.refresh(c3)

    # 3. Créer 4 stagiaires
    s1 = Stagiaire(nom="Charlie",  email="charlie@ex.fr")
    s2 = Stagiaire(nom="Diane",    email="diane@ex.fr")
    s3 = Stagiaire(nom="Eve",      email="eve@ex.fr")
    s4 = Stagiaire(nom="Frank",    email="frank@ex.fr")
    db.add_all([s1, s2, s3, s4])
    db.commit()
    for s in [s1, s2, s3, s4]:
        db.refresh(s)

    # 4. Inscrire 3 stagiaires au cours 1, 2 au cours 2
    for stagiaire in [s1, s2, s3]:
        db.add(Inscription(cours_id=c1.id, stagiaire_id=stagiaire.id))
    for stagiaire in [s2, s4]:
        db.add(Inscription(cours_id=c2.id, stagiaire_id=stagiaire.id))
    db.commit()

    # 5. Lister les cours publiés triés par prix croissant
    print("\n--- Cours publiés ---")
    stmt = select(Cours).where(Cours.publie == True).order_by(Cours.prix)
    for cours in db.execute(stmt).scalars().all():
        print(f"  {cours.titre} — {cours.prix} € — {cours.duree_heures}h")

    # 6. Compter les inscrits par cours
    print("\n--- Inscrits par cours ---")
    stmt = (
        select(Cours.titre, func.count(Inscription.stagiaire_id).label("nb"))
        .join(Inscription, Inscription.cours_id == Cours.id)
        .group_by(Cours.titre)
    )
    for titre, nb in db.execute(stmt).all():
        print(f"  {titre} : {nb} inscrits")

    # 7. Stagiaires inscrits au cours 1
    print(f"\n--- Stagiaires du cours '{c1.titre}' ---")
    stmt = (
        select(Stagiaire)
        .join(Inscription, Inscription.stagiaire_id == Stagiaire.id)
        .where(Inscription.cours_id == c1.id)
    )
    for st in db.execute(stmt).scalars().all():
        print(f"  {st.nom} ({st.email})")

finally:
    db.close()
```

```bash
python seed.py
```

Résultat attendu :
```
--- Cours publiés ---
  Python Initiation — 975 € — 35h
  FastAPI + ORM — 975 € — 35h

--- Inscrits par cours ---
  Python Initiation : 3 inscrits
  FastAPI + ORM : 2 inscrits

--- Stagiaires du cours 'Python Initiation' ---
  Charlie (charlie@ex.fr)
  Diane (diane@ex.fr)
  Eve (eve@ex.fr)
```
