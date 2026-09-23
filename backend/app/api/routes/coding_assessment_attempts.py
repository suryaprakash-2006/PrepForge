from fastapi import APIRouter, Depends, Path, status
from typing import List
from app.api.deps import get_current_user
from app.schemas.coding_attempt import (
    ProblemSubmissionRequest,
    ProblemSubmissionResponse,
    SubmitCodingAttemptResponse,
    CodingAttemptResponse,
    CodingAttemptHistoryItem
)
from app.services import coding_assessment as coding_assessment_service

router = APIRouter()

@router.get("", response_model=List[CodingAttemptHistoryItem])
async def list_user_coding_attempts(
    current_user: dict = Depends(get_current_user)
):
    """
    Get all coding assessment attempts for the authenticated user.
    """
    user_id = str(current_user["_id"])
    return await coding_assessment_service.get_user_coding_attempts(user_id)

@router.get("/{attempt_id}", response_model=CodingAttemptResponse)
async def get_coding_attempt(
    attempt_id: str = Path(..., description="Coding assessment attempt ID"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific coding assessment attempt. Enforces user isolation.
    """
    user_id = str(current_user["_id"])
    return await coding_assessment_service.get_coding_attempt(user_id=user_id, attempt_id=attempt_id)

@router.post("/{attempt_id}/problems/{problem_id}/submit", response_model=ProblemSubmissionResponse)
async def submit_problem_code(
    submission: ProblemSubmissionRequest,
    attempt_id: str = Path(..., description="Coding assessment attempt ID"),
    problem_id: str = Path(..., description="Coding problem ID"),
    current_user: dict = Depends(get_current_user)
):
    """
    Save or update code submission for a problem in an active attempt.
    Payload strictly validated (max 64KB).
    NO CODE EXECUTION: Stored strictly as plain text.
    """
    user_id = str(current_user["_id"])
    return await coding_assessment_service.save_problem_submission(
        user_id=user_id,
        attempt_id=attempt_id,
        problem_id=problem_id,
        request=submission
    )

@router.post("/{attempt_id}/submit", response_model=SubmitCodingAttemptResponse)
async def submit_coding_attempt(
    attempt_id: str = Path(..., description="Coding assessment attempt ID"),
    current_user: dict = Depends(get_current_user)
):
    """
    Finalize and submit a coding assessment attempt.
    Makes the attempt immutable.
    """
    user_id = str(current_user["_id"])
    return await coding_assessment_service.submit_coding_attempt(
        user_id=user_id,
        attempt_id=attempt_id
    )
