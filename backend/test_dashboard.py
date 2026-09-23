import pytest
import uuid
from starlette.testclient import TestClient
from app.main import app
from app.data.curriculum import CURRICULUM

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def get_auth_token(client: TestClient, email: str, password: str = "password123"):
    client.post(
        "/api/v1/auth/register",
        json={"name": "Test User", "email": email, "password": password}
    )
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password}
    )
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    return login_res.json()["access_token"]

def test_unauthenticated_dashboard_returns_401(client: TestClient):
    """GET /api/v1/dashboard without token must return 401 Unauthorized."""
    res = client.get("/api/v1/dashboard")
    assert res.status_code == 401

def test_new_user_dashboard_zero_progress(client: TestClient):
    """New user must have 0 completed tasks and correct total tasks."""
    user_email = f"dash_new_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}
    
    res = client.get("/api/v1/dashboard", headers=headers)
    assert res.status_code == 200
    data = res.json()
    
    # Check overall
    assert data["overall"]["total_tasks"] == 204
    assert data["overall"]["completed_tasks"] == 0
    assert data["overall"]["remaining_tasks"] == 204
    assert data["overall"]["completion_percentage"] == 0.0
    
    # Check current week (Week 1 default)
    assert data["current_week"]["week_number"] == 1
    assert data["current_week"]["completed_tasks"] == 0
    assert data["current_week"]["total_tasks"] == 17
    assert data["current_week"]["completion_percentage"] == 0.0
    
    # Check today (Day 1 default)
    assert data["today"]["day_number"] == 1
    assert data["today"]["day_name"] == "Monday"
    assert data["today"]["task_count"] == 2
    assert data["today"]["completed_tasks"] == 0
    assert data["today"]["completion_percentage"] == 0.0
    
    # Check categories
    categories = data["categories"]
    assert len(categories) > 0
    for cat in categories:
        assert cat["completed_tasks"] == 0
        assert cat["completion_percentage"] == 0.0
        assert cat["total_tasks"] > 0

def test_dashboard_updates_on_task_completion(client: TestClient):
    """Completing a task must update overall, week, day, and category progress."""
    user_email = f"dash_prog_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Complete task_1_1 (Python fundamentals: category='Python', day=1, week=1)
    patch_res = client.patch(
        "/api/v1/tasks/task_1_1",
        headers=headers,
        json={"completed": True}
    )
    assert patch_res.status_code == 200
    
    res = client.get("/api/v1/dashboard", headers=headers)
    assert res.status_code == 200
    data = res.json()
    
    # Overall updated
    assert data["overall"]["completed_tasks"] == 1
    assert data["overall"]["remaining_tasks"] == 203
    assert data["overall"]["completion_percentage"] == round((1 / 204) * 100, 1)
    
    # Week 1 updated
    assert data["current_week"]["week_number"] == 1
    assert data["current_week"]["completed_tasks"] == 1
    assert data["current_week"]["completion_percentage"] == round((1 / 17) * 100, 1)
    
    # Today (Day 1) updated
    assert data["today"]["day_number"] == 1
    assert data["today"]["completed_tasks"] == 1
    assert data["today"]["completion_percentage"] == round((1 / 2) * 100, 1)
    
    # Python category updated
    py_cat = next(c for c in data["categories"] if c["category"] == "Python")
    assert py_cat["completed_tasks"] == 1
    assert py_cat["completion_percentage"] == round((1 / py_cat["total_tasks"]) * 100, 1)

def test_dashboard_user_isolation(client: TestClient):
    """User A's task completion must not affect User B's dashboard."""
    user_a = f"dash_a_{uuid.uuid4().hex[:8]}@example.com"
    user_b = f"dash_b_{uuid.uuid4().hex[:8]}@example.com"
    
    token_a = get_auth_token(client, user_a)
    token_b = get_auth_token(client, user_b)
    
    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}
    
    # User A completes multiple tasks
    client.patch("/api/v1/tasks/task_1_1", headers=headers_a, json={"completed": True})
    client.patch("/api/v1/tasks/task_1_2", headers=headers_a, json={"completed": True})
    
    # User A sees progress
    dash_a = client.get("/api/v1/dashboard", headers=headers_a).json()
    assert dash_a["overall"]["completed_tasks"] == 2
    
    # User B sees 0 progress
    dash_b = client.get("/api/v1/dashboard", headers=headers_b).json()
    assert dash_b["overall"]["completed_tasks"] == 0
    assert dash_b["overall"]["completion_percentage"] == 0.0
    assert dash_b["current_week"]["completed_tasks"] == 0
    assert dash_b["today"]["completed_tasks"] == 0

def test_dashboard_totals_match_curriculum(client: TestClient):
    """Verify sum of category total_tasks equals overall total_tasks."""
    user_email = f"dash_totals_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}
    
    res = client.get("/api/v1/dashboard", headers=headers)
    assert res.status_code == 200
    data = res.json()
    
    curriculum_tasks = [t for w in CURRICULUM for d in w.get("days", []) for t in d.get("tasks", [])]
    assert data["overall"]["total_tasks"] == len(curriculum_tasks)
    
    category_tasks_sum = sum(c["total_tasks"] for c in data["categories"])
    assert category_tasks_sum == len(curriculum_tasks)


def test_dashboard_latest_assessment(client: TestClient):
    """Verify dashboard includes latest_assessment only when a submitted attempt exists."""
    user_email = f"dash_ass_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    # Initial: no assessment completed
    res1 = client.get("/api/v1/dashboard", headers=headers)
    assert res1.status_code == 200
    assert res1.json().get("latest_assessment") is None

    # Start and submit an assessment
    start_res = client.post("/api/v1/assessments/baseline-assessment/attempts", headers=headers)
    assert start_res.status_code == 201
    att_id = start_res.json()["attempt_id"]

    sub_res = client.post(f"/api/v1/assessment-attempts/{att_id}/submit", headers=headers)
    assert sub_res.status_code == 200

    # Dashboard now returns latest_assessment
    res2 = client.get("/api/v1/dashboard", headers=headers)
    assert res2.status_code == 200
    latest = res2.json().get("latest_assessment")
    assert latest is not None
    assert latest["assessment_id"] == "baseline-assessment"
    assert latest["attempt_id"] == att_id
    assert latest["percentage"] is not None
    assert latest["score"] is not None
    assert latest["total_marks"] == 10

