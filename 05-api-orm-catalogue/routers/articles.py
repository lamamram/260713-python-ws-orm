from fastapi import APIRouter, Path, Query, HTTPException, Depends
from datetime import datetime
from exceptions import RessourceNonTrouveException
from dependencies import get_query_params, GetQueryParams
from schemas.articles import ArticleCreation, ArticleResponse
from typing import List

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.get("/", response_model=List[ArticleResponse])
def list_articles(
    # params est un terme consacré dans fastapi pour désigner les paramètres de requête (query params)
    # on peut utiliser Depends pour injecter une dépendance dans la route
    
    # la fonction get_query_params est appelée et sont retour est injectée dans la variable params
    # ici les paramètres de cette fonctions épousent les paramètres de la route, donc fastapi va automatiquement les remplir avec les valeurs de la requête
    params: dict = Depends(get_query_params),
    
    # idem pour une classe
    # params: GetQueryParams = Depends()
):
    return {
        "pagination": params,
        # "page": page,
        # "taille": taille,
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


@router.get("/{article_id}", response_model=ArticleResponse)
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