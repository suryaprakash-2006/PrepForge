from datetime import datetime, timezone
from pymongo.errors import DuplicateKeyError
from app.db.connection import db_client
from app.data.curriculum import CURRICULUM, CURRICULUM_VERSION

async def initialize_default_roadmap(user_id: str):
    """
    Seeds the default 12-week roadmap and tasks for a specific user.
    Idempotent: Silently ignores if a week or task already exists.
    Progress is preserved because existing tasks are never overwritten.
    """
    db = db_client.database
    now = datetime.now(timezone.utc)
    
    for week_data in CURRICULUM:
        week_doc = {
            "user_id": user_id,
            "week_number": week_data["week_number"],
            "title": week_data["title"],
            "description": week_data["description"],
            "start_date": None,
            "end_date": None,
            "created_at": now,
            "updated_at": now
        }
        
        # Upsert or Insert week idempotently
        try:
            result = await db["weeks"].insert_one(week_doc)
            week_id = str(result.inserted_id)
        except DuplicateKeyError:
            # Week already exists, fetch it to get the week_id
            existing_week = await db["weeks"].find_one({
                "user_id": user_id, 
                "week_number": week_data["week_number"]
            })
            week_id = str(existing_week["_id"])
            
        # Initialize tasks for this week
        for task_data in week_data.get("tasks", []):
            # Check if task already exists (by title within the same week for the user)
            existing_task = await db["tasks"].find_one({
                "user_id": user_id,
                "week_id": week_id,
                "title": task_data["title"]
            })
            
            if not existing_task:
                task_doc = {
                    "user_id": user_id,
                    "week_id": week_id,
                    "title": task_data["title"],
                    "description": task_data.get("description"),
                    "category": task_data.get("category"),
                    "day_number": task_data.get("day_number"),
                    "estimated_minutes": task_data.get("estimated_minutes"),
                    "completed": False,
                    "completed_at": None,
                    "created_at": now,
                    "updated_at": now
                }
                await db["tasks"].insert_one(task_doc)

