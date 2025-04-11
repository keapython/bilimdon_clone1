from pydantic import BaseModel



class TopicCreate(BaseModel):
    name: str

class TopicResponse(BaseModel):
    id:int
    name:str
