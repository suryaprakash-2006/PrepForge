import pytest
import uuid
from starlette.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def get_auth_token(client: TestClient, email: str, password: str = "password123"):
    client.post(
        "/api/v1/auth/register",
        json={"name": "Coding Assessment Tester", "email": email, "password": password}
    )
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password}
    )
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    return login_res.json()["access_token"]


def test_unauthenticated_coding_endpoints_return_401(client: TestClient):
    """Verify all coding assessment endpoints require authentication."""
    assert client.get("/api/v1/coding-assessments").status_code == 401
    assert client.get("/api/v1/coding-assessments/attempts").status_code == 401
    assert client.get("/api/v1/coding-assessments/week-11-coding-assessment-1").status_code == 401
    assert client.post("/api/v1/coding-assessments/week-11-coding-assessment-1/attempts").status_code == 401
    assert client.get("/api/v1/coding-assessment-attempts").status_code == 401
    assert client.get("/api/v1/coding-assessment-attempts/some-id").status_code == 401
    assert client.post("/api/v1/coding-assessment-attempts/some-id/problems/two-sum-sorted/submit", json={"code": "x=1", "language": "python"}).status_code == 401
    assert client.post("/api/v1/coding-assessment-attempts/some-id/submit").status_code == 401


def test_authenticated_coding_assessments_list(client: TestClient):
    """Verify published coding assessments are listed correctly."""
    user_email = f"code_list_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/v1/coding-assessments", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    
    ids = [a["id"] for a in data]
    assert "week-11-coding-assessment-1" in ids
    assert "week-11-coding-assessment-2" in ids

    w11_1 = next(a for a in data if a["id"] == "week-11-coding-assessment-1")
    assert w11_1["week_number"] == 11
    assert w11_1["assessment_type"] == "TIMED_CODING"
    assert w11_1["duration_minutes"] == 60
    assert w11_1["problem_count"] == 3
    assert len(w11_1["problem_ids"]) == 3


def test_get_coding_assessment_detail_with_problems(client: TestClient):
    """Verify fetching coding assessment detail includes full problem descriptions and starter codes."""
    user_email = f"code_det_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/v1/coding-assessments/week-11-coding-assessment-1", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == "week-11-coding-assessment-1"
    assert len(data["problems"]) == 3

    problem_ids = [p["id"] for p in data["problems"]]
    assert problem_ids == ["two-sum-sorted", "longest-substring-distinct", "binary-tree-level-order-zigzag"]

    two_sum = data["problems"][0]
    assert two_sum["title"] == "Two Sum in a Sorted Array"
    assert two_sum["difficulty"] == "EASY"
    assert "python" in two_sum["starter_code"]
    assert "cpp" in two_sum["starter_code"]
    assert len(two_sum["examples"]) >= 2
    assert len(two_sum["constraints"]) >= 3


def test_non_existent_coding_assessment_returns_404(client: TestClient):
    """Verify fetching an invalid assessment ID returns 404."""
    user_email = f"code_404_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/v1/coding-assessments/non-existent-assessment", headers=headers)
    assert res.status_code == 404


def test_start_coding_assessment_attempt(client: TestClient):
    """Verify starting a coding assessment attempt creates an IN_PROGRESS attempt."""
    user_email = f"code_start_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    res = client.post("/api/v1/coding-assessments/week-11-coding-assessment-1/attempts", headers=headers)
    assert res.status_code == 201
    data = res.json()
    assert data["attempt_id"] is not None
    assert data["assessment_id"] == "week-11-coding-assessment-1"
    assert data["status"] == "IN_PROGRESS"
    assert data["duration_minutes"] == 60
    assert len(data["problems"]) == 3
    assert len(data["problem_states"]) == 3
    for ps in data["problem_states"]:
        assert ps["submission_status"] == "NOT_SUBMITTED"


def test_submit_problem_code_valid(client: TestClient):
    """Verify saving a problem submission updates problem state."""
    user_email = f"code_sub_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    start_res = client.post("/api/v1/coding-assessments/week-11-coding-assessment-1/attempts", headers=headers)
    assert start_res.status_code == 201
    attempt_id = start_res.json()["attempt_id"]

    # Submit solution for two-sum-sorted
    solution_code = """
def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1
    while left < right:
        s = numbers[left] + numbers[right]
        if s == target:
            return [left + 1, right + 1]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []
"""
    sub_res = client.post(
        f"/api/v1/coding-assessment-attempts/{attempt_id}/problems/two-sum-sorted/submit",
        json={"code": solution_code, "language": "python"},
        headers=headers
    )
    assert sub_res.status_code == 200
    sub_data = sub_res.json()
    assert sub_data["status"] == "saved"
    assert sub_data["problem_id"] == "two-sum-sorted"
    assert sub_data["submission_status"] == "SUBMITTED"
    assert sub_data["saved_at"] is not None

    # Check attempt state
    att_res = client.get(f"/api/v1/coding-assessment-attempts/{attempt_id}", headers=headers)
    assert att_res.status_code == 200
    states = att_res.json()["problem_states"]
    two_sum_state = next(ps for ps in states if ps["problem_id"] == "two-sum-sorted")
    assert two_sum_state["submission_status"] == "SUBMITTED"
    assert two_sum_state["language"] == "python"
    assert "two_sum_sorted" in two_sum_state["code"]


