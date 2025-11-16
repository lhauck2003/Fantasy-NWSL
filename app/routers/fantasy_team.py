## Holds the Code for getting a fantasy team information and gives the user ability to sub,
## transfer, or view their team for the week 
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# sample data
team_db = {
    "000001": {
        "goalkeeper": [
            { "id": 100, "name": "GK A", "position": "GK", "team": "Team A", "price": 5.0 , "captain": False}
        ],
        "defenders": [
            { "id": 3,  "name": "DEF A", "position": "DEF", "team": "Team A", "price": 5.0, "captain": False },
            { "id": 4,  "name": "DEF B", "position": "DEF", "team": "Team B", "price": 4.5, "captain": False },
            { "id": 5,  "name": "DEF C", "position": "DEF", "team": "Team A", "price": 5.1, "captain": False },
            { "id": 11, "name": "DEF D", "position": "DEF", "team": "Team B", "price": 5.1, "captain": False },
        ],
        "midfielders": [
            { "id": 6, "name": "MID A", "position": "MID", "team": "Team A", "price": 7.0, "captain": False },
            { "id": 7, "name": "MID B", "position": "MID", "team": "Team B", "price": 8.0, "captain": False },
            { "id": 8, "name": "MID C", "position": "MID", "team": "Team A", "price": 6.5, "captain": False },
            { "id": 9, "name": "MID D", "position": "MID", "team": "Team B", "price": 6.1, "captain": False },
        ],
        "forwards": [
            { "id": 1, "name": "FWD A", "position": "FWD", "team": "Team A", "price": 9.0, "captain": True },
            { "id": 2, "name": "FWD B", "position": "FWD", "team": "Team B", "price": 8.5, "captain": False },
        ], 
        "substitutes": [
            { "id": 20, "name": "Sub DEF", "position": "DEF", "team": "Team A", "price": 4.0, "captain": False },
            { "id": 21, "name": "Sub GK",  "position": "GK",  "team": "Team B", "price": 4.5, "captain": False },
            { "id": 22, "name": "Sub MID", "position": "MID", "team": "Team A", "price": 4.3, "captain": False },
            { "id": 23, "name": "Sub FWD", "position": "FWD", "team": "Team B", "price": 4.7, "captain": False },
        ]
    }
}


class TeamRequest(BaseModel):
    userID: str

@router.post('/fetch_team')
def fetch_team(request: TeamRequest):
    team = get_team(request.userID)
    if not team:
        raise HTTPException(status_code=404, detail="User not found") 
    return team

class TeamPost(BaseModel):
    userID: str
    team: dict

@router.post('/save_team')
def save_team(request: TeamPost):
    set_team(request.userID, request.team)

def set_team(userID: str, team: dict):
    team_db['userID'] = team
    print(team_db)

def get_team(userID: str):
    return team_db.get(userID)