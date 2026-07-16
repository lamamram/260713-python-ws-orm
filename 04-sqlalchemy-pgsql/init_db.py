"""
script d'initialisation de la base de données PostgreSQL avec SQLAlchemy
utilise une fonction init_db() idempotente pour créer les tables si elles n'existent pas déjà
"""

from database import engine, SessionLocal, Base, Utilisateur, Article, Tag, ProfilUtilisateur
import sys

def init_db():
    """
    Initialise la base de données en créant les tables définies dans les modèles SQLAlchemy.
    Cette fonction est idempotente : elle ne recrée pas les tables si elles existent déjà.
    """
    if len(sys.argv) > 1 and sys.argv[1] == "--force-delete":
        # Supprime toutes les tables existantes avant de les recréer
        Base.metadata.drop_all(bind=engine)
        print("Toutes les tables existantes ont été supprimées.")

    # Crée toutes les tables définies dans les modèles SQLAlchemy
    # si elles existent déjà, cette opération est ignorée (idempotente)
    # => CREATE TABLE IF NOT EXISTS ...
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée avec succès !")
    
    # une session s'ouvre et se ferme !!!
    with SessionLocal() as session:
        print("insertion des utilisateurs...")
        user_admin = Utilisateur(
            username="admin", 
            email="adm@example.com",
            hashed_password="roottoor",
            is_admin=True
        )
        user_admin.hash_password()
        user_normal = Utilisateur(
            username="gars", 
            email="gars@example.com",
            hashed_password="roottoor"
        )
        user_normal.hash_password()
        session.add_all([user_admin, user_normal])
        # print(user_normal)
        # flush pour obtenir les IDs générés, les valeurs par défaut et les valeurs calculées par la base de données
        # écrit dans le cache de la session mais ne valide pas encore la transaction
        # ce cache == identity map: permet de retrouver les objets déjà présents dans la session et d'éviter les doublons
        session.flush()
        # print(user_normal)

        session.commit()  # Valide la transaction et écrit les changements dans la base de données
if __name__ == "__main__":
    init_db()