from fastapi import APIRouter, Path, Query
from schemas.taches import TacheResponse, TacheCreation
from typing import List
from datetime import datetime

router = APIRouter(prefix="/taches", tags=["taches"])

@router.get("/", response_model=List[TacheResponse])
def get_taches(
    priorite: int = Query(default=None, ge=1, le=5, description="Filtrer les tâches par priorité (1 à 5)")
):
    taches = [
        {"id": 1, "titre": "Faire les courses", "date_creation": datetime.now()},
        {"id": 2, "priorite": 2, "titre": "Faire le ménage", "date_creation": datetime.now()}
    ]
    if priorite:
        taches = [tache for tache in taches if tache.get("priorite", 3) == priorite]
    return taches

@router.post("/", response_model=TacheResponse)
def create_tache(tache: TacheCreation):
    new_tache = {
        "id": 3,
        **tache.model_dump(),
        "date_creation": datetime.now()
    }
    return new_tache