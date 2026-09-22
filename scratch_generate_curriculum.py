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
        "targets": {"coding": 14, "sql": 12},
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
        "targets": {"coding": 14, "sql": 12},
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
        "targets": {"coding": 14, "sql": 12, "cs": 30},
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
        "targets": {"coding": 14, "sql": 12, "cs": 35},
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
        "targets": {"coding": 14, "sql": 12, "cs": 35},
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
        "targets": {"coding": 14, "sql": 12, "cs": 40},
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
        "targets": {"coding": 14, "sql": 12, "cs": 40},
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
        "targets": {"coding": 14, "sql": 15, "cs": 20},
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
        "targets": {"coding": 12, "sql": 12},
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
        "targets": {"coding": 10, "sql": 10}, # Added arbitrary for 10
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
        "targets": {"coding": 21, "sql": 15, "cs": 40},
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
        "targets": {"coding": 21, "sql": 12, "cs": 40},
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
        "targets": w["targets"],
        "days": get_days(week_id, w["week_number"])
    }
    
    # Optional fields from prompt
    # I won't explicitly add empty assessments/mocks unless needed, but schemas can handle missing.
    
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

with open("backend/app/data/curriculum.py", "w") as f:
    f.write('CURRICULUM_VERSION = "planner-2026-09-v2"\n\n')
    f.write('CURRICULUM = ')
    f.write(json.dumps(curriculum, indent=4))
    f.write('\n')
