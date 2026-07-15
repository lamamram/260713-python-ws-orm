from fastapi import APIRouter, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from exceptions import RessourceNonTrouveException

router = APIRouter(prefix="/articles", tags=["Articles"])

# ------------ pydantic requests schémas ------------
class ArticleCreation(BaseModel):
    titre: str = Field(min_length=3, max_length=200)
    contenu: str = Field(min_length=10)
    categorie: Optional[str] = None

# ------------ pydantic responses schémas ------------

class ArticleResponse(BaseModel):
    id: int
    titre: str
    contenu: str
    publie: bool = False
    date_creation: datetime
    categorie: Optional[str] = None
    # nb-vues est caclulé par le serveur, donc on gère ici ses contraintes
    nb_vues: int = Field(default=0, ge=0)

# ----------- routes ------------

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

@router.post("/", status_code=201, response_model=ArticleResponse)
def create_article(article: ArticleCreation):
    """
    Reçoit un corps JSON :
    {"titre": "Mon article", "contenu": "...", "publie": false}
    """

    # REM: on retourne un dictionnaire MAIS 
    # fastapi va le convertir en ArticleResponse grâce à la déclaration response_model=ArticleResponse
    return { "id": 1, **article.model_dump(), "date_creation": datetime.now() }


@router.get("/{article_id}")
def get_article(article_id: int = Path(gt=0, description="L'ID de l'article doit être un entier positif")):
    """Retourne un article fictif identifié par son ID entier."""
    articles = range(1, 100)
    if article_id not in articles:
        # raise HTTPException(
        #     status_code=404, 
        #     detail=f"Article {article_id} non trouvé"
        # )
        raise RessourceNonTrouveException(
            id=article_id, 
            resource_type="article"
        )
    
    return {"id": article_id, "titre": f"Article numéro {article_id}"}

@router.delete("/{article_id}", status_code=204)
def delete_article(article_id: int = Path(gt=0, description="L'ID de l'article doit être un entier positif")):
    """Supprime un article fictif identifié par son ID entier."""
    return None