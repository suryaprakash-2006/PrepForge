from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    week_id: str
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    day_number: Optional[int] = Field(None, ge=1, le=7)
    estimated_minutes: Optional[int] = Field(None, ge=0)
    completed: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    day_number: Optional[int] = Field(None, ge=1, le=7)
    estimated_minutes: Optional[int] = Field(None, ge=0)
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: str
    user_id: str
    week_id: str
    title: str
    description: Optional[str]
    category: Optional[str]
    day_number: Optional[int]
    estimated_minutes: Optional[int]
    completed: bool
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
