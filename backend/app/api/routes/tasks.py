from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime, timezone

from app.api.deps import get_current_user
from app.schemas.task import TaskUpdate, TaskResponse
from app.db.connection import db_client
from app.data.curriculum import CURRICULUM

router = APIRouter()

@router.get("", response_model=List[TaskResponse])
async def get_tasks(
    week_id: Optional[str] = None, 
    completed: Optional[bool] = None, 
    current_user: dict = Depends(get_current_user)
):
    user_id = str(current_user["_id"])
    progress_cursor = db_client.database["task_progress"].find({"user_id": user_id})
    progress_list = await progress_cursor.to_list(length=None)
    progress_map = {p["task_id"]: p for p in progress_list}
    
    result = []
    for w in CURRICULUM:
        if week_id and w["id"] != week_id:
            continue
        for d in w.get("days", []):
            for t in d.get("tasks", []):
                prog = progress_map.get(t["id"], {})
                is_completed = prog.get("completed", False)
                if completed is not None and is_completed != completed:
                    continue
                
                merged = {**t}
                merged["week_id"] = w["id"]
                merged["day_id"] = d["id"]
                merged["user_id"] = user_id
                merged["completed"] = is_completed
                merged["completed_at"] = prog.get("completed_at")
                # Convert default iso strings if present
                merged["created_at"] = prog.get("created_at") or datetime.now(timezone.utc)
                merged["updated_at"] = prog.get("updated_at") or datetime.now(timezone.utc)
                result.append(merged)
            
    return result

@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task_update: TaskUpdate, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    
    # Verify task exists in curriculum
    curr_task = None
    curr_week = None
    curr_day = None
    for w in CURRICULUM:
        for d in w.get("days", []):
            for t in d.get("tasks", []):
                if t["id"] == task_id:
                    curr_task = t
                    curr_week = w
                    curr_day = d
                    break
            if curr_task:
                break
        if curr_task:
            break
            
    if not curr_task:
        raise HTTPException(404, "Task not found in curriculum")
        
    update_data = task_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(400, "No fields to update")
        
    now = datetime.now(timezone.utc)
    set_fields = {"updated_at": now}
    
    if "completed" in update_data:
        set_fields["completed"] = update_data["completed"]
        if update_data["completed"]:
            set_fields["completed_at"] = now
        else:
            set_fields["completed_at"] = None
            
    await db_client.database["task_progress"].update_one(
        {"user_id": user_id, "task_id": task_id},
        {"$set": set_fields},
        upsert=True
    )
    
    # Fetch updated progress
    prog = await db_client.database["task_progress"].find_one({"user_id": user_id, "task_id": task_id})
    
    merged = {**curr_task}
    merged["week_id"] = curr_week["id"]
    merged["day_id"] = curr_day["id"]
    merged["user_id"] = user_id
    merged["completed"] = prog.get("completed", False)
    merged["completed_at"] = prog.get("completed_at")
    merged["created_at"] = prog.get("created_at") or now
    merged["updated_at"] = prog.get("updated_at") or now
    
    return merged
