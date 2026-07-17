from fastapi import APIRouter, Path, Query, HTTPException, Depends
from datetime import datetime
from exceptions import RessourceNonTrouveException
from dependencies import get_query_params, GetQueryParams
from schemas.articles import ArticleCreation, ArticleResponse
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db, Article

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.get("/", response_model=List[ArticleResponse])
def list_articles(
    params: dict = Depends(get_query_params),
    db: Session = Depends(get_db)
):
    return db.execute(select(Article)).scalars().all()

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
def get_article(
    article_id: int = Path(gt=0, description="L'ID de l'article doit être un entier positif"),
    db: Session = Depends(get_db)
):
    """Retourne un article fictif identifié par son ID entier."""
    article = db.get(Article, article_id)
    if article is None:
        raise RessourceNonTrouveException(
            id=article_id, 
            resource_type="article"
        )
    
    return article

@router.delete("/{article_id}", status_code=204)
def delete_article(article_id: int = Path(gt=0, description="L'ID de l'article doit être un entier positif")):
    """Supprime un article fictif identifié par son ID entier."""
    return None