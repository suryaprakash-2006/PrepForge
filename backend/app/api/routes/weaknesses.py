from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.api.deps import get_current_user
from app.schemas.weakness import (
    WeaknessCreate,
    WeaknessUpdate,
    WeaknessResponse,
    WeaknessStatus,
    WeaknessPriority
)
from app.services import weakness as weakness_service

router = APIRouter()

@router.post("", response_model=WeaknessResponse, status_code=status.HTTP_201_CREATED)
async def create_weakness(
    weakness_in: WeaknessCreate,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user["_id"])
    return await weakness_service.create_weakness(user_id, weakness_in)

@router.get("", response_model=List[WeaknessResponse])
async def list_weaknesses(
    status: Optional[WeaknessStatus] = None,
    priority: Optional[WeaknessPriority] = None,
    topic: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user["_id"])
    return await weakness_service.get_weaknesses(
        user_id=user_id,
        status=status.value if status else None,
        priority=priority.value if priority else None,
        topic=topic
    )

@router.get("/{weakness_id}", response_model=WeaknessResponse)
async def get_weakness(
    weakness_id: str,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user["_id"])
    item = await weakness_service.get_weakness(user_id, weakness_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weakness not found"
        )
    return item

@router.patch("/{weakness_id}", response_model=WeaknessResponse)
async def update_weakness(
    weakness_id: str,
    weakness_update: WeaknessUpdate,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user["_id"])
    updated = await weakness_service.update_weakness(user_id, weakness_id, weakness_update)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weakness not found"
        )
    return updated

@router.delete("/{weakness_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_weakness(
    weakness_id: str,
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user["_id"])
    deleted = await weakness_service.delete_weakness(user_id, weakness_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Weakness not found"
        )
    return None
