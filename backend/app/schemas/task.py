from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class Subtask(BaseModel):
    title: str
    completed: bool = False

class TaskCreate(BaseModel):
    week_id: str
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    day_number: Optional[int] = Field(None, ge=1, le=7)
    estimated_minutes: Optional[int] = Field(None, ge=0)
    completed: bool = False
    task_type: Optional[str] = None
    difficulty: Optional[str] = None
    priority: Optional[str] = None
    subtasks: Optional[List[Subtask]] = []

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    day_number: Optional[int] = Field(None, ge=1, le=7)
    estimated_minutes: Optional[int] = Field(None, ge=0)
    completed: Optional[bool] = None
    task_type: Optional[str] = None
    difficulty: Optional[str] = None
    priority: Optional[str] = None
    subtasks: Optional[List[Subtask]] = None

class TaskResponse(BaseModel):
    id: str
    user_id: str
    week_id: str
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    day_number: Optional[int] = None
    estimated_minutes: Optional[int] = None
    completed: bool
    task_type: Optional[str] = None
    difficulty: Optional[str] = None
    priority: Optional[str] = None
    subtasks: Optional[List[Subtask]] = []
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
