from datetime import datetime, timezone
from pymongo.errors import DuplicateKeyError
from app.db.connection import db_client
from app.data.curriculum import CURRICULUM

async def initialize_default_roadmap(user_id: str):
    """
    Initializes or migrates the user's roadmap.
    Since curriculum is now static and shared, this mostly handles migrating
    existing legacy task progress (from Phase 6A/6B) to the new `task_progress` model.
    """
    db = db_client.database
    
    # 1. Fetch legacy tasks
    legacy_tasks_cursor = db["tasks"].find({"user_id": user_id})
    legacy_tasks = await legacy_tasks_cursor.to_list(length=None)
    
    if legacy_tasks:
        for lt in legacy_tasks:
            # Find the corresponding curriculum task by title
            curr_task = next((t for w in CURRICULUM for t in w.get("tasks", []) if t["title"] == lt["title"]), None)
            
            if curr_task:
                # Upsert into task_progress
                await db["task_progress"].update_one(
                    {"user_id": user_id, "task_id": curr_task["id"]},
                    {"$set": {
                        "completed": lt.get("completed", False),
                        "completed_at": lt.get("completed_at")
                    }},
                    upsert=True
                )
        
        # Mark user as migrated if we wanted to (optional), but upsert is safe.
    
    # No more copying curriculum to db["weeks"] or db["tasks"]!
