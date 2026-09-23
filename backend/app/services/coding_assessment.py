"""
PrepForge — Timed Coding Assessment Service

Business logic for:
- Fetching published coding assessments and problem statements
- Starting user-scoped coding attempts
- Saving individual problem submissions (plain text, max 64KB)
- Submitting coding attempts (immutable once submitted)
- User isolation and attempt history

NO CODE EXECUTION: Code is stored strictly as untrusted plain text without eval, exec, subprocess, Docker, or external judge APIs.
"""

from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
import uuid
from fastapi import HTTPException, status
from app.db.connection import db_client
from app.schemas.coding_problem import (
    CodingProblemResponse,
    CodingExample,
    CodingDifficulty,
    CodingStatus
)
from app.schemas.coding_assessment import (
    CodingAssessmentResponse,
    CodingAssessmentDetailResponse
)
from app.schemas.coding_attempt import (
    CodingAttemptStatus,
    CodingSubmissionStatus,
    ProblemSubmissionRequest,
    ProblemSubmissionResponse,
    CodingProblemState,
    StartCodingAttemptResponse,
    SubmitCodingAttemptResponse,
    CodingAttemptResponse,
    CodingAttemptHistoryItem
)


async def get_published_coding_assessments() -> List[CodingAssessmentResponse]:
    """Return all published coding assessments."""
    db = db_client.database
    docs = await db["coding_assessments"].find({"status": "PUBLISHED"}).sort("week_number", 1).to_list(length=None)
    results = []
    for d in docs:
        results.append(CodingAssessmentResponse(
            id=d["id"],
            title=d["title"],
            description=d.get("description", ""),
            week_number=d.get("week_number"),
            assessment_type=d.get("assessment_type", "TIMED_CODING"),
            duration_minutes=d["duration_minutes"],
            problem_count=d.get("problem_count", len(d.get("problem_ids", []))),
            passing_score=d.get("passing_score", 60),
            status=d["status"],
            problem_ids=d.get("problem_ids", [])
        ))
    return results


async def get_coding_assessment_detail(assessment_id: str) -> CodingAssessmentDetailResponse:
    """Return a single coding assessment with full problem definitions."""
    db = db_client.database
    assessment = await db["coding_assessments"].find_one({"id": assessment_id, "status": "PUBLISHED"})
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding assessment not found"
        )

    problem_ids = assessment.get("problem_ids", [])
    problems_cursor = db["coding_problems"].find({"id": {"$in": problem_ids}, "status": "PUBLISHED"})
    problem_docs = await problems_cursor.to_list(length=None)
    
    # Map by ID to maintain order of problem_ids in the assessment
    problems_by_id = {p["id"]: p for p in problem_docs}
    
    problems_list: List[CodingProblemResponse] = []
    for pid in problem_ids:
        p = problems_by_id.get(pid)
        if p:
            examples = [
                CodingExample(
                    input=ex.get("input", ""),
                    output=ex.get("output", ""),
                    explanation=ex.get("explanation", "")
                )
                for ex in p.get("examples", [])
            ]
            problems_list.append(CodingProblemResponse(
                id=p["id"],
                title=p["title"],
                slug=p.get("slug", p["id"]),
                description=p.get("description", ""),
                category=p.get("category", "DSA"),
                topic=p.get("topic", "General"),
                difficulty=CodingDifficulty(p.get("difficulty", "MEDIUM")),
                constraints=p.get("constraints", []),
                input_format=p.get("input_format", ""),
                output_format=p.get("output_format", ""),
                examples=examples,
                starter_code=p.get("starter_code", {}),
                expected_language=p.get("expected_language", ["python", "cpp"]),
                tags=p.get("tags", []),
                marks=p.get("marks", 10),
                status=CodingStatus(p.get("status", "PUBLISHED"))
            ))

    return CodingAssessmentDetailResponse(
        id=assessment["id"],
        title=assessment["title"],
        description=assessment.get("description", ""),
        week_number=assessment.get("week_number"),
        assessment_type=assessment.get("assessment_type", "TIMED_CODING"),
        duration_minutes=assessment["duration_minutes"],
        problem_count=len(problems_list),
        passing_score=assessment.get("passing_score", 60),
        status=assessment["status"],
        problem_ids=problem_ids,
        problems=problems_list
    )


