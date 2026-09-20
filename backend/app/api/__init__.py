from fastapi import APIRouter
from app.api.routes import auth, weeks, tasks

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(weeks.router, prefix="/weeks", tags=["Weeks"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
