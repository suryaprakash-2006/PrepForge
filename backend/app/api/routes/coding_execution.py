from fastapi import APIRouter, Depends, Path, status
from typing import List
from app.api.deps import get_current_user
from app.schemas.coding_execution_job import (
    CodingExecutionJobResponse,
    JobStatusResponse
)
from app.schemas.coding_execution_result import (
    ExecutionResultStatusResponse,
    CodingExecutionResultResponse
)
from app.schemas.coding_test_case import (
    CodingTestCasePublicResponse
)
from app.services import (
    coding_execution as coding_execution_service,
    coding_test_cases as coding_test_cases_service
)

router = APIRouter()

@router.get("/jobs/{job_id}", response_model=CodingExecutionJobResponse)
async def get_execution_job(
    job_id: str = Path(..., description="Unique execution job ID"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get execution job details and status. Enforces user isolation.
    """
    user_id = str(current_user["_id"])
    return await coding_execution_service.get_execution_job(user_id=user_id, job_id=job_id)

@router.get("/results/{job_id}", response_model=ExecutionResultStatusResponse)
async def get_execution_result(
    job_id: str = Path(..., description="Unique execution job ID"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get execution result for a job.
    Returns status and verdict/metrics once completed.
    Hidden test cases do not reveal expected output.
    """
    user_id = str(current_user["_id"])
    return await coding_execution_service.get_execution_result(user_id=user_id, job_id=job_id)

@router.get("/problems/{problem_id}/test-cases", response_model=List[CodingTestCasePublicResponse])
async def get_problem_test_cases(
    problem_id: str = Path(..., description="Coding problem ID"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get test cases for a problem.
    SECURITY INVARIANT: Hidden test cases will NOT include expected_output.
    """
    return await coding_test_cases_service.get_public_test_cases(problem_id=problem_id)
