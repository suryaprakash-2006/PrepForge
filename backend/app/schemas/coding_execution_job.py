from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class CodingExecutionJobResponse(BaseModel):
    id: str
    user_id: str
    attempt_id: str
    problem_id: str
    status: JobStatus
    source_submission_id: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    worker_id: Optional[str] = None
    error_code: Optional[str] = None

class JobStatusResponse(BaseModel):
    job_id: str
    attempt_id: str
    problem_id: str
    status: JobStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
