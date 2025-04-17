from pydantic import BaseModel

from datetime import datetime


class ParticipationResponse(BaseModel):
    id: int 
    game_id: int
    start_time: datetime
    end_time: datetime
    gained_score: int
    registered_at: datetime

class ParticipationCreate(BaseModel):
    game_id: int
    start_time: datetime
    end_time: datetime


class ParticipationUpdate(BaseModel):
    game_id: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    