from fastapi import APIRouter, Path, Query
from typing import Optional

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.get("/")
def list_articles(
    page: int = Query(1, gt=0, description="Numéro de la page (doit être un entier positif)"),
    taille: int = Query(10, gt=0, le=100, description="Nombre d'articles par page (doit être un entier positif entre 1 et 100)"),
    # Optional est une annotation de type qui indique que la variable peut être de type str ou None
    # comme str | None mais Optional est plus explicite pour les devs et fastapi
    categorie: Optional[str] = None
):
    """
    GET /articles → page=1, taille=10
    GET /articles?page=2&taille=5 → page=2, taille=5
    GET /articles?categorie=python → filtre par catégorie
    """
    return {
        "page": page,
        "taille": taille,
        "categorie": categorie,
        "articles": [],
    }

@router.get("/{article_id}")
def get_article(article_id: int = Path(gt=0, description="L'ID de l'article doit être un entier positif")):
    """Retourne un article fictif identifié par son ID entier."""
    return {"id": article_id, "titre": f"Article numéro {article_id}"}