import pytest
import uuid
from datetime import datetime, timezone
import concurrent.futures
import pymongo
from starlette.testclient import TestClient
from app.main import app
from app.core.config import settings
from app.schemas.coding_execution_job import JobStatus
from app.schemas.coding_execution_result import ExecutionVerdict
from app.services.coding_test_cases import CODING_TEST_CASES_SEED

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def get_auth_token(client: TestClient, email: str, password: str = "password123"):
    client.post(
        "/api/v1/auth/register",
        json={"name": "Queue Tester", "email": email, "password": password}
    )
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password}
    )
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    return login_res.json()["access_token"]


def test_unauthenticated_execution_endpoints_return_401(client: TestClient):
    """Verify all coding execution endpoints require authentication."""
    assert client.get("/api/v1/coding-execution/jobs/job-123").status_code == 401
    assert client.get("/api/v1/coding-execution/results/job-123").status_code == 401
    assert client.get("/api/v1/coding-execution/problems/two-sum-sorted/test-cases").status_code == 401


def test_submission_creates_queued_execution_job(client: TestClient):
    """
    Scenario 1 & 3:
    Submitting problem code creates a QUEUED execution job with JWT-derived user_id.
    """
    user_email = f"queue_sub_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    # Start an attempt
    start_res = client.post(
        "/api/v1/coding-assessments/week-11-coding-assessment-1/attempts",
        headers=headers
    )
    assert start_res.status_code == 201
    attempt_id = start_res.json()["attempt_id"]

    # Submit solution for two-sum-sorted
    code_payload = {
        "code": "def two_sum(nums, target):\n    return [1, 2]",
        "language": "python"
    }
    sub_res = client.post(
        f"/api/v1/coding-assessment-attempts/{attempt_id}/problems/two-sum-sorted/submit",
        json=code_payload,
        headers=headers
    )
    assert sub_res.status_code == 200
    sub_data = sub_res.json()
    assert sub_data["status"] == "QUEUED"
    assert "job_id" in sub_data
    assert sub_data["job_id"] is not None
    job_id = sub_data["job_id"]

    # Retrieve the execution job via endpoint
    job_res = client.get(f"/api/v1/coding-execution/jobs/{job_id}", headers=headers)
    assert job_res.status_code == 200
    job_data = job_res.json()
    assert job_data["id"] == job_id
    assert job_data["attempt_id"] == attempt_id
    assert job_data["problem_id"] == "two-sum-sorted"
    assert job_data["status"] == "QUEUED"
    assert job_data["started_at"] is None
    assert job_data["completed_at"] is None


def test_cross_user_execution_job_isolation(client: TestClient):
    """
    Scenario 2:
    Cross-user access to another user's execution job returns 404.
    """
    user_a = f"user_a_{uuid.uuid4().hex[:8]}@example.com"
    user_b = f"user_b_{uuid.uuid4().hex[:8]}@example.com"
    token_a = get_auth_token(client, user_a)
    token_b = get_auth_token(client, user_b)
    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User A creates attempt & submits
    start_res = client.post(
        "/api/v1/coding-assessments/week-11-coding-assessment-1/attempts",
        headers=headers_a
    )
    attempt_id = start_res.json()["attempt_id"]
    sub_res = client.post(
        f"/api/v1/coding-assessment-attempts/{attempt_id}/problems/two-sum-sorted/submit",
        json={"code": "x = 10", "language": "python"},
        headers=headers_a
    )
    job_id = sub_res.json()["job_id"]

    # User A can access
    assert client.get(f"/api/v1/coding-execution/jobs/{job_id}", headers=headers_a).status_code == 200

    # User B cannot access User A's job -> 404
    assert client.get(f"/api/v1/coding-execution/jobs/{job_id}", headers=headers_b).status_code == 404


