"""
PrepForge — Coding Test Cases Service & Seed Data

Manages test case definitions for curated DSA problems.
Enforces security invariant:
- Hidden test cases MUST NEVER expose expected_output to public/frontend consumers.
- Test cases are stored in the MongoDB 'coding_test_cases' collection with idempotent seeding.
"""

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from app.db.connection import db_client
from app.schemas.coding_test_case import (
    CodingTestCaseInternal,
    CodingTestCasePublicResponse
)

CODING_TEST_CASES_SEED: List[Dict[str, Any]] = [
    # 1. two-sum-sorted
    {
        "id": "tc-two-sum-01",
        "problem_id": "two-sum-sorted",
        "order": 1,
        "input": "4\n2 7 11 15\n9\n",
        "expected_output": "1 2",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-two-sum-02",
        "problem_id": "two-sum-sorted",
        "order": 2,
        "input": "3\n2 3 4\n6\n",
        "expected_output": "1 3",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-two-sum-03",
        "problem_id": "two-sum-sorted",
        "order": 3,
        "input": "2\n-1 0\n-1\n",
        "expected_output": "1 2",
        "is_hidden": True,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-two-sum-04",
        "problem_id": "two-sum-sorted",
        "order": 4,
        "input": "5\n1 2 3 4 5\n8\n",
        "expected_output": "3 5",
        "is_hidden": True,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },

    # 2. longest-substring-distinct
    {
        "id": "tc-longest-sub-01",
        "problem_id": "longest-substring-distinct",
        "order": 1,
        "input": "eceba\n2\n",
        "expected_output": "3",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-longest-sub-02",
        "problem_id": "longest-substring-distinct",
        "order": 2,
        "input": "aa\n1\n",
        "expected_output": "2",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-longest-sub-03",
        "problem_id": "longest-substring-distinct",
        "order": 3,
        "input": "a\n0\n",
        "expected_output": "0",
        "is_hidden": True,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-longest-sub-04",
        "problem_id": "longest-substring-distinct",
        "order": 4,
        "input": "abaccc\n2\n",
        "expected_output": "4",
        "is_hidden": True,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },

    # 3. search-rotated-array
    {
        "id": "tc-search-rotated-01",
        "problem_id": "search-rotated-array",
        "order": 1,
        "input": "7\n4 5 6 7 0 1 2\n0\n",
        "expected_output": "4",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-search-rotated-02",
        "problem_id": "search-rotated-array",
        "order": 2,
        "input": "7\n4 5 6 7 0 1 2\n3\n",
        "expected_output": "-1",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-search-rotated-03",
        "problem_id": "search-rotated-array",
        "order": 3,
        "input": "1\n1\n0\n",
        "expected_output": "-1",
        "is_hidden": True,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-search-rotated-04",
        "problem_id": "search-rotated-array",
        "order": 4,
        "input": "3\n5 1 3\n5\n",
        "expected_output": "0",
        "is_hidden": True,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },

    # 4. reverse-linked-list-k-group
    {
        "id": "tc-reverse-k-01",
        "problem_id": "reverse-linked-list-k-group",
        "order": 1,
        "input": "5\n1 2 3 4 5\n2\n",
        "expected_output": "2 1 4 3 5",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-reverse-k-02",
        "problem_id": "reverse-linked-list-k-group",
        "order": 2,
        "input": "5\n1 2 3 4 5\n3\n",
        "expected_output": "3 2 1 4 5",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-reverse-k-03",
        "problem_id": "reverse-linked-list-k-group",
        "order": 3,
        "input": "1\n1\n1\n",
        "expected_output": "1",
        "is_hidden": True,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },

    # 5. valid-parentheses-depth
    {
        "id": "tc-valid-paren-01",
        "problem_id": "valid-parentheses-depth",
        "order": 1,
        "input": "(1+(2*3)+((8)/4))+1\n",
        "expected_output": "3",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-valid-paren-02",
        "problem_id": "valid-parentheses-depth",
        "order": 2,
        "input": "(1)+((2))+(((3)))\n",
        "expected_output": "3",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-valid-paren-03",
        "problem_id": "valid-parentheses-depth",
        "order": 3,
        "input": "1+(2*3)\n",
        "expected_output": "1",
        "is_hidden": True,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },

    # 6. binary-tree-level-order-zigzag
    {
        "id": "tc-zigzag-01",
        "problem_id": "binary-tree-level-order-zigzag",
        "order": 1,
        "input": "3 9 20 null null 15 7\n",
        "expected_output": "[[3],[20,9],[15,7]]",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-zigzag-02",
        "problem_id": "binary-tree-level-order-zigzag",
        "order": 2,
        "input": "1\n",
        "expected_output": "[[1]]",
        "is_hidden": True,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },

    # 7. kth-largest-stream
    {
        "id": "tc-kth-largest-01",
        "problem_id": "kth-largest-stream",
        "order": 1,
        "input": "3\n4 5 8 2\n3 5 10 9 4\n",
        "expected_output": "4 5 5 8 8 8",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-kth-largest-02",
        "problem_id": "kth-largest-stream",
        "order": 2,
        "input": "1\n\n-3 -2 -4 0 4\n",
        "expected_output": "-3 -2 -2 0 4",
        "is_hidden": True,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },

    # 8. number-of-islands-grid
    {
        "id": "tc-islands-01",
        "problem_id": "number-of-islands-grid",
        "order": 1,
        "input": "4 5\n1 1 0 0 0\n1 1 0 0 0\n0 0 1 0 0\n0 0 0 1 1\n",
        "expected_output": "3",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-islands-02",
        "problem_id": "number-of-islands-grid",
        "order": 2,
        "input": "1 1\n0\n",
        "expected_output": "0",
        "is_hidden": True,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },

    # 9. generate-balanced-parentheses
    {
        "id": "tc-gen-paren-01",
        "problem_id": "generate-balanced-parentheses",
        "order": 1,
        "input": "3\n",
        "expected_output": "((())),(()()),(())(),()(()),()()()",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-gen-paren-02",
        "problem_id": "generate-balanced-parentheses",
        "order": 2,
        "input": "1\n",
        "expected_output": "()",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-gen-paren-03",
        "problem_id": "generate-balanced-parentheses",
        "order": 3,
        "input": "2\n",
        "expected_output": "(()) ()()",
        "is_hidden": True,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },

    # 10. trapping-rain-water-elevation
    {
        "id": "tc-trapping-water-01",
        "problem_id": "trapping-rain-water-elevation",
        "order": 1,
        "input": "12\n0 1 0 2 1 0 1 3 2 1 2 1\n",
        "expected_output": "6",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-trapping-water-02",
        "problem_id": "trapping-rain-water-elevation",
        "order": 2,
        "input": "6\n4 2 0 3 2 5\n",
        "expected_output": "9",
        "is_hidden": False,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    },
    {
        "id": "tc-trapping-water-03",
        "problem_id": "trapping-rain-water-elevation",
        "order": 3,
        "input": "3\n2 0 2\n",
        "expected_output": "2",
        "is_hidden": True,
        "time_limit_ms": 2000,
        "memory_limit_mb": 256
    }
]