async def start_coding_attempt(user_id: str, assessment_id: str) -> StartCodingAttemptResponse:
    """
    Start a new coding assessment attempt for the user.
    Loads the assessment problems and creates an IN_PROGRESS attempt record.
    """
    db = db_client.database
    assessment_detail = await get_coding_assessment_detail(assessment_id)

    now = datetime.now(timezone.utc)
    attempt_id = str(uuid.uuid4())

    initial_problem_states = [
        {
            "problem_id": p.id,
            "code": p.starter_code.get("python", ""),
            "language": "python",
            "submission_status": CodingSubmissionStatus.NOT_SUBMITTED.value,
            "saved_at": None
        }
        for p in assessment_detail.problems
    ]

    attempt_doc = {
        "id": attempt_id,
        "user_id": user_id,
        "assessment_id": assessment_id,
        "assessment_title": assessment_detail.title,
        "status": CodingAttemptStatus.IN_PROGRESS.value,
        "started_at": now,
        "duration_minutes": assessment_detail.duration_minutes,
        "submitted_at": None,
        "problem_states": initial_problem_states,
        "score": None,
        "total_marks": None,
        "percentage": None,
        "passed": None
    }

    await db["coding_assessment_attempts"].insert_one(attempt_doc)

    return StartCodingAttemptResponse(
        attempt_id=attempt_id,
        assessment_id=assessment_id,
        status=CodingAttemptStatus.IN_PROGRESS.value,
        started_at=now,
        duration_minutes=assessment_detail.duration_minutes,
        problems=assessment_detail.problems,
        problem_states=[
            CodingProblemState(
                problem_id=ps["problem_id"],
                code=ps["code"],
                language=ps["language"],
                submission_status=CodingSubmissionStatus(ps["submission_status"]),
                saved_at=ps["saved_at"]
            )
            for ps in initial_problem_states
        ]
    )


async def get_user_coding_attempts(user_id: str) -> List[CodingAttemptHistoryItem]:
    """Return attempt history for the authenticated user, ordered by started_at desc."""
    db = db_client.database
    cursor = db["coding_assessment_attempts"].find({"user_id": user_id}).sort("started_at", -1)
    docs = await cursor.to_list(length=None)

    # Fetch assessment details to populate week_number if needed
    assessments_cursor = db["coding_assessments"].find({})
    assessments_list = await assessments_cursor.to_list(length=None)
    assessments_map = {a["id"]: a for a in assessments_list}

    history: List[CodingAttemptHistoryItem] = []
    for d in docs:
        assessment_info = assessments_map.get(d.get("assessment_id"), {})
        problem_states = d.get("problem_states", [])
        submitted_count = sum(
            1 for ps in problem_states
            if ps.get("submission_status") == CodingSubmissionStatus.SUBMITTED.value
        )

        history.append(CodingAttemptHistoryItem(
            attempt_id=d["id"],
            assessment_id=d["assessment_id"],
            assessment_title=d.get("assessment_title") or assessment_info.get("title", "Coding Assessment"),
            week_number=assessment_info.get("week_number"),
            status=d["status"],
            started_at=d["started_at"],
            duration_minutes=d.get("duration_minutes", assessment_info.get("duration_minutes", 60)),
            submitted_at=d.get("submitted_at"),
            problem_count=len(problem_states),
            submitted_problems_count=submitted_count,
            score=d.get("score"),
            percentage=d.get("percentage"),
            passed=d.get("passed")
        ))
    return history


async def get_coding_attempt(user_id: str, attempt_id: str) -> CodingAttemptResponse:
    """
    Return a single coding assessment attempt.
    Enforces user isolation: returns 404 if attempt doesn't belong to the user.
    """
    db = db_client.database
    attempt = await db["coding_assessment_attempts"].find_one({"id": attempt_id, "user_id": user_id})
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding assessment attempt not found"
        )

    problem_states = [
        CodingProblemState(
            problem_id=ps["problem_id"],
            code=ps.get("code", ""),
            language=ps.get("language", "python"),
            submission_status=CodingSubmissionStatus(ps.get("submission_status", "NOT_SUBMITTED")),
            saved_at=ps.get("saved_at")
        )
        for ps in attempt.get("problem_states", [])
    ]

    return CodingAttemptResponse(
        attempt_id=attempt["id"],
        assessment_id=attempt["assessment_id"],
        assessment_title=attempt.get("assessment_title", "Coding Assessment"),
        status=attempt["status"],
        started_at=attempt["started_at"],
        duration_minutes=attempt.get("duration_minutes", 60),
        submitted_at=attempt.get("submitted_at"),
        problem_states=problem_states,
        score=attempt.get("score"),
        total_marks=attempt.get("total_marks"),
        percentage=attempt.get("percentage"),
        passed=attempt.get("passed")
    )


