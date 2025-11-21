from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, Union
from modules.players import get_players_db

router = APIRouter()

class PlayerRequest(BaseModel):
    which: Union[str, Dict[str, Any]]

@router.post("/players")
async def get_players(req: PlayerRequest):
    filters = req.which
    players = await get_players_db()
    # Return all players
    if filters == "all":
        return {
            "players": [
                {"id": pid, **dict(player)}
                for pid, player in players.items()
            ]
        }

    # Filtering
    results = []
    for pid, player in players.items():
        match = True
        for key, value in filters.items():
            if player.get(key) != value:
                match = False
                break
        if match:
            results.append({"id": pid, **dict(player)})

    return {"players": results}
