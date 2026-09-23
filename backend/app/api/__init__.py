from fastapi import APIRouter
from app.api.routes import (
    auth,
    weeks,
    tasks,
    dashboard,
    weaknesses,
    weekly_reviews,
    assessments,
    assessment_attempts,
    coding_assessments,
    coding_assessment_attempts,
    coding_execution
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(weeks.router, prefix="/weeks", tags=["Weeks"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(weaknesses.router, prefix="/weaknesses", tags=["Weaknesses"])
api_router.include_router(weekly_reviews.router, prefix="/weekly-reviews", tags=["Weekly Reviews"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["Assessments"])
api_router.include_router(assessment_attempts.router, prefix="/assessment-attempts", tags=["Assessment Attempts"])
api_router.include_router(coding_assessments.router, prefix="/coding-assessments", tags=["Coding Assessments"])
api_router.include_router(coding_assessment_attempts.router, prefix="/coding-assessment-attempts", tags=["Coding Assessment Attempts"])
api_router.include_router(coding_execution.router, prefix="/coding-execution", tags=["Coding Execution"])


