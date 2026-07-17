from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

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
