from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class WeekCreate(BaseModel):
    week_number: int = Field(..., ge=1, le=12)
    phase: Optional[str] = None
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    targets: Optional[Dict[str, Any]] = None
    assessments: Optional[List[Dict[str, Any]]] = None
    mocks: Optional[List[Dict[str, Any]]] = None
    milestones: Optional[List[Dict[str, Any]]] = None

class WeekResponse(BaseModel):
    id: str
    user_id: str
    week_number: int
    phase: Optional[str] = None
    title: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    targets: Optional[Dict[str, Any]] = None
    assessments: Optional[List[Dict[str, Any]]] = None
    mocks: Optional[List[Dict[str, Any]]] = None
    milestones: Optional[List[Dict[str, Any]]] = None
    days: Optional[List[Dict[str, Any]]] = None
    created_at: datetime
    updated_at: datetime
