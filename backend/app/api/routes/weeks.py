from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.api.deps import get_current_user
from app.schemas.week import WeekResponse
from app.data.curriculum import CURRICULUM
from app.services.roadmap import initialize_default_roadmap

router = APIRouter()

@router.post("/initialize", status_code=status.HTTP_200_OK)
async def initialize_roadmap(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    await initialize_default_roadmap(user_id)
    return {"status": "success", "message": "Roadmap initialized successfully."}

@router.get("", response_model=List[WeekResponse])
async def get_weeks(current_user: dict = Depends(get_current_user)):
    # Curriculum identity and user progress are separated.
    # Weeks are fully static/shared definitions, no DB fetch required.
    user_id = str(current_user["_id"])
    result = []
    for w in CURRICULUM:
        w_copy = dict(w)
        w_copy["user_id"] = user_id
        w_copy["created_at"] = w_copy.get("created_at") or "2026-01-01T00:00:00Z"
        w_copy["updated_at"] = w_copy.get("updated_at") or "2026-01-01T00:00:00Z"
        result.append(w_copy)
    return result

@router.get("/{week_id}", response_model=WeekResponse)
async def get_week(week_id: str, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    for w in CURRICULUM:
        if w["id"] == week_id:
            w_copy = dict(w)
            w_copy["user_id"] = user_id
            w_copy["created_at"] = w_copy.get("created_at") or "2026-01-01T00:00:00Z"
            w_copy["updated_at"] = w_copy.get("updated_at") or "2026-01-01T00:00:00Z"
            return w_copy
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Week not found")
