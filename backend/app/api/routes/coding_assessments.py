from fastapi import APIRouter, Depends, Path, status
from typing import List
from app.api.deps import get_current_user
from app.schemas.coding_assessment import (
    CodingAssessmentResponse,
    CodingAssessmentDetailResponse
)
from app.schemas.coding_attempt import (
    StartCodingAttemptResponse,
    CodingAttemptHistoryItem
)
from app.services import coding_assessment as coding_assessment_service

router = APIRouter()

@router.get("", response_model=List[CodingAssessmentResponse])
async def list_coding_assessments(
    current_user: dict = Depends(get_current_user)
):
    """
    List all published timed coding assessments.
    """
    return await coding_assessment_service.get_published_coding_assessments()

@router.get("/attempts", response_model=List[CodingAttemptHistoryItem])
async def list_user_coding_attempts(
    current_user: dict = Depends(get_current_user)
):
    """
    Get coding assessment attempt history for the authenticated user only.
    """
    user_id = str(current_user["_id"])
    return await coding_assessment_service.get_user_coding_attempts(user_id)

@router.get("/{assessment_id}", response_model=CodingAssessmentDetailResponse)
async def get_coding_assessment(
    assessment_id: str = Path(..., description="Unique coding assessment identifier"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get published coding assessment with problem definitions.
    """
    return await coding_assessment_service.get_coding_assessment_detail(assessment_id)

@router.post("/{assessment_id}/attempts", response_model=StartCodingAttemptResponse, status_code=status.HTTP_201_CREATED)
async def start_coding_attempt(
    assessment_id: str = Path(..., description="Unique coding assessment identifier"),
    current_user: dict = Depends(get_current_user)
):
    """
    Start a new coding assessment attempt. Returns problems and initial states.
    """
    user_id = str(current_user["_id"])
    return await coding_assessment_service.start_coding_attempt(user_id=user_id, assessment_id=assessment_id)
