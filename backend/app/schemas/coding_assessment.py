from typing import List, Optional
from pydantic import BaseModel
from app.schemas.coding_problem import CodingProblemResponse

class CodingAssessmentResponse(BaseModel):
    id: str
    title: str
    description: str
    week_number: Optional[int] = None
    assessment_type: str = "TIMED_CODING"
    duration_minutes: int
    problem_count: int
    passing_score: int
    status: str = "PUBLISHED"
    problem_ids: List[str]

class CodingAssessmentDetailResponse(CodingAssessmentResponse):
    problems: List[CodingProblemResponse]
