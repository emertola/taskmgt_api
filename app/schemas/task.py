from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime