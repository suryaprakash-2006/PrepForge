import pytest
import uuid
from starlette.testclient import TestClient
from app.main import app
from app.db.connection import db_client
from app.data.assessment_seed import seed_assessments

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def get_auth_token(client: TestClient, email: str, password: str = "password123"):
    client.post(
        "/api/v1/auth/register",
        json={"name": "Assessment Tester", "email": email, "password": password}
    )
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password}
    )
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    return login_res.json()["access_token"]

def test_unauthenticated_assessment_endpoints_return_401(client: TestClient):
    """Verify assessments endpoints require authentication."""
    assert client.get("/api/v1/assessments").status_code == 401
    assert client.get("/api/v1/assessments/attempts").status_code == 401
    assert client.get("/api/v1/assessments/baseline-assessment").status_code == 401
    assert client.post("/api/v1/assessments/baseline-assessment/attempts").status_code == 401
    assert client.patch("/api/v1/assessment-attempts/some-id/answers/q-id", json={"selected_answer": "A"}).status_code == 401
    assert client.post("/api/v1/assessment-attempts/some-id/submit").status_code == 401

def test_authenticated_assessment_list_works(client: TestClient):
    """Verify published assessments are listed."""
    user_email = f"ass_list_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/v1/assessments", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 5
    ids = [a["id"] for a in data]
    assert "baseline-assessment" in ids
    assert "week-3-quiz" in ids
    assert "week-5-quiz" in ids
    assert "week-7-quiz" in ids
    assert "week-9-quiz" in ids

def test_assessment_metadata_does_not_expose_answers(client: TestClient):
    """Verify assessment metadata endpoint does not contain questions or answers."""
    user_email = f"ass_meta_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/v1/assessments/baseline-assessment", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == "baseline-assessment"
    assert data["assessment_type"] == "BASELINE"
    assert data["duration_minutes"] == 30
    assert data["question_count"] == 10
    assert data["passing_score"] == 60
    assert "questions" not in data
    assert "correct_answer" not in data

def test_start_assessment_and_sanitized_questions(client: TestClient):
    """Verify starting an attempt returns attempt metadata and sanitized questions."""
    user_email = f"ass_start_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    res = client.post("/api/v1/assessments/baseline-assessment/attempts", headers=headers)
    assert res.status_code == 201
    data = res.json()
    assert data["attempt_id"] is not None
    assert data["assessment_id"] == "baseline-assessment"
    assert data["status"] == "IN_PROGRESS"
    assert data["duration_minutes"] == 30
    assert len(data["questions"]) == 10

    # Ensure no security leaks in questions
    for q in data["questions"]:
        assert "correct_answer" not in q
        assert "explanation" not in q
        assert "is_correct" not in q
        assert len(q["options"]) == 4
        assert q["marks"] == 1
        assert q["question"] is not None

def test_submit_valid_answer_does_not_leak_correctness(client: TestClient):
    """Verify answering a question records answer without returning correctness."""
    user_email = f"ass_ans_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    start_res = client.post("/api/v1/assessments/baseline-assessment/attempts", headers=headers)
    assert start_res.status_code == 201
    start_data = start_res.json()
    attempt_id = start_data["attempt_id"]
    q1 = start_data["questions"][0]

    ans_res = client.patch(
        f"/api/v1/assessment-attempts/{attempt_id}/answers/{q1['id']}",
        headers=headers,
        json={"selected_answer": q1["options"][0]}
    )
    assert ans_res.status_code == 200
    ans_data = ans_res.json()
    assert ans_data["status"] == "recorded"
    assert ans_data["question_id"] == q1["id"]
    assert ans_data["selected_answer"] == q1["options"][0]
    assert "is_correct" not in ans_data
    assert "score" not in ans_data

def test_cannot_answer_with_extra_fields(client: TestClient):
    """Verify extra payload fields on answer submission are rejected."""
    user_email = f"ass_extra_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    start_res = client.post("/api/v1/assessments/baseline-assessment/attempts", headers=headers)
    attempt_id = start_res.json()["attempt_id"]
    q1 = start_res.json()["questions"][0]

    res = client.patch(
        f"/api/v1/assessment-attempts/{attempt_id}/answers/{q1['id']}",
        headers=headers,
        json={"selected_answer": "A", "is_correct": True, "marks": 100}
    )
    assert res.status_code == 422