def test_cross_user_execution_result_isolation(client: TestClient):
    """
    Scenario 10:
    Cross-user access to another user's execution result returns 404.
    """
    user_a = f"res_iso_a_{uuid.uuid4().hex[:8]}@example.com"
    user_b = f"res_iso_b_{uuid.uuid4().hex[:8]}@example.com"
    token_a = get_auth_token(client, user_a)
    token_b = get_auth_token(client, user_b)
    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User A starts and submits
    start_res = client.post(
        "/api/v1/coding-assessments/week-11-coding-assessment-1/attempts",
        headers=headers_a
    )
    attempt_id = start_res.json()["attempt_id"]
    sub_res = client.post(
        f"/api/v1/coding-assessment-attempts/{attempt_id}/problems/two-sum-sorted/submit",
        json={"code": "print('hello')", "language": "python"},
        headers=headers_a
    )
    job_id = sub_res.json()["job_id"]

    # User A queries result -> returns not-ready status
    res_a = client.get(f"/api/v1/coding-execution/results/{job_id}", headers=headers_a)
    assert res_a.status_code == 200
    assert res_a.json()["status"] == "QUEUED"

    # User B queries User A's result -> 404
    res_b = client.get(f"/api/v1/coding-execution/results/{job_id}", headers=headers_b)
    assert res_b.status_code == 404


def test_job_claim_and_completion_lifecycle(client: TestClient):
    """
    Scenario 5 & 7:
    Verify atomic state transition: QUEUED -> RUNNING -> COMPLETED and hidden test case result filtering.
    """
    user_email = f"worker_test_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    # User creates attempt and submits
    start_res = client.post("/api/v1/coding-assessments/week-11-coding-assessment-1/attempts", headers=headers)
    attempt_id = start_res.json()["attempt_id"]
    sub_res = client.post(
        f"/api/v1/coding-assessment-attempts/{attempt_id}/problems/two-sum-sorted/submit",
        json={"code": "def two_sum(): pass", "language": "python"},
        headers=headers
    )
    job_id = sub_res.json()["job_id"]

    sync_client = pymongo.MongoClient(settings.MONGODB_URL)
    db = sync_client[settings.DATABASE_NAME]

    # Verify initial status is QUEUED
    initial_job = db["coding_execution_jobs"].find_one({"id": job_id})
    assert initial_job["status"] == "QUEUED"

    # Worker claims job (QUEUED -> RUNNING)
    now = datetime.now(timezone.utc)
    claimed_job = db["coding_execution_jobs"].find_one_and_update(
        {"id": job_id, "status": "QUEUED"},
        {"$set": {"status": "RUNNING", "worker_id": "worker-node-1", "started_at": now}},
        return_document=pymongo.ReturnDocument.AFTER
    )
    assert claimed_job is not None
    assert claimed_job["status"] == "RUNNING"
    assert claimed_job["worker_id"] == "worker-node-1"

    # Worker completes job (RUNNING -> COMPLETED)
    completed_now = datetime.now(timezone.utc)
    completed_job = db["coding_execution_jobs"].find_one_and_update(
        {"id": job_id, "status": "RUNNING"},
        {"$set": {"status": "COMPLETED", "completed_at": completed_now}},
        return_document=pymongo.ReturnDocument.AFTER
    )
    assert completed_job is not None
    assert completed_job["status"] == "COMPLETED"

    # Insert execution result
    result_doc = {
        "id": str(uuid.uuid4()),
        "job_id": job_id,
        "attempt_id": attempt_id,
        "problem_id": "two-sum-sorted",
        "user_id": initial_job["user_id"],
        "verdict": ExecutionVerdict.ACCEPTED.value,
        "passed_test_cases": 4,
        "total_test_cases": 4,
        "execution_time_ms": 35,
        "memory_used_mb": 14.2,
        "compile_output": "",
        "runtime_output": "",
        "test_case_results": [
            {
                "test_case_id": "tc-two-sum-01",
                "order": 1,
                "is_hidden": False,
                "verdict": "ACCEPTED",
                "time_ms": 10,
                "memory_mb": 12.0,
                "user_output": "1 2",
                "expected_output": "1 2"
            },
            {
                "test_case_id": "tc-two-sum-03",
                "order": 3,
                "is_hidden": True,
                "verdict": "ACCEPTED",
                "time_ms": 12,
                "memory_mb": 14.2,
                "user_output": "1 2",
                "expected_output": "1 2"
            }
        ],
        "created_at": completed_now
    }
    db["coding_execution_results"].insert_one(result_doc)
    sync_client.close()

    # Retrieve execution result via API as user
    res_response = client.get(f"/api/v1/coding-execution/results/{job_id}", headers=headers)
    assert res_response.status_code == 200
    res_data = res_response.json()
    assert res_data["status"] == "COMPLETED"
    assert res_data["result"] is not None
    assert res_data["result"]["verdict"] == "ACCEPTED"
    assert res_data["result"]["passed_test_cases"] == 4

    # Security check: hidden test case must not expose user_output or expected_output
    tc_results = res_data["result"]["test_case_results"]
    assert len(tc_results) == 2
    public_tc = next(tc for tc in tc_results if not tc["is_hidden"])
    hidden_tc = next(tc for tc in tc_results if tc["is_hidden"])
    assert public_tc["expected_output"] == "1 2"
    assert public_tc["user_output"] == "1 2"
    assert hidden_tc["expected_output"] is None
    assert hidden_tc["user_output"] is None


