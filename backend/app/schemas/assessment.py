from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class AssessmentType(str, Enum):
    QUIZ = "QUIZ"
    BASELINE = "BASELINE"
    TIMED_CODING = "TIMED_CODING"
    MOCK = "MOCK"

class AssessmentStatus(str, Enum):
    PUBLISHED = "PUBLISHED"
    DRAFT = "DRAFT"
    ARCHIVED = "ARCHIVED"

class QuestionType(str, Enum):
    MCQ = "MCQ"

class DifficultyLevel(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class AssessmentResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = ""
    week_number: Optional[int] = None
    assessment_type: AssessmentType
    duration_minutes: int
    question_count: int
    passing_score: int
    status: AssessmentStatus

class QuestionClientResponse(BaseModel):
    id: str
    assessment_id: str
    question_number: int
    question_type: QuestionType
    category: str
    topic: str
    difficulty: DifficultyLevel
    question: str
    options: List[str]
    marks: int = 1

class QuestionInternal(BaseModel):
    id: str
    assessment_id: str
    question_number: int
    question_type: QuestionType
    category: str
    topic: str
    difficulty: DifficultyLevel
    question: str
    options: List[str]
    correct_answer: str
    explanation: str
    marks: int = 1
