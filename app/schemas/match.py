from pydantic import BaseModel

class MatchBase(BaseModel):
    home_team_id: int
    away_team_id: int
    home_score: int
    away_score: int

class MatchCreate(MatchBase):
    pass

class Match(MatchBase):
    id: int
    class Config:
        orm_mode = True
