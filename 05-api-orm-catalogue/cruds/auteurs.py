from sqlalchemy.orm import Session
from database import auteur

def get_auteur_id(
    db: Session,
    auteur_id: int 
):
    return db.get(auteur, auteur_id)