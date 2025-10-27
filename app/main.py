from fastapi import FastAPI
from app.db.database import engine
from app.db import catalog
from app.routers import players, matches, fantasy, users

# Create tables if not using Alembic yet
catalog.Base.metadata.create_all(bind=engine)

app = FastAPI(title="NWSL Fantasy API")

# Include routers
app.include_router(players.router)
app.include_router(matches.router)
app.include_router(fantasy.router)
app.include_router(users.router)
