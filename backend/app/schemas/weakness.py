from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class WeaknessPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class WeaknessStatus(str, Enum):
    OPEN = "OPEN"
    REVIEWED = "REVIEWED"
    RESOLVED = "RESOLVED"

class WeaknessSourceType(str, Enum):
    MANUAL = "MANUAL"
    ASSESSMENT = "ASSESSMENT"

class WeaknessCreate(BaseModel):
    model_config = {"extra": "forbid"}
    
    topic: str = Field(..., min_length=1, max_length=200)
    problem_concept: str = Field(..., min_length=1)
    what_i_got_wrong: str = Field(..., min_length=1)
    correct_concept: str = Field(..., min_length=1)
    priority: WeaknessPriority
    retry_date: Optional[datetime] = None
    date: Optional[datetime] = None
    status: Optional[WeaknessStatus] = WeaknessStatus.OPEN
    source_type: Optional[WeaknessSourceType] = WeaknessSourceType.MANUAL
    source_assessment_id: Optional[str] = None
    source_attempt_id: Optional[str] = None
    source_question_id: Optional[str] = None

    @field_validator("topic", "problem_concept", "what_i_got_wrong", "correct_concept")
    @classmethod
    def validate_not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or whitespace-only")
        return v.strip()

class WeaknessUpdate(BaseModel):
    model_config = {"extra": "forbid"}
    
    topic: Optional[str] = Field(None, min_length=1, max_length=200)
    problem_concept: Optional[str] = Field(None, min_length=1)
    what_i_got_wrong: Optional[str] = Field(None, min_length=1)
    correct_concept: Optional[str] = Field(None, min_length=1)
    priority: Optional[WeaknessPriority] = None
    retry_date: Optional[datetime] = None
    status: Optional[WeaknessStatus] = None

    @field_validator("topic", "problem_concept", "what_i_got_wrong", "correct_concept")
    @classmethod
    def validate_not_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError("Field cannot be empty or whitespace-only")
            return v.strip()
        return v

class WeaknessResponse(BaseModel):
    id: str
    user_id: str
    date: datetime
    topic: str
    problem_concept: str
    what_i_got_wrong: str
    correct_concept: str
    priority: WeaknessPriority
    retry_date: Optional[datetime] = None
    status: WeaknessStatus
    source_type: Optional[WeaknessSourceType] = WeaknessSourceType.MANUAL
    source_assessment_id: Optional[str] = None
    source_attempt_id: Optional[str] = None
    source_question_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
