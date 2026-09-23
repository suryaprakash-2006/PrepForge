from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OverallProgress(BaseModel):
    total_tasks: int
    completed_tasks: int
    remaining_tasks: int
    completion_percentage: float

class CurrentWeekProgress(BaseModel):
    week_number: int
    title: str
    completed_tasks: int
    total_tasks: int
    completion_percentage: float

class TodayProgress(BaseModel):
    day_number: int
    day_name: str
    task_count: int
    completed_tasks: int
    completion_percentage: float

class CategoryProgress(BaseModel):
    category: str
    total_tasks: int
    completed_tasks: int
    completion_percentage: float

class LatestAssessmentProgress(BaseModel):
    assessment_id: str
    assessment_title: str
    attempt_id: str
    percentage: float
    score: int
    total_marks: int
    passed: bool
    submitted_at: datetime

class DashboardResponse(BaseModel):
    overall: OverallProgress
    current_week: CurrentWeekProgress
    today: TodayProgress
    categories: List[CategoryProgress]
    latest_assessment: Optional[LatestAssessmentProgress] = None
