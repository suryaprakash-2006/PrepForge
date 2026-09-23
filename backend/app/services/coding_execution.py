"""
PrepForge — Coding Execution Job Queue Service

Manages the asynchronous lifecycle for code execution jobs:
- Validates attempt ownership, problem assignment, and active status
- Enqueues jobs in MongoDB with status QUEUED
- Provides atomic claim semantics (QUEUED -> RUNNING) for future worker daemons
- Enforces strict state transitions (QUEUED -> RUNNING -> COMPLETED / FAILED)
- Enforces user isolation on job and result retrieval

NO CODE EXECUTION: This service creates and transitions job state only.
"""

from datetime import datetime, timezone
from typing import Optional, Dict, Any
import uuid
from pymongo import ReturnDocument
from fastapi import HTTPException, status
from app.db.connection import db_client
from app.schemas.coding_execution_job import (
    JobStatus,
    CodingExecutionJobResponse,
    JobStatusResponse
)
from app.schemas.coding_execution_result import (
    ExecutionVerdict,
    CodingExecutionResultResponse,
    ExecutionResultStatusResponse,
    TestCaseResultItem
)
from app.schemas.coding_attempt import CodingAttemptStatus


async def create_execution_job(
    user_id: str,
    attempt_id: str,
    problem_id: str,
    source_submission_id: Optional[str] = None
) -> CodingExecutionJobResponse:
    """
    Create a new QUEUED execution job for a problem submission.
    Verifications:
    1. Authenticated user owns the coding attempt.
    2. Attempt exists and status is IN_PROGRESS.
    3. Problem belongs to the relevant assessment.
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
            detail="Cannot create execution job for a submitted attempt"
        )

    # Verify problem belongs to this assessment
    problem_states = attempt.get("problem_states", [])
    matching_state = next((ps for ps in problem_states if ps.get("problem_id") == problem_id), None)
    if not matching_state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Problem '{problem_id}' is not part of this coding assessment attempt"
        )

    now = datetime.now(timezone.utc)
    job_id = str(uuid.uuid4())

    job_doc = {
        "id": job_id,
        "user_id": user_id,
        "attempt_id": attempt_id,
        "problem_id": problem_id,
        "status": JobStatus.QUEUED.value,
        "source_submission_id": source_submission_id or str(uuid.uuid4()),
        "created_at": now,
        "started_at": None,
        "completed_at": None,
        "worker_id": None,
        "error_code": None
    }

    await db["coding_execution_jobs"].insert_one(job_doc)

    return CodingExecutionJobResponse(
        id=job_doc["id"],
        user_id=job_doc["user_id"],
        attempt_id=job_doc["attempt_id"],
        problem_id=job_doc["problem_id"],
        status=JobStatus.QUEUED,
        source_submission_id=job_doc["source_submission_id"],
        created_at=job_doc["created_at"],
        started_at=None,
        completed_at=None,
        worker_id=None,
        error_code=None
    )


async def get_execution_job(user_id: str, job_id: str) -> CodingExecutionJobResponse:
    """
    Retrieve an execution job by ID.
    Enforces user isolation: returns 404 if not found or owned by another user.
    """
    db = db_client.database
    job = await db["coding_execution_jobs"].find_one({"id": job_id, "user_id": user_id})
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution job not found"
        )

    return CodingExecutionJobResponse(
        id=job["id"],
        user_id=job["user_id"],
        attempt_id=job["attempt_id"],
        problem_id=job["problem_id"],
        status=JobStatus(job["status"]),
        source_submission_id=job.get("source_submission_id"),
        created_at=job["created_at"],
        started_at=job.get("started_at"),
        completed_at=job.get("completed_at"),
        worker_id=job.get("worker_id"),
        error_code=job.get("error_code")
    )


async def get_execution_result(user_id: str, job_id: str) -> ExecutionResultStatusResponse:
    """
    Retrieve the execution result for a job.
    If job is still QUEUED or RUNNING (or unjudged), returns a structured not-ready status.
    Enforces user isolation: returns 404 if job does not belong to user.
    """
    db = db_client.database
    job = await db["coding_execution_jobs"].find_one({"id": job_id, "user_id": user_id})
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution job not found"
        )

    current_status = job.get("status", JobStatus.QUEUED.value)
    if current_status in [JobStatus.QUEUED.value, JobStatus.RUNNING.value]:
        return ExecutionResultStatusResponse(
            job_id=job_id,
            status=current_status,
            message="Execution job is currently queued/running. Result not ready yet.",
            result=None
        )

    result_doc = await db["coding_execution_results"].find_one({"job_id": job_id})
    if not result_doc:
        return ExecutionResultStatusResponse(
            job_id=job_id,
            status=current_status,
            message=f"Job marked {current_status}, but detailed result document is not present.",
            result=None
        )

    test_case_results = None
    if "test_case_results" in result_doc:
        test_case_results = [
            TestCaseResultItem(
                test_case_id=tc["test_case_id"],
                order=tc["order"],
                is_hidden=tc["is_hidden"],
                verdict=ExecutionVerdict(tc["verdict"]),
                time_ms=tc.get("time_ms"),
                memory_mb=tc.get("memory_mb"),
                user_output=tc.get("user_output") if not tc["is_hidden"] else None,
                expected_output=tc.get("expected_output") if not tc["is_hidden"] else None
            )
            for tc in result_doc.get("test_case_results", [])
        ]

    result_response = CodingExecutionResultResponse(
        id=result_doc["id"],
        job_id=result_doc["job_id"],
        attempt_id=result_doc["attempt_id"],
        problem_id=result_doc["problem_id"],
        verdict=ExecutionVerdict(result_doc["verdict"]),
        passed_test_cases=result_doc.get("passed_test_cases", 0),
        total_test_cases=result_doc.get("total_test_cases", 0),
        execution_time_ms=result_doc.get("execution_time_ms"),
        memory_used_mb=result_doc.get("memory_used_mb"),
        compile_output=result_doc.get("compile_output"),
        runtime_output=result_doc.get("runtime_output"),
        test_case_results=test_case_results,
        created_at=result_doc["created_at"]
    )

    return ExecutionResultStatusResponse(
        job_id=job_id,
        status=current_status,
        message="Execution result retrieved successfully.",
        result=result_response
    )


async def claim_next_execution_job(worker_id: str) -> Optional[CodingExecutionJobResponse]:
    """
    Atomically claim the next QUEUED execution job using MongoDB atomic update semantics.
    Prevents race conditions when multiple workers poll the queue.
    Transitions: QUEUED -> RUNNING.
    """
    db = db_client.database
    now = datetime.now(timezone.utc)

    job = await db["coding_execution_jobs"].find_one_and_update(
        {"status": JobStatus.QUEUED.value},
        {
            "$set": {
                "status": JobStatus.RUNNING.value,
                "worker_id": worker_id,
                "started_at": now
            }
        },
        sort=[("created_at", 1)],
        return_document=ReturnDocument.AFTER
    )

    if not job:
        return None

    return CodingExecutionJobResponse(
        id=job["id"],
        user_id=job["user_id"],
        attempt_id=job["attempt_id"],
        problem_id=job["problem_id"],
        status=JobStatus.RUNNING,
        source_submission_id=job.get("source_submission_id"),
        created_at=job["created_at"],
        started_at=job.get("started_at"),
        completed_at=job.get("completed_at"),
        worker_id=job.get("worker_id"),
        error_code=job.get("error_code")
    )


async def complete_execution_job(
    job_id: str,
    worker_id: str,
    result_data: Optional[Dict[str, Any]] = None
) -> CodingExecutionJobResponse:
    """
    Complete an in-progress execution job.
    Enforces valid state transition: RUNNING -> COMPLETED.
    Rejects any transition if job is not currently RUNNING.
    """
    db = db_client.database
    now = datetime.now(timezone.utc)

    # First verify current job status
    job = await db["coding_execution_jobs"].find_one({"id": job_id})
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution job not found"
        )

    if job.get("status") != JobStatus.RUNNING.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid state transition: Cannot complete job with status '{job.get('status')}'. Must be RUNNING."
        )

    updated_job = await db["coding_execution_jobs"].find_one_and_update(
        {"id": job_id, "status": JobStatus.RUNNING.value},
        {
            "$set": {
                "status": JobStatus.COMPLETED.value,
                "completed_at": now
            }
        },
        return_document=ReturnDocument.AFTER
    )

    if not updated_job:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to complete job: status conflict or concurrent update"
        )

    # Optionally persist result record if provided
    if result_data:
        result_id = result_data.get("id") or str(uuid.uuid4())
        res_doc = {
            "id": result_id,
            "job_id": job_id,
            "attempt_id": job["attempt_id"],
            "problem_id": job["problem_id"],
            "user_id": job["user_id"],
            "verdict": result_data.get("verdict", ExecutionVerdict.ACCEPTED.value),
            "passed_test_cases": result_data.get("passed_test_cases", 0),
            "total_test_cases": result_data.get("total_test_cases", 0),
            "execution_time_ms": result_data.get("execution_time_ms"),
            "memory_used_mb": result_data.get("memory_used_mb"),
            "compile_output": result_data.get("compile_output", ""),
            "runtime_output": result_data.get("runtime_output", ""),
            "test_case_results": result_data.get("test_case_results", []),
            "created_at": now
        }
        await db["coding_execution_results"].update_one(
            {"job_id": job_id},
            {"$set": res_doc},
            upsert=True
        )

    return CodingExecutionJobResponse(
        id=updated_job["id"],
        user_id=updated_job["user_id"],
        attempt_id=updated_job["attempt_id"],
        problem_id=updated_job["problem_id"],
        status=JobStatus.COMPLETED,
        source_submission_id=updated_job.get("source_submission_id"),
        created_at=updated_job["created_at"],
        started_at=updated_job.get("started_at"),
        completed_at=updated_job.get("completed_at"),
        worker_id=updated_job.get("worker_id"),
        error_code=updated_job.get("error_code")
    )


async def fail_execution_job(
    job_id: str,
    worker_id: str,
    error_code: str = "SYSTEM_ERROR"
) -> CodingExecutionJobResponse:
    """
    Fail an in-progress execution job.
    Enforces valid state transition: RUNNING -> FAILED.
    Rejects any transition if job is not currently RUNNING.
    """
    db = db_client.database
    now = datetime.now(timezone.utc)

    job = await db["coding_execution_jobs"].find_one({"id": job_id})
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution job not found"
        )

    if job.get("status") != JobStatus.RUNNING.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid state transition: Cannot fail job with status '{job.get('status')}'. Must be RUNNING."
        )

    updated_job = await db["coding_execution_jobs"].find_one_and_update(
        {"id": job_id, "status": JobStatus.RUNNING.value},
        {
            "$set": {
                "status": JobStatus.FAILED.value,
                "error_code": error_code,
                "completed_at": now
            }
        },
        return_document=ReturnDocument.AFTER
    )

    if not updated_job:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to fail job: status conflict or concurrent update"
        )

    return CodingExecutionJobResponse(
        id=updated_job["id"],
        user_id=updated_job["user_id"],
        attempt_id=updated_job["attempt_id"],
        problem_id=updated_job["problem_id"],
        status=JobStatus.FAILED,
        source_submission_id=updated_job.get("source_submission_id"),
        created_at=updated_job["created_at"],
        started_at=updated_job.get("started_at"),
        completed_at=updated_job.get("completed_at"),
        worker_id=updated_job.get("worker_id"),
        error_code=updated_job.get("error_code")
    )
