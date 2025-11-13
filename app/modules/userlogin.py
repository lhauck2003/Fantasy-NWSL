## Handles the logging in of users for the Fantasy NWSL application.
## Uses FastAPI for API routing
## Uses Argon2 for password hashing and verification
from fastapi import APIRouter, HTTPException, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from argon2 import PasswordHasher
# from db.data import user_db

# mock user database
user_db = {
    "testuser": {
        "username": "testuser",
        "hashed_password": PasswordHasher().hash("test123")  # hash for "testpassword"
        }
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # all origins allowed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

# User Data comes from database

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login_user(request: LoginRequest):
    ph = PasswordHasher()
    # Fetch user from database (pseudo-code)
    user = get_user_from_db(request.username)  # This function should be implemented to fetch user data
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        ph.verify(user['hashed_password'], request.password)
        return {"message": "Login successful"}
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")    
    
def get_user_from_db(username: str):
    return user_db.get(username)

app.include_router(router)

