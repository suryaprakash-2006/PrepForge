import pytest
import uuid
from datetime import datetime, timezone, timedelta
from starlette.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def get_auth_token(client: TestClient, email: str, password: str = "password123"):
    client.post(
        "/api/v1/auth/register",
        json={"name": "Review Tester", "email": email, "password": password}
    )
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password}
    )
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    return login_res.json()["access_token"]

def test_unauthenticated_access_returns_401(client: TestClient):
    """Verify weekly review endpoints require authentication."""
    assert client.get("/api/v1/weekly-reviews/1").status_code == 401
    assert client.put("/api/v1/weekly-reviews/1", json={}).status_code == 401

def test_invalid_week_number_returns_422(client: TestClient):
    """Verify week_number constraints (1..12)."""
    user_email = f"rev_val_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    assert client.get("/api/v1/weekly-reviews/0", headers=headers).status_code == 422
    assert client.get("/api/v1/weekly-reviews/13", headers=headers).status_code == 422
    assert client.get("/api/v1/weekly-reviews/-5", headers=headers).status_code == 422
    assert client.put("/api/v1/weekly-reviews/0", headers=headers, json={}).status_code == 422
    assert client.put("/api/v1/weekly-reviews/13", headers=headers, json={}).status_code == 422

def test_get_weekly_review_default_empty_reflection(client: TestClient):
    """Verify initial GET returns clean defaults and derived structure."""
    user_email = f"rev_def_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/v1/weekly-reviews/1", headers=headers)
    assert res.status_code == 200
    data = res.json()

    assert data["week"]["week_number"] == 1
    assert data["week"]["title"] is not None
    assert data["progress"]["total_tasks"] > 0
    assert data["progress"]["completed_tasks"] == 0
    assert data["progress"]["completion_percentage"] == 0.0
    assert isinstance(data["targets"], dict)
    assert isinstance(data["categories"], list)
    assert len(data["categories"]) > 0
    assert data["weakness_summary"]["open"] == 0
    assert data["mistakes_to_review"] == []
    assert data["reflection"]["weakest_topics"] == []
    assert data["reflection"]["improved_topics"] == []
    assert data["reflection"]["carry_forward_topics"] == []
    assert data["reflection"]["next_priorities"] == []
    assert data["reflection"]["confidence"] is None
    assert data["reflection"]["motivation"] is None
    assert data["assessment_status"] == "No assessment data available yet."

def test_save_weekly_reflection_upsert(client: TestClient):
    """Verify saving/updating user reflection via PUT."""
    user_email = f"rev_save_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "weakest_topics": ["Binary Search on Answer", "Bitwise Trick 3"],
        "improved_topics": ["Sliding Window Maximum"],
        "carry_forward_topics": ["Dynamic Programming on Trees"],
        "next_priorities": ["Complete 10 LeetCode Mediums"],
        "confidence": 4,
        "motivation": 5,
        "schedule_adjustments": "Spend 30 mins more daily on SQL queries."
    }

    put_res = client.put("/api/v1/weekly-reviews/1", headers=headers, json=payload)
    assert put_res.status_code == 200
    data = put_res.json()

    assert data["reflection"]["weakest_topics"] == ["Binary Search on Answer", "Bitwise Trick 3"]
    assert data["reflection"]["improved_topics"] == ["Sliding Window Maximum"]
    assert data["reflection"]["carry_forward_topics"] == ["Dynamic Programming on Trees"]
    assert data["reflection"]["next_priorities"] == ["Complete 10 LeetCode Mediums"]
    assert data["reflection"]["confidence"] == 4
    assert data["reflection"]["motivation"] == 5
    assert data["reflection"]["schedule_adjustments"] == "Spend 30 mins more daily on SQL queries."
    assert data["reflection"]["updated_at"] is not None

    # Verify subsequent GET returns the saved reflection
    get_res = client.get("/api/v1/weekly-reviews/1", headers=headers)
    assert get_res.status_code == 200
    get_data = get_res.json()
    assert get_data["reflection"]["confidence"] == 4
    assert get_data["reflection"]["motivation"] == 5
    assert len(get_data["reflection"]["weakest_topics"]) == 2

def test_confidence_and_motivation_bounds(client: TestClient):
    """Verify validation error when rating is out of 1..5 range."""
    user_email = f"rev_bounds_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    assert client.put("/api/v1/weekly-reviews/1", headers=headers, json={"confidence": 0}).status_code == 422
    assert client.put("/api/v1/weekly-reviews/1", headers=headers, json={"confidence": 6}).status_code == 422
    assert client.put("/api/v1/weekly-reviews/1", headers=headers, json={"motivation": 0}).status_code == 422
    assert client.put("/api/v1/weekly-reviews/1", headers=headers, json={"motivation": 10}).status_code == 422

def test_extra_fields_rejected(client: TestClient):
    """Verify that attempting to pass user_id or extra fields fails with 422."""
    user_email = f"rev_extra_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "confidence": 3,
        "user_id": "malicious_user_id",
        "custom_injected_metric": 100
    }
    res = client.put("/api/v1/weekly-reviews/1", headers=headers, json=payload)
    assert res.status_code == 422