def test_scoring_and_pass_fail_calculation(client: TestClient):
    """Verify submit calculates score, percentage, and pass/fail accurately."""
    user_email = f"ass_score_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    # Start Week 3 Quiz
    start_res = client.post("/api/v1/assessments/week-3-quiz/attempts", headers=headers)
    assert start_res.status_code == 201
    start_data = start_res.json()
    attempt_id = start_data["attempt_id"]
    questions = start_data["questions"]

    correct_map = {
        "w3-q1": "O(N)",
        "w3-q2": "mid = low + (high - low) / 2",
        "w3-q3": "O(1)",
        "w3-q4": "next_node = curr.next; curr.next = prev; prev = curr; curr = next_node",
        "w3-q5": "Stack",
        "w3-q6": "O(N)",
        "w3-q7": "O(1)",
        "w3-q8": "A correlated subquery references columns from the outer query and re-evaluates for each candidate row",
        "w3-q9": "Every non-prime attribute is fully functionally dependent on the entire primary key (no partial dependencies)",
        "w3-q10": "All operations within a transaction execute completely or none are applied (all-or-nothing)"
    }

    # Answer 7 correctly and 3 incorrectly (70% score -> Passed >= 60%)
    for i, q in enumerate(questions):
        q_id = q["id"]
        if i < 7:
            ans = correct_map[q_id]
        else:
            ans = "WRONG_ANSWER"
        res = client.patch(
            f"/api/v1/assessment-attempts/{attempt_id}/answers/{q_id}",
            headers=headers,
            json={"selected_answer": ans}
        )
        assert res.status_code == 200

    # Submit attempt
    submit_res = client.post(f"/api/v1/assessment-attempts/{attempt_id}/submit", headers=headers)
    assert submit_res.status_code == 200
    result = submit_res.json()
    assert result["attempt_id"] == attempt_id
    assert result["status"] == "SUBMITTED"
    assert result["score"] == 7
    assert result["total_marks"] == 10
    assert result["percentage"] == 70.0
    assert result["passed"] is True

def test_failing_score_sets_passed_false(client: TestClient):
    """Verify scoring below passing score sets passed=False."""
    user_email = f"ass_fail_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    start_res = client.post("/api/v1/assessments/week-5-quiz/attempts", headers=headers)
    attempt_id = start_res.json()["attempt_id"]
    q1 = start_res.json()["questions"][0]

    # Answer only 1 question correctly (10% score -> Failed < 60%)
    client.patch(
        f"/api/v1/assessment-attempts/{attempt_id}/answers/{q1['id']}",
        headers=headers,
        json={"selected_answer": "Inorder Traversal"} # w5-q1 BST inorder traversal is sorted
    )

    submit_res = client.post(f"/api/v1/assessment-attempts/{attempt_id}/submit", headers=headers)
    assert submit_res.status_code == 200
    result = submit_res.json()
    assert result["score"] == 1
    assert result["percentage"] == 10.0
    assert result["passed"] is False

def test_attempt_immutability_after_submission(client: TestClient):
    """Verify answers cannot be changed and submit cannot be re-run after submission."""
    user_email = f"ass_imm_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    start_res = client.post("/api/v1/assessments/week-7-quiz/attempts", headers=headers)
    attempt_id = start_res.json()["attempt_id"]
    q1 = start_res.json()["questions"][0]

    # Submit
    sub1 = client.post(f"/api/v1/assessment-attempts/{attempt_id}/submit", headers=headers)
    assert sub1.status_code == 200

    # Attempt to answer after submit -> 400
    ans_res = client.patch(
        f"/api/v1/assessment-attempts/{attempt_id}/answers/{q1['id']}",
        headers=headers,
        json={"selected_answer": "Missing or unreachable base case causing infinite call frame allocations on the execution stack"}
    )
    assert ans_res.status_code == 400

    # Attempt to submit again -> 400
    sub2 = client.post(f"/api/v1/assessment-attempts/{attempt_id}/submit", headers=headers)
    assert sub2.status_code == 400

