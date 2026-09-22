from typing import Dict, Any, Set
from app.data.curriculum import CURRICULUM
from app.db.connection import db_client
from app.schemas.dashboard import (
    DashboardResponse,
    OverallProgress,
    CurrentWeekProgress,
    TodayProgress,
    CategoryProgress
)

def calc_percentage(completed: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((completed / total) * 100.0, 1)

def determine_current_week(curriculum: list, completed_task_ids: Set[str]) -> dict:
    """
    Determines the current active week for the user.
    Finds the first week that is not 100% completed.
    Defaults to Week 1 if no progress or if all weeks completed.
    """
    if not curriculum:
        return {}
    
    for w in curriculum:
        w_tasks = [t["id"] for d in w.get("days", []) for t in d.get("tasks", [])]
        if not w_tasks:
            continue
        completed_in_week = sum(1 for tid in w_tasks if tid in completed_task_ids)
        if completed_in_week < len(w_tasks):
            return w
            
    return curriculum[0]

def determine_current_day(current_week: dict, completed_task_ids: Set[str]) -> dict:
    """
    Determines the current active day within the current week.
    Finds the first day that is not 100% completed.
    Defaults to Day 1 of the current week.
    """
    days = current_week.get("days", [])
    if not days:
        return {}
        
    for d in days:
        d_tasks = [t["id"] for t in d.get("tasks", [])]
        if not d_tasks:
            continue
        completed_in_day = sum(1 for tid in d_tasks if tid in completed_task_ids)
        if completed_in_day < len(d_tasks):
            return d
            
    return days[0]

async def get_dashboard_data(user_id: str) -> DashboardResponse:
    """
    Aggregates dashboard data for the authenticated user from the static curriculum
    and the user's task_progress records in MongoDB.
    """
    db = db_client.database
    
    # 1. Fetch user's progress records
    progress_cursor = db["task_progress"].find({"user_id": user_id})
    progress_list = await progress_cursor.to_list(length=None)
    completed_task_ids = {p["task_id"] for p in progress_list if p.get("completed", False)}
    
    # 2. Overall aggregation
    all_tasks = [t for w in CURRICULUM for d in w.get("days", []) for t in d.get("tasks", [])]
    total_tasks = len(all_tasks)
    completed_tasks = sum(1 for t in all_tasks if t["id"] in completed_task_ids)
    remaining_tasks = max(0, total_tasks - completed_tasks)
    overall_percentage = calc_percentage(completed_tasks, total_tasks)
    
    overall = OverallProgress(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        remaining_tasks=remaining_tasks,
        completion_percentage=overall_percentage
    )
    
    # 3. Current week aggregation
    curr_week = determine_current_week(CURRICULUM, completed_task_ids)
    curr_week_tasks = [t for d in curr_week.get("days", []) for t in d.get("tasks", [])]
    cw_total = len(curr_week_tasks)
    cw_completed = sum(1 for t in curr_week_tasks if t["id"] in completed_task_ids)
    cw_percentage = calc_percentage(cw_completed, cw_total)
    
    current_week = CurrentWeekProgress(
        week_number=curr_week.get("week_number", 1),
        title=curr_week.get("title", ""),
        completed_tasks=cw_completed,
        total_tasks=cw_total,
        completion_percentage=cw_percentage
    )
    
    # 4. Today aggregation (Day within current week)
    curr_day = determine_current_day(curr_week, completed_task_ids)
    day_tasks = curr_day.get("tasks", [])
    today_total = len(day_tasks)
    today_completed = sum(1 for t in day_tasks if t["id"] in completed_task_ids)
    today_percentage = calc_percentage(today_completed, today_total)
    
    today = TodayProgress(
        day_number=curr_day.get("day_number", 1),
        day_name=curr_day.get("day_name", "Monday"),
        task_count=today_total,
        completed_tasks=today_completed,
        completion_percentage=today_percentage
    )
    
    # 5. Category aggregation
    category_counts: Dict[str, Dict[str, int]] = {}
    for t in all_tasks:
        cat = t.get("category", "General")
        if cat not in category_counts:
            category_counts[cat] = {"total": 0, "completed": 0}
        category_counts[cat]["total"] += 1
        if t["id"] in completed_task_ids:
            category_counts[cat]["completed"] += 1
            
    categories = []
    for cat, counts in sorted(category_counts.items(), key=lambda item: item[0]):
        c_tot = counts["total"]
        c_comp = counts["completed"]
        categories.append(CategoryProgress(
            category=cat,
            total_tasks=c_tot,
            completed_tasks=c_comp,
            completion_percentage=calc_percentage(c_comp, c_tot)
        ))
        
    return DashboardResponse(
        overall=overall,
        current_week=current_week,
        today=today,
        categories=categories
    )
