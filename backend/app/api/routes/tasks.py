from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timezone
from bson import ObjectId

from app.api.deps import get_current_user
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.db.connection import db_client

router = APIRouter()

def serialize_task(task: dict) -> dict:
    task["id"] = str(task.pop("_id"))
    return task

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task_in: TaskCreate, current_user: dict = Depends(get_current_user)):
    db = db_client.database
    user_id = str(current_user["_id"])
    now = datetime.now(timezone.utc)
    
    if not ObjectId.is_valid(task_in.week_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid week ID format")
    
    # Verify the week belongs to the user
    week = await db["weeks"].find_one({"_id": ObjectId(task_in.week_id), "user_id": user_id})
    if not week:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Week not found or does not belong to user")
        
    task_doc = task_in.model_dump()
    task_doc["user_id"] = user_id
    task_doc["completed_at"] = now if task_in.completed else None
    task_doc["created_at"] = now
    task_doc["updated_at"] = now
    
    result = await db["tasks"].insert_one(task_doc)
    created_task = await db["tasks"].find_one({"_id": result.inserted_id})
    return serialize_task(created_task)

@router.get("", response_model=List[TaskResponse])
async def get_tasks(
    week_id: Optional[str] = None, 
    completed: Optional[bool] = None, 
    current_user: dict = Depends(get_current_user)
):
    db = db_client.database
    user_id = str(current_user["_id"])
    
    query = {"user_id": user_id}
    if week_id:
        if not ObjectId.is_valid(week_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid week ID format")
        query["week_id"] = week_id
    if completed is not None:
        query["completed"] = completed
        
    cursor = db["tasks"].find(query).sort("created_at", 1)
    tasks = await cursor.to_list(length=500)
    
    return [serialize_task(t) for t in tasks]

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, current_user: dict = Depends(get_current_user)):
    db = db_client.database
    user_id = str(current_user["_id"])
    
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid task ID format")
        
    task = await db["tasks"].find_one({"_id": ObjectId(task_id), "user_id": user_id})
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
    return serialize_task(task)

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_update: TaskUpdate, current_user: dict = Depends(get_current_user)):
    db = db_client.database
    user_id = str(current_user["_id"])
    
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid task ID format")
        
    existing_task = await db["tasks"].find_one({"_id": ObjectId(task_id), "user_id": user_id})
    if not existing_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        
    update_data = task_update.model_dump(exclude_unset=True)
    if not update_data:
        return serialize_task(existing_task)
        
    now = datetime.now(timezone.utc)
    update_data["updated_at"] = now
    
    # Handle completed_at logic
    if "completed" in update_data:
        if update_data["completed"] and not existing_task.get("completed"):
            update_data["completed_at"] = now
        elif not update_data["completed"] and existing_task.get("completed"):
            update_data["completed_at"] = None
            
    await db["tasks"].update_one(
        {"_id": ObjectId(task_id), "user_id": user_id},
        {"$set": update_data}
    )
    
    updated_task = await db["tasks"].find_one({"_id": ObjectId(task_id)})
    return serialize_task(updated_task)