def test_user_isolation(client: TestClient):
    """Verify User A's reflection is not visible to User B."""
    user_a_email = f"rev_iso_a_{uuid.uuid4().hex[:8]}@example.com"
    user_b_email = f"rev_iso_b_{uuid.uuid4().hex[:8]}@example.com"
    token_a = get_auth_token(client, user_a_email)
    token_b = get_auth_token(client, user_b_email)

    # User A saves reflection for Week 2
    client.put(
        "/api/v1/weekly-reviews/2",
        headers={"Authorization": f"Bearer {token_a}"},
        json={"weakest_topics": ["User A Topic"], "confidence": 5}
    )

    # User B checks Week 2
    res_b = client.get(
        "/api/v1/weekly-reviews/2",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert res_b.status_code == 200
    data_b = res_b.json()
    assert data_b["reflection"]["weakest_topics"] == []
    assert data_b["reflection"]["confidence"] is None

def test_derived_metrics_and_weaknesses_integration(client: TestClient):
    """Verify task completions and weaknesses dynamically populate derived metrics in weekly review."""
    user_email = f"rev_derived_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch roadmap to get week 1 tasks
    weeks_res = client.get("/api/v1/weeks", headers=headers)
    assert weeks_res.status_code == 200
    week_1 = weeks_res.json()[0]
    task_1 = week_1["days"][0]["tasks"][0]

    # Initial review check: 0 completed
    rev_initial = client.get("/api/v1/weekly-reviews/1", headers=headers).json()
    assert rev_initial["progress"]["completed_tasks"] == 0

    # Complete task 1
    patch_res = client.patch(f"/api/v1/tasks/{task_1['id']}", headers=headers, json={"completed": True})
    assert patch_res.status_code == 200
    assert patch_res.json()["completed"] is True


    # Add a weakness
    weak_res = client.post(
        "/api/v1/weaknesses",
        headers=headers,
        json={
            "topic": "Arrays & Strings",
            "problem_concept": "Prefix Sum Bounds",
            "what_i_got_wrong": "Off-by-one in index 0",
            "correct_concept": "Allocate size n+1 for 1-based prefix sums",
            "priority": "HIGH"
        }
    )
    assert weak_res.status_code == 201

    # Check review again
    rev_after = client.get("/api/v1/weekly-reviews/1", headers=headers).json()
    assert rev_after["progress"]["completed_tasks"] == 1
    assert rev_after["progress"]["completion_percentage"] > 0
    assert rev_after["weakness_summary"]["open"] == 1
    assert rev_after["weakness_summary"]["high_priority"] == 1
    assert len(rev_after["mistakes_to_review"]) == 1
    assert rev_after["mistakes_to_review"][0]["problem_concept"] == "Prefix Sum Bounds"

def test_list_cleaning_and_trimming(client: TestClient):
    """Verify whitespace is trimmed and blank items are removed from reflection lists."""
    user_email = f"rev_clean_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "weakest_topics": ["  Trees  ", "", "   ", "Graphs"],
        "improved_topics": ["  Dynamic Programming  "],
        "carry_forward_topics": ["", "  Tries  "],
        "next_priorities": ["   Priority Queue   ", " "]
    }

    res = client.put("/api/v1/weekly-reviews/3", headers=headers, json=payload)
    assert res.status_code == 200
    ref = res.json()["reflection"]
    assert ref["weakest_topics"] == ["Trees", "Graphs"]
    assert ref["improved_topics"] == ["Dynamic Programming"]
    assert ref["carry_forward_topics"] == ["Tries"]
    assert ref["next_priorities"] == ["Priority Queue"]

def test_mistakes_to_review_cap_and_resolved_handling(client: TestClient):
    """Verify mistakes_to_review caps at 5 and excludes RESOLVED weaknesses."""
    user_email = f"rev_cap_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    # Create 6 OPEN weaknesses and 1 RESOLVED weakness
    for i in range(6):
        client.post(
            "/api/v1/weaknesses",
            headers=headers,
            json={
                "topic": f"Topic {i}",
                "problem_concept": f"Concept {i}",
                "what_i_got_wrong": f"Mistake {i}",
                "correct_concept": f"Solution {i}",
                "priority": "MEDIUM"
            }
        )

    res_w = client.post(
        "/api/v1/weaknesses",
        headers=headers,
        json={
            "topic": "Resolved Topic",
            "problem_concept": "Resolved Concept",
            "what_i_got_wrong": "Resolved Mistake",
            "correct_concept": "Resolved Solution",
            "priority": "LOW"
        }
    )
    res_w_id = res_w.json()["id"]
    client.patch(
        f"/api/v1/weaknesses/{res_w_id}",
        headers=headers,
        json={"status": "RESOLVED"}
    )

    review_res = client.get("/api/v1/weekly-reviews/1", headers=headers)
    assert review_res.status_code == 200
    data = review_res.json()
    assert data["weakness_summary"]["open"] == 6
    assert data["weakness_summary"]["resolved"] == 1
    # mistakes_to_review is capped at 5
    assert len(data["mistakes_to_review"]) == 5
    for item in data["mistakes_to_review"]:
        assert item["status"] != "RESOLVED"

