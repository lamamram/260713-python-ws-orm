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
    # page1 == offset=0, limit=10
    # page2 == offset=10, limit=10
    # (page_num - 1) * limit
    offset, limit = (params["page"] - 1) * params["taille"], params["taille"]
    ## SELECT * FROM articles OFFSET 0 LIMIT 10
    articles = db.execute(select(Article).offset(offset).limit(limit)).scalars().all()
    return articles

@router.post("/", status_code=201, response_model=ArticleResponse)
def create_article(
    article: ArticleCreation,
    db: Session = Depends(get_db)
):
    """
    Reçoit un corps JSON :
    {"titre": "Mon article", "contenu": "...", "publie": false}
    """
    new_article = Article(
        titre=article.titre,
        contenu=article.contenu,
        auteur_id=1  # pour l'instant, on met un auteur fictif
    )
    # insérer l'article dans la base de données
    db.add(new_article)
    # pas besoin de flusher car db.commit() va flusher automatiquement
    db.commit()
    return new_article


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
def delete_article(
    article_id: int = Path(gt=0, description="L'ID de l'article doit être un entier positif"),
    db: Session = Depends(get_db)
):
    """Supprime un article fictif identifié par son ID entier."""
    article = db.get(Article, article_id)
    if article is None:
        raise RessourceNonTrouveException(
            id=article_id, 
            resource_type="article"
        )
    db.delete(article) 
    db.commit()
    return None