from fastapi import FastAPI
from app.db.database import engine
from app.db import catalog
from app.routers import players, leagues, auth, matches, fantasy_team, users

# Create tables if not using Alembic yet
catalog.Base.metadata.create_all(bind=engine)

app = FastAPI(title="NWSL Fantasy API")

# Include routers
app.include_router(players.router)
app.include_router(leagues.router)
app.include_router(fantasy_team.router)
app.include_router(auth.router)
# Include other routers as needed

@app.get("/")
def read_root():
    return {"message": "Welcome to the NWSL Fantasy API!"}


