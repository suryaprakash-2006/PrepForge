from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas.assessment import QuestionClientResponse
from app.schemas.weakness import WeaknessPriority

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

class AttemptResultQuestionItem(BaseModel):
    question_id: str
    question_number: int
    question: str
    options: List[str]
    category: str
    topic: str
    difficulty: str
    marks: int
    selected_answer: Optional[str] = None
    correct_answer: str
    explanation: str
    is_correct: bool
    marks_awarded: int
    is_in_weaknesses: bool = False
    weakness_id: Optional[str] = None

class AttemptResultSummary(BaseModel):
    total_questions: int
    correct_count: int
    incorrect_count: int
    unanswered_count: int

class AttemptResultResponse(BaseModel):
    attempt_id: str
    assessment_id: str
    assessment_title: str
    status: AttemptStatus
    score: int
    total_marks: int
    percentage: float
    passed: bool
    started_at: datetime
    submitted_at: Optional[datetime] = None
    summary: AttemptResultSummary
    questions: List[AttemptResultQuestionItem]

class CreateWeaknessFromMistakeRequest(BaseModel):
    model_config = {"extra": "forbid"}
    question_id: str = Field(..., min_length=1)
    priority: Optional[WeaknessPriority] = WeaknessPriority.MEDIUM
    what_i_got_wrong: Optional[str] = None
    correct_concept: Optional[str] = None
    retry_date: Optional[datetime] = None
