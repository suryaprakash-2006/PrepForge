import pytest
from app.data.curriculum import CURRICULUM

VALID_TASK_TYPES = {
    "LEARN",
    "CONCEPT_CHECK",
    "PRACTICE",
    "CODING",
    "SQL",
    "CORE_CS",
    "PROJECT",
    "ASSESSMENT",
    "MOCK_INTERVIEW",
    "REVISION",
    "WEAKNESS_REVIEW"
}

def test_exactly_12_weeks():
    assert len(CURRICULUM) == 12

def test_exactly_7_days_per_week():
    for w in CURRICULUM:
        assert len(w.get("days", [])) == 7, f"Week {w['id']} does not have 7 days"

def test_exactly_84_day_containers():
    total_days = sum(len(w.get("days", [])) for w in CURRICULUM)
    assert total_days == 84

def test_unique_ids():
    week_ids = set()
    day_ids = set()
    task_ids = set()
    
    for w in CURRICULUM:
        assert w["id"] not in week_ids, f"Duplicate week ID: {w['id']}"
        week_ids.add(w["id"])
        
        for d in w.get("days", []):
            assert d["id"] not in day_ids, f"Duplicate day ID: {d['id']}"
            day_ids.add(d["id"])
            assert d["week_id"] == w["id"]
            
            for t in d.get("tasks", []):
                assert t["id"] not in task_ids, f"Duplicate task ID: {t['id']}"
                task_ids.add(t["id"])
                assert t["week_id"] == w["id"]
                assert t["day_id"] == d["id"]
                assert t["day_number"] == d["day_number"]

def test_daily_time_budgets_and_task_sums():
    for w in CURRICULUM:
        for d in w.get("days", []):
            expected_budget = 150 if d["day_number"] <= 5 else 180
            assert d["time_budget_minutes"] == expected_budget, (
                f"{w['id']} {d['id']} time_budget_minutes is {d['time_budget_minutes']}, expected {expected_budget}"
            )
            task_sum = sum(t.get("estimated_minutes", 0) for t in d.get("tasks", []))
            assert task_sum == expected_budget, (
                f"{w['id']} {d['id']} task sum is {task_sum}m, expected {expected_budget}m"
            )

def test_task_types_validity():
    for w in CURRICULUM:
        for d in w.get("days", []):
            for t in d.get("tasks", []):
                assert t.get("task_type") in VALID_TASK_TYPES, (
                    f"Invalid task_type '{t.get('task_type')}' in task {t['id']}"
                )
                assert t.get("category"), f"Missing category in task {t['id']}"
                assert t.get("title"), f"Missing title in task {t['id']}"

def test_subtask_structure():
    for w in CURRICULUM:
        for d in w.get("days", []):
            for t in d.get("tasks", []):
                if "subtasks" in t:
                    assert isinstance(t["subtasks"], list)
                    for st in t["subtasks"]:
                        assert "title" in st
                        assert "completed" in st
                        assert st["completed"] is False

def test_weekly_targets_metadata():
    for w in CURRICULUM:
        assert "targets" in w
        assert isinstance(w["targets"], dict)
        assert len(w["targets"]) > 0, f"Week {w['id']} missing targets metadata"

def test_week_1_topics():
    w = next(w for w in CURRICULUM if w["week_number"] == 1)
    content = str(w)
    assert "Python fundamentals" in content
    assert "C++ fundamentals" in content
    assert "C++ STL" in content
    assert "Arrays" in content
    assert "Strings" in content
    assert "Big-O" in content
    assert "Time complexity" in content
    assert "Space complexity" in content
    assert "SELECT" in content
    assert "WHERE" in content
    assert "DISTINCT" in content
    assert "ORDER BY" in content
    assert "LIMIT" in content
    assert "Resume" in content
    assert "Weakness" in content
    assert "Baseline" in content

def test_week_2_topics():
    w = next(w for w in CURRICULUM if w["week_number"] == 2)
    content = str(w)
    assert "Hashing" in content
    assert "Python dict" in content
    assert "Python set" in content
    assert "unordered_map" in content
    assert "Two Pointers" in content
    assert "Prefix Sums" in content
    assert "GROUP BY" in content
    assert "HAVING" in content
    assert "INNER JOIN" in content
    assert "LEFT JOIN" in content
    assert "RIGHT JOIN" in content
    assert "Relational model" in content
    assert "Keys" in content
    assert "Constraints" in content
    assert "Relationships" in content
    assert "Resume" in content
    assert "Weakness" in content

def test_week_3_topics():
    w = next(w for w in CURRICULUM if w["week_number"] == 3)
    content = str(w)
    assert "Sliding Window" in content
    assert "Binary Search" in content
    assert "Linked Lists" in content
    assert "Stack" in content
    assert "Queue" in content
    assert "Subqueries" in content
    assert "Correlated Queries" in content
    assert "1NF" in content
    assert "2NF" in content
    assert "3NF" in content
    assert "Transactions" in content
    assert "ACID" in content
    assert "OOP" in content
    assert "Project Defence" in content
    assert "Weekly Quiz" in content

def test_week_4_topics():
    w = next(w for w in CURRICULUM if w["week_number"] == 4)
    content = str(w)
    assert "Linked List consolidation" in content
    assert "Stack" in content
    assert "Queue" in content
    assert "CTEs" in content
    assert "Recursive CTEs" in content
    assert "Virtual functions" in content
    assert "Overloading" in content
    assert "Composition" in content
    assert "REST APIs" in content
    assert "HTTP" in content
    assert "Project" in content
    assert "Mock Interview #1" in content

