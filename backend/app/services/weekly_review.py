from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from fastapi import HTTPException, status

from app.db.connection import db_client
from app.data.curriculum import CURRICULUM
from app.schemas.weekly_review import (
    WeeklyReviewResponse,
    WeeklyReviewWeekInfo,
    WeeklyReviewProgress,
    WeeklyReviewTargetProgress,
    WeeklyReviewCategoryProgress,
    WeeklyReviewWeaknessSummary,
    WeeklyReviewMistakeItem,
    WeeklyReviewAssessmentInfo,
    WeeklyReflectionResponse,
    WeeklyReflectionUpdate
)

def calc_percentage(completed: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((completed / total) * 100.0, 1)

async def get_weekly_review(user_id: str, week_number: int) -> WeeklyReviewResponse:
    if week_number < 1 or week_number > 12:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="week_number must be between 1 and 12"
        )
        
    week = next((w for w in CURRICULUM if w["week_number"] == week_number), None)
    if not week:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Week {week_number} not found in curriculum"
        )
        
    db = db_client.database
    
    # 1. Fetch user's task progress
    progress_list = await db["task_progress"].find({"user_id": user_id}).to_list(length=None)
    completed_ids = {p["task_id"] for p in progress_list if p.get("completed", False)}
    
    # 2. Week tasks & completion
    w_tasks = [t for d in week.get("days", []) for t in d.get("tasks", [])]
    total_tasks = len(w_tasks)
    completed_tasks = sum(1 for t in w_tasks if t["id"] in completed_ids)
    remaining_tasks = max(0, total_tasks - completed_tasks)
    comp_pct = calc_percentage(completed_tasks, total_tasks)
    
    progress = WeeklyReviewProgress(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        remaining_tasks=remaining_tasks,
        completion_percentage=comp_pct
    )
    
    # 3. Targets progress
    raw_targets = week.get("targets", {})
    targets_dict: Dict[str, WeeklyReviewTargetProgress] = {}
    
    for key, target_val in raw_targets.items():
        if not isinstance(target_val, int):
            continue
        key_lower = key.lower()
        if "coding" in key_lower:
            comp_count = sum(1 for t in w_tasks if (t.get("category") == "DSA" or t.get("task_type") == "CODING") and t["id"] in completed_ids)
        elif "sql" in key_lower:
            comp_count = sum(1 for t in w_tasks if (t.get("category") == "SQL" or t.get("task_type") == "SQL") and t["id"] in completed_ids)
        elif "cs" in key_lower:
            comp_count = sum(1 for t in w_tasks if t.get("category") in ["CS", "DBMS", "OOP", "OS", "CN", "Computer Architecture", "Software Engineering"] and t["id"] in completed_ids)
        else:
            comp_count = sum(1 for t in w_tasks if t["id"] in completed_ids)
            
        targets_dict[key] = WeeklyReviewTargetProgress(
            target=target_val,
            completed=comp_count
        )
        
    # 4. Categories breakdown for this week
    category_counts: Dict[str, Dict[str, int]] = {}
    for t in w_tasks:
        cat = t.get("category", "General")
        if cat not in category_counts:
            category_counts[cat] = {"total": 0, "completed": 0}
        category_counts[cat]["total"] += 1
        if t["id"] in completed_ids:
            category_counts[cat]["completed"] += 1
            
    categories = []
    for cat, counts in sorted(category_counts.items(), key=lambda x: x[0]):
        c_tot = counts["total"]
        c_comp = counts["completed"]
        categories.append(WeeklyReviewCategoryProgress(
            category=cat,
            total_tasks=c_tot,
            completed_tasks=c_comp,
            completion_percentage=calc_percentage(c_comp, c_tot)
        ))
        
    # 5. Weakness summary & mistakes to review
    weakness_docs = await db["weaknesses"].find({"user_id": user_id}).sort("created_at", -1).to_list(length=None)
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    open_count = 0
    high_count = 0
    due_count = 0
    resolved_count = 0
    unresolved_mistakes = []
    
    for w in weakness_docs:
        w_status = w.get("status", "OPEN")
        w_pri = w.get("priority", "MEDIUM")
        
        if w_status == "RESOLVED":
            resolved_count += 1
        else:
            open_count += 1
            if w_pri in ["HIGH", "CRITICAL"]:
                high_count += 1
            if w.get("retry_date"):
                r_date = w["retry_date"].strftime("%Y-%m-%d") if isinstance(w["retry_date"], datetime) else str(w["retry_date"])[:10]
                if r_date <= today_str:
                    due_count += 1
            unresolved_mistakes.append(WeeklyReviewMistakeItem(
                id=str(w["_id"]),
                topic=w.get("topic", ""),
                problem_concept=w.get("problem_concept", ""),
                what_i_got_wrong=w.get("what_i_got_wrong", ""),
                correct_concept=w.get("correct_concept", ""),
                priority=w_pri,
                status=w_status
            ))
            
    weakness_summary = WeeklyReviewWeaknessSummary(
        open=open_count,
        high_priority=high_count,
        due=due_count,
        resolved=resolved_count
    )
    
    # 6. User reflection record
    review_doc = await db["weekly_reviews"].find_one({"user_id": user_id, "week_number": week_number})
    if review_doc:
        reflection = WeeklyReflectionResponse(
            weakest_topics=review_doc.get("weakest_topics", []),
            improved_topics=review_doc.get("improved_topics", []),
            carry_forward_topics=review_doc.get("carry_forward_topics", []),
            next_priorities=review_doc.get("next_priorities", []),
            confidence=review_doc.get("confidence"),
            motivation=review_doc.get("motivation"),
            schedule_adjustments=review_doc.get("schedule_adjustments", ""),
            updated_at=review_doc.get("updated_at")
        )
    else:
        reflection = WeeklyReflectionResponse()

    # 7. Assessment performance for this week
    assessment_docs = await db["assessments"].find({"week_number": week_number}).to_list(length=None)
    assessment_ids = [a["id"] for a in assessment_docs]
    
    assessment_status = "No assessment data available yet."
    assessment_info = WeeklyReviewAssessmentInfo(
        assessments_completed=0,
        latest_assessment_percentage=None,
        average_assessment_percentage=None,
        passed_assessments=0,
        failed_assessments=0,
        summary="No assessment data available yet."
    )

    if assessment_ids:
        attempts = await db["assessment_attempts"].find({
            "user_id": user_id,
            "assessment_id": {"$in": assessment_ids},
            "status": "SUBMITTED"
        }).sort("submitted_at", -1).to_list(length=None)

        if attempts:
            completed_count = len(attempts)
            latest_attempt = attempts[0]
            latest_pct = latest_attempt.get("percentage", 0.0)
            percentages = [att.get("percentage", 0.0) for att in attempts if att.get("percentage") is not None]
            avg_pct = round(sum(percentages) / len(percentages), 1) if percentages else latest_pct
            passed_count = sum(1 for att in attempts if att.get("passed") is True)
            failed_count = sum(1 for att in attempts if att.get("passed") is False)
            
            pass_str = "Passed" if latest_attempt.get("passed") else "Needs Improvement"
            summary_str = f"Completed {completed_count} attempt(s) with latest score {latest_pct}% ({pass_str})."
            assessment_status = summary_str
            assessment_info = WeeklyReviewAssessmentInfo(
                assessments_completed=completed_count,
                latest_assessment_percentage=latest_pct,
                average_assessment_percentage=avg_pct,
                passed_assessments=passed_count,
                failed_assessments=failed_count,
                summary=summary_str
            )
        
    return WeeklyReviewResponse(
        week=WeeklyReviewWeekInfo(
            week_number=week["week_number"],
            title=week.get("title", ""),
            phase=week.get("phase")
        ),
        progress=progress,
        targets=targets_dict,
        categories=categories,
        weakness_summary=weakness_summary,
        mistakes_to_review=unresolved_mistakes[:5],
        reflection=reflection,
        assessment_status=assessment_status,
        assessment_info=assessment_info
    )

async def save_weekly_reflection(user_id: str, week_number: int, data: WeeklyReflectionUpdate) -> WeeklyReviewResponse:
    if week_number < 1 or week_number > 12:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="week_number must be between 1 and 12"
        )
        
    db = db_client.database
    now = datetime.now(timezone.utc)
    
    def clean_list(items: Optional[List[str]]) -> List[str]:
        if not items:
            return []
        cleaned = []
        for item in items:
            s = item.strip()
            if s:
                cleaned.append(s)
        return cleaned
        
    update_doc = {
        "user_id": user_id,
        "week_number": week_number,
        "weakest_topics": clean_list(data.weakest_topics),
        "improved_topics": clean_list(data.improved_topics),
        "carry_forward_topics": clean_list(data.carry_forward_topics),
        "next_priorities": clean_list(data.next_priorities),
        "confidence": data.confidence,
        "motivation": data.motivation,
        "schedule_adjustments": (data.schedule_adjustments or "").strip(),
        "updated_at": now
    }
    
    await db["weekly_reviews"].update_one(
        {"user_id": user_id, "week_number": week_number},
        {"$set": update_doc, "$setOnInsert": {"created_at": now}},
        upsert=True
    )
    
    return await get_weekly_review(user_id, week_number)