def test_user_isolation(client: TestClient):
    """Verify User A cannot access, answer, or submit User B's attempt (returns 404)."""
    user_a = f"ass_iso_a_{uuid.uuid4().hex[:8]}@example.com"

    user_b = f"ass_iso_b_{uuid.uuid4().hex[:8]}@example.com"
    token_a = get_auth_token(client, user_a)
    token_b = get_auth_token(client, user_b)

    # User A starts an attempt
    start_a = client.post(
        "/api/v1/assessments/week-9-quiz/attempts",
        headers={"Authorization": f"Bearer {token_a}"}
    )
    attempt_a_id = start_a.json()["attempt_id"]
    q1 = start_a.json()["questions"][0]

    # User B tries to answer User A's attempt -> 404
    ans_b = client.patch(
        f"/api/v1/assessment-attempts/{attempt_a_id}/answers/{q1['id']}",
        headers={"Authorization": f"Bearer {token_b}"},
        json={"selected_answer": "O(V + E)"}
    )
    assert ans_b.status_code == 404

    # User B tries to submit User A's attempt -> 404
    sub_b = client.post(
        f"/api/v1/assessment-attempts/{attempt_a_id}/submit",
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert sub_b.status_code == 404

def test_invalid_assessment_id_returns_404(client: TestClient):
    """Verify 404 for non-existent assessment."""
    user_email = f"ass_inv_a_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    assert client.get("/api/v1/assessments/non-existent-id", headers=headers).status_code == 404
    assert client.post("/api/v1/assessments/non-existent-id/attempts", headers=headers).status_code == 404

def test_invalid_question_id_returns_400(client: TestClient):
    """Verify answering non-existent question returns 400."""
    user_email = f"ass_inv_q_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    start_res = client.post("/api/v1/assessments/baseline-assessment/attempts", headers=headers)
    attempt_id = start_res.json()["attempt_id"]

    res = client.patch(
        f"/api/v1/assessment-attempts/{attempt_id}/answers/fake-q-id",
        headers=headers,
        json={"selected_answer": "A"}
    )
    assert res.status_code == 400

def test_cannot_answer_question_from_another_assessment(client: TestClient):
    """Verify question belonging to Week 5 Quiz cannot be answered in Baseline Assessment attempt."""
    user_email = f"ass_cross_q_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    start_base = client.post("/api/v1/assessments/baseline-assessment/attempts", headers=headers)
    attempt_id = start_base.json()["attempt_id"]

    # w5-q1 belongs to week-5-quiz, not baseline-assessment
    res = client.patch(
        f"/api/v1/assessment-attempts/{attempt_id}/answers/w5-q1",
        headers=headers,
        json={"selected_answer": "O(1)"}
    )
    assert res.status_code == 400

def test_multiple_independent_attempts(client: TestClient):
    """Verify user can take multiple independent attempts of the same assessment."""
    user_email = f"ass_multi_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    att1 = client.post("/api/v1/assessments/week-3-quiz/attempts", headers=headers).json()
    att2 = client.post("/api/v1/assessments/week-3-quiz/attempts", headers=headers).json()

    assert att1["attempt_id"] != att2["attempt_id"]

    # Submit attempt 1 with 0 score
    client.post(f"/api/v1/assessment-attempts/{att1['attempt_id']}/submit", headers=headers)

    # Attempt 2 is still IN_PROGRESS and can be answered
    q1 = att2["questions"][0]
    ans_res = client.patch(
        f"/api/v1/assessment-attempts/{att2['attempt_id']}/answers/{q1['id']}",
        headers=headers,
        json={"selected_answer": "O(N)"}
    )
    assert ans_res.status_code == 200

def test_user_attempt_history(client: TestClient):
    """Verify history lists user's attempts in order."""
    user_email = f"ass_hist_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    # Start 2 attempts
    client.post("/api/v1/assessments/baseline-assessment/attempts", headers=headers)
    att2 = client.post("/api/v1/assessments/week-3-quiz/attempts", headers=headers).json()
    client.post(f"/api/v1/assessment-attempts/{att2['attempt_id']}/submit", headers=headers)

    hist_res = client.get("/api/v1/assessments/attempts", headers=headers)
    assert hist_res.status_code == 200
    history = hist_res.json()
    assert len(history) == 2
    assert history[0]["assessment_title"] is not None
    assert history[0]["status"] in ["IN_PROGRESS", "SUBMITTED"]

def test_question_count_matches_assessment_definition(client: TestClient):
    """Verify each seeded assessment has exactly 10 questions."""
    user_email = f"ass_cnt_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    assessments = ["baseline-assessment", "week-3-quiz", "week-5-quiz", "week-7-quiz", "week-9-quiz"]
    for ass_id in assessments:
        res = client.post(f"/api/v1/assessments/{ass_id}/attempts", headers=headers)
        assert res.status_code == 201
        assert len(res.json()["questions"]) == 10

def test_idempotent_seed_does_not_create_duplicates(client: TestClient):
    """Verify calling seed upsert operations multiple times maintains exact document counts."""
    from datetime import datetime, timezone
    from app.core.config import settings
    from app.data.assessment_seed import ASSESSMENTS_SEED, QUESTIONS_SEED
    import pymongo

    sync_client = pymongo.MongoClient(settings.MONGODB_URL)
    db = sync_client[settings.DATABASE_NAME]

    now = datetime.now(timezone.utc)
    for a in ASSESSMENTS_SEED:
        doc = {**a, "updated_at": now}
        db["assessments"].update_one(
            {"id": a["id"]},
            {"$set": doc, "$setOnInsert": {"created_at": now}},
            upsert=True
        )

    for q in QUESTIONS_SEED:
        doc = {**q, "updated_at": now}
        db["assessment_questions"].update_one(
            {"id": q["id"]},
            {"$set": doc, "$setOnInsert": {"created_at": now}},
            upsert=True
        )

    ass_count = db["assessments"].count_documents({})
    q_count = db["assessment_questions"].count_documents({})
    sync_client.close()

    assert ass_count == 5, f"Expected 5 assessments, got {ass_count}"
    assert q_count == 50, f"Expected 50 questions, got {q_count}"

def test_unanswered_questions_score_zero_and_answer_replacement(client: TestClient):
    """Verify that unanswered questions award 0 marks and updating an answer before submission replaces the prior value."""
    user_email = f"ass_unans_{uuid.uuid4().hex[:8]}@example.com"
    token = get_auth_token(client, user_email)
    headers = {"Authorization": f"Bearer {token}"}

    start_res = client.post("/api/v1/assessments/baseline-assessment/attempts", headers=headers)
    assert start_res.status_code == 201
    data = start_res.json()
    attempt_id = data["attempt_id"]
    q1 = data["questions"][0]

    # First, select wrong answer
    res1 = client.patch(
        f"/api/v1/assessment-attempts/{attempt_id}/answers/{q1['id']}",
        headers=headers,
        json={"selected_answer": "O(1)"}
    )
    assert res1.status_code == 200

    # Then change mind and select correct answer
    res2 = client.patch(
        f"/api/v1/assessment-attempts/{attempt_id}/answers/{q1['id']}",
        headers=headers,
        json={"selected_answer": "  O(N)  "}  # with extra whitespace
    )
    assert res2.status_code == 200

    # Submit without answering the remaining 9 questions
    submit_res = client.post(f"/api/v1/assessment-attempts/{attempt_id}/submit", headers=headers)
    assert submit_res.status_code == 200
    res_data = submit_res.json()
    assert res_data["score"] == 1
    assert res_data["total_marks"] == 10
    assert res_data["percentage"] == 10.0
    assert res_data["passed"] is False

def test_content_invariants_and_single_matching_correct_answers():
    """Verify all 50 questions have exactly one valid option matching correct_answer, 4 options, marks=1, and explanation."""
    from app.data.assessment_seed import ASSESSMENTS_SEED, QUESTIONS_SEED

    assert len(ASSESSMENTS_SEED) == 5
    assert len(QUESTIONS_SEED) == 50

    assessment_ids = {a["id"] for a in ASSESSMENTS_SEED}
    assert assessment_ids == {"baseline-assessment", "week-3-quiz", "week-5-quiz", "week-7-quiz", "week-9-quiz"}

    for a in ASSESSMENTS_SEED:
        assert a["question_count"] == 10
        assert a["duration_minutes"] == 30
        assert a["passing_score"] == 60
        assert a["status"] == "PUBLISHED"

    # Verify each question
    questions_per_assessment = {}
    seen_q_numbers = {}

    for q in QUESTIONS_SEED:
        ass_id = q["assessment_id"]
        assert ass_id in assessment_ids
        questions_per_assessment[ass_id] = questions_per_assessment.get(ass_id, 0) + 1

        # Check unique question numbers
        q_num = q["question_number"]
        if ass_id not in seen_q_numbers:
            seen_q_numbers[ass_id] = set()
        assert q_num not in seen_q_numbers[ass_id], f"Duplicate question number {q_num} in {ass_id}"
        seen_q_numbers[ass_id].add(q_num)

        # Options check
        options = q["options"]
        assert len(options) == 4, f"Question {q['id']} does not have 4 options"
        assert len(set(options)) == 4, f"Question {q['id']} has duplicate options"

        # Correct answer check
        correct = q["correct_answer"]
        assert correct in options, f"Question {q['id']} correct_answer '{correct}' not found in options {options}"
        matches = [opt for opt in options if opt == correct]
        assert len(matches) == 1, f"Question {q['id']} has multiple matches for correct_answer"

        # Metadata checks
        assert q["marks"] == 1
        assert len(q["explanation"].strip()) > 10
        assert len(q["question"].strip()) > 10
        assert q["question_type"] == "MCQ"
        assert q["difficulty"] in ["EASY", "MEDIUM", "HARD"]

    for ass_id in assessment_ids:
        assert questions_per_assessment[ass_id] == 10
        assert seen_q_numbers[ass_id] == set(range(1, 11))




