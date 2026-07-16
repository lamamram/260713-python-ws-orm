from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
# pip install python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()  # charge les variables d'environnement depuis le fichier .env

pg_user = os.getenv("PG_USER", "root")
pg_pass = os.getenv("PG_PASS", "")
pg_host = os.getenv("PG_HOST", "localhost")
pg_port = os.getenv("PG_PORT", "5432")
pg_db = os.getenv("PG_DB", "default")

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