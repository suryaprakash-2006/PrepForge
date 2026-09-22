from fastapi import APIRouter, Depends, Path
from app.api.deps import get_current_user
from app.schemas.weekly_review import WeeklyReviewResponse, WeeklyReflectionUpdate
from app.services import weekly_review as weekly_review_service

router = APIRouter()

@router.get("/{week_number}", response_model=WeeklyReviewResponse)
async def get_weekly_review(
    week_number: int = Path(..., ge=1, le=12, description="Curriculum week number (1-12)"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get weekly review derived metrics and saved reflection for a specific week.
    """
    user_id = str(current_user["_id"])
    return await weekly_review_service.get_weekly_review(user_id=user_id, week_number=week_number)

@router.put("/{week_number}", response_model=WeeklyReviewResponse)
async def save_weekly_reflection(
    weekly_reflection: WeeklyReflectionUpdate,
    week_number: int = Path(..., ge=1, le=12, description="Curriculum week number (1-12)"),
    current_user: dict = Depends(get_current_user)
):
    """
    Save or update user reflection for a specific week and return full weekly review.
    """
    user_id = str(current_user["_id"])
    return await weekly_review_service.save_weekly_reflection(
        user_id=user_id,
        week_number=week_number,
        data=weekly_reflection
    )
