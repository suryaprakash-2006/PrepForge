from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.coding_problem import CodingProblemResponse

class CodingSubmissionStatus(str, Enum):
    NOT_SUBMITTED = "NOT_SUBMITTED"
    SUBMITTED = "SUBMITTED"

class CodingAttemptStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    SUBMITTED = "SUBMITTED"

class ProblemSubmissionRequest(BaseModel):
    model_config = {"extra": "forbid"}
    code: str = Field(..., max_length=65536, description="Source code text, max 64KB")
    language: str = Field(..., min_length=1, max_length=32, description="Target programming language")

class ProblemSubmissionResponse(BaseModel):
    status: str = "QUEUED"
    submission_id: Optional[str] = None
    job_id: Optional[str] = None
    problem_id: str
    language: str
    submission_status: CodingSubmissionStatus = CodingSubmissionStatus.SUBMITTED
    saved_at: datetime

class CodingProblemState(BaseModel):
    problem_id: str
    code: str = ""
    language: str = "python"
    submission_status: CodingSubmissionStatus = CodingSubmissionStatus.NOT_SUBMITTED
    saved_at: Optional[datetime] = None

class StartCodingAttemptResponse(BaseModel):
    attempt_id: str
    assessment_id: str
    status: str = "IN_PROGRESS"
    started_at: datetime
    duration_minutes: int
    problems: List[CodingProblemResponse]
    problem_states: List[CodingProblemState]

class SubmitCodingAttemptResponse(BaseModel):
    attempt_id: str
    assessment_id: str
    status: str = "SUBMITTED"
    submitted_at: datetime
    message: str = "Coding assessment submitted. Submissions stored for future evaluation."

class CodingAttemptResponse(BaseModel):
    attempt_id: str
    assessment_id: str
    assessment_title: str
    status: str
    started_at: datetime
    duration_minutes: int
    submitted_at: Optional[datetime] = None
    problem_states: List[CodingProblemState]
    score: Optional[int] = None
    total_marks: Optional[int] = None
    percentage: Optional[float] = None
    passed: Optional[bool] = None

class CodingAttemptHistoryItem(BaseModel):
    attempt_id: str
    assessment_id: str
    assessment_title: str
    week_number: Optional[int] = None
    status: str
    started_at: datetime
    duration_minutes: int
    submitted_at: Optional[datetime] = None
    problem_count: int
    submitted_problems_count: int
    score: Optional[int] = None
    percentage: Optional[float] = None
    passed: Optional[bool] = None
