import pytest
import uuid
from starlette.testclient import TestClient
from app.main import app
from app.db.connection import db_client

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def get_auth_token(client: TestClient, email: str, password: str = "password123"):
    # Try registering user
    reg_res = client.post(
        "/api/v1/auth/register",
        json={"name": "Test User", "email": email, "password": password}
    )
    # Login to get JWT token
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password}
    )
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    token = login_res.json()["access_token"]
    return token

def test_task_progress_unique_compound_index(client: TestClient):
    """Verify unique compound index on (user_id, task_id) in task_progress collection."""
    import pymongo
    from app.core.config import settings
    sync_client = pymongo.MongoClient(settings.MONGODB_URL)
    db = sync_client[settings.DATABASE_NAME]
    indexes = db["task_progress"].index_information()
    found = False
    for idx_name, idx_info in indexes.items():
        key = idx_info.get("key")
        unique = idx_info.get("unique", False)
        if key == [("user_id", 1), ("task_id", 1)] and unique:
            found = True
            break
    sync_client.close()
    assert found, f"Unique compound index on (user_id, task_id) not found in {indexes}"

def test_user_isolation_and_persistence(client: TestClient):
    """
    Verify:
    1. User A completes task_1_1
    2. User B requests task_1_1 -> sees completed = False
    3. User B completes task_1_1 -> User A still True, User B True
    4. User A uncompletes task_1_1 -> User A False, User B True
    """
    user_a_email = f"user_a_{uuid.uuid4().hex[:8]}@example.com"
    user_b_email = f"user_b_{uuid.uuid4().hex[:8]}@example.com"
    
    token_a = get_auth_token(client, user_a_email)
    token_b = get_auth_token(client, user_b_email)
    
    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}
    
    # 1. User A completes task_1_1
    patch_res_a = client.patch(
        "/api/v1/tasks/task_1_1",
        headers=headers_a,
        json={"completed": True}
    )
    assert patch_res_a.status_code == 200
    data_a = patch_res_a.json()
    assert data_a["id"] == "task_1_1"
    assert data_a["completed"] is True
    assert data_a["completed_at"] is not None
    
    # 2. User B gets tasks -> task_1_1 must be False for User B
    get_res_b = client.get("/api/v1/tasks", headers=headers_b)
    assert get_res_b.status_code == 200
    task_1_1_b = next(t for t in get_res_b.json() if t["id"] == "task_1_1")
    assert task_1_1_b["completed"] is False
    assert task_1_1_b["completed_at"] is None
    
    # 3. User B completes task_1_1
    patch_res_b = client.patch(
        "/api/v1/tasks/task_1_1",
        headers=headers_b,
        json={"completed": True}
    )
    assert patch_res_b.status_code == 200
    assert patch_res_b.json()["completed"] is True
    
    # User A check -> still True
    get_res_a = client.get("/api/v1/tasks", headers=headers_a)
    task_1_1_a = next(t for t in get_res_a.json() if t["id"] == "task_1_1")
    assert task_1_1_a["completed"] is True
    
    # 4. User A uncompletes task_1_1
    unpatch_a = client.patch(
        "/api/v1/tasks/task_1_1",
        headers=headers_a,
        json={"completed": False}
    )
    assert unpatch_a.status_code == 200
    assert unpatch_a.json()["completed"] is False
    assert unpatch_a.json()["completed_at"] is None
    
    # User B check -> still True
    get_res_b2 = client.get("/api/v1/tasks", headers=headers_b)
    task_1_1_b2 = next(t for t in get_res_b2.json() if t["id"] == "task_1_1")
    assert task_1_1_b2["completed"] is True
    assert task_1_1_b2["completed_at"] is not None

def test_persistence_across_new_requests(client: TestClient):
    """Verify completed status persists across multiple subsequent GET requests."""
    user_email = f"user_p_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Initially False
    res1 = client.get("/api/v1/tasks", headers=headers)
    t = next(task for task in res1.json() if task["id"] == "task_1_2")
    assert t["completed"] is False
    
    # Set to True
    patch_res = client.patch("/api/v1/tasks/task_1_2", headers=headers, json={"completed": True})
    assert patch_res.status_code == 200
    assert patch_res.json()["completed"] is True
    completed_at = patch_res.json()["completed_at"]
    assert completed_at is not None
    
    # Fetch multiple times
    for _ in range(3):
        res = client.get("/api/v1/tasks", headers=headers)
        t = next(task for task in res.json() if task["id"] == "task_1_2")
        assert t["completed"] is True
        assert t["completed_at"] == completed_at

def test_authorization_cannot_control_user_id(client: TestClient):
    """Verify that passing user_id in TaskUpdate is rejected or has no effect on other users."""
    user_victim = f"victim_{uuid.uuid4().hex[:8]}@example.com"
    user_attacker = f"attacker_{uuid.uuid4().hex[:8]}@example.com"
    
    token_v = get_auth_token(client, user_victim)
    token_a = get_auth_token(client, user_attacker)
    
    headers_v = {"Authorization": f"Bearer {token_v}"}
    headers_a = {"Authorization": f"Bearer {token_a}"}
    
    # Attacker tries to pass another user's ID
    res = client.patch(
        "/api/v1/tasks/task_1_3",
        headers=headers_a,
        json={"completed": True, "user_id": "fake_or_other_user_id"}
    )
    # Extra field user_id should be forbidden (422) by Pydantic schema
    assert res.status_code == 422
    
    # Victim's task remains False
    res_v = client.get("/api/v1/tasks", headers=headers_v)
    t_v = next(task for task in res_v.json() if task["id"] == "task_1_3")
    assert t_v["completed"] is False

def test_invalid_task_returns_404(client: TestClient):
    """Verify PATCH /api/v1/tasks/nonexistent-task returns 404."""
    user_email = f"user_inv_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}
    
    res = client.patch(
        "/api/v1/tasks/nonexistent-task-9999",
        headers=headers,
        json={"completed": True}
    )
    assert res.status_code == 404
    assert res.json()["detail"] == "Task not found in curriculum"

def test_duplicate_progress_prevention(client: TestClient):
    """Verify repeatedly sending PATCH completed=True or toggling does not duplicate documents."""
    user_email = f"user_dup_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Repeatedly send completed=True
    client.patch("/api/v1/tasks/task_1_4", headers=headers, json={"completed": True})
    client.patch("/api/v1/tasks/task_1_4", headers=headers, json={"completed": True})
    client.patch("/api/v1/tasks/task_1_4", headers=headers, json={"completed": False})
    client.patch("/api/v1/tasks/task_1_4", headers=headers, json={"completed": True})
    
    get_res = client.get("/api/v1/tasks", headers=headers)
    t = next(task for task in get_res.json() if task["id"] == "task_1_4")
    assert t["completed"] is True
    assert t["completed_at"] is not None

    import pymongo
    from app.core.config import settings
    sync_client = pymongo.MongoClient(settings.MONGODB_URL)
    db = sync_client[settings.DATABASE_NAME]
    doc_count = db["task_progress"].count_documents({"user_id": t["user_id"], "task_id": "task_1_4"})
    sync_client.close()
    assert doc_count == 1, f"Expected exactly 1 progress document, found {doc_count}"
