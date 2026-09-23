from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class ExecutionVerdict(str, Enum):
    ACCEPTED = "ACCEPTED"
    WRONG_ANSWER = "WRONG_ANSWER"
    TIME_LIMIT_EXCEEDED = "TIME_LIMIT_EXCEEDED"
    MEMORY_LIMIT_EXCEEDED = "MEMORY_LIMIT_EXCEEDED"
    COMPILE_ERROR = "COMPILE_ERROR"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    OUTPUT_LIMIT_EXCEEDED = "OUTPUT_LIMIT_EXCEEDED"
    SYSTEM_ERROR = "SYSTEM_ERROR"

class TestCaseResultItem(BaseModel):
    test_case_id: str
    order: int
    is_hidden: bool
    verdict: ExecutionVerdict
    time_ms: Optional[int] = None
    memory_mb: Optional[float] = None
    user_output: Optional[str] = None
    expected_output: Optional[str] = None

class CodingExecutionResultResponse(BaseModel):
    id: str
    job_id: str
    attempt_id: str
    problem_id: str
    verdict: ExecutionVerdict
    passed_test_cases: int
    total_test_cases: int
    execution_time_ms: Optional[int] = None
    memory_used_mb: Optional[float] = None
    compile_output: Optional[str] = None
    runtime_output: Optional[str] = None
    test_case_results: Optional[List[TestCaseResultItem]] = None
    created_at: datetime

class ExecutionResultStatusResponse(BaseModel):
    job_id: str
    status: str
    message: str
    result: Optional[CodingExecutionResultResponse] = None
