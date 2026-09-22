import json

def get_empty_days(week_id):
    days = []
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for i, name in enumerate(day_names):
        days.append({
            "id": f"{week_id}_day_{i+1}",
            "week_id": week_id,
            "day_number": i+1,
            "day_name": name,
            "time_budget_minutes": 150 if i < 5 else 180,
            "tasks": []
        })
    return days

CURRICULUM = [
    {
        "week_number": 1,
        "phase": "Phase 1 — Foundation",
        "title": "Baseline Assessment & Core Fundamentals",
        "description": "Establish a baseline and begin core preparation.",
        "targets": {"coding": 14, "sql": 12},
        "assessments": [
            {"type": "Baseline", "topics": ["General Programming", "Basic Logic"], "title": "Week 1 baseline coding evaluation"}
        ],
        "mocks": [],
        "milestones": [],
        "days": get_empty_days("week_1")
    }
]

# We will populate the curriculum programmatically and then dump it as python code.
