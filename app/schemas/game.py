from pydantic import BaseModel

from datetime import datetime


class GameResponse(BaseModel):
    id: int
    title: str
    owner_id: int
    topic_id: int
    description: str
    score: int
    start_time: datetime
    end_time: datetime


class GameCreate(BaseModel):
    title: str
    description: str
    topic_id: int


class GameUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    topic_id: str | None = None
