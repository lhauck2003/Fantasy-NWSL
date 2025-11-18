from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.db import catalog
from routers import userlogin, fantasy_team, players

app = FastAPI(title="NWSL Fantasy API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # all origins allowed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# app.include_router(leagues.router)
app.include_router(fantasy_team.router)
app.include_router(players.router)
# app.include_router(auth.router)
app.include_router(userlogin.router)