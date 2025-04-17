from pydantic import BaseModel

from datetime import datetime


class OptionResponse(BaseModel):
    id: int
    question_id: int
    title: str
    is_correct: bool
    created_at: datetime


class OptionCreate(BaseModel):
    question_id: int
    title: str
    is_correct: bool

class OptionUpdate(BaseModel):
    title: str | None = None
    is_correct: bool | None = None


