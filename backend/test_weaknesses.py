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
        json={"name": "Test User", "email": email, "password": password}
    )
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password}
    )
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    return login_res.json()["access_token"]

def test_unauthenticated_weaknesses_access_returns_401(client: TestClient):
    """Verify all weakness endpoints require authentication."""
    assert client.get("/api/v1/weaknesses").status_code == 401
    assert client.post("/api/v1/weaknesses", json={}).status_code == 401
    assert client.get("/api/v1/weaknesses/some-id").status_code == 401
    assert client.patch("/api/v1/weaknesses/some-id", json={}).status_code == 401
    assert client.delete("/api/v1/weaknesses/some-id").status_code == 401

def test_create_and_get_weakness(client: TestClient):
    """Verify creating a weakness sets default status=OPEN and returns valid response."""
    user_email = f"weak_create_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "topic": "Dynamic Programming",
        "problem_concept": "0/1 Knapsack",
        "what_i_got_wrong": "Used greedy ratio instead of 2D DP state table",
        "correct_concept": "0/1 Knapsack has optimal substructure requiring DP state dp[i][w]",
        "priority": "HIGH"
    }
    
    res = client.post("/api/v1/weaknesses", headers=headers, json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["id"] is not None
    assert data["topic"] == "Dynamic Programming"
    assert data["problem_concept"] == "0/1 Knapsack"
    assert data["priority"] == "HIGH"
    assert data["status"] == "OPEN"
    assert data["date"] is not None
    assert data["created_at"] is not None
    
    weakness_id = data["id"]
    
    # Get by ID
    get_res = client.get(f"/api/v1/weaknesses/{weakness_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == weakness_id

def test_update_and_delete_weakness(client: TestClient):
    """Verify updating and deleting weaknesses."""
    user_email = f"weak_upd_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}
    
    create_res = client.post(
        "/api/v1/weaknesses",
        headers=headers,
        json={
            "topic": "SQL",
            "problem_concept": "Self Joins",
            "what_i_got_wrong": "Missed table alias resulting in ambiguous column error",
            "correct_concept": "Always alias both sides in a self-join",
            "priority": "MEDIUM"
        }
    )
    assert create_res.status_code == 201
    w_id = create_res.json()["id"]
    
    # Update status to REVIEWED and priority to CRITICAL
    patch_res = client.patch(
        f"/api/v1/weaknesses/{w_id}",
        headers=headers,
        json={
            "status": "REVIEWED",
            "priority": "CRITICAL"
        }
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "REVIEWED"
    assert patch_res.json()["priority"] == "CRITICAL"
    
    # Delete
    del_res = client.delete(f"/api/v1/weaknesses/{w_id}", headers=headers)
    assert del_res.status_code == 204
    
    # Verify 404 after deletion
    assert client.get(f"/api/v1/weaknesses/{w_id}", headers=headers).status_code == 404

def test_user_isolation_for_weaknesses(client: TestClient):
    """Verify User A's weakness is completely invisible and inaccessible to User B."""
    user_a = f"weak_a_{uuid.uuid4().hex[:8]}@example.com"
    user_b = f"weak_b_{uuid.uuid4().hex[:8]}@example.com"
    
    token_a = get_auth_token(client, user_a)
    token_b = get_auth_token(client, user_b)
    
    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}
    
    # User A creates a weakness
    create_res = client.post(
        "/api/v1/weaknesses",
        headers=headers_a,
        json={
            "topic": "Graphs",
            "problem_concept": "Dijkstra's Algorithm",
            "what_i_got_wrong": "Forgot to check if distance is already smaller before pushing",
            "correct_concept": "Lazy deletion / visited check in priority queue",
            "priority": "HIGH"
        }
    )
    assert create_res.status_code == 201
    w_id = create_res.json()["id"]
    
    # User B list -> must not contain User A's weakness
    list_b = client.get("/api/v1/weaknesses", headers=headers_b).json()
    assert all(item["id"] != w_id for item in list_b)
    
    # User B get by ID -> 404
    assert client.get(f"/api/v1/weaknesses/{w_id}", headers=headers_b).status_code == 404
    
    # User B update -> 404
    assert client.patch(
        f"/api/v1/weaknesses/{w_id}",
        headers=headers_b,
        json={"priority": "LOW"}
    ).status_code == 404
    
    # User B delete -> 404
    assert client.delete(f"/api/v1/weaknesses/{w_id}", headers=headers_b).status_code == 404
    
    # User A can still retrieve and delete it
    assert client.get(f"/api/v1/weaknesses/{w_id}", headers=headers_a).status_code == 200

def test_validation_errors(client: TestClient):
    """Verify validation for invalid enums and whitespace-only strings."""
    user_email = f"weak_val_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Invalid priority
    res_pri = client.post(
        "/api/v1/weaknesses",
        headers=headers,
        json={
            "topic": "OS",
            "problem_concept": "Deadlocks",
            "what_i_got_wrong": "Wrong definition",
            "correct_concept": "4 necessary conditions",
            "priority": "SUPER_HIGH"
        }
    )
    assert res_pri.status_code == 422
    
    # Invalid status
    res_sta = client.post(
        "/api/v1/weaknesses",
        headers=headers,
        json={
            "topic": "OS",
            "problem_concept": "Deadlocks",
            "what_i_got_wrong": "Wrong definition",
            "correct_concept": "4 necessary conditions",
            "priority": "HIGH",
            "status": "FINISHED"
        }
    )
    assert res_sta.status_code == 422
    
    # Whitespace-only topic
    res_ws = client.post(
        "/api/v1/weaknesses",
        headers=headers,
        json={
            "topic": "   ",
            "problem_concept": "Deadlocks",
            "what_i_got_wrong": "Wrong definition",
            "correct_concept": "4 necessary conditions",
            "priority": "HIGH"
        }
    )
    assert res_ws.status_code == 422

def test_filtering_weaknesses(client: TestClient):
    """Verify filtering by status, priority, and topic."""
    user_email = f"weak_filt_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create 3 distinct weaknesses
    client.post(
        "/api/v1/weaknesses",
        headers=headers,
        json={
            "topic": "Trees",
            "problem_concept": "LCA in BST",
            "what_i_got_wrong": "Traversed whole tree",
            "correct_concept": "Use BST property",
            "priority": "LOW",
            "status": "OPEN"
        }
    )
    client.post(
        "/api/v1/weaknesses",
        headers=headers,
        json={
            "topic": "Trees",
            "problem_concept": "Tree Diameter",
            "what_i_got_wrong": "Calculated depth only",
            "correct_concept": "Diameter is max(left_depth + right_depth)",
            "priority": "CRITICAL",
            "status": "RESOLVED"
        }
    )
    client.post(
        "/api/v1/weaknesses",
        headers=headers,
        json={
            "topic": "Networks",
            "problem_concept": "TCP 3-Way Handshake",
            "what_i_got_wrong": "Forgot SYN-ACK sequence",
            "correct_concept": "SYN -> SYN-ACK -> ACK",
            "priority": "HIGH",
            "status": "OPEN"
        }
    )
    
    # Filter by topic
    res_topic = client.get("/api/v1/weaknesses?topic=Trees", headers=headers)
    assert res_topic.status_code == 200
    assert len(res_topic.json()) == 2
    
    # Filter by status
    res_status = client.get("/api/v1/weaknesses?status=RESOLVED", headers=headers)
    assert res_status.status_code == 200
    assert len(res_status.json()) == 1
    assert res_status.json()[0]["problem_concept"] == "Tree Diameter"
    
    # Filter by priority
    res_pri = client.get("/api/v1/weaknesses?priority=CRITICAL", headers=headers)
    assert res_pri.status_code == 200
    assert len(res_pri.json()) == 1
    assert res_pri.json()[0]["topic"] == "Trees"
