from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TacheResponse(BaseModel):
    id: int
    titre: str = Field(min_length=3, max_length=100)
    description: Optional[str] = None
    terminee: bool = False
    priorite: int = Field(default=3, ge=1, le=5)
    date_creation: datetime

class TacheCreation(BaseModel):
    titre: str = Field(min_length=3, max_length=100)
    description: Optional[str] = None
    priorite: int = Field(default=3, ge=1, le=5)
