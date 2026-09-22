from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
import uuid
from fastapi import HTTPException, status
from app.db.connection import db_client
from app.schemas.assessment import (
    AssessmentResponse,
    QuestionClientResponse,
    QuestionInternal,
    AssessmentStatus
)
from app.schemas.assessment_attempt import (
    StartAttemptResponse,
    SubmitAttemptResponse,
    AttemptHistoryItem,
    AnswerRecordResponse,
    AttemptStatus
)


async def get_published_assessments() -> List[AssessmentResponse]:
    """Return all published assessments metadata."""
    db = db_client.database
    docs = await db["assessments"].find({"status": "PUBLISHED"}).to_list(length=None)
    results = []
    for d in docs:
        results.append(AssessmentResponse(
            id=d["id"],
            title=d["title"],
            description=d.get("description", ""),
            week_number=d.get("week_number"),
            assessment_type=d["assessment_type"],
            duration_minutes=d["duration_minutes"],
            question_count=d["question_count"],
            passing_score=d["passing_score"],
            status=d["status"]
        ))
    return results

async def get_assessment(assessment_id: str) -> AssessmentResponse:
    """Return single published assessment metadata. Raises 404 if not found."""
    db = db_client.database
    d = await db["assessments"].find_one({"id": assessment_id, "status": "PUBLISHED"})
    if not d:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    return AssessmentResponse(
        id=d["id"],
        title=d["title"],
        description=d.get("description", ""),
        week_number=d.get("week_number"),
        assessment_type=d["assessment_type"],
        duration_minutes=d["duration_minutes"],
        question_count=d["question_count"],
        passing_score=d["passing_score"],
        status=d["status"]
    )

async def start_assessment_attempt(user_id: str, assessment_id: str) -> StartAttemptResponse:
    """
    Start a new assessment attempt for the authenticated user.
    Returns attempt metadata and sanitized questions without correct answers.
    """
    db = db_client.database
    assessment = await db["assessments"].find_one({"id": assessment_id, "status": "PUBLISHED"})
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    # Fetch questions sorted by question_number
    q_cursor = db["assessment_questions"].find({"assessment_id": assessment_id}).sort("question_number", 1)
    q_docs = await q_cursor.to_list(length=None)

    now = datetime.now(timezone.utc)
    attempt_id = str(uuid.uuid4())

    attempt_doc = {
        "id": attempt_id,
        "user_id": user_id,
        "assessment_id": assessment_id,
        "status": AttemptStatus.IN_PROGRESS.value,
        "started_at": now,
        "submitted_at": None,
        "score": None,
        "total_marks": None,
        "percentage": None,
        "passed": None,
        "answers": [],
        "created_at": now,
        "updated_at": now
    }

    await db["assessment_attempts"].insert_one(attempt_doc)

    client_questions = [
        QuestionClientResponse(
            id=q["id"],
            assessment_id=q["assessment_id"],
            question_number=q["question_number"],
            question_type=q["question_type"],
            category=q["category"],
            topic=q["topic"],
            difficulty=q["difficulty"],
            question=q["question"],
            options=q["options"],
            marks=q.get("marks", 1)
        )
        for q in q_docs
    ]

    return StartAttemptResponse(
        attempt_id=attempt_id,
        assessment_id=assessment_id,
        status=AttemptStatus.IN_PROGRESS,
        started_at=now,
        duration_minutes=assessment["duration_minutes"],
        questions=client_questions
    )

async def record_answer(user_id: str, attempt_id: str, question_id: str, selected_answer: str) -> AnswerRecordResponse:
    """
    Store or update an answer for an active attempt.
    Verifies user ownership, attempt IN_PROGRESS status, and question membership.
    Never exposes correctness or marks.
    """
    db = db_client.database
    attempt = await db["assessment_attempts"].find_one({"id": attempt_id})
    if not attempt or attempt.get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment attempt not found"
        )

    if attempt.get("status") != AttemptStatus.IN_PROGRESS.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment attempt is already submitted and cannot be modified"
        )

    # Verify question exists and belongs to this assessment
    question = await db["assessment_questions"].find_one({
        "id": question_id,
        "assessment_id": attempt["assessment_id"]
    })
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question does not belong to this assessment"
        )

    cleaned_answer = selected_answer.strip()
    if not cleaned_answer:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="selected_answer cannot be empty"
        )

    now = datetime.now(timezone.utc)
    answers = attempt.get("answers", [])
    
    # Update existing or append new answer
    found = False
    for a in answers:
        if a["question_id"] == question_id:
            a["selected_answer"] = cleaned_answer
            a["answered_at"] = now
            found = True
            break

    if not found:
        answers.append({
            "question_id": question_id,
            "selected_answer": cleaned_answer,
            "answered_at": now
        })

    await db["assessment_attempts"].update_one(
        {"id": attempt_id},
        {"$set": {"answers": answers, "updated_at": now}}
    )

    return AnswerRecordResponse(
        status="recorded",
        question_id=question_id,
        selected_answer=cleaned_answer
    )

