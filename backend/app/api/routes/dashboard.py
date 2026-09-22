from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard import get_dashboard_data

router = APIRouter()

@router.get("", response_model=DashboardResponse)
async def get_dashboard(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    return await get_dashboard_data(user_id)
