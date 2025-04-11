from pydantic import BaseModel

from datetime import datetime
from typing import Optional


class QuestionCreate(BaseModel):
    title: str
    description: Optional[str] = None
    topic_id: int
    owner_id: int
    

class QuestionResponse(BaseModel):
    id:int
    title: str
    description: Optional[str] = None
    topic_id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime 


class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    topic_id: Optional[int] = None
    owner_id: Optional[int] = None