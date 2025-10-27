from pydantic import BaseModel

class FantasyPointsBase(BaseModel):
    player_id: int
    gameweek: int
    points: int

class FantasyPointsCreate(FantasyPointsBase):
    pass

class FantasyPoints(FantasyPointsBase):
    id: int
    class Config:
        orm_mode = True
