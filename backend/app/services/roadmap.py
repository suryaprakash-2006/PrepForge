from datetime import datetime, timezone
from pymongo.errors import DuplicateKeyError
from app.db.connection import db_client

DEFAULT_ROADMAP = [
    {"week_number": 1, "title": "Foundations & Environment Setup", "description": "Setting up the project, understanding the tools."},
    {"week_number": 2, "title": "Python & Problem Solving", "description": "Core Python concepts and basic problem solving."},
    {"week_number": 3, "title": "Data Structures & Algorithms I", "description": "Arrays, Strings, Linked Lists."},
    {"week_number": 4, "title": "Data Structures & Algorithms II", "description": "Trees, Graphs, and Hash Tables."},
    {"week_number": 5, "title": "Database Management Systems", "description": "Relational databases, normalisation, indexing."},
    {"week_number": 6, "title": "SQL Practice", "description": "Complex queries, joins, and aggregations."},
    {"week_number": 7, "title": "Object-Oriented Programming", "description": "Classes, inheritance, polymorphism, and patterns."},
    {"week_number": 8, "title": "Operating Systems & Computer Networks", "description": "Processes, threads, OSI model, TCP/IP."},
    {"week_number": 9, "title": "System Design Basics", "description": "Scaling, load balancing, caching architectures."},
    {"week_number": 10, "title": "Mock Interviews & Assessments", "description": "Practice interviews and timed assessments."},
    {"week_number": 11, "title": "Project Building & Refinement", "description": "Polishing the portfolio projects."},
    {"week_number": 12, "title": "Final Internship Preparation", "description": "Resume review, final revisions, and interview readiness."}
]

async def initialize_default_roadmap(user_id: str):
    """
    Seeds the default 12-week roadmap for a specific user.
    Silently ignores if a week already exists due to unique index.
    """
    db = db_client.database
    now = datetime.now(timezone.utc)
    
    for week_data in DEFAULT_ROADMAP:
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
        
        try:
            await db["weeks"].insert_one(week_doc)
        except DuplicateKeyError:
            pass # Week already exists for this user, skip.
