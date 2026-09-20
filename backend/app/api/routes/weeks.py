from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime, timezone
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from app.api.deps import get_current_user
from app.schemas.week import WeekCreate, WeekResponse
from app.db.connection import db_client

router = APIRouter()

def serialize_week(week: dict) -> dict:
    week["id"] = str(week.pop("_id"))
    return week

@router.post("", response_model=WeekResponse, status_code=status.HTTP_201_CREATED)
async def create_week(week_in: WeekCreate, current_user: dict = Depends(get_current_user)):
    db = db_client.database
    now = datetime.now(timezone.utc)
    user_id = str(current_user["_id"])
    
    week_doc = week_in.model_dump()
    week_doc["user_id"] = user_id
    week_doc["created_at"] = now
    week_doc["updated_at"] = now
    
    try:
        result = await db["weeks"].insert_one(week_doc)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Week {week_in.week_number} already exists for this user."
        )
    
    created_week = await db["weeks"].find_one({"_id": result.inserted_id})
    return serialize_week(created_week)

@router.get("", response_model=List[WeekResponse])
async def get_weeks(current_user: dict = Depends(get_current_user)):
    db = db_client.database
    user_id = str(current_user["_id"])
    
    cursor = db["weeks"].find({"user_id": user_id}).sort("week_number", 1)
    weeks = await cursor.to_list(length=100)
    
    return [serialize_week(w) for w in weeks]

@router.get("/{week_id}", response_model=WeekResponse)
async def get_week(week_id: str, current_user: dict = Depends(get_current_user)):
    db = db_client.database
    user_id = str(current_user["_id"])
    
    if not ObjectId.is_valid(week_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid week ID format")
        
    week = await db["weeks"].find_one({"_id": ObjectId(week_id), "user_id": user_id})
    if not week:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Week not found")
        
    return serialize_week(week)
