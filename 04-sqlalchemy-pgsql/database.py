from sqlalchemy import create_engine, Integer, String, Boolean, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
# pip install python-dotenv
from dotenv import load_dotenv
import os
from datetime import datetime
from typing import List

load_dotenv()  # charge les variables d'environnement depuis le fichier .env

pg_user = os.getenv("PG_USER", "root")
pg_pass = os.getenv("PG_PASS", "")
pg_host = os.getenv("PG_HOST", "localhost")
pg_port = os.getenv("PG_PORT", "5432")
pg_db = os.getenv("PG_DB", "default")

######################## CONFIGURATION d'un sessions SQLAlchemy pour PostgreSQL ########################

# chaine de connexion (connection string) pour 
DATABASE_URL = f"postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
engine = create_engine(
    DATABASE_URL,
    pool_size=15,  # nombre maximum de connexions persistentes dispos dans le pool pour les utilisateurs
    max_overflow=5,  # nombre maximum de connexions supplémentaires au-delà du pool_size en cas de pic
)

SessionLocal = sessionmaker(
    autocommit=False,# les transactions ne sont pas validées automatiquement, il faut appeler session.commit() pour valider
    autoflush=False, 
    bind=engine
)


def get_db():
    """
    1. Fournit une session de base de données SQLAlchemy pour chaque requête FastAPI.
    en utilisant le mécanisme Depends(get_db) pour rendre la session dispo dans les gestionnaires fastAPI
    2. sa forme de générateur (yield) permet de temporiser l'execution après le yield 
    et de de s'assurer que la session est toujours fermée après utilisation, même en cas d'exception.
    """
    db = SessionLocal()
    try:
        yield db          # Fournit la session
    finally:
        db.close()        # Toujours fermer même en cas d'exception

####################### MODELISATION DES MODELES (tables) avec SQLAlchemy #######################

class Base(DeclarativeBase):
    """
    Classe de base pour les modèles SQLAlchemy.
    Tous les modèles (tables) doivent hériter de cette classe.
    Base permet également de créer des méthodes et des attributs communs à tous les modèles si nécessaire.
    """
    pass

class Utilisateur(Base):
    """
    Modèle représentant un utilisateur.
    Chaque instance de cette classe correspond à une ligne dans la table 'utilisateurs'.
    """
    __tablename__ = "utilisateurs"  # Nom de la table dans la base de données

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # Clé primaire auto-incrémentée
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)  # Nom d'utilisateur unique et obligatoire
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)  # Mot de passe haché obligatoire
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)  # Indique si l'utilisateur est actif, par défaut True
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)  # Indique si l'utilisateur est administrateur, par défaut False
    # Date de création, par défaut la date actuelle calculée par la base de données 
    # func permet d'utiliser les fonctions de la bdd ici NOW()
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)

    ## relations
    articles: Mapped[List["Article"]] = relationship(
        back_populates="auteur",
        cascade="all, delete-orphab")  # Relation avec les articles écrits par l'utilisateur

    def __str__(self):
        """
        Représentation en chaîne de caractères de l'objet Utilisateur.
        Utile pour le débogage et la journalisation.
        """
        return f"Utilisateur(id={self.id}, username='{self.username}', email='{self.email}', active={self.active}, is_admin={self.is_admin}, created_at={self.created_at})"

class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titre: Mapped[str] = mapped_column(String(200), nullable=False)
    contenu: Mapped[str] = mapped_column(Text, nullable=False)
    publie: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    auteur_id: Mapped[int] = mapped_column(Integer, ForeignKey("utilisateurs.id"), nullable=False)

    ## relations: ce ne sont pas des colonnes de la table, on les utilise en python
    # sur un objet article = Article(), on a article.auteur
    # grâce à back_populates, on peut faire l'inverse: sur un objet utilisateur = Utilisateur(), on a utilisateur.articles
    auteur: Mapped["Utilisateur"] = relationship(back_populates="articles")

    def __str__(self):
        return f"Article(id={self.id}, titre='{self.titre}', publie={self.publie}, created_at={self.created_at}, auteur_id={self.auteur_id})"