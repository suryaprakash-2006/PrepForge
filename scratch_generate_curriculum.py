import json

DSA_SUBTASKS = [
    {"title": "Understand problem", "completed": False},
    {"title": "Identify constraints", "completed": False},
    {"title": "Brute force", "completed": False},
    {"title": "Complexity", "completed": False},
    {"title": "Identify bottleneck", "completed": False},
    {"title": "Optimize", "completed": False},
    {"title": "Explain optimization", "completed": False},
    {"title": "Code", "completed": False},
    {"title": "Test", "completed": False},
    {"title": "Edge cases", "completed": False},
    {"title": "Final complexity", "completed": False}
]

SQL_SUBTASKS = [
    {"title": "Understand requirement", "completed": False},
    {"title": "Identify tables", "completed": False},
    {"title": "Write query", "completed": False},
    {"title": "Filtering", "completed": False},
    {"title": "Aggregation", "completed": False},
    {"title": "Optimize", "completed": False},
    {"title": "Edge cases", "completed": False},
    {"title": "Verify", "completed": False}
]

def make_task(title, category, task_type, time_budget, subtasks=None, desc=None):
    t = {
        "title": title,
        "category": category,
        "task_type": task_type,
        "estimated_minutes": time_budget
    }
    if subtasks:
        t["subtasks"] = subtasks
    if desc:
        t["description"] = desc
    return t

def get_days(week_id, week_number):
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

