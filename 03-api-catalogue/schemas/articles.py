from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

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