def test_job_claim_and_failure_lifecycle(client: TestClient):
    """
    Scenario 8:
    Verify atomic state transition: QUEUED -> RUNNING -> FAILED.
    """
    user_email = f"fail_test_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    start_res = client.post("/api/v1/coding-assessments/week-11-coding-assessment-1/attempts", headers=headers)
    attempt_id = start_res.json()["attempt_id"]
    sub_res = client.post(
        f"/api/v1/coding-assessment-attempts/{attempt_id}/problems/two-sum-sorted/submit",
        json={"code": "x = 1", "language": "python"},
        headers=headers
    )
    job_id = sub_res.json()["job_id"]

    sync_client = pymongo.MongoClient(settings.MONGODB_URL)
    db = sync_client[settings.DATABASE_NAME]

    now = datetime.now(timezone.utc)
    claimed = db["coding_execution_jobs"].find_one_and_update(
        {"id": job_id, "status": "QUEUED"},
        {"$set": {"status": "RUNNING", "worker_id": "worker-err", "started_at": now}},
        return_document=pymongo.ReturnDocument.AFTER
    )
    assert claimed["status"] == "RUNNING"

    failed = db["coding_execution_jobs"].find_one_and_update(
        {"id": job_id, "status": "RUNNING"},
        {"$set": {"status": "FAILED", "error_code": "SANDBOX_OOM", "completed_at": now}},
        return_document=pymongo.ReturnDocument.AFTER
    )
    assert failed["status"] == "FAILED"
    assert failed["error_code"] == "SANDBOX_OOM"
    sync_client.close()

    # Query via API
    job_res = client.get(f"/api/v1/coding-execution/jobs/{job_id}", headers=headers)
    assert job_res.status_code == 200
    assert job_res.json()["status"] == "FAILED"
    assert job_res.json()["error_code"] == "SANDBOX_OOM"


def test_invalid_state_transitions_rejected(client: TestClient):
    """
    Scenario 9:
    Direct completion of a QUEUED job or completed job is disallowed by atomic preconditions.
    """
    sync_client = pymongo.MongoClient(settings.MONGODB_URL)
    db = sync_client[settings.DATABASE_NAME]

    job_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    db["coding_execution_jobs"].insert_one({
        "id": job_id,
        "user_id": "test-user",
        "attempt_id": "att-1",
        "problem_id": "two-sum-sorted",
        "status": "QUEUED",
        "created_at": now
    })

    # Direct complete on QUEUED job without being RUNNING must find 0 matching documents
    res_complete = db["coding_execution_jobs"].find_one_and_update(
        {"id": job_id, "status": "RUNNING"},
        {"$set": {"status": "COMPLETED", "completed_at": now}}
    )
    assert res_complete is None

    # Transition to RUNNING
    claimed = db["coding_execution_jobs"].find_one_and_update(
        {"id": job_id, "status": "QUEUED"},
        {"$set": {"status": "RUNNING", "worker_id": "w1", "started_at": now}},
        return_document=pymongo.ReturnDocument.AFTER
    )
    assert claimed is not None

    # Transition to COMPLETED
    completed = db["coding_execution_jobs"].find_one_and_update(
        {"id": job_id, "status": "RUNNING"},
        {"$set": {"status": "COMPLETED", "completed_at": now}},
        return_document=pymongo.ReturnDocument.AFTER
    )
    assert completed is not None

    # Attempting to complete again must fail (0 matching documents)
    second_complete = db["coding_execution_jobs"].find_one_and_update(
        {"id": job_id, "status": "RUNNING"},
        {"$set": {"status": "COMPLETED", "completed_at": now}}
    )
    assert second_complete is None
    sync_client.close()


