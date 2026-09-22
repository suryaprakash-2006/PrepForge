from fastapi import APIRouter
from app.api.routes import auth, weeks, tasks, dashboard, weaknesses, weekly_reviews

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(weeks.router, prefix="/weeks", tags=["Weeks"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(weaknesses.router, prefix="/weaknesses", tags=["Weaknesses"])
api_router.include_router(weekly_reviews.router, prefix="/weekly-reviews", tags=["Weekly Reviews"])