def test_week_5_topics():
    w = next(w for w in CURRICULUM if w["week_number"] == 5)
    content = str(w)
    assert "Binary Trees" in content
    assert "Tree traversals" in content
    assert "BST" in content
    assert "Tree height" in content
    assert "Tree diameter" in content
    assert "LCA" in content
    assert "Window Functions" in content
    assert "ROW_NUMBER" in content
    assert "RANK" in content
    assert "DENSE_RANK" in content
    assert "LAG" in content
    assert "LEAD" in content
    assert "indexing" in content
    assert "B/B+ trees" in content
    assert "Query optimization" in content
    assert "Processes vs Threads" in content
    assert "CPU scheduling" in content
    assert "Context switching" in content

def test_week_6_topics():
    w = next(w for w in CURRICULUM if w["week_number"] == 6)
    content = str(w)
    assert "Heap" in content
    assert "Priority Queue" in content
    assert "Kth largest" in content
    assert "Median" in content
    assert "K-closest" in content
    assert "Adjacency matrix" in content
    assert "BFS" in content
    assert "DFS" in content
    assert "Complex SQL" in content
    assert "Memory hierarchy" in content
    assert "Paging" in content
    assert "Virtual memory" in content
    assert "Deadlocks" in content
    assert "Synchronization" in content
    assert "Mutex" in content
    assert "Semaphore" in content
    assert "OSI model" in content
    assert "TCP/IP" in content
    assert "TCP vs UDP" in content
    assert "Mock Interview #2" in content

def test_week_7_topics():
    w = next(w for w in CURRICULUM if w["week_number"] == 7)
    content = str(w)
    assert "Recursion" in content
    assert "Backtracking" in content
    assert "Permutations" in content
    assert "Combinations" in content
    assert "Subsets" in content
    assert "Sudoku" in content
    assert "DNS" in content
    assert "DHCP" in content
    assert "ARP" in content
    assert "Routing" in content
    assert "HTTP/HTTPS" in content
    assert "CPU" in content
    assert "ALU" in content
    assert "Control Unit" in content
    assert "Registers" in content
    assert "Pipelining" in content
    assert "RISC" in content
    assert "CISC" in content
    assert "Git" in content
    assert "GitHub" in content
    assert "Testing" in content
    assert "Debugging" in content
    assert "Project Defence" in content

def test_week_8_topics():
    w = next(w for w in CURRICULUM if w["week_number"] == 8)
    content = str(w)
    assert "Greedy" in content
    assert "Dynamic Programming introduction" in content
    assert "NumPy" in content
    assert "Pandas" in content
    assert "DataFrames" in content
    assert "Mean" in content
    assert "Median" in content
    assert "Mode" in content
    assert "Variance" in content
    assert "Standard deviation" in content
    assert "Correlation" in content
    assert "Covariance" in content
    assert "Data cleaning" in content
    assert "Missing values" in content
    assert "EDA" in content
    assert "Mixed SQL" in content

def test_week_9_topics():
    w = next(w for w in CURRICULUM if w["week_number"] == 9)
    content = str(w)
    assert "Supervised Learning" in content
    assert "Unsupervised Learning" in content
    assert "Train/Validation/Test" in content
    assert "Cross-validation" in content
    assert "Overfitting" in content
    assert "Underfitting" in content
    assert "Regression" in content
    assert "Classification" in content
    assert "Decision Trees" in content
    assert "Random Forest" in content
    assert "KNN" in content
    assert "Naive Bayes" in content
    assert "ML evaluation metrics" in content
    assert "EDA" in content
    assert "Outliers" in content
    assert "Visualization" in content
    assert "BattWin-Verify" in content

def test_week_10_topics():
    w = next(w for w in CURRICULUM if w["week_number"] == 10)
    content = str(w)
    assert "Gradient Boosting" in content
    assert "XGBoost" in content
    assert "K-Means" in content
    assert "PCA" in content
    assert "Feature Engineering" in content
    assert "Hyperparameter tuning" in content
    assert "Class imbalance" in content
    assert "Data leakage" in content
    assert "Architecture" in content
    assert "Backend" in content
    assert "SDE fundamentals" in content
    assert "System Design basics" in content
    assert "Full Integration Mock #3" in content

def test_week_11_topics():
    w = next(w for w in CURRICULUM if w["week_number"] == 11)
    content = str(w)
    assert "Mixed DSA revision" in content
    assert "Weak DSA topics" in content
    assert "SQL revision" in content
    assert "DBMS revision" in content
    assert "OOP revision" in content
    assert "OS revision" in content
    assert "CN revision" in content
    assert "Architecture revision" in content
    assert "Data Science revision" in content
    assert "ML revision" in content
    assert "Project Defence" in content
    assert "Resume revision" in content
    assert "ATS review" in content
    assert "Mistake-pattern analysis" in content
    assert "Timed Coding Assessment #1" in content
    assert "Timed Coding Assessment #2" in content
    assert "Comprehensive Mock" in content

def test_week_12_topics():
    w = next(w for w in CURRICULUM if w["week_number"] == 12)
    content = str(w)
    assert "Python revision" in content
    assert "C++ revision" in content
    assert "DSA revision" in content
    assert "SQL revision" in content
    assert "DBMS revision" in content
    assert "OOP revision" in content
    assert "OS revision" in content
    assert "CN revision" in content
    assert "Architecture revision" in content
    assert "Data Science revision" in content
    assert "ML revision" in content
    assert "Project preparation" in content
    assert "Resume" in content
    assert "Communication/interview preparation" in content
    assert "Weakness revision" in content
    assert "Final readiness" in content or "FINAL READINESS REVIEW" in content
    assert "Multiple mock interviews" in content or "Final internship simulation" in content
