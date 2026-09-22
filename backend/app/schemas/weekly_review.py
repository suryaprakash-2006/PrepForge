from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field

class WeeklyReflectionUpdate(BaseModel):
    model_config = {"extra": "forbid"}
    
    weakest_topics: Optional[List[str]] = Field(default_factory=list)
    improved_topics: Optional[List[str]] = Field(default_factory=list)
    carry_forward_topics: Optional[List[str]] = Field(default_factory=list)
    next_priorities: Optional[List[str]] = Field(default_factory=list)
    confidence: Optional[int] = Field(None, ge=1, le=5)
    motivation: Optional[int] = Field(None, ge=1, le=5)
    schedule_adjustments: Optional[str] = ""

class WeeklyReflectionResponse(BaseModel):
    weakest_topics: List[str] = Field(default_factory=list)
    improved_topics: List[str] = Field(default_factory=list)
    carry_forward_topics: List[str] = Field(default_factory=list)
    next_priorities: List[str] = Field(default_factory=list)
    confidence: Optional[int] = None
    motivation: Optional[int] = None
    schedule_adjustments: Optional[str] = ""
    updated_at: Optional[datetime] = None

class WeeklyReviewTargetProgress(BaseModel):
    target: int
    completed: int

class WeeklyReviewCategoryProgress(BaseModel):
    category: str
    total_tasks: int
    completed_tasks: int
    completion_percentage: float

class WeeklyReviewWeekInfo(BaseModel):
    week_number: int
    title: str
    phase: Optional[str] = None

class WeeklyReviewProgress(BaseModel):
    total_tasks: int
    completed_tasks: int
    remaining_tasks: int
    completion_percentage: float

class WeeklyReviewWeaknessSummary(BaseModel):
    open: int
    high_priority: int
    due: int
    resolved: int

class WeeklyReviewMistakeItem(BaseModel):
    id: str
    topic: str
    problem_concept: str
    what_i_got_wrong: str
    correct_concept: str
    priority: str
    status: str

class WeeklyReviewResponse(BaseModel):
    week: WeeklyReviewWeekInfo
    progress: WeeklyReviewProgress
    targets: Dict[str, WeeklyReviewTargetProgress]
    categories: List[WeeklyReviewCategoryProgress]
    weakness_summary: WeeklyReviewWeaknessSummary
    mistakes_to_review: List[WeeklyReviewMistakeItem]
    reflection: WeeklyReflectionResponse
    assessment_status: Optional[str] = "No assessment data available yet."