async def save_problem_submission(
    user_id: str,
    attempt_id: str,
    problem_id: str,
    request: ProblemSubmissionRequest
) -> ProblemSubmissionResponse:
    """
    Save or update code submission for a single problem in an IN_PROGRESS attempt.
    Enforces:
    - User ownership (404 if mismatch or not found)
    - Attempt status == IN_PROGRESS (400 if already submitted)
    - Problem belongs to assessment (400 if not part of attempt)
    - Code payload <= 64KB (enforced by Pydantic and double-checked here)
    """
    db = db_client.database
    attempt = await db["coding_assessment_attempts"].find_one({"id": attempt_id, "user_id": user_id})
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding assessment attempt not found"
        )

    if attempt.get("status") != CodingAttemptStatus.IN_PROGRESS.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify a submitted assessment attempt. Submissions are immutable."
        )

    problem_states = attempt.get("problem_states", [])
    matching_state = next((ps for ps in problem_states if ps.get("problem_id") == problem_id), None)
    if not matching_state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Problem '{problem_id}' is not part of this coding assessment attempt"
        )

    # Validate size in bytes as well
    if len(request.code.encode("utf-8")) > 65536:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Code payload exceeds maximum allowed size of 64KB"
        )

    now = datetime.now(timezone.utc)
    submission_id = str(uuid.uuid4())

    # Update problem_state in database
    await db["coding_assessment_attempts"].update_one(
        {"id": attempt_id, "user_id": user_id, "status": CodingAttemptStatus.IN_PROGRESS.value},
        {
            "$set": {
                "problem_states.$[elem].code": request.code,
                "problem_states.$[elem].language": request.language,
                "problem_states.$[elem].submission_status": CodingSubmissionStatus.SUBMITTED.value,
                "problem_states.$[elem].saved_at": now
            }
        },
        array_filters=[{"elem.problem_id": problem_id}]
    )

    # Create asynchronous execution job (QUEUED)
    from app.services.coding_execution import create_execution_job
    job = await create_execution_job(
        user_id=user_id,
        attempt_id=attempt_id,
        problem_id=problem_id,
        source_submission_id=submission_id
    )

    return ProblemSubmissionResponse(
        status="QUEUED",
        submission_id=submission_id,
        job_id=job.id,
        problem_id=problem_id,
        language=request.language,
        submission_status=CodingSubmissionStatus.SUBMITTED,
        saved_at=now
    )


async def submit_coding_attempt(user_id: str, attempt_id: str) -> SubmitCodingAttemptResponse:
    """
    Finalize and submit a coding assessment attempt.
    Once submitted, attempt becomes immutable.
    NO CODE EXECUTION: Scores, percentages, and pass/fail remain None.
    """
    db = db_client.database
    attempt = await db["coding_assessment_attempts"].find_one({"id": attempt_id, "user_id": user_id})
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding assessment attempt not found"
        )

    if attempt.get("status") == CodingAttemptStatus.SUBMITTED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coding assessment attempt has already been submitted"
        )

    now = datetime.now(timezone.utc)

    await db["coding_assessment_attempts"].update_one(
        {"id": attempt_id, "user_id": user_id},
        {
            "$set": {
                "status": CodingAttemptStatus.SUBMITTED.value,
                "submitted_at": now
            }
        }
    )

    return SubmitCodingAttemptResponse(
        attempt_id=attempt_id,
        assessment_id=attempt["assessment_id"],
        status=CodingAttemptStatus.SUBMITTED.value,
        submitted_at=now,
        message="Coding assessment submitted. Submissions stored for future evaluation."
    )
