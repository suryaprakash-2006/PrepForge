from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class CodingDifficulty(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class CodingStatus(str, Enum):
    PUBLISHED = "PUBLISHED"
    DRAFT = "DRAFT"
    ARCHIVED = "ARCHIVED"

class CodingExample(BaseModel):
    input: str
    output: str
    explanation: Optional[str] = ""

class CodingProblemResponse(BaseModel):
    id: str
    title: str
    slug: str
    description: str
    category: str
    topic: str
    difficulty: CodingDifficulty
    constraints: List[str]
    input_format: str
    output_format: str
    examples: List[CodingExample]
    starter_code: Dict[str, str]
    expected_language: List[str] = ["python", "cpp"]
    tags: List[str] = []
    marks: int = 10
    status: CodingStatus = CodingStatus.PUBLISHED
