from pydantic import BaseModel
from typing import Optional


# Modèle Pydantic pour l'API
class Todo(BaseModel):
    id: int
    title: str
    description: str = None
    completed: bool = False

    class Config:
        from_attributes = True


# Modèle Pydantic pour la mise à jour d'une tâche
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None