from pydantic import BaseModel
from typing import List

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

class DashboardResponse(BaseModel):
    overall: OverallProgress
    current_week: CurrentWeekProgress
    today: TodayProgress
    categories: List[CategoryProgress]