async def submit_attempt(user_id: str, attempt_id: str) -> SubmitAttemptResponse:
    """
    Submit an assessment attempt. Evaluates all answers, computes total marks, score,
    percentage, and pass/fail, then marks attempt as SUBMITTED and immutable.
    """
    db = db_client.database
    attempt = await db["assessment_attempts"].find_one({"id": attempt_id})
    if not attempt or attempt.get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment attempt not found"
        )

    if attempt.get("status") != AttemptStatus.IN_PROGRESS.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment attempt already submitted"
        )

    assessment = await db["assessments"].find_one({"id": attempt["assessment_id"]})
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment metadata not found"
        )

    # Fetch all questions for this assessment
    q_docs = await db["assessment_questions"].find({"assessment_id": attempt["assessment_id"]}).to_list(length=None)
    q_map = {q["id"]: q for q in q_docs}

    total_marks = sum(q.get("marks", 1) for q in q_docs)
    answers = attempt.get("answers", [])
    total_score = 0

    evaluated_answers = []
    for a in answers:
        q_id = a["question_id"]
        q = q_map.get(q_id)
        if q:
            correct_ans = q.get("correct_answer", "").strip()
            user_ans = a.get("selected_answer", "").strip()
            is_correct = (user_ans.lower() == correct_ans.lower())
            marks_awarded = q.get("marks", 1) if is_correct else 0
            if is_correct:
                total_score += marks_awarded
            evaluated_answers.append({
                "question_id": q_id,
                "selected_answer": user_ans,
                "is_correct": is_correct,
                "marks_awarded": marks_awarded,
                "answered_at": a.get("answered_at")
            })

    percentage = round((total_score / total_marks) * 100.0, 1) if total_marks > 0 else 0.0
    passing_score = assessment.get("passing_score", 60)
    passed = percentage >= passing_score

    now = datetime.now(timezone.utc)

    await db["assessment_attempts"].update_one(
        {"id": attempt_id},
        {"$set": {
            "status": AttemptStatus.SUBMITTED.value,
            "submitted_at": now,
            "score": total_score,
            "total_marks": total_marks,
            "percentage": percentage,
            "passed": passed,
            "answers": evaluated_answers,
            "updated_at": now
        }}
    )

    return SubmitAttemptResponse(
        attempt_id=attempt_id,
        status=AttemptStatus.SUBMITTED,
        score=total_score,
        total_marks=total_marks,
        percentage=percentage,
        passed=passed,
        submitted_at=now
    )

async def get_user_attempts_history(user_id: str) -> List[AttemptHistoryItem]:
    """Return attempt history only for the authenticated user."""
    db = db_client.database
    attempts = await db["assessment_attempts"].find({"user_id": user_id}).sort("started_at", -1).to_list(length=None)
    
    assessments_docs = await db["assessments"].find({}).to_list(length=None)
    assessments_map = {a["id"]: a for a in assessments_docs}

    results = []
    for att in attempts:
        ass_id = att.get("assessment_id", "")
        meta = assessments_map.get(ass_id, {})
        results.append(AttemptHistoryItem(
            attempt_id=att["id"],
            assessment_id=ass_id,
            assessment_title=meta.get("title", ass_id),
            assessment_type=meta.get("assessment_type", "QUIZ"),
            week_number=meta.get("week_number"),
            status=att.get("status", "IN_PROGRESS"),
            started_at=att["started_at"],
            submitted_at=att.get("submitted_at"),
            score=att.get("score"),
            total_marks=att.get("total_marks"),
            percentage=att.get("percentage"),
            passed=att.get("passed")
        ))

    return results
