from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/auteurs", tags=["Auteurs"])

# ------------ pydantic requests schémas ------------

class AuteurCreation(BaseModel):
    nom: str = Field(min_length=2, max_length=100)
    email: EmailStr
    age: int = Field(ge=18, le=120)
    tags: List[str] = Field(default_factory=list)
    biographie: Optional[str] = Field(default="", max_length=2000)

# ------------ pydantic responses schémas ------------

class AuteurResponse(BaseModel):
    id: int
    nom: str = Field(min_length=2, max_length=100)
    email: EmailStr                                    # Valide le format email
    age: int = Field(ge=18, le=120)
    tags: List[str] = Field(default_factory=list)     # Liste vide par défaut à la place de [""]
    biographie: str = Field(default="", max_length=2000)

# ----------- routes ------------

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