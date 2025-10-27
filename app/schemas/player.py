from pydantic import BaseModel

class PlayerBase(BaseModel):
    name: str
    position: str
    team_id: int

class PlayerCreate(PlayerBase):
    pass

class Player(PlayerBase):
    id: int
    class Config:
        orm_mode = True