weeks_data = [
    {
        "week_number": 1,
        "phase": "Phase 1 — Foundation",
        "title": "Baseline Assessment & Core Fundamentals",
        "description": "Establish a baseline evaluation and build core programming fundamentals across Python, C++, STL, and basic SQL.",
        "targets": {"coding": 14, "sql": 12},
        "assessments": [
            {"type": "Baseline", "topics": ["General Programming", "Basic Logic"], "title": "Week 1 baseline coding evaluation"}
        ],
        "mocks": [],
        "milestones": [],
        "days_populate": {
            1: [make_task("Python fundamentals", "Python", "LEARN", 60), make_task("Solve 2 Arrays coding problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            2: [make_task("C++ fundamentals", "C++", "LEARN", 60), make_task("Solve 2 Arrays coding problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            3: [make_task("C++ STL basics", "C++", "LEARN", 60), make_task("Solve 3 Strings coding problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            4: [make_task("Big-O notation, Time complexity, Space complexity", "DSA", "LEARN", 60), make_task("Solve 3 Strings coding problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            5: [make_task("SQL SELECT, WHERE, DISTINCT", "SQL", "LEARN", 30), make_task("Solve 6 SQL queries", "SQL", "SQL", 60, SQL_SUBTASKS), make_task("Solve 2 Strings coding problems", "DSA", "CODING", 60, DSA_SUBTASKS)],
            6: [make_task("SQL ORDER BY, LIMIT", "SQL", "LEARN", 30), make_task("Solve 6 SQL queries", "SQL", "SQL", 60, SQL_SUBTASKS), make_task("Resume corrections", "Resume", "PROJECT", 90)],
            7: [make_task("Baseline coding assessment", "Assessment", "ASSESSMENT", 90), make_task("Mistake review & Weakness logging", "Weakness Review", "WEAKNESS_REVIEW", 45), make_task("Weekly review", "Revision", "REVISION", 45)]
        }
    },
    {
        "week_number": 2,
        "phase": "Phase 1 — Foundation",
        "title": "Hashing & Joins",
        "description": "Master hash maps, two pointers, prefix sums, and relational database joins and constraints.",
        "targets": {"coding": 14, "sql": 12},
        "assessments": [],
        "mocks": [],
        "milestones": [],
        "days_populate": {
            1: [make_task("Python dict, Python set", "Python", "LEARN", 45), make_task("C++ unordered_map, C++ set", "C++", "LEARN", 45), make_task("Solve 2 Hashing problems", "DSA", "CODING", 60, DSA_SUBTASKS)],
            2: [make_task("vector/STL revision", "C++", "LEARN", 30), make_task("Solve 3 Hashing problems", "DSA", "CODING", 120, DSA_SUBTASKS)],
            3: [make_task("Two Pointers", "DSA", "LEARN", 60), make_task("Solve 3 Two Pointers problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            4: [make_task("Prefix Sums", "DSA", "LEARN", 60), make_task("Solve 3 Prefix Sums problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            5: [make_task("Relational model, Keys, Constraints, Relationships", "DBMS", "LEARN", 60), make_task("Solve 3 Prefix Sums/Hashing problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            6: [make_task("GROUP BY, HAVING", "SQL", "LEARN", 30), make_task("INNER JOIN, LEFT JOIN, RIGHT JOIN", "SQL", "LEARN", 60), make_task("Solve 6 SQL queries", "SQL", "SQL", 90, SQL_SUBTASKS)],
            7: [make_task("Solve 6 SQL queries", "SQL", "SQL", 60, SQL_SUBTASKS), make_task("Resume continuation", "Resume", "PROJECT", 60), make_task("Weakness review", "Weakness Review", "WEAKNESS_REVIEW", 60)]
        }
    },
    {
        "week_number": 3,
        "phase": "Phase 1 — Foundation",
        "title": "Sliding Window & Foundational Concepts",
        "description": "Advanced array techniques, linked structures, subqueries, normalization, and OOP paradigms.",
        "targets": {"coding": 14, "sql": 12, "cs": 30},
        "assessments": [
            {"type": "Quiz", "title": "Week 3 Quiz", "topics": ["Hashing", "Joins", "OOP", "DBMS"]}
        ],
        "mocks": [],
        "milestones": [
            {"title": "Foundation completed", "target_week": 3, "description": "Completed foundational data structures and core CS topics."}
        ],
        "days_populate": {
            1: [make_task("Sliding Window", "DSA", "LEARN", 60), make_task("Solve 3 Sliding Window problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            2: [make_task("Binary Search", "DSA", "LEARN", 60), make_task("Solve 3 Binary Search problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            3: [make_task("Linked Lists", "DSA", "LEARN", 60), make_task("Solve 3 Linked Lists problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            4: [make_task("Stack, Queue", "DSA", "LEARN", 60), make_task("Solve 3 Stack/Queue problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            5: [make_task("Solve 2 mixed problems", "DSA", "CODING", 60, DSA_SUBTASKS), make_task("SQL Subqueries, Correlated Queries", "SQL", "LEARN", 45), make_task("Solve 6 SQL queries", "SQL", "SQL", 45, SQL_SUBTASKS)],
            6: [make_task("1NF, 2NF, 3NF, Transactions, ACID", "DBMS", "LEARN", 60), make_task("OOP, Encapsulation, Abstraction, Inheritance, Polymorphism", "OOP", "LEARN", 60), make_task("Solve 6 SQL queries", "SQL", "SQL", 60, SQL_SUBTASKS)],
            7: [make_task("30 CS questions practice", "CS", "PRACTICE", 45), make_task("Weekly Quiz", "Assessment", "ASSESSMENT", 45), make_task("Weakness Review", "Weakness Review", "WEAKNESS_REVIEW", 30), make_task("Project Defence preparation & Review", "Project Defence", "PROJECT", 30), make_task("Weekly Review", "Revision", "REVISION", 30)]
        }
    },
    {
        "week_number": 4,
        "phase": "Phase 2 — Core Interview Preparation",
        "title": "Data Structures Consolidation & First Mock",
        "description": "Consolidate linear data structures, master CTEs, REST APIs, and conduct technical Mock Interview #1.",
        "targets": {"coding": 14, "sql": 12, "cs": 35, "mock": 1},
        "assessments": [],
        "mocks": [
            {"title": "Week 4 — Mock #1", "target_week": 4, "duration": 45, "areas": ["Arrays", "Strings", "SQL", "OOP"], "purpose": "First technical mock interview exposure."}
        ],
        "milestones": [
            {"title": "First mock interview", "target_week": 4, "description": "Complete your first live technical mock interview."}
        ],
        "days_populate": {
            1: [make_task("Linked List consolidation", "DSA", "LEARN", 60), make_task("Solve 3 Linked List problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            2: [make_task("Stack, Queue review", "DSA", "LEARN", 45), make_task("Solve 3 Stack/Queue problems", "DSA", "CODING", 105, DSA_SUBTASKS)],
            3: [make_task("Solve 3 mixed DSA problems", "DSA", "CODING", 90, DSA_SUBTASKS), make_task("CTEs, Recursive CTEs", "SQL", "LEARN", 60)],
            4: [make_task("Virtual functions, Overloading, Composition", "OOP", "LEARN", 60), make_task("REST APIs, HTTP methods, HTTP status codes", "CN", "LEARN", 90)],
            5: [make_task("Solve 3 mixed DSA problems", "DSA", "CODING", 90, DSA_SUBTASKS), make_task("Solve 6 SQL queries", "SQL", "SQL", 60, SQL_SUBTASKS)],
            6: [make_task("Solve 2 mixed DSA problems", "DSA", "CODING", 60, DSA_SUBTASKS), make_task("Solve 6 SQL queries", "SQL", "SQL", 60, SQL_SUBTASKS), make_task("Project explanation preparation", "Project Defence", "PROJECT", 60)],
            7: [make_task("35 CS questions practice", "CS", "PRACTICE", 60), make_task("Weakness review", "Weakness Review", "WEAKNESS_REVIEW", 60), make_task("Mock Interview #1", "Mock Interview", "MOCK_INTERVIEW", 60)]
        }
    },
    {
        "week_number": 5,
        "phase": "Phase 2 — Core Interview Preparation",
        "title": "Trees & Binary Search Trees",
        "description": "Master hierarchical trees, BST traversals, SQL window functions, DBMS indexing, and OS scheduling.",
        "targets": {"coding": 14, "sql": 12, "cs": 35},
        "assessments": [
            {"type": "Quiz", "title": "Week 5 Quiz", "topics": ["Trees", "BST", "Window Functions", "OS Scheduling"]}
        ],
        "mocks": [],
        "milestones": [],
        "days_populate": {
            1: [make_task("Binary Trees, Tree traversals (preorder, inorder, postorder, level order)", "DSA", "LEARN", 60), make_task("Solve 3 Tree problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            2: [make_task("Tree height, Tree diameter, LCA", "DSA", "LEARN", 60), make_task("Solve 3 Tree path problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            3: [make_task("BST search, insert, delete, validation", "DSA", "LEARN", 60), make_task("Solve 3 BST problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            4: [make_task("Solve 3 Tree/BST problems", "DSA", "CODING", 90, DSA_SUBTASKS), make_task("SQL Window Functions: ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD", "SQL", "LEARN", 60)],
            5: [make_task("Solve 2 Tree/BST problems", "DSA", "CODING", 60, DSA_SUBTASKS), make_task("DBMS indexing, B/B+ trees, Query optimization", "DBMS", "LEARN", 90)],
            6: [make_task("Processes vs Threads, CPU scheduling, Context switching", "OS", "LEARN", 90), make_task("Solve 6 SQL queries", "SQL", "SQL", 90, SQL_SUBTASKS)],
            7: [make_task("Statistics/probability where applicable", "Data Science", "LEARN", 45), make_task("Solve 6 SQL queries", "SQL", "SQL", 45, SQL_SUBTASKS), make_task("35 CS questions practice", "CS", "PRACTICE", 90)]
        }
    },
    {
        "week_number": 6,
        "phase": "Phase 2 — Core Interview Preparation",
        "title": "Heap, Priority Queue & Graphs",
        "description": "Deep dive into Priority Queues, Graph BFS/DFS representations, OS memory/deadlocks, Networking, and Mock #2.",
        "targets": {"coding": 14, "sql": 12, "cs": 40, "mock": 1},
        "assessments": [],
        "mocks": [
            {"title": "Week 6 — Mock #2", "target_week": 6, "duration": 45, "areas": ["Trees", "Heaps", "Graphs", "OS"], "purpose": "Second technical mock interview."}
        ],
        "milestones": [],
        "days_populate": {
            1: [make_task("Heap, Heap operations, Priority Queue", "DSA", "LEARN", 60), make_task("Solve 3 Heap problems (Kth largest, Median, K-closest)", "DSA", "CODING", 90, DSA_SUBTASKS)],
            2: [make_task("Graph representations (Adjacency matrix, list)", "DSA", "LEARN", 45), make_task("BFS, DFS", "DSA", "LEARN", 45), make_task("Solve 2 Graph problem solving", "DSA", "CODING", 60, DSA_SUBTASKS)],
            3: [make_task("Solve 3 Graph problem solving", "DSA", "CODING", 90, DSA_SUBTASKS), make_task("Memory hierarchy, Paging, Virtual memory", "OS", "LEARN", 60)],
            4: [make_task("Solve 3 Graph problem solving", "DSA", "CODING", 90, DSA_SUBTASKS), make_task("Deadlocks, Synchronization, Mutex, Semaphore", "OS", "LEARN", 60)],
            5: [make_task("Solve 3 mixed Graph/Heap problems", "DSA", "CODING", 90, DSA_SUBTASKS), make_task("Complex SQL practice", "SQL", "PRACTICE", 60)],
            6: [make_task("OSI model, TCP/IP, TCP vs UDP", "CN", "LEARN", 90), make_task("Solve 6 SQL queries", "SQL", "SQL", 90, SQL_SUBTASKS)],
            7: [make_task("Solve 6 SQL queries", "SQL", "SQL", 60, SQL_SUBTASKS), make_task("40 CS questions practice", "CS", "PRACTICE", 60), make_task("Mock Interview #2 & review", "Mock Interview", "MOCK_INTERVIEW", 60)]
        }
    },
    {
        "week_number": 7,
        "phase": "Phase 2 — Core Interview Preparation",
        "title": "Recursion, Backtracking & Final Core CS",
        "description": "Exhaustive recursion, backtracking, computer architecture, networking protocols, Git, and Core CS consolidation.",
        "targets": {"coding": 14, "sql": 12, "cs": 40},
        "assessments": [
            {"type": "Quiz", "title": "Week 7 Quiz", "topics": ["Recursion", "Backtracking", "Architecture", "Networks"]}
        ],
        "mocks": [],
        "milestones": [
            {"title": "Core CS coverage completed", "target_week": 7, "description": "Finished OOP, OS, CN, DBMS, and Computer Architecture."}
        ],
        "days_populate": {
            1: [make_task("Recursion, Recursive thinking", "DSA", "LEARN", 60), make_task("Solve 3 Recursion problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            2: [make_task("Backtracking, Permutations, Combinations", "DSA", "LEARN", 60), make_task("Solve 3 Backtracking problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            3: [make_task("Subsets, Sudoku", "DSA", "LEARN", 60), make_task("Solve 3 Backtracking problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            4: [make_task("Graph traversal revision", "DSA", "REVISION", 60), make_task("Solve 3 mixed DSA problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            5: [make_task("Solve 2 mixed DSA problems", "DSA", "CODING", 60, DSA_SUBTASKS), make_task("SQL revision, SQL optimization", "SQL", "REVISION", 90)],
            6: [make_task("DNS, DHCP, ARP, Routing, HTTP/HTTPS, REST APIs", "CN", "LEARN", 60), make_task("CPU, ALU, Control Unit, Registers, Pipelining, RISC, CISC", "Computer Architecture", "LEARN", 60), make_task("Solve 6 SQL queries", "SQL", "SQL", 60, SQL_SUBTASKS)],
            7: [make_task("Git, GitHub, Testing, Debugging", "Software Engineering", "LEARN", 45), make_task("Solve 6 SQL queries", "SQL", "SQL", 45, SQL_SUBTASKS), make_task("40 CS questions practice", "CS", "PRACTICE", 30), make_task("Weekly Quiz", "Assessment", "ASSESSMENT", 20), make_task("Project Defence Q&A", "Project Defence", "PROJECT", 20), make_task("Weakness Review", "Weakness Review", "WEAKNESS_REVIEW", 20)]
        }
    },
    {
        "week_number": 8,
        "phase": "Phase 3 — Domain Preparation",
        "title": "Greedy & Data Science Foundations",
        "description": "Transition to Greedy algorithms, introductory Dynamic Programming, NumPy arrays, Pandas DataFrames, and EDA.",
        "targets": {"coding": 14, "sql": 15, "cs": 20},
        "assessments": [],
        "mocks": [],
        "milestones": [],
        "days_populate": {
            1: [make_task("Greedy algorithms, Greedy problem solving", "DSA", "LEARN", 60), make_task("Solve 3 Greedy algorithms", "DSA", "CODING", 90, DSA_SUBTASKS)],
            2: [make_task("Dynamic Programming introduction", "DSA", "LEARN", 60), make_task("Solve 3 DP/Greedy problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            3: [make_task("Solve 3 DP/Greedy problems", "DSA", "CODING", 90, DSA_SUBTASKS), make_task("NumPy, NumPy arrays, NumPy operations, Broadcasting", "Data Science", "LEARN", 60)],
            4: [make_task("Solve 3 mixed DSA problems", "DSA", "CODING", 90, DSA_SUBTASKS), make_task("Pandas, DataFrames, Indexing", "Data Science", "LEARN", 60)],
            5: [make_task("Solve 2 mixed DSA problems", "DSA", "CODING", 60, DSA_SUBTASKS), make_task("Pandas operations, Mean, Median, Mode, Variance, Standard deviation", "Data Science", "LEARN", 90)],
            6: [make_task("Correlation, Covariance, Data cleaning, Missing values", "Data Science", "LEARN", 60), make_task("EDA", "Data Science", "LEARN", 60), make_task("Mixed SQL (8 queries)", "SQL", "SQL", 60, SQL_SUBTASKS)],
            7: [make_task("Mixed SQL (7 queries)", "SQL", "SQL", 60, SQL_SUBTASKS), make_task("20 targeted CS/domain questions", "CS", "PRACTICE", 120)]
        }
    },
    {
        "week_number": 9,
        "phase": "Phase 3 — Domain Preparation",
        "title": "ML Fundamentals & Algorithms",
        "description": "Core machine learning algorithms, model evaluation, validation techniques, and BattWin-Verify deep dive.",
        "targets": {"coding": 12, "sql": 12},
        "assessments": [
            {"type": "Quiz", "title": "Week 9 Quiz", "topics": ["ML Classification", "Regression", "Evaluation Metrics"]}
        ],
        "mocks": [],
        "milestones": [],
        "days_populate": {
            1: [make_task("Supervised Learning, Unsupervised Learning", "Machine Learning", "LEARN", 60), make_task("Solve 2 DSA problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            2: [make_task("Train/Validation/Test, Cross-validation, Overfitting, Underfitting", "Machine Learning", "LEARN", 60), make_task("Solve 2 DSA problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            3: [make_task("Regression, Classification", "Machine Learning", "LEARN", 60), make_task("Solve 2 DSA problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            4: [make_task("Decision Trees, Random Forest", "Machine Learning", "LEARN", 60), make_task("Solve 2 DSA problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            5: [make_task("KNN, Naive Bayes", "Machine Learning", "LEARN", 60), make_task("Solve 2 DSA problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            6: [make_task("ML evaluation metrics, EDA, Outliers, Visualization", "Machine Learning", "LEARN", 90), make_task("Solve 6 SQL queries", "SQL", "SQL", 90, SQL_SUBTASKS)],
            7: [make_task("Data practice", "Data Science", "PRACTICE", 60), make_task("BattWin-Verify deep dive", "Project", "PROJECT", 60), make_task("Solve 2 DSA problems", "DSA", "CODING", 30, DSA_SUBTASKS), make_task("Solve 6 SQL queries", "SQL", "SQL", 30, SQL_SUBTASKS)]
        }
    },
    {
        "week_number": 10,
        "phase": "Phase 3 — Domain Preparation",
        "title": "Advanced ML & Full Integration",
        "description": "Advanced ML ensembles, unsupervised clustering, system design fundamentals, and comprehensive Mock #3.",
        "targets": {"coding": 10, "sql": 10, "mock": 1},
        "assessments": [],
        "mocks": [
            {"title": "Week 10 — Mock #3", "target_week": 10, "duration": 60, "areas": ["DSA", "SQL", "Core CS", "ML/Domain", "Project"], "purpose": "Full integration mock interview."}
        ],
        "milestones": [
            {"title": "Full mixed mock", "target_week": 10, "description": "Complete full multi-topic technical mock interview."}
        ],
        "days_populate": {
            1: [make_task("Gradient Boosting, XGBoost", "Machine Learning", "LEARN", 90), make_task("Solve 2 DSA problems", "DSA", "CODING", 60, DSA_SUBTASKS)],
            2: [make_task("K-Means, PCA", "Machine Learning", "LEARN", 90), make_task("Solve 2 DSA problems", "DSA", "CODING", 60, DSA_SUBTASKS)],
            3: [make_task("Feature Engineering, Hyperparameter tuning", "Machine Learning", "LEARN", 90), make_task("Solve 2 DSA problems", "DSA", "CODING", 60, DSA_SUBTASKS)],
            4: [make_task("Class imbalance, Data leakage", "Machine Learning", "LEARN", 90), make_task("Solve 2 DSA problems", "DSA", "CODING", 60, DSA_SUBTASKS)],
            5: [make_task("Architecture, Backend, SDE fundamentals", "SDE", "LEARN", 90), make_task("Solve 2 DSA problems", "DSA", "CODING", 60, DSA_SUBTASKS)],
            6: [make_task("System Design basics", "SDE", "LEARN", 90), make_task("Mixed SQL", "SQL", "SQL", 90, SQL_SUBTASKS)],
            7: [make_task("Mixed SQL", "SQL", "SQL", 60, SQL_SUBTASKS), make_task("Mixed DSA", "DSA", "CODING", 60, DSA_SUBTASKS), make_task("Full Integration Mock #3", "Mock Interview", "MOCK_INTERVIEW", 60)]
        }
    },
    {
        "week_number": 11,
        "phase": "Phase 4 — Interview Mode",
        "title": "Intensive Revision & Simulation",
        "description": "High-intensity mixed revision, timed coding assessments, ATS resume reviews, and simulation mocks.",
        "targets": {"coding": 21, "sql": 15, "cs": 40, "assessments": 2, "mock": 1},
        "assessments": [
            {"type": "Coding", "title": "Timed Coding Assessment #1"},
            {"type": "Coding", "title": "Timed Coding Assessment #2"}
        ],
        "mocks": [
            {"title": "Week 11 — Comprehensive Mock", "target_week": 11, "duration": 60, "areas": ["Comprehensive"], "purpose": "Intensive simulation mock."}
        ],
        "milestones": [
            {"title": "Interview Mode begins", "target_week": 11, "description": "Transition to full interview simulation mode."}
        ],
        "days_populate": {
            1: [make_task("Mixed DSA revision", "DSA", "REVISION", 60), make_task("Solve 3 coding problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            2: [make_task("Weak DSA topics revision", "DSA", "REVISION", 60), make_task("Solve 3 coding problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            3: [make_task("SQL revision, DBMS revision", "SQL", "REVISION", 60), make_task("Solve 3 coding problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            4: [make_task("OOP revision, OS revision", "CS", "REVISION", 60), make_task("Solve 3 coding problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            5: [make_task("CN revision, Architecture revision", "CS", "REVISION", 60), make_task("Solve 3 coding problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            6: [make_task("Data Science revision, ML revision", "Data Science", "REVISION", 60), make_task("Solve 3 coding problems", "DSA", "CODING", 90, DSA_SUBTASKS), make_task("Solve 8 SQL queries", "SQL", "SQL", 30, SQL_SUBTASKS)],
            7: [make_task("Project Defence, Resume revision, ATS review", "Project", "PROJECT", 40), make_task("Mistake-pattern analysis", "Weakness Review", "WEAKNESS_REVIEW", 20), make_task("Timed Coding Assessment #1", "Assessment", "ASSESSMENT", 30), make_task("Timed Coding Assessment #2", "Assessment", "ASSESSMENT", 30), make_task("Comprehensive Mock", "Mock Interview", "MOCK_INTERVIEW", 30), make_task("Solve 3 coding problems", "DSA", "CODING", 15, DSA_SUBTASKS), make_task("Solve 7 SQL queries", "SQL", "SQL", 15, SQL_SUBTASKS)]
        }
    },
    {
        "week_number": 12,
        "phase": "Phase 4 — Interview Mode",
        "title": "Final Polish & Interview Readiness",
        "description": "Final readiness evaluation, complete portfolio polishing, communication practice, and final mock gauntlet.",
        "targets": {"coding": 21, "sql": 12, "cs": 40, "mock": "3-4"},
        "assessments": [
            {"type": "Full", "title": "Final Readiness Assessment"}
        ],
        "mocks": [
            {"title": "Week 12 — Final Internship Simulation Gauntlet", "target_week": 12, "duration": 180, "areas": ["All"], "purpose": "Final interview readiness simulation."}
        ],
        "milestones": [
            {"title": "Final readiness completed", "target_week": 12, "description": "Complete final readiness checklist and interview preparation."}
        ],
        "days_populate": {
            1: [make_task("Python revision, C++ revision", "CS", "REVISION", 60), make_task("Solve 3 coding problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            2: [make_task("DSA revision", "DSA", "REVISION", 60), make_task("Solve 3 coding problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            3: [make_task("SQL revision, DBMS revision", "SQL", "REVISION", 60), make_task("Solve 3 coding problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            4: [make_task("OOP revision, OS revision", "CS", "REVISION", 60), make_task("Solve 3 coding problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            5: [make_task("CN revision, Architecture revision", "CS", "REVISION", 60), make_task("Solve 3 coding problems", "DSA", "CODING", 90, DSA_SUBTASKS)],
            6: [make_task("Data Science revision, ML revision", "Data Science", "REVISION", 60), make_task("Solve 3 coding problems", "DSA", "CODING", 90, DSA_SUBTASKS), make_task("Solve 6 SQL queries", "SQL", "SQL", 30, SQL_SUBTASKS)],
            7: [make_task("Project preparation, Resume, Communication/interview preparation", "Project", "PROJECT", 45), make_task("Weakness revision", "Weakness Review", "WEAKNESS_REVIEW", 30), make_task("Solve 3 coding problems", "DSA", "CODING", 15, DSA_SUBTASKS), make_task("Solve 6 SQL queries", "SQL", "SQL", 15, SQL_SUBTASKS), make_task("Multiple mock interviews, Final internship simulation", "Mock Interview", "MOCK_INTERVIEW", 45), make_task("FINAL READINESS REVIEW", "Revision", "REVISION", 30)]
        }
    }
]

curriculum = []
for w in weeks_data:
    week_id = f"week_{w['week_number']}"
    w_out = {
        "id": week_id,
        "week_number": w["week_number"],
        "phase": w["phase"],
        "title": w["title"],
        "description": w["description"],
        "targets": w["targets"],
        "assessments": w.get("assessments", []),
        "mocks": w.get("mocks", []),
        "milestones": w.get("milestones", []),
        "days": get_days(week_id, w["week_number"])
    }
    
    task_idx = 1
    for day_num in range(1, 8):
        day_tasks = w["days_populate"].get(day_num, [])
        for t in day_tasks:
            t["id"] = f"task_{w['week_number']}_{task_idx}"
            t["week_id"] = week_id
            t["day_number"] = day_num
            t["day_id"] = w_out["days"][day_num-1]["id"]
            w_out["days"][day_num-1]["tasks"].append(t)
            task_idx += 1
            
    curriculum.append(w_out)

json_str = json.dumps(curriculum, indent=4)
# Fix python boolean & None literals
python_str = json_str.replace(": false", ": False").replace(": true", ": True").replace(": null", ": None")

with open("backend/app/data/curriculum.py", "w", encoding="utf-8") as f:
    f.write('CURRICULUM_VERSION = "planner-2026-09-v2"\n\n')
    f.write('CURRICULUM = ')
    f.write(python_str)
    f.write('\n')

print("Successfully generated backend/app/data/curriculum.py")
