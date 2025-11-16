from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

players_db = {
    1: {"name": "DEF A", "position": "DEF", "team": "Team A", "price": 9.5},
    2: {"name": "DEF B", "position": "DEF", "team": "Team C", "price": 5.5},
    3: {"name": "DEF C", "position": "DEF", "team": "Team D", "price": 8.5},
    4: {"name": "FW A",  "position": "FW",  "team": "Team B", "price": 4.5},
}

class PlayerRequest(BaseModel):
    which: Dict[str, Any]

@router.post("/players")
def get_players(req: PlayerRequest):
    filters = req.which

    # Handle "all"
    if filters == "all":
        return {"players": [
            {"id": pid, **pdata} for pid, pdata in players_db.items()
        ]}

    # Otherwise filter normally
    results = []
    for pid, pdata in players_db.items():
        match = True
        for key, value in filters.items():
            if key not in pdata or pdata[key] != value:
                match = False
                break
        if match:
            results.append({"id": pid, **pdata})

    return {"players": results}