def test_submit_problem_not_in_assessment_returns_400(client: TestClient):
    """Verify submitting code for a problem not in the assessment is rejected."""
    user_email = f"code_notpart_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    start_res = client.post("/api/v1/coding-assessments/week-11-coding-assessment-1/attempts", headers=headers)
    attempt_id = start_res.json()["attempt_id"]

    # Search rotated array belongs to assessment 2, not 1
    sub_res = client.post(
        f"/api/v1/coding-assessment-attempts/{attempt_id}/problems/search-rotated-array/submit",
        json={"code": "print(1)", "language": "python"},
        headers=headers
    )
    assert sub_res.status_code == 400


def test_submit_problem_exceeding_64kb_rejected(client: TestClient):
    """Verify code payloads > 64KB are rejected."""
    user_email = f"code_size_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    start_res = client.post("/api/v1/coding-assessments/week-11-coding-assessment-1/attempts", headers=headers)
    attempt_id = start_res.json()["attempt_id"]

    large_code = "x = 1\n" * 20000  # > 100 KB
    sub_res = client.post(
        f"/api/v1/coding-assessment-attempts/{attempt_id}/problems/two-sum-sorted/submit",
        json={"code": large_code, "language": "python"},
        headers=headers
    )
    # Pydantic max_length validator triggers 422 Unprocessable Entity
    assert sub_res.status_code in [400, 422]


def test_submit_coding_attempt_finalizes_and_becomes_immutable(client: TestClient):
    """Verify finalizing an attempt marks it SUBMITTED and prevents further edits."""
    user_email = f"code_fin_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    start_res = client.post("/api/v1/coding-assessments/week-11-coding-assessment-1/attempts", headers=headers)
    attempt_id = start_res.json()["attempt_id"]

    # Save a problem
    client.post(
        f"/api/v1/coding-assessment-attempts/{attempt_id}/problems/two-sum-sorted/submit",
        json={"code": "def two_sum_sorted(): pass", "language": "python"},
        headers=headers
    )

    # Submit assessment
    submit_res = client.post(f"/api/v1/coding-assessment-attempts/{attempt_id}/submit", headers=headers)
    assert submit_res.status_code == 200
    sub_data = submit_res.json()
    assert sub_data["status"] == "SUBMITTED"
    assert sub_data["submitted_at"] is not None

    # Check attempt: scores must be None (NO CODE EXECUTION / NO FABRICATED SCORES)
    att_res = client.get(f"/api/v1/coding-assessment-attempts/{attempt_id}", headers=headers)
    assert att_res.status_code == 200
    att_data = att_res.json()
    assert att_data["status"] == "SUBMITTED"
    assert att_data["score"] is None
    assert att_data["percentage"] is None
    assert att_data["passed"] is None

    # Further edits should fail with 400
    edit_res = client.post(
        f"/api/v1/coding-assessment-attempts/{attempt_id}/problems/two-sum-sorted/submit",
        json={"code": "def changed(): pass", "language": "python"},
        headers=headers
    )
    assert edit_res.status_code == 400

    # Resubmission should fail with 400
    resub_res = client.post(f"/api/v1/coding-assessment-attempts/{attempt_id}/submit", headers=headers)
    assert resub_res.status_code == 400


