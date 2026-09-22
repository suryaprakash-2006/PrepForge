from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas.assessment import QuestionClientResponse

class AttemptStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    SUBMITTED = "SUBMITTED"

class AnswerSubmission(BaseModel):
    model_config = {"extra": "forbid"}
    selected_answer: str = Field(..., min_length=1, description="Selected option text or letter")

class AnswerRecordResponse(BaseModel):
    status: str = "recorded"
    question_id: str
    selected_answer: str

class StartAttemptResponse(BaseModel):
    attempt_id: str
    assessment_id: str
    status: AttemptStatus
    started_at: datetime
    duration_minutes: int
    questions: List[QuestionClientResponse]

class SubmitAttemptResponse(BaseModel):
    attempt_id: str
    status: AttemptStatus
    score: int
    total_marks: int
    percentage: float
    passed: bool
    submitted_at: datetime

class AttemptHistoryItem(BaseModel):
    attempt_id: str
    assessment_id: str
    assessment_title: str
    assessment_type: str
    week_number: Optional[int] = None
    status: str
    started_at: datetime
    submitted_at: Optional[datetime] = None
    score: Optional[int] = None
    total_marks: Optional[int] = None
    percentage: Optional[float] = None
    passed: Optional[bool] = None
