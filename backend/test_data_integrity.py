import pytest
from app.data.curriculum import CURRICULUM

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
        assert w["id"] not in week_ids
        week_ids.add(w["id"])
        
        for d in w.get("days", []):
            assert d["id"] not in day_ids
            day_ids.add(d["id"])
            assert d["week_id"] == w["id"]
            
            for t in d.get("tasks", []):
                assert t["id"] not in task_ids
                task_ids.add(t["id"])
                assert t["week_id"] == w["id"]

def test_week_3_topics():
    w3 = next(w for w in CURRICULUM if w["week_number"] == 3)
    topics = str(w3)
    assert "Binary Search" in topics
    assert "Linked Lists" in topics
    assert "Stack" in topics
    assert "Queue" in topics
    assert "Subqueries" in topics
    assert "Correlated Queries" in topics
    assert "1NF" in topics
    assert "2NF" in topics
    assert "3NF" in topics
    assert "Transactions" in topics
    assert "ACID" in topics
    assert "OOP" in topics
    assert "Project Defence" in topics

def test_week_6_topics():
    w6 = next(w for w in CURRICULUM if w["week_number"] == 6)
    topics = str(w6)
    assert "Heap" in topics
    assert "Priority Queue" in topics
    assert "BFS" in topics
    assert "DFS" in topics
    assert "Paging" in topics
    assert "Virtual memory" in topics
    assert "Deadlocks" in topics
    assert "Synchronization" in topics

def test_week_9_topics():
    w9 = next(w for w in CURRICULUM if w["week_number"] == 9)
    topics = str(w9)
    assert "Supervised Learning" in topics
    assert "Unsupervised Learning" in topics
    assert "Regression" in topics
    assert "Classification" in topics
    assert "Decision Trees" in topics
    assert "Random Forest" in topics
    assert "KNN" in topics
    assert "Naive Bayes" in topics
    assert "Cross-validation" in topics
    assert "EDA" in topics
    assert "Outliers" in topics
    assert "Visualization" in topics
    assert "BattWin-Verify" in topics