def test_user_isolation_enforced(client: TestClient):
    """Verify User B cannot view or modify User A's coding attempt."""
    user_a_email = f"user_a_{uuid.uuid4().hex[:8]}@example.com"
    user_b_email = f"user_b_{uuid.uuid4().hex[:8]}@example.com"

    token_a = get_auth_token(client, user_a_email)
    token_b = get_auth_token(client, user_b_email)

    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User A starts attempt
    start_res = client.post("/api/v1/coding-assessments/week-11-coding-assessment-1/attempts", headers=headers_a)
    attempt_id = start_res.json()["attempt_id"]

    # User B attempts to access User A's attempt -> 404
    get_res = client.get(f"/api/v1/coding-assessment-attempts/{attempt_id}", headers=headers_b)
    assert get_res.status_code == 404

    # User B attempts to submit code to User A's attempt -> 404
    sub_res = client.post(
        f"/api/v1/coding-assessment-attempts/{attempt_id}/problems/two-sum-sorted/submit",
        json={"code": "hacked = True", "language": "python"},
        headers=headers_b
    )
    assert sub_res.status_code == 404

    # User B attempts to finalize User A's attempt -> 404
    fin_res = client.post(f"/api/v1/coding-assessment-attempts/{attempt_id}/submit", headers=headers_b)
    assert fin_res.status_code == 404


def test_attempt_history_and_retakes(client: TestClient):
    """Verify attempt history lists all user attempts and retakes create independent records."""
    user_email = f"code_hist_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    # First attempt
    res1 = client.post("/api/v1/coding-assessments/week-11-coding-assessment-1/attempts", headers=headers)
    att1_id = res1.json()["attempt_id"]

    # Save 1 problem and submit
    client.post(
        f"/api/v1/coding-assessment-attempts/{att1_id}/problems/two-sum-sorted/submit",
        json={"code": "pass", "language": "python"},
        headers=headers
    )
    client.post(f"/api/v1/coding-assessment-attempts/{att1_id}/submit", headers=headers)

    # Second attempt (retake)
    res2 = client.post("/api/v1/coding-assessments/week-11-coding-assessment-1/attempts", headers=headers)
    att2_id = res2.json()["attempt_id"]
    assert att2_id != att1_id

    # Check history
    hist_res = client.get("/api/v1/coding-assessment-attempts", headers=headers)
    assert hist_res.status_code == 200
    hist = hist_res.json()
    assert len(hist) >= 2
    ids = [item["attempt_id"] for item in hist]
    assert att1_id in ids
    assert att2_id in ids

    item1 = next(item for item in hist if item["attempt_id"] == att1_id)
    assert item1["status"] == "SUBMITTED"
    assert item1["problem_count"] == 3
    assert item1["submitted_problems_count"] == 1

    item2 = next(item for item in hist if item["attempt_id"] == att2_id)
    assert item2["status"] == "IN_PROGRESS"
    assert item2["submitted_problems_count"] == 0


def test_strict_no_code_execution_invariant(client: TestClient):
    """Verify arbitrary scripts are stored purely as passive strings with no side effects."""
    user_email = f"code_sec_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    start_res = client.post("/api/v1/coding-assessments/week-11-coding-assessment-2/attempts", headers=headers)
    attempt_id = start_res.json()["attempt_id"]

    dangerous_payload = """
import os, sys, subprocess
try:
    os.system("echo hacked > hack.txt")
    subprocess.run(["calc.exe"])
except:
    pass
"""
    sub_res = client.post(
        f"/api/v1/coding-assessment-attempts/{attempt_id}/problems/search-rotated-array/submit",
        json={"code": dangerous_payload, "language": "python"},
        headers=headers
    )
    assert sub_res.status_code == 200

    # Retrieve and verify exact string preserved without execution
    att_res = client.get(f"/api/v1/coding-assessment-attempts/{attempt_id}", headers=headers)
    assert att_res.status_code == 200
    states = att_res.json()["problem_states"]
    saved_state = next(ps for ps in states if ps["problem_id"] == "search-rotated-array")
    assert saved_state["code"] == dangerous_payload


def test_existing_mcq_assessments_remain_unaffected(client: TestClient):
    """Verify MCQ assessment functionality and scoring remain 100% intact."""
    user_email = f"mcq_unaff_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    # Start baseline MCQ assessment
    start_res = client.post("/api/v1/assessments/baseline-assessment/attempts", headers=headers)
    assert start_res.status_code == 201
    attempt_id = start_res.json()["attempt_id"]
    questions = start_res.json()["questions"]
    assert len(questions) == 10

    # Submit answers
    for q in questions:
        client.patch(
            f"/api/v1/assessment-attempts/{attempt_id}/answers/{q['id']}",
            json={"selected_answer": "A"},
            headers=headers
        )

    # Submit attempt and verify scoring works for MCQ
    sub_res = client.post(f"/api/v1/assessment-attempts/{attempt_id}/submit", headers=headers)
    assert sub_res.status_code == 200
    res_data = sub_res.json()
    assert res_data["status"] == "SUBMITTED"
    assert res_data["score"] is not None
    assert res_data["total_marks"] == 10
    assert res_data["percentage"] is not None
