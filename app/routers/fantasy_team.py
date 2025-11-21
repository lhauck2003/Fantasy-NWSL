## Holds the Code for getting a fantasy team information and gives the user ability to sub,
## transfer, or view their team for the week 
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from modules.fantasy_team import get_fantasy_team, save_fantasy_team

router = APIRouter()

class TeamRequest(BaseModel):
    userID: str

@router.post('/fetch_team')
async def fetch_team(request: TeamRequest):
    team = await get_team(request.userID)
    #print(team)
    if not team:
        return default_team()
        raise HTTPException(status_code=404, detail="User not found") 
    return team

class TeamPost(BaseModel):
    userID: str
    team: dict

@router.post('/save_team')
async def save_team(request: TeamPost):
    (error, message) = await set_team(request.userID, request.team)
    if error:
        print("Error saving team:", message)
        raise HTTPException(status_code=404, detail=message)
    

async def set_team(userID: str, team: dict):
    #team_db['userID'] = team
    #return False, ""
    (error, message) = await save_fantasy_team(team, userID)
    return (error, message)

async def get_team(userID: str):
    team = await get_fantasy_team(userID)
    return team[userID]
    #return team_db.get(userID)#

def default_team():
    # formation is 4-4-2 plus 4 substitutes
    return {
        "goalkeeper": [ {"player_id": "a", "player": "+","position": "G"}],
        "defenders": [  {"player_id": "b", "player": "+", "position": "D"},
                        {"player_id": "c", "player": "+", "position": "D"},
                        {"player_id": "d", "player": "+", "position": "D"},
                        {"player_id": "e", "player": "+", "position": "D"},
                   ],
        "midfielders": [{"player_id": "f", "player": "+", "position": "M"},
                        {"player_id": "g", "player": "+", "position": "M"},
                        {"player_id": "h", "player": "+", "position": "M"},
                        {"player_id": "i", "player": "+", "position": "M"},
                    ],
        "forwards": [   {"player_id": "j", "player": "+", "position": "F"},
                        {"player_id": "k", "player": "+", "position": "F"},
                ],
        "substitutes": [{"player_id": "l", "player": "+", "position": "G"},
                        {"player_id": "m", "player": "+", "position": "D"},
                        {"player_id": "n", "player": "+", "position": "M"},
                        {"player_id": "o", "player": "+", "position": "F"},
                    ],  
    }
