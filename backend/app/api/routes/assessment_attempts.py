from fastapi import APIRouter, Depends, Path, status
from app.api.deps import get_current_user
from app.schemas.assessment_attempt import (
    AnswerSubmission,
    AnswerRecordResponse,
    SubmitAttemptResponse,
    AttemptResultResponse,
    CreateWeaknessFromMistakeRequest
)
from app.schemas.weakness import WeaknessResponse
from app.services import assessment as assessment_service

router = APIRouter()

@router.patch("/{attempt_id}/answers/{question_id}", response_model=AnswerRecordResponse)
async def submit_answer(
    answer_in: AnswerSubmission,
    attempt_id: str = Path(..., description="Assessment attempt ID"),
    question_id: str = Path(..., description="Assessment question ID"),
    current_user: dict = Depends(get_current_user)
):
    """
    Store or update an answer for an active assessment attempt.
    Never exposes correctness or marks prior to submission.
    """
    user_id = str(current_user["_id"])
    return await assessment_service.record_answer(
        user_id=user_id,
        attempt_id=attempt_id,
        question_id=question_id,
        selected_answer=answer_in.selected_answer
    )

@router.post("/{attempt_id}/submit", response_model=SubmitAttemptResponse)
async def submit_attempt(
    attempt_id: str = Path(..., description="Assessment attempt ID"),
    current_user: dict = Depends(get_current_user)
):
    """
    Finalize and submit an assessment attempt.
    Calculates marks, percentage, and pass/fail, making the attempt immutable.
    """
    user_id = str(current_user["_id"])
    return await assessment_service.submit_attempt(
        user_id=user_id,
        attempt_id=attempt_id
    )

@router.get("/{attempt_id}/result", response_model=AttemptResultResponse)
async def get_attempt_result(
    attempt_id: str = Path(..., description="Assessment attempt ID"),
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve full question-by-question breakdown, correct answers, explanations,
    and weakness logging status for a submitted attempt.
    Strictly forbidden on IN_PROGRESS attempts.
    """
    user_id = str(current_user["_id"])
    return await assessment_service.get_attempt_result(
        user_id=user_id,
        attempt_id=attempt_id
    )

@router.post("/{attempt_id}/weaknesses", response_model=WeaknessResponse, status_code=status.HTTP_201_CREATED)
async def create_weakness_from_mistake(
    data: CreateWeaknessFromMistakeRequest,
    attempt_id: str = Path(..., description="Assessment attempt ID"),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a tracked weakness record from an incorrect or unanswered question
    in a submitted assessment attempt.
    Idempotent: returns the existing weakness if already logged.
    """
    user_id = str(current_user["_id"])
    return await assessment_service.create_weakness_from_attempt(
        user_id=user_id,
        attempt_id=attempt_id,
        data=data
    )
