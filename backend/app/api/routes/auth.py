from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError

from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.core.security import get_password_hash, verify_password, create_access_token
from app.api.deps import get_current_user
from app.db.connection import db_client

router = APIRouter()

def serialize_user(user: dict) -> dict:
    """Helper to convert MongoDB user dict to UserResponse compatible dict"""
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"],
    }

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    db = db_client.database
    
    # Normalize email to lowercase
    normalized_email = user_in.email.lower()
    
    # Create user document
    now = datetime.now(timezone.utc)
    user_doc = {
        "name": user_in.name,
        "email": normalized_email,
        "password_hash": get_password_hash(user_in.password),
        "created_at": now,
        "updated_at": now
    }
    
    try:
        result = await db["users"].insert_one(user_doc)
        user_doc["_id"] = result.inserted_id
        return serialize_user(user_doc)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists."
        )

@router.post("/login", response_model=Token)
async def login(login_in: UserLogin):
    db = db_client.database
    normalized_email = login_in.email.lower()
    
    user = await db["users"].find_one({"email": normalized_email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
        
    if not verify_password(login_in.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
        
    access_token = create_access_token(subject=str(user["_id"]))
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return serialize_user(current_user)
