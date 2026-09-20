CURRICULUM_VERSION = "planner-2026-09-v1"

DSA_SUBTASKS = [
    {"title": "Understand problem", "completed": False},
    {"title": "Identify constraints", "completed": False},
    {"title": "Brute force", "completed": False},
    {"title": "Complexity analysis", "completed": False},
    {"title": "Identify bottleneck", "completed": False},
    {"title": "Optimize", "completed": False},
    {"title": "Explain why optimization works", "completed": False},
    {"title": "Code optimal solution", "completed": False},
    {"title": "Test", "completed": False},
    {"title": "Edge cases", "completed": False},
    {"title": "Final complexity", "completed": False}
]

SQL_SUBTASKS = [
    {"title": "Understand requirements", "completed": False},
    {"title": "Identify tables", "completed": False},
    {"title": "Write simple query", "completed": False},
    {"title": "Add filtering", "completed": False},
    {"title": "Add aggregation", "completed": False},
    {"title": "Optimize", "completed": False},
    {"title": "Test edge cases", "completed": False},
    {"title": "Verify output", "completed": False}
]

# Helper function to auto-assign IDs if needed, but we'll do it explicitly
# to avoid runtime modifications of the static curriculum structure.

CURRICULUM = [
    {
        "week_number": 1,
        "phase": "Phase 1 — Foundation",
        "title": "Baseline Assessment & Core Fundamentals",
        "description": "Establish a baseline and begin core preparation.",
        "targets": {"Coding": 14, "SQL": 12},
        "assessments": [
            {"type": "Baseline", "topics": ["General Programming", "Basic Logic"], "title": "Week 1 baseline coding evaluation"}
        ],
        "mocks": [],
        "milestones": [],
        "tasks": [
            {"title": "Complete Baseline Coding Evaluation", "category": "Problem Solving", "task_type": "ASSESSMENT", "estimated_minutes": 120, "description": "Take the initial baseline test."},
            {"title": "Solve 2 basic arrays problems", "category": "DSA", "task_type": "CODING", "estimated_minutes": 60, "subtasks": DSA_SUBTASKS},
            {"title": "Solve 2 basic string problems", "category": "DSA", "task_type": "CODING", "estimated_minutes": 60, "subtasks": DSA_SUBTASKS},
            {"title": "Solve 3 basic SELECT & WHERE problems", "category": "SQL", "task_type": "SQL", "estimated_minutes": 60, "subtasks": SQL_SUBTASKS},
            {"title": "Review OOP Fundamentals", "category": "OOP", "task_type": "LEARN", "estimated_minutes": 60, "description": "Review classes, objects, and encapsulation."}
        ]
    },
    {
        "week_number": 2,
        "phase": "Phase 1 — Foundation",
        "title": "Hashing & Joins",
        "description": "Introduction to hash maps and multi-table SQL queries.",
        "targets": {},
        "assessments": [],
        "mocks": [],
        "milestones": [],
        "tasks": [
            {"title": "Solve 3 Hash Map problems (e.g., Two Sum)", "category": "DSA", "task_type": "CODING", "estimated_minutes": 90, "subtasks": DSA_SUBTASKS},
            {"title": "Solve 3 SQL JOIN problems", "category": "SQL", "task_type": "SQL", "estimated_minutes": 90, "subtasks": SQL_SUBTASKS},
            {"title": "Review OS Processes and Threads", "category": "Operating Systems", "task_type": "CORE_CS", "estimated_minutes": 60}
        ]
    },
    {
        "week_number": 3,
        "phase": "Phase 1 — Foundation",
        "title": "Sliding Window & Foundational Concepts",
        "description": "Advanced array techniques and core computer science fundamentals.",
        "targets": {},
        "assessments": [
            {"type": "Quiz", "title": "Week 3 quiz", "topics": ["Hashing", "Joins", "OS"]}
        ],
        "mocks": [],
        "milestones": [
            {"title": "Foundation completed", "target_week": 3, "description": "Completed all foundational topics."}
        ],
        "tasks": [
            {"title": "Solve 3 Sliding Window problems", "category": "DSA", "task_type": "CODING", "estimated_minutes": 90, "subtasks": DSA_SUBTASKS},
            {"title": "Take Week 3 Quiz", "category": "Revision", "task_type": "ASSESSMENT", "estimated_minutes": 45}
        ]
    },
    {
        "week_number": 4,
        "phase": "Phase 2 — Core Interview Preparation",
        "title": "Data Structures Consolidation & First Mock",
        "description": "Consolidating early DSA and introducing mock interviews.",
        "targets": {"Coding": 14, "SQL": 12, "CS": 35, "Mock": 1},
        "assessments": [],
        "mocks": [
            {"title": "Week 4 — Mock #1", "target_week": 4, "duration": 45, "areas": ["Arrays", "Strings", "SQL"], "purpose": "First mock interview exposure."}
        ],
        "milestones": [
            {"title": "First mock interview", "target_week": 4, "description": "Complete your first technical mock interview."}
        ],
        "tasks": [
            {"title": "Conduct Mock Interview #1", "category": "Mock Interviews", "task_type": "MOCK_INTERVIEW", "estimated_minutes": 60},
            {"title": "Solve 3 Linked List problems", "category": "DSA", "task_type": "CODING", "estimated_minutes": 90, "subtasks": DSA_SUBTASKS},
            {"title": "Review Computer Networks (OSI Model)", "category": "Computer Networks", "task_type": "CORE_CS", "estimated_minutes": 60}
        ]
    },
    {
        "week_number": 5,
        "phase": "Phase 2 — Core Interview Preparation",
        "title": "Trees & Binary Search Trees",
        "description": "Mastering hierarchical data structures.",
        "targets": {},
        "assessments": [
            {"type": "Quiz", "title": "Week 5 quiz"}
        ],
        "mocks": [],
        "milestones": [],
        "tasks": [
            {"title": "Solve 3 Tree Traversal problems", "category": "DSA", "task_type": "CODING", "estimated_minutes": 90, "subtasks": DSA_SUBTASKS},
            {"title": "Take Week 5 Quiz", "category": "Revision", "task_type": "ASSESSMENT", "estimated_minutes": 45}
        ]
    },
    {
        "week_number": 6,
        "phase": "Phase 2 — Core Interview Preparation",
        "title": "Heap, Priority Queue & Graphs",
        "description": "Advanced data structures and graph traversal.",
        "targets": {},
        "assessments": [],
        "mocks": [
            {"title": "Week 6 — Mock #2", "target_week": 6, "duration": 45, "areas": ["Trees", "Heaps"], "purpose": "Note: Corrected from PDF typo."}
        ],
        "milestones": [],
        "tasks": [
            {"title": "Solve 2 Graph BFS/DFS problems", "category": "DSA", "task_type": "CODING", "estimated_minutes": 90, "subtasks": DSA_SUBTASKS},
            {"title": "Conduct Mock Interview #2", "category": "Mock Interviews", "task_type": "MOCK_INTERVIEW", "estimated_minutes": 60}
        ]
    },
    {
        "week_number": 7,
        "phase": "Phase 2 — Core Interview Preparation",
        "title": "Recursion, Backtracking & Final Core CS",
        "description": "Advanced problem solving and concluding core CS topics.",
        "targets": {},
        "assessments": [
            {"type": "Quiz", "title": "Week 7 quiz"}
        ],
        "mocks": [],
        "milestones": [
            {"title": "Core CS coverage completed", "target_week": 7, "description": "Finished OOP, OS, CN, and DBMS."}
        ],
        "tasks": [
            {"title": "Solve 2 Backtracking problems", "category": "DSA", "task_type": "CODING", "estimated_minutes": 90, "subtasks": DSA_SUBTASKS},
            {"title": "Take Week 7 Quiz", "category": "Revision", "task_type": "ASSESSMENT", "estimated_minutes": 45}
        ]
    },
    {
        "week_number": 8,
        "phase": "Phase 3 — Domain Preparation",
        "title": "Greedy & Data Science Foundations",
        "description": "Domain-specific preparation begins alongside Greedy algorithms.",
        "targets": {},
        "assessments": [],
        "mocks": [],
        "milestones": [],
        "tasks": [
            {"title": "Learn Pandas/NumPy Basics", "category": "Data Science", "task_type": "LEARN", "estimated_minutes": 90},
            {"title": "Solve 2 Greedy algorithms", "category": "DSA", "task_type": "CODING", "estimated_minutes": 60, "subtasks": DSA_SUBTASKS}
        ]
    },
    {
        "week_number": 9,
        "phase": "Phase 3 — Domain Preparation",
        "title": "ML Fundamentals & Algorithms",
        "description": "Core Machine Learning concepts.",
        "targets": {},
        "assessments": [
            {"type": "Quiz", "title": "Week 9 quiz"}
        ],
        "mocks": [],
        "milestones": [],
        "tasks": [
            {"title": "Review Supervised vs Unsupervised ML", "category": "AI/ML", "task_type": "LEARN", "estimated_minutes": 60},
            {"title": "Take Week 9 Quiz", "category": "Revision", "task_type": "ASSESSMENT", "estimated_minutes": 45}
        ]
    },
    {
        "week_number": 10,
        "phase": "Phase 3 — Domain Preparation",
        "title": "Advanced ML & Full Integration",
        "description": "Wrapping up domain preparation and combining knowledge.",
        "targets": {},
        "assessments": [],
        "mocks": [
            {"title": "Week 10 — Mock #3", "target_week": 10, "duration": 60, "areas": ["Domain", "DSA"], "purpose": "Full mixed mock."}
        ],
        "milestones": [
            {"title": "Full mixed mock", "target_week": 10, "description": "Complete a full mixed mock interview."}
        ],
        "tasks": [
            {"title": "Review ML Evaluation Metrics", "category": "AI/ML", "task_type": "LEARN", "estimated_minutes": 60},
            {"title": "Conduct Mock Interview #3", "category": "Mock Interviews", "task_type": "MOCK_INTERVIEW", "estimated_minutes": 60}
        ]
    },
    {
        "week_number": 11,
        "phase": "Phase 4 — Interview Mode",
        "title": "Intensive Revision & Simulation",
        "description": "Heavy practice, timed assessments, and mock interviews.",
        "targets": {"Coding": 21, "SQL": 15, "CS": 40, "Assessments": 2, "Mock": 1},
        "assessments": [
            {"type": "Coding", "title": "Week 11 coding assessment #1"},
            {"type": "Coding", "title": "Week 11 coding assessment #2"}
        ],
        "mocks": [
            {"title": "Week 11 — Mocks #4-5", "target_week": 11, "duration": 45, "areas": ["Comprehensive"], "purpose": "Intensive mock practice."}
        ],
        "milestones": [
            {"title": "Interview Mode begins", "target_week": 11, "description": "Transition to full interview simulation."}
        ],
        "tasks": [
            {"title": "Take Week 11 coding assessment #1", "category": "Assessment", "task_type": "ASSESSMENT", "estimated_minutes": 60},
            {"title": "Take Week 11 coding assessment #2", "category": "Assessment", "task_type": "ASSESSMENT", "estimated_minutes": 60},
            {"title": "Conduct Mock Interviews #4-5", "category": "Mock Interviews", "task_type": "MOCK_INTERVIEW", "estimated_minutes": 90}
        ]
    },
    {
        "week_number": 12,
        "phase": "Phase 4 — Interview Mode",
        "title": "Final Polish & Interview Readiness",
        "description": "Final readiness evaluation and mock gauntlet.",
        "targets": {"Coding": 21, "SQL": 12, "CS": 40, "Mock": "3-4"},
        "assessments": [
            {"type": "Full", "title": "Week 12 final/full mock assessment"}
        ],
        "mocks": [
            {"title": "Week 12 — Mocks #6-8", "target_week": 12, "duration": 60, "areas": ["All"], "purpose": "Final polish."}
        ],
        "milestones": [
            {"title": "Final readiness assessment", "target_week": 12, "description": "Complete final readiness checklist and assessment."}
        ],
        "tasks": [
            {"title": "Take Week 12 final/full mock assessment", "category": "Assessment", "task_type": "ASSESSMENT", "estimated_minutes": 120},
            {"title": "Conduct Mock Interviews #6-8", "category": "Mock Interviews", "task_type": "MOCK_INTERVIEW", "estimated_minutes": 180},
            {"title": "Complete final readiness checklist", "category": "Revision", "task_type": "MILESTONE", "estimated_minutes": 60}
        ]
    }
]

for w_idx, week in enumerate(CURRICULUM):
    week["id"] = f"week_{week['week_number']}"
    for t_idx, task in enumerate(week.get("tasks", [])):
        task["id"] = f"task_{week['week_number']}_{t_idx+1}"
        task["week_id"] = week["id"]
