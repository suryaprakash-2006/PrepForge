from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class WeekCreate(BaseModel):
    week_number: int = Field(..., ge=1, le=12)
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class WeekResponse(BaseModel):
    id: str
    user_id: str
    week_number: int
    title: str
    description: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