async def seed_coding_test_cases(db) -> None:
    """
    Idempotent seed function for coding problem test cases.
    """
    now = datetime.now(timezone.utc)
    for tc in CODING_TEST_CASES_SEED:
        doc = {
            **tc,
            "updated_at": now
        }
        await db["coding_test_cases"].update_one(
            {"id": tc["id"]},
            {
                "$set": doc,
                "$setOnInsert": {"created_at": now}
            },
            upsert=True
        )


async def get_public_test_cases(problem_id: str) -> List[CodingTestCasePublicResponse]:
    """
    Retrieve test cases for a problem formatted safely for public/client consumption.
    SECURITY INVARIANT:
    - If is_hidden is True, expected_output is strictly None.
    - If is_hidden is False, expected_output is safely exposed.
    """
    db = db_client.database
    cursor = db["coding_test_cases"].find({"problem_id": problem_id}).sort("order", 1)
    docs = await cursor.to_list(length=None)

    results: List[CodingTestCasePublicResponse] = []
    for d in docs:
        is_hidden = d.get("is_hidden", False)
        results.append(CodingTestCasePublicResponse(
            id=d["id"],
            problem_id=d["problem_id"],
            order=d.get("order", 1),
            input=d.get("input", "") if not is_hidden else "",
            expected_output=d.get("expected_output") if not is_hidden else None,
            is_hidden=is_hidden,
            time_limit_ms=d.get("time_limit_ms", 2000),
            memory_limit_mb=d.get("memory_limit_mb", 256),
            created_at=d.get("created_at", datetime.now(timezone.utc)),
            updated_at=d.get("updated_at", datetime.now(timezone.utc))
        ))
    return results


async def get_internal_test_cases(problem_id: str) -> List[CodingTestCaseInternal]:
    """
    Retrieve full test cases with expected_output.
    Strictly for internal judge worker usage.
    """
    db = db_client.database
    cursor = db["coding_test_cases"].find({"problem_id": problem_id}).sort("order", 1)
    docs = await cursor.to_list(length=None)

    results: List[CodingTestCaseInternal] = []
    for d in docs:
        results.append(CodingTestCaseInternal(
            id=d["id"],
            problem_id=d["problem_id"],
            order=d.get("order", 1),
            input=d.get("input", ""),
            expected_output=d.get("expected_output", ""),
            is_hidden=d.get("is_hidden", False),
            time_limit_ms=d.get("time_limit_ms", 2000),
            memory_limit_mb=d.get("memory_limit_mb", 256),
            created_at=d.get("created_at", datetime.now(timezone.utc)),
            updated_at=d.get("updated_at", datetime.now(timezone.utc))
        ))
    return results