def test_concurrent_worker_claim_race_condition(client: TestClient):
    """
    Scenario 6:
    When multiple workers concurrently attempt to claim a single available job, exactly one succeeds.
    """
    sync_client = pymongo.MongoClient(settings.MONGODB_URL)
    db = sync_client[settings.DATABASE_NAME]

    # Delete all queued jobs to isolate
    db["coding_execution_jobs"].delete_many({"status": "QUEUED"})

    # Insert exactly one QUEUED job
    test_job_id = f"race_job_{uuid.uuid4().hex[:8]}"
    db["coding_execution_jobs"].insert_one({
        "id": test_job_id,
        "user_id": "race-user",
        "attempt_id": "race-att",
        "problem_id": "two-sum-sorted",
        "status": "QUEUED",
        "created_at": datetime.now(timezone.utc)
    })

    def worker_claim_attempt(worker_name: str):
        c = pymongo.MongoClient(settings.MONGODB_URL)
        worker_db = c[settings.DATABASE_NAME]
        claimed = worker_db["coding_execution_jobs"].find_one_and_update(
            {"status": "QUEUED"},
            {
                "$set": {
                    "status": "RUNNING",
                    "worker_id": worker_name,
                    "started_at": datetime.now(timezone.utc)
                }
            },
            sort=[("created_at", 1)],
            return_document=pymongo.ReturnDocument.AFTER
        )
        c.close()
        return claimed

    workers = [f"worker-{i}" for i in range(5)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(worker_claim_attempt, workers))

    successful = [r for r in results if r is not None]
    failed = [r for r in results if r is None]

    assert len(successful) == 1, f"Expected exactly 1 claim, got {len(successful)}"
    assert len(failed) == 4
    assert successful[0]["id"] == test_job_id
    sync_client.close()


def test_public_test_cases_hide_expected_output_for_hidden_cases(client: TestClient):
    """
    Scenario 12:
    Public test case querying never exposes expected_output for is_hidden=True.
    """
    user_email = f"tc_tester_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/v1/coding-execution/problems/two-sum-sorted/test-cases", headers=headers)
    assert res.status_code == 200
    test_cases = res.json()
    assert len(test_cases) >= 4

    public_cases = [tc for tc in test_cases if not tc["is_hidden"]]
    hidden_cases = [tc for tc in test_cases if tc["is_hidden"]]

    assert len(public_cases) >= 1
    assert len(hidden_cases) >= 1

    # Public cases expose input and expected_output
    for tc in public_cases:
        assert tc["input"] != ""
        assert tc["expected_output"] is not None

    # Hidden cases must NEVER expose expected_output or raw input
    for tc in hidden_cases:
        assert tc["expected_output"] is None
        assert tc["input"] == ""


def test_test_cases_seeding_idempotency(client: TestClient):
    """
    Scenario 13:
    Calling seed upsert operations multiple times is idempotent and covers all 10 problems.
    """
    sync_client = pymongo.MongoClient(settings.MONGODB_URL)
    db = sync_client[settings.DATABASE_NAME]

    now = datetime.now(timezone.utc)
    for tc in CODING_TEST_CASES_SEED:
        doc = {**tc, "updated_at": now}
        db["coding_test_cases"].update_one(
            {"id": tc["id"]},
            {"$set": doc, "$setOnInsert": {"created_at": now}},
            upsert=True
        )

    count_1 = db["coding_test_cases"].count_documents({})

    for tc in CODING_TEST_CASES_SEED:
        doc = {**tc, "updated_at": now}
        db["coding_test_cases"].update_one(
            {"id": tc["id"]},
            {"$set": doc, "$setOnInsert": {"created_at": now}},
            upsert=True
        )

    count_2 = db["coding_test_cases"].count_documents({})
    assert count_1 == count_2
    assert count_1 >= 30, f"Expected at least 30 test cases across 10 problems, got {count_1}"

    distinct_problems = db["coding_test_cases"].distinct("problem_id")
    sync_client.close()
    assert len(distinct_problems) == 10
