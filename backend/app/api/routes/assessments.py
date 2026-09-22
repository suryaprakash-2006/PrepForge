from fastapi import APIRouter, Depends, Path, status
from typing import List
from app.api.deps import get_current_user
from app.schemas.assessment import AssessmentResponse
from app.schemas.assessment_attempt import (
    StartAttemptResponse,
    AttemptHistoryItem
)
from app.services import assessment as assessment_service

router = APIRouter()

@router.get("", response_model=List[AssessmentResponse])
async def list_assessments(
    current_user: dict = Depends(get_current_user)
):
    """
    List all published assessments.
    """
    return await assessment_service.get_published_assessments()

@router.get("/attempts", response_model=List[AttemptHistoryItem])
async def list_user_attempts(
    current_user: dict = Depends(get_current_user)
):
    """
    Get attempt history for the authenticated user only.
    """
    user_id = str(current_user["_id"])
    return await assessment_service.get_user_attempts_history(user_id)

@router.get("/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(
    assessment_id: str = Path(..., description="Unique assessment identifier"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get published assessment metadata.
    """
    return await assessment_service.get_assessment(assessment_id)

@router.post("/{assessment_id}/attempts", response_model=StartAttemptResponse, status_code=status.HTTP_201_CREATED)
async def start_assessment_attempt(
    assessment_id: str = Path(..., description="Unique assessment identifier"),
    current_user: dict = Depends(get_current_user)
):
    """
    Start a new assessment attempt. Returns sanitized questions without correct answers.
    """
    user_id = str(current_user["_id"])
    return await assessment_service.start_assessment_attempt(user_id=user_id, assessment_id=assessment_id)
