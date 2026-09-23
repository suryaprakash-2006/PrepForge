from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field

class CodingTestCaseBase(BaseModel):
    id: str
    problem_id: str
    order: int = 1
    input: str
    is_hidden: bool = False
    time_limit_ms: int = Field(default=2000, gt=0, description="Execution time limit in milliseconds")
    memory_limit_mb: int = Field(default=256, gt=0, description="Execution memory limit in megabytes")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CodingTestCaseInternal(CodingTestCaseBase):
    """
    Internal test case model containing expected_output.
    Strictly for internal judge/worker use. NEVER returned directly to clients if hidden.
    """
    expected_output: str

class CodingTestCasePublicResponse(CodingTestCaseBase):
    """
    Client-facing test case model.
    Expected output is only included for public (sample) test cases (is_hidden=False).
    For hidden cases, expected_output is strictly None.
    """
    expected_output: Optional[str] = None
