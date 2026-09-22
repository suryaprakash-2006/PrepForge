from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.db.connection import db_client
from app.schemas.weakness import WeaknessCreate, WeaknessUpdate

def _format_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return doc
    doc["id"] = str(doc.pop("_id"))
    return doc

async def create_weakness(user_id: str, data: WeaknessCreate) -> Dict[str, Any]:
    db = db_client.database
    now = datetime.now(timezone.utc)
    
    doc = data.model_dump()
    doc["user_id"] = user_id
    if not doc.get("date"):
        doc["date"] = now
    if not doc.get("status"):
        doc["status"] = "OPEN"
    doc["created_at"] = now
    doc["updated_at"] = now
    
    result = await db["weaknesses"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return _format_doc(doc)

async def get_weaknesses(
    user_id: str,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    topic: Optional[str] = None
) -> List[Dict[str, Any]]:
    db = db_client.database
    query: Dict[str, Any] = {"user_id": user_id}
    
    if status:
        query["status"] = status
    if priority:
        query["priority"] = priority
    if topic:
        query["topic"] = topic
        
    cursor = db["weaknesses"].find(query).sort("created_at", -1)
    docs = await cursor.to_list(length=None)
    return [_format_doc(doc) for doc in docs]

async def get_weakness(user_id: str, weakness_id: str) -> Optional[Dict[str, Any]]:
    if not ObjectId.is_valid(weakness_id):
        return None
        
    db = db_client.database
    doc = await db["weaknesses"].find_one({"_id": ObjectId(weakness_id), "user_id": user_id})
    if not doc:
        return None
    return _format_doc(doc)

async def update_weakness(user_id: str, weakness_id: str, data: WeaknessUpdate) -> Optional[Dict[str, Any]]:
    if not ObjectId.is_valid(weakness_id):
        return None
        
    db = db_client.database
    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        return await get_weakness(user_id, weakness_id)
        
    now = datetime.now(timezone.utc)
    update_data["updated_at"] = now
    
    result = await db["weaknesses"].update_one(
        {"_id": ObjectId(weakness_id), "user_id": user_id},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        return None
        
    return await get_weakness(user_id, weakness_id)

async def delete_weakness(user_id: str, weakness_id: str) -> bool:
    if not ObjectId.is_valid(weakness_id):
        return False
        
    db = db_client.database
    result = await db["weaknesses"].delete_one({"_id": ObjectId(weakness_id), "user_id": user_id})
    return result.deleted_count > 0
