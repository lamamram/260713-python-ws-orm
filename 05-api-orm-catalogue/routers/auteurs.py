from fastapi import APIRouter, Path, Query
from schemas.auteurs import AuteurCreation, AuteurResponse

router = APIRouter(prefix="/auteurs", tags=["Auteurs"])

@router.get("/")
def list_auteurs(
    page: int = Query(1, gt=0, description="Numéro de la page (doit être un entier positif)"),
    taille: int = Query(10, gt=0, le=100, description="Nombre d'auteurs par page (doit être un entier positif entre 1 et 100)")
):
    """
    GET /auteurs → page=1, taille=10
    GET /auteurs?page=2&taille=5 → page=2, taille=5
    """
    return {
        "page": page,
        "taille": taille,
        "auteurs": [],
    }

@router.post("/", response_model=AuteurResponse, status_code=201)
def create_auteur(auteur: AuteurCreation):
    """
    Crée un nouvel auteur.
    """
    return {
        "id": 1, **auteur.model_dump()  # Retourne l'auteur créé avec un ID fictif
    }