"""
PrepForge — Curated Coding Problems & Timed Coding Assessments Seed Bank

Authoritative 10 coding problems and 2 Week 11 Timed Coding Assessments.
Strictly original concise interview-oriented descriptions.
Idempotent upsert logic ensuring zero duplicates on multiple server startups.
"""

from typing import List, Dict, Any

CODING_PROBLEMS_SEED: List[Dict[str, Any]] = [
    {
        "id": "two-sum-sorted",
        "title": "Two Sum in a Sorted Array",
        "slug": "two-sum-sorted",
        "category": "DSA",
        "topic": "Arrays & Two Pointers",
        "difficulty": "EASY",
        "description": "Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number. Return the indices of the two numbers (1-indexed) as an integer array of length 2.",
        "constraints": [
            "2 <= numbers.length <= 3 * 10^4",
            "-1000 <= numbers[i] <= 1000",
            "numbers is sorted in non-decreasing order",
            "-1000 <= target <= 1000",
            "Exactly one valid solution exists"
        ],
        "input_format": "numbers: List[int], target: int",
        "output_format": "List[int] containing two 1-based indices [index1, index2]",
        "examples": [
            {
                "input": "numbers = [2, 7, 11, 15], target = 9",
                "output": "[1, 2]",
                "explanation": "The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2."
            },
            {
                "input": "numbers = [2, 3, 4], target = 6",
                "output": "[1, 3]",
                "explanation": "The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3."
            }
        ],
        "starter_code": {
            "python": "def two_sum_sorted(numbers: list[int], target: int) -> list[int]:\n    # Write your solution here\n    pass\n",
            "cpp": "#include <vector>\n\nclass Solution {\npublic:\n    std::vector<int> twoSum(std::vector<int>& numbers, int target) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "expected_language": ["python", "cpp"],
        "tags": ["Two Pointers", "Array", "Binary Search"],
        "marks": 10,
        "status": "PUBLISHED"
    },
    {
        "id": "longest-substring-distinct",
        "title": "Longest Substring with At Most K Distinct Characters",
        "slug": "longest-substring-distinct",
        "category": "DSA",
        "topic": "Sliding Window",
        "difficulty": "MEDIUM",
        "description": "Given a string s and an integer k, return the length of the longest substring of s that contains at most k distinct characters.",
        "constraints": [
            "1 <= s.length <= 5 * 10^4",
            "0 <= k <= 50",
            "s consists of lowercase English letters"
        ],
        "input_format": "s: str, k: int",
        "output_format": "int representing the maximum length of such substring",
        "examples": [
            {
                "input": "s = 'eceba', k = 2",
                "output": "3",
                "explanation": "The substring is 'ece' with length 3."
            },
            {
                "input": "s = 'aa', k = 1",
                "output": "2",
                "explanation": "The substring is 'aa' with length 2."
            }
        ],
        "starter_code": {
            "python": "def length_of_longest_substring_k_distinct(s: str, k: int) -> int:\n    # Write your solution here\n    pass\n",
            "cpp": "#include <string>\n\nclass Solution {\npublic:\n    int lengthOfLongestSubstringKDistinct(std::string s, int k) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "expected_language": ["python", "cpp"],
        "tags": ["Sliding Window", "Hash Table", "String"],
        "marks": 10,
        "status": "PUBLISHED"
    },
    {
        "id": "search-rotated-array",
        "title": "Search in Rotated Sorted Array",
        "slug": "search-rotated-array",
        "category": "DSA",
        "topic": "Binary Search",
        "difficulty": "MEDIUM",
        "description": "There is an integer array nums sorted in ascending order with distinct values that was rotated at an unknown pivot index. Given nums and target, return the index of target if it exists, or -1 if not found. Must run in O(log n) time.",
        "constraints": [
            "1 <= nums.length <= 5000",
            "-10^4 <= nums[i] <= 10^4",
            "All values of nums are unique",
            "-10^4 <= target <= 10^4"
        ],
        "input_format": "nums: List[int], target: int",
        "output_format": "int (0-based index of target, or -1)",
        "examples": [
            {
                "input": "nums = [4, 5, 6, 7, 0, 1, 2], target = 0",
                "output": "4",
                "explanation": "Element 0 is present at index 4."
            },
            {
                "input": "nums = [4, 5, 6, 7, 0, 1, 2], target = 3",
                "output": "-1",
                "explanation": "Element 3 is not in the array."
            }
        ],
        "starter_code": {
            "python": "def search(nums: list[int], target: int) -> int:\n    # Write your solution here\n    pass\n",
            "cpp": "#include <vector>\n\nclass Solution {\npublic:\n    int search(std::vector<int>& nums, int target) {\n        // Write your solution here\n        return -1;\n    }\n};\n"
        },
        "expected_language": ["python", "cpp"],
        "tags": ["Binary Search", "Array"],
        "marks": 10,
        "status": "PUBLISHED"
    },
    {
        "id": "reverse-linked-list-k-group",
        "title": "Reverse Nodes in k-Group",
        "slug": "reverse-linked-list-k-group",
        "category": "DSA",
        "topic": "Linked Lists",
        "difficulty": "HARD",
        "description": "Given the head of a singly linked list, reverse the nodes of the list k at a time, and return the modified list. k is a positive integer. If the number of nodes is not a multiple of k, left-out nodes at the end should remain in original order.",
        "constraints": [
            "1 <= k <= n <= 5000",
            "0 <= Node.val <= 1000"
        ],
        "input_format": "head: ListNode, k: int",
        "output_format": "ListNode (head of modified linked list)",
        "examples": [
            {
                "input": "head = [1, 2, 3, 4, 5], k = 2",
                "output": "[2, 1, 4, 3, 5]",
                "explanation": "Nodes 1 and 2 are reversed, then nodes 3 and 4 are reversed. Node 5 remains as is."
            },
            {
                "input": "head = [1, 2, 3, 4, 5], k = 3",
                "output": "[3, 2, 1, 4, 5]",
                "explanation": "Nodes 1, 2, 3 reversed. Nodes 4, 5 remain as is."
            }
        ],
        "starter_code": {
            "python": "# Definition for singly-linked list.\n# class ListNode:\n#     def __init__(self, val=0, next=None):\n#         self.val = val\n#         self.next = next\n\ndef reverse_k_group(head, k: int):\n    # Write your solution here\n    pass\n",
            "cpp": "/**\n * Definition for singly-linked list.\n * struct ListNode {\n *     int val;\n *     ListNode *next;\n *     ListNode() : val(0), next(nullptr) {}\n *     ListNode(int x) : val(x), next(nullptr) {}\n *     ListNode(int x, ListNode *next) : val(x), next(next) {}\n * };\n */\nclass Solution {\npublic:\n    ListNode* reverseKGroup(ListNode* head, int k) {\n        // Write your solution here\n        return head;\n    }\n};\n"
        },
        "expected_language": ["python", "cpp"],
        "tags": ["Linked List", "Recursion"],
        "marks": 10,
        "status": "PUBLISHED"
    },
    {
        "id": "valid-parentheses-depth",
        "title": "Maximum Nesting Depth of Valid Parentheses",
        "slug": "valid-parentheses-depth",
        "category": "DSA",
        "topic": "Stack & Strings",
        "difficulty": "EASY",
        "description": "Given a valid parentheses string s, return the maximum nesting depth of the parentheses. Nesting depth is the maximum number of open parentheses active at any single position in the string.",
        "constraints": [
            "1 <= s.length <= 100",
            "s consists of digits 0-9 and operators +, -, *, /, (, and )",
            "s is guaranteed to be a valid parentheses string"
        ],
        "input_format": "s: str",
        "output_format": "int representing maximum nesting depth",
        "examples": [
            {
                "input": "s = '(1+(2*3)+((8)/4))+1'",
                "output": "3",
                "explanation": "Digit 8 is inside 3 nested pairs of parentheses in the string."
            },
            {
                "input": "s = '(1)+((2))+(((3)))'",
                "output": "3",
                "explanation": "Digit 3 is inside 3 nested pairs."
            }
        ],
        "starter_code": {
            "python": "def max_depth(s: str) -> int:\n    # Write your solution here\n    pass\n",
            "cpp": "#include <string>\n\nclass Solution {\npublic:\n    int maxDepth(std::string s) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "expected_language": ["python", "cpp"],
        "tags": ["Stack", "String"],
        "marks": 10,
        "status": "PUBLISHED"
    },
    {
        "id": "binary-tree-level-order-zigzag",
        "title": "Binary Tree Zigzag Level Order Traversal",
        "slug": "binary-tree-level-order-zigzag",
        "category": "DSA",
        "topic": "Trees & BFS",
        "difficulty": "MEDIUM",
        "description": "Given the root of a binary tree, return the zigzag level order traversal of its nodes' values (i.e., from left to right, then right to left for the next level and alternate between).",
        "constraints": [
            "The number of nodes in the tree is in the range [0, 2000]",
            "-100 <= Node.val <= 100"
        ],
        "input_format": "root: TreeNode",
        "output_format": "List[List[int]] representing zigzag level order values",
        "examples": [
            {
                "input": "root = [3, 9, 20, null, null, 15, 7]",
                "output": "[[3], [20, 9], [15, 7]]",
                "explanation": "Level 1 is left-to-right [3], level 2 is right-to-left [20, 9], level 3 is left-to-right [15, 7]."
            }
        ],
        "starter_code": {
            "python": "# Definition for a binary tree node.\n# class TreeNode:\n#     def __init__(self, val=0, left=None, right=None):\n#         self.val = val\n#         self.left = left\n#         self.right = right\n\ndef zigzag_level_order(root) -> list[list[int]]:\n    # Write your solution here\n    pass\n",
            "cpp": "#include <vector>\n\n/**\n * Definition for a binary tree node.\n * struct TreeNode {\n *     int val;\n *     TreeNode *left;\n *     TreeNode *right;\n *     TreeNode() : val(0), left(nullptr), right(nullptr) {}\n *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}\n * };\n */\nclass Solution {\npublic:\n    std::vector<std::vector<int>> zigzagLevelOrder(TreeNode* root) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "expected_language": ["python", "cpp"],
        "tags": ["Tree", "BFS", "Binary Tree"],
        "marks": 10,
        "status": "PUBLISHED"
    },
    {
        "id": "kth-largest-stream",
        "title": "Kth Largest Element in a Stream",
        "slug": "kth-largest-stream",
        "category": "DSA",
        "topic": "Heaps & Priority Queue",
        "difficulty": "EASY",
        "description": "Design a class to find the kth largest element in a stream of numbers. Note that it is the kth largest element in sorted order, not the kth distinct element. Implement the KthLargest class with a constructor and an add(val) method.",
        "constraints": [
            "1 <= k <= 10^4",
            "0 <= nums.length <= 10^4",
            "-10^4 <= nums[i] <= 10^4",
            "-10^4 <= val <= 10^4",
            "At most 10^4 calls will be made to add"
        ],
        "input_format": "k: int, nums: List[int], sequential calls to add(val: int)",
        "output_format": "int (the kth largest element after each addition)",
        "examples": [
            {
                "input": "KthLargest(3, [4, 5, 8, 2]); add(3); add(5); add(10); add(9); add(4);",
                "output": "[4, 5, 5, 8, 8, 8]",
                "explanation": "k=3. Stream values added sequentially return the 3rd largest item."
            }
        ],
        "starter_code": {
            "python": "import heapq\n\nclass KthLargest:\n    def __init__(self, k: int, nums: list[int]):\n        # Initialize data structure\n        pass\n\n    def add(self, val: int) -> int:\n        # Add value and return kth largest\n        pass\n",
            "cpp": "#include <vector>\n#include <queue>\n\nclass KthLargest {\npublic:\n    KthLargest(int k, std::vector<int>& nums) {\n        // Initialize data structure\n    }\n    \n    int add(int val) {\n        // Add value and return kth largest\n        return 0;\n    }\n};\n"
        },
        "expected_language": ["python", "cpp"],
        "tags": ["Heap", "Design", "Priority Queue"],
        "marks": 10,
        "status": "PUBLISHED"
    },
    {
        "id": "number-of-islands-grid",
        "title": "Number of Islands in 2D Grid",
        "slug": "number-of-islands-grid",
        "category": "DSA",
        "topic": "Graphs & DFS/BFS",
        "difficulty": "MEDIUM",
        "description": "Given an m x n 2D binary grid grid representing a map of '1's (land) and '0's (water), return the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.",
        "constraints": [
            "m == grid.length",
            "n == grid[i].length",
            "1 <= m, n <= 300",
            "grid[i][j] is '0' or '1'"
        ],
        "input_format": "grid: List[List[str]]",
        "output_format": "int representing total connected islands",
        "examples": [
            {
                "input": "grid = [['1','1','0','0','0'],['1','1','0','0','0'],['0','0','1','0','0'],['0','0','0','1','1']]",
                "output": "3",
                "explanation": "Three distinct connected components of land exist."
            }
        ],
        "starter_code": {
            "python": "def num_islands(grid: list[list[str]]) -> int:\n    # Write your solution here\n    pass\n",
            "cpp": "#include <vector>\n\nclass Solution {\npublic:\n    int numIslands(std::vector<std::vector<char>>& grid) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "expected_language": ["python", "cpp"],
        "tags": ["Graph", "DFS", "BFS", "Matrix"],
        "marks": 10,
        "status": "PUBLISHED"
    },
    {
        "id": "generate-balanced-parentheses",
        "title": "Generate Balanced Parentheses Combinations",
        "slug": "generate-balanced-parentheses",
        "category": "DSA",
        "topic": "Recursion & Backtracking",
        "difficulty": "MEDIUM",
        "description": "Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.",
        "constraints": [
            "1 <= n <= 8"
        ],
        "input_format": "n: int",
        "output_format": "List[str] containing all unique well-formed combinations",
        "examples": [
            {
                "input": "n = 3",
                "output": "['((()))', '(()())', '(())()', '()(())', '()()()']",
                "explanation": "All 5 valid combinations of 3 pairs of parentheses."
            },
            {
                "input": "n = 1",
                "output": "['()']",
                "explanation": "Single valid pair."
            }
        ],
        "starter_code": {
            "python": "def generate_parenthesis(n: int) -> list[str]:\n    # Write your solution here\n    pass\n",
            "cpp": "#include <vector>\n#include <string>\n\nclass Solution {\npublic:\n    std::vector<std::string> generateParenthesis(int n) {\n        // Write your solution here\n        return {};\n    }\n};\n"
        },
        "expected_language": ["python", "cpp"],
        "tags": ["Backtracking", "String", "Recursion"],
        "marks": 10,
        "status": "PUBLISHED"
    },
    {
        "id": "trapping-rain-water-elevation",
        "title": "Trapping Rain Water Elevation Profile",
        "slug": "trapping-rain-water-elevation",
        "category": "DSA",
        "topic": "Two Pointers & Dynamic Programming",
        "difficulty": "HARD",
        "description": "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "constraints": [
            "n == height.length",
            "1 <= n <= 2 * 10^4",
            "0 <= height[i] <= 10^5"
        ],
        "input_format": "height: List[int]",
        "output_format": "int representing total volume of trapped water",
        "examples": [
            {
                "input": "height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]",
                "output": "6",
                "explanation": "The elevation profile traps 6 units of rain water."
            },
            {
                "input": "height = [4, 2, 0, 3, 2, 5]",
                "output": "9",
                "explanation": "The elevation profile traps 9 units of rain water."
            }
        ],
        "starter_code": {
            "python": "def trap(height: list[int]) -> int:\n    # Write your solution here\n    pass\n",
            "cpp": "#include <vector>\n\nclass Solution {\npublic:\n    int trap(std::vector<int>& height) {\n        // Write your solution here\n        return 0;\n    }\n};\n"
        },
        "expected_language": ["python", "cpp"],
        "tags": ["Two Pointers", "Dynamic Programming", "Stack", "Array"],
        "marks": 10,
        "status": "PUBLISHED"
    }
]

CODING_ASSESSMENTS_SEED: List[Dict[str, Any]] = [
    {
        "id": "week-11-coding-assessment-1",
        "title": "Week 11 Timed Coding Assessment #1",
        "description": "Intensive 60-minute interview simulation focusing on linear data structures, sliding window, and tree traversals.",
        "week_number": 11,
        "assessment_type": "TIMED_CODING",
        "duration_minutes": 60,
        "problem_count": 3,
        "passing_score": 60,
        "status": "PUBLISHED",
        "problem_ids": [
            "two-sum-sorted",
            "longest-substring-distinct",
            "binary-tree-level-order-zigzag"
        ]
    },
    {
        "id": "week-11-coding-assessment-2",
        "title": "Week 11 Timed Coding Assessment #2",
        "description": "Challenging 75-minute algorithmic simulation evaluating binary search, graph traversal, and elevation profile trapping.",
        "week_number": 11,
        "assessment_type": "TIMED_CODING",
        "duration_minutes": 75,
        "problem_count": 3,
        "passing_score": 60,
        "status": "PUBLISHED",
        "problem_ids": [
            "search-rotated-array",
            "number-of-islands-grid",
            "trapping-rain-water-elevation"
        ]
    }
]


async def seed_coding_assessments(db) -> None:
    """
    Idempotent seed function for coding problems and timed coding assessments.
    Upserts each record so multiple application startups do not produce duplicate entries.
    """
    # 1. Upsert coding problems
    for problem in CODING_PROBLEMS_SEED:
        await db["coding_problems"].update_one(
            {"id": problem["id"]},
            {"$set": problem},
            upsert=True
        )

    # 2. Upsert coding assessments
    for assessment in CODING_ASSESSMENTS_SEED:
        await db["coding_assessments"].update_one(
            {"id": assessment["id"]},
            {"$set": assessment},
            upsert=True
        )
