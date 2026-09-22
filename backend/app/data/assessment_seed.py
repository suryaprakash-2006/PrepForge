from datetime import datetime, timezone
import logging
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)

ASSESSMENTS_SEED = [
    {
        "id": "baseline-assessment",
        "title": "Comprehensive Baseline Assessment",
        "description": "Evaluate foundational readiness across Core CS, Algorithms, SQL, and System Concepts before diving into the 12-week roadmap.",
        "week_number": None,
        "assessment_type": "BASELINE",
        "duration_minutes": 30,
        "question_count": 10,
        "passing_score": 60,
        "status": "PUBLISHED"
    },
    {
        "id": "week-3-quiz",
        "title": "Week 3 Mastery Quiz: Arrays, Pointers & SQL Basics",
        "description": "Test your mastery of two-pointer techniques, sliding windows, prefix sums, bitwise basics, and SQL querying.",
        "week_number": 3,
        "assessment_type": "QUIZ",
        "duration_minutes": 30,
        "question_count": 10,
        "passing_score": 60,
        "status": "PUBLISHED"
    },
    {
        "id": "week-5-quiz",
        "title": "Week 5 Mastery Quiz: Linked Lists, Stacks & DBMS",
        "description": "Assess deep conceptual knowledge of Linked List manipulations, Monotonic Stacks, Recursion, and Database Transactions.",
        "week_number": 5,
        "assessment_type": "QUIZ",
        "duration_minutes": 30,
        "question_count": 10,
        "passing_score": 60,
        "status": "PUBLISHED"
    },
    {
        "id": "week-7-quiz",
        "title": "Week 7 Mastery Quiz: Trees, Heaps & Operating Systems",
        "description": "Evaluate binary tree traversals, BST properties, Min/Max Heap operations, and OS Process/Thread synchronization.",
        "week_number": 7,
        "assessment_type": "QUIZ",
        "duration_minutes": 30,
        "question_count": 10,
        "passing_score": 60,
        "status": "PUBLISHED"
    },
    {
        "id": "week-9-quiz",
        "title": "Week 9 Mastery Quiz: Graphs, Intro DP & Networks",
        "description": "Test graph traversals, shortest path algorithms, dynamic programming fundamentals, and networking protocols.",
        "week_number": 9,
        "assessment_type": "QUIZ",
        "duration_minutes": 30,
        "question_count": 10,
        "passing_score": 60,
        "status": "PUBLISHED"
    }
]

QUESTIONS_SEED = [
    # -------------------------------------------------------------
    # 1. BASELINE ASSESSMENT (10 Questions)
    # -------------------------------------------------------------
    {
        "id": "base-q1",
        "assessment_id": "baseline-assessment",
        "question_number": 1,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Time Complexity",
        "difficulty": "EASY",
        "question": "What is the worst-case time complexity of searching for an element in an unsorted array of size N?",
        "options": ["O(1)", "O(log N)", "O(N)", "O(N log N)"],
        "correct_answer": "O(N)",
        "explanation": "In an unsorted array, we may need to inspect every element sequentially from index 0 to N-1, giving O(N) linear time.",
        "marks": 1
    },
    {
        "id": "base-q2",
        "assessment_id": "baseline-assessment",
        "question_number": 2,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Data Structures",
        "difficulty": "EASY",
        "question": "Which data structure follows the Last-In-First-Out (LIFO) principle?",
        "options": ["Queue", "Stack", "Binary Heap", "Linked List"],
        "correct_answer": "Stack",
        "explanation": "A Stack operates under the LIFO (Last-In-First-Out) order where the most recently added element is removed first.",
        "marks": 1
    },
    {
        "id": "base-q3",
        "assessment_id": "baseline-assessment",
        "question_number": 3,
        "question_type": "MCQ",
        "category": "OOP",
        "topic": "Polymorphism",
        "difficulty": "MEDIUM",
        "question": "Which concept allows a subclass to provide a specific implementation of a method already defined in its superclass?",
        "options": ["Method Overloading", "Method Overriding", "Encapsulation", "Data Hiding"],
        "correct_answer": "Method Overriding",
        "explanation": "Method Overriding occurs when a child class redefines a method from its parent class with the same signature to provide specific runtime behavior.",
        "marks": 1
    },
    {
        "id": "base-q4",
        "assessment_id": "baseline-assessment",
        "question_number": 4,
        "question_type": "MCQ",
        "category": "DBMS",
        "topic": "ACID Properties",
        "difficulty": "EASY",
        "question": "Which ACID property guarantees that once a transaction commits, its changes survive even in the event of a system crash?",
        "options": ["Atomicity", "Consistency", "Isolation", "Durability"],
        "correct_answer": "Durability",
        "explanation": "Durability guarantees that the effects of committed transactions are permanently stored in non-volatile storage and survive crashes.",
        "marks": 1
    },
    {
        "id": "base-q5",
        "assessment_id": "baseline-assessment",
        "question_number": 5,
        "question_type": "MCQ",
        "category": "SQL",
        "topic": "Constraints",
        "difficulty": "EASY",
        "question": "What is the key difference between a PRIMARY KEY and a UNIQUE constraint in standard SQL?",
        "options": [
            "A table can have multiple PRIMARY KEYs but only one UNIQUE constraint",
            "PRIMARY KEY columns cannot contain NULL values, whereas UNIQUE columns can accept NULL",
            "UNIQUE constraints automatically create clustered indexes while PRIMARY KEY never does",
            "There is no functional difference"
        ],
        "correct_answer": "PRIMARY KEY columns cannot contain NULL values, whereas UNIQUE columns can accept NULL",
        "explanation": "A PRIMARY KEY uniquely identifies each record and forbids NULLs. A UNIQUE constraint also enforces distinctness but permits NULL values.",
        "marks": 1
    },
    {
        "id": "base-q6",
        "assessment_id": "baseline-assessment",
        "question_number": 6,
        "question_type": "MCQ",
        "category": "OS",
        "topic": "Memory Management",
        "difficulty": "MEDIUM",
        "question": "What is a 'Page Fault' in an operating system?",
        "options": [
            "An error caused by corrupted physical RAM sectors",
            "An access trap generated when a requested virtual page is not currently in physical memory",
            "A segmentation violation caused by writing to read-only memory",
            "An invalid cache line eviction in L1 cache"
        ],
        "correct_answer": "An access trap generated when a requested virtual page is not currently in physical memory",
        "explanation": "A Page Fault occurs when a program attempts to access a memory page that is mapped in virtual address space but not loaded into physical RAM.",
        "marks": 1
    },
    {
        "id": "base-q7",
        "assessment_id": "baseline-assessment",
        "question_number": 7,
        "question_type": "MCQ",
        "category": "OS",
        "topic": "Deadlocks",
        "difficulty": "MEDIUM",
        "question": "Which of the following is NOT one of the four Coffman conditions necessary for a deadlock?",
        "options": ["Mutual Exclusion", "Hold and Wait", "Preemption Allowed", "Circular Wait"],
        "correct_answer": "Preemption Allowed",
        "explanation": "The condition for deadlock is 'No Preemption' (resources cannot be forcibly taken away). Allowing preemption actively prevents deadlock.",
        "marks": 1
    },
    {
        "id": "base-q8",
        "assessment_id": "baseline-assessment",
        "question_number": 8,
        "question_type": "MCQ",
        "category": "CN",
        "topic": "Transport Layer",
        "difficulty": "EASY",
        "question": "Why is UDP preferred over TCP for real-time video streaming and gaming?",
        "options": [
            "UDP guarantees in-order delivery and packet acknowledgement",
            "UDP has lower latency overhead because it does not require connection handshakes or retransmissions",
            "UDP performs hardware-level error correction",
            "UDP encrypts all packet payloads by default"
        ],
        "correct_answer": "UDP has lower latency overhead because it does not require connection handshakes or retransmissions",
        "explanation": "UDP is connectionless and does not retransmit lost packets, prioritizing low latency and real-time throughput over guaranteed reliability.",
        "marks": 1
    },
    {
        "id": "base-q9",
        "assessment_id": "baseline-assessment",
        "question_number": 9,
        "question_type": "MCQ",
        "category": "Python",
        "topic": "Data Types & Mutability",
        "difficulty": "EASY",
        "question": "In Python, which of the following standard data types is immutable?",
        "options": ["List", "Dictionary", "Tuple", "Set"],
        "correct_answer": "Tuple",
        "explanation": "Tuples in Python are immutable sequences; once created, their elements cannot be added, removed, or reassigned.",
        "marks": 1
    },
    {
        "id": "base-q10",
        "assessment_id": "baseline-assessment",
        "question_number": 10,
        "question_type": "MCQ",
        "category": "Computer Architecture",
        "topic": "Caching",
        "difficulty": "MEDIUM",
        "question": "Accessing memory locations adjacent to recently accessed data benefits primarily from which principle?",
        "options": ["Temporal Locality", "Spatial Locality", "Instruction Pipelining", "Branch Prediction"],
        "correct_answer": "Spatial Locality",
        "explanation": "Spatial Locality states that if a particular storage location is referenced at a particular time, then nearby memory locations are likely to be referenced soon.",
        "marks": 1
    },

    # -------------------------------------------------------------
    # 2. WEEK 3 QUIZ: Arrays, Pointers & SQL Basics (10 Questions)
    # -------------------------------------------------------------
    {
        "id": "w3-q1",
        "assessment_id": "week-3-quiz",
        "question_number": 1,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Two Pointers",
        "difficulty": "EASY",
        "question": "Given a sorted array, what is the time complexity to find if two numbers sum to target T using two pointers?",
        "options": ["O(1)", "O(log N)", "O(N)", "O(N^2)"],
        "correct_answer": "O(N)",
        "explanation": "With one pointer at index 0 and one at N-1, each step increments the left or decrements the right pointer, scanning the array in linear O(N) time.",
        "marks": 1
    },
    {
        "id": "w3-q2",
        "assessment_id": "week-3-quiz",
        "question_number": 2,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Sliding Window",
        "difficulty": "MEDIUM",
        "question": "When finding the maximum sum subarray of fixed size K in an array of size N, what is the optimal time complexity using a sliding window?",
        "options": ["O(N * K)", "O(N)", "O(N log K)", "O(K)"],
        "correct_answer": "O(N)",
        "explanation": "By sliding the window of size K (adding the incoming element and subtracting the outgoing element), each element is processed in O(1) time, yielding O(N) total.",
        "marks": 1
    },
    {
        "id": "w3-q3",
        "assessment_id": "week-3-quiz",
        "question_number": 3,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Prefix Sum",
        "difficulty": "EASY",
        "question": "After building a prefix sum array `P` of size N in O(N) preprocessing time, what is the query time to compute `sum(arr[L..R])`?",
        "options": ["O(1)", "O(R - L)", "O(log N)", "O(N)"],
        "correct_answer": "O(1)",
        "explanation": "Range sum `sum(arr[L..R])` is computed directly in O(1) as `P[R] - P[L - 1]` (with 0-based bounds handling).",
        "marks": 1
    },
    {
        "id": "w3-q4",
        "assessment_id": "week-3-quiz",
        "question_number": 4,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Kadane's Algorithm",
        "difficulty": "MEDIUM",
        "question": "In Kadane's Algorithm for Maximum Subarray Sum, what is the state transition at each element `x` with `current_sum`?",
        "options": [
            "current_sum = max(0, current_sum + x)",
            "current_sum = max(x, current_sum + x)",
            "current_sum = current_sum * x",
            "current_sum = max(current_sum, x)"
        ],
        "correct_answer": "current_sum = max(x, current_sum + x)",
        "explanation": "At each element x, we decide whether to extend the existing contiguous subarray (`current_sum + x`) or start a fresh subarray at `x`.",
        "marks": 1
    },
    {
        "id": "w3-q5",
        "assessment_id": "week-3-quiz",
        "question_number": 5,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Bit Manipulation",
        "difficulty": "EASY",
        "question": "In an array where every element appears twice except one unique element, which operation finds the unique element in O(N) time and O(1) auxiliary space?",
        "options": ["Bitwise AND (&)", "Bitwise OR (|)", "Bitwise XOR (^)", "Bitwise NOT (~)"],
        "correct_answer": "Bitwise XOR (^)",
        "explanation": "Since `x ^ x = 0` and `x ^ 0 = x`, XORing all elements cancels duplicate pairs, leaving only the unique element.",
        "marks": 1
    },
    {
        "id": "w3-q6",
        "assessment_id": "week-3-quiz",
        "question_number": 6,
        "question_type": "MCQ",
        "category": "SQL",
        "topic": "Aggregation & Filtering",
        "difficulty": "EASY",
        "question": "Which SQL clause is used to filter groups created by `GROUP BY` based on aggregate conditions?",
        "options": ["WHERE", "HAVING", "ORDER BY", "FILTER"],
        "correct_answer": "HAVING",
        "explanation": "The `HAVING` clause filters aggregated results produced by `GROUP BY`, whereas `WHERE` filters individual rows prior to grouping.",
        "marks": 1
    },
    {
        "id": "w3-q7",
        "assessment_id": "week-3-quiz",
        "question_number": 7,
        "question_type": "MCQ",
        "category": "SQL",
        "topic": "Aggregate Functions",
        "difficulty": "EASY",
        "question": "What is the difference between `COUNT(*)` and `COUNT(column_name)` in SQL?",
        "options": [
            "COUNT(*) counts all rows including NULLs; COUNT(col) ignores rows where col is NULL",
            "COUNT(*) is slower and only counts non-NULL rows",
            "COUNT(col) counts duplicate values only once",
            "They are identical in all SQL engines"
        ],
        "correct_answer": "COUNT(*) counts all rows including NULLs; COUNT(col) ignores rows where col is NULL",
        "explanation": "`COUNT(*)` returns total row count regardless of nullability, while `COUNT(column_name)` counts only rows where `column_name IS NOT NULL`.",
        "marks": 1
    },
    {
        "id": "w3-q8",
        "assessment_id": "week-3-quiz",
        "question_number": 8,
        "question_type": "MCQ",
        "category": "SQL",
        "topic": "Execution Order",
        "difficulty": "MEDIUM",
        "question": "In standard SQL query execution, which step executes before `SELECT`?",
        "options": ["ORDER BY", "LIMIT", "WHERE and GROUP BY", "DISTINCT"],
        "correct_answer": "WHERE and GROUP BY",
        "explanation": "Logical SQL order is: FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT.",
        "marks": 1
    },
    {
        "id": "w3-q9",
        "assessment_id": "week-3-quiz",
        "question_number": 9,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Binary Search",
        "difficulty": "EASY",
        "question": "In standard binary search on array `A[0..N-1]`, how should the midpoint `mid` be calculated to avoid 32-bit integer overflow?",
        "options": [
            "mid = (low + high) / 2",
            "mid = low + (high - low) / 2",
            "mid = (high - low) / 2",
            "mid = high + (low / 2)"
        ],
        "correct_answer": "mid = low + (high - low) / 2",
        "explanation": "`low + (high - low) / 2` calculates the identical midpoint value without risking overflow from `low + high` exceeding INT_MAX.",
        "marks": 1
    },
    {
        "id": "w3-q10",
        "assessment_id": "week-3-quiz",
        "question_number": 10,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Array Manipulation",
        "difficulty": "MEDIUM",
        "question": "To rotate an array of size N to the right by K positions in O(1) space, what sequence of reverse operations is optimal?",
        "options": [
            "Reverse whole array, reverse first K elements, reverse remaining N-K elements",
            "Reverse first N-K elements, reverse whole array, reverse first K elements",
            "Reverse first K elements, reverse last K elements",
            "Rotate one-by-one K times"
        ],
        "correct_answer": "Reverse whole array, reverse first K elements, reverse remaining N-K elements",
        "explanation": "Reversing the entire array, then reversing `[0..K-1]` and `[K..N-1]` achieves rotation in O(N) time and O(1) space.",
        "marks": 1
    },

    # -------------------------------------------------------------
    # 3. WEEK 5 QUIZ: Linked Lists, Stacks & DBMS (10 Questions)
    # -------------------------------------------------------------
    {
        "id": "w5-q1",
        "assessment_id": "week-5-quiz",
        "question_number": 1,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Linked Lists",
        "difficulty": "EASY",
        "question": "What is the space complexity of Floyd's Tortoise and Hare algorithm for detecting cycles in a singly linked list?",
        "options": ["O(1)", "O(N)", "O(log N)", "O(N^2)"],
        "correct_answer": "O(1)",
        "explanation": "Floyd's algorithm uses only two pointer variables (slow and fast), requiring O(1) auxiliary memory.",
        "marks": 1
    },
    {
        "id": "w5-q2",
        "assessment_id": "week-5-quiz",
        "question_number": 2,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Linked Lists",
        "difficulty": "EASY",
        "question": "When iteratively reversing a singly linked list with pointers `prev`, `curr`, `next_node`, what is the correct pointer update inside the loop?",
        "options": [
            "next_node = curr.next; curr.next = prev; prev = curr; curr = next_node",
            "curr.next = prev; next_node = curr.next; prev = curr; curr = next_node",
            "prev = curr; curr.next = prev; curr = curr.next",
            "curr.next = next_node; next_node.next = prev; prev = curr"
        ],
        "correct_answer": "next_node = curr.next; curr.next = prev; prev = curr; curr = next_node",
        "explanation": "We must save `curr.next` first, reverse the pointer `curr.next = prev`, then advance `prev` and `curr` forward.",
        "marks": 1
    },
    {
        "id": "w5-q3",
        "assessment_id": "week-5-quiz",
        "question_number": 3,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Monotonic Stack",
        "difficulty": "MEDIUM",
        "question": "What is the overall time complexity of finding the Next Greater Element for all elements in an array of size N using a monotonic stack?",
        "options": ["O(N^2)", "O(N log N)", "O(N)", "O(2^N)"],
        "correct_answer": "O(N)",
        "explanation": "Each element is pushed onto and popped from the stack at most once, resulting in amortized O(N) linear time.",
        "marks": 1
    },
    {
        "id": "w5-q4",
        "assessment_id": "week-5-quiz",
        "question_number": 4,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Stacks",
        "difficulty": "MEDIUM",
        "question": "How can a Min-Stack support `push()`, `pop()`, and `getMin()` in O(1) time complexity?",
        "options": [
            "Sort the stack after every push operation",
            "Maintain an auxiliary stack tracking the running minimum at each element level",
            "Traverse elements on every getMin() call",
            "Use a binary search tree instead of a stack"
        ],
        "correct_answer": "Maintain an auxiliary stack tracking the running minimum at each element level",
        "explanation": "Maintaining an auxiliary min-stack (or storing pairs `(val, current_min)`) allows retrieving the minimum in O(1) time.",
        "marks": 1
    },
    {
        "id": "w5-q5",
        "assessment_id": "week-5-quiz",
        "question_number": 5,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Queues",
        "difficulty": "MEDIUM",
        "question": "When implementing a Queue using two Stacks (`in_stack` and `out_stack`), what is the amortized time complexity of the `dequeue()` operation?",
        "options": ["O(1)", "O(log N)", "O(N)", "O(N^2)"],
        "correct_answer": "O(1)",
        "explanation": "Each element is pushed to `in_stack` once, moved to `out_stack` once, and popped once. Amortized cost per operation is O(1).",
        "marks": 1
    },
    {
        "id": "w5-q6",
        "assessment_id": "week-5-quiz",
        "question_number": 6,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Recursion",
        "difficulty": "EASY",
        "question": "What happens if a recursive function does not define or reach a valid base case?",
        "options": ["It returns null", "Stack Overflow Error due to infinite recursive call frames", "Heap corruption", "O(1) premature termination"],
        "correct_answer": "Stack Overflow Error due to infinite recursive call frames",
        "explanation": "Without a terminating base case, recursive calls consume execution call stack memory until the call stack limit is exceeded.",
        "marks": 1
    },
    {
        "id": "w5-q7",
        "assessment_id": "week-5-quiz",
        "question_number": 7,
        "question_type": "MCQ",
        "category": "DBMS",
        "topic": "Indexing",
        "difficulty": "MEDIUM",
        "question": "Why are B+ Trees preferred over Binary Search Trees for relational database disk indexing?",
        "options": [
            "B+ Trees have higher branching factor and shallow height, minimizing disk I/O operations",
            "B+ Trees only store data in memory and never touch disk",
            "Binary Search Trees cannot support range queries",
            "B+ Trees store duplicate keys without any pointer overhead"
        ],
        "correct_answer": "B+ Trees have higher branching factor and shallow height, minimizing disk I/O operations",
        "explanation": "A high fan-out (branching factor) keeps the B+ tree height very low (3-4 levels), dramatically reducing expensive disk block reads.",
        "marks": 1
    },
    {
        "id": "w5-q8",
        "assessment_id": "week-5-quiz",
        "question_number": 8,
        "question_type": "MCQ",
        "category": "DBMS",
        "topic": "Indexing",
        "difficulty": "MEDIUM",
        "question": "How many Clustered Indexes can a single relational table have?",
        "options": ["Only 1", "Up to 16", "Unlimited", "Zero"],
        "correct_answer": "Only 1",
        "explanation": "A Clustered Index dictates the physical ordering of records in storage. Because physical data can only be sorted in one order, a table can have only one clustered index.",
        "marks": 1
    },
    {
        "id": "w5-q9",
        "assessment_id": "week-5-quiz",
        "question_number": 9,
        "question_type": "MCQ",
        "category": "DBMS",
        "topic": "Transaction Isolation",
        "difficulty": "MEDIUM",
        "question": "What concurrency phenomenon occurs when a transaction reads uncommitted changes written by another concurrent transaction that subsequently rolls back?",
        "options": ["Dirty Read", "Non-Repeatable Read", "Phantom Read", "Lost Update"],
        "correct_answer": "Dirty Read",
        "explanation": "A Dirty Read occurs when Transaction A reads data modified by Transaction B before B has committed, and B eventually aborts.",
        "marks": 1
    },
    {
        "id": "w5-q10",
        "assessment_id": "week-5-quiz",
        "question_number": 10,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Stacks",
        "difficulty": "EASY",
        "question": "Which data structure is ideally suited to validate matched pairs of parentheses like `{[()]}`?",
        "options": ["Queue", "Stack", "Min Heap", "Hash Table only"],
        "correct_answer": "Stack",
        "explanation": "A Stack matches open brackets against closing brackets by matching the most recently opened symbol first (LIFO property).",
        "marks": 1
    },

    # -------------------------------------------------------------
    # 4. WEEK 7 QUIZ: Trees, Heaps & Operating Systems (10 Questions)
    # -------------------------------------------------------------
    {
        "id": "w7-q1",
        "assessment_id": "week-7-quiz",
        "question_number": 1,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Trees",
        "difficulty": "EASY",
        "question": "Which tree traversal produces elements in strictly ascending order when executed on a valid Binary Search Tree (BST)?",
        "options": ["Preorder Traversal", "Inorder Traversal", "Postorder Traversal", "Level-order Traversal"],
        "correct_answer": "Inorder Traversal",
        "explanation": "Inorder traversal (Left -> Node -> Right) visits BST elements in non-decreasing sorted order.",
        "marks": 1
    },
    {
        "id": "w7-q2",
        "assessment_id": "week-7-quiz",
        "question_number": 2,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Trees",
        "difficulty": "MEDIUM",
        "question": "In a BST, if both target nodes `p` and `q` are strictly smaller than `root.val`, where is their Lowest Common Ancestor (LCA)?",
        "options": [
            "At root itself",
            "In root.left subtree",
            "In root.right subtree",
            "Undefined"
        ],
        "correct_answer": "In root.left subtree",
        "explanation": "By BST properties, all values smaller than root reside strictly in the left subtree, so LCA must lie in `root.left`.",
        "marks": 1
    },
    {
        "id": "w7-q3",
        "assessment_id": "week-7-quiz",
        "question_number": 3,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Trees",
        "difficulty": "EASY",
        "question": "What is the recurrence relation for the maximum depth (height) of a binary tree rooted at `node`?",
        "options": [
            "depth(node) = depth(node.left) + depth(node.right)",
            "depth(node) = 1 + max(depth(node.left), depth(node.right))",
            "depth(node) = 1 + min(depth(node.left), depth(node.right))",
            "depth(node) = max(depth(node.left), depth(node.right))"
        ],
        "correct_answer": "depth(node) = 1 + max(depth(node.left), depth(node.right))",
        "explanation": "The height of a binary tree is 1 (for the current node) plus the maximum of the depths of its left and right subtrees.",
        "marks": 1
    },
    {
        "id": "w7-q4",
        "assessment_id": "week-7-quiz",
        "question_number": 4,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Heaps",
        "difficulty": "EASY",
        "question": "What is the worst-case time complexity of inserting a new element into a binary Max Heap of size N?",
        "options": ["O(1)", "O(log N)", "O(N)", "O(N log N)"],
        "correct_answer": "O(log N)",
        "explanation": "Insertion appends the element at the end of the heap array and bubbles up (heapifies up) along tree height, taking O(log N).",
        "marks": 1
    },
    {
        "id": "w7-q5",
        "assessment_id": "week-7-quiz",
        "question_number": 5,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Heaps",
        "difficulty": "MEDIUM",
        "question": "To find the Kth largest element in an unsorted stream of N numbers in optimal memory, which data structure is best?",
        "options": ["Min-Heap of size K", "Max-Heap of size N", "Sorted Array of size N", "Queue of size K"],
        "correct_answer": "Min-Heap of size K",
        "explanation": "A Min-Heap of size K maintains the top K largest elements seen so far; its root always contains the Kth largest element.",
        "marks": 1
    },
    {
        "id": "w7-q6",
        "assessment_id": "week-7-quiz",
        "question_number": 6,
        "question_type": "MCQ",
        "category": "OS",
        "topic": "Processes & Threads",
        "difficulty": "EASY",
        "question": "Which resource is shared by all threads belonging to the same process?",
        "options": ["Stack Memory", "Registers & Program Counter", "Heap Memory and Code/Data Segment", "Thread ID"],
        "correct_answer": "Heap Memory and Code/Data Segment",
        "explanation": "Threads within the same process share the virtual address space (Heap, global data, code segment, and open files), but each has its own private Stack.",
        "marks": 1
    },
    {
        "id": "w7-q7",
        "assessment_id": "week-7-quiz",
        "question_number": 7,
        "question_type": "MCQ",
        "category": "OS",
        "topic": "Synchronization",
        "difficulty": "MEDIUM",
        "question": "What is the essential difference between a Mutex and a Counting Semaphore?",
        "options": [
            "A Mutex has ownership and can only be unlocked by the thread that locked it; a Counting Semaphore can be signaled by any thread",
            "A Mutex allows multiple threads concurrently while a Semaphore allows only one",
            "Semaphores are only implemented in hardware",
            "Mutexes can never cause deadlocks"
        ],
        "correct_answer": "A Mutex has ownership and can only be unlocked by the thread that locked it; a Counting Semaphore can be signaled by any thread",
        "explanation": "A Mutex is a locking mechanism with thread ownership, whereas a Semaphore is a signaling mechanism with an integer counter.",
        "marks": 1
    },
    {
        "id": "w7-q8",
        "assessment_id": "week-7-quiz",
        "question_number": 8,
        "question_type": "MCQ",
        "category": "OS",
        "topic": "Context Switching",
        "difficulty": "MEDIUM",
        "question": "Where does the OS kernel store the CPU state and registers during a process context switch?",
        "options": ["Process Control Block (PCB)", "File Allocation Table (FAT)", "L1 Data Cache", "TLB Register"],
        "correct_answer": "Process Control Block (PCB)",
        "explanation": "The PCB (Process Control Block) stores process state, CPU registers, program counter, memory management info, and accounting data.",
        "marks": 1
    },
    {
        "id": "w7-q9",
        "assessment_id": "week-7-quiz",
        "question_number": 9,
        "question_type": "MCQ",
        "category": "OS",
        "topic": "CPU Scheduling",
        "difficulty": "MEDIUM",
        "question": "Which non-preemptive CPU scheduling algorithm achieves the minimum average waiting time for a given set of stationary processes?",
        "options": ["First-Come First-Served (FCFS)", "Shortest Job First (SJF)", "Round Robin (RR)", "Priority Scheduling"],
        "correct_answer": "Shortest Job First (SJF)",
        "explanation": "SJF is provably optimal for minimizing average waiting time by scheduling shorter burst times first.",
        "marks": 1
    },
    {
        "id": "w7-q10",
        "assessment_id": "week-7-quiz",
        "question_number": 10,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Trees",
        "difficulty": "EASY",
        "question": "Which traversal algorithm is used to perform a Level-Order Traversal of a binary tree?",
        "options": ["Breadth-First Search (BFS) using a Queue", "Depth-First Search (DFS) using a Stack", "Morris Traversal", "Binary Search"],
        "correct_answer": "Breadth-First Search (BFS) using a Queue",
        "explanation": "BFS using a FIFO Queue processes nodes level by level from top to bottom.",
        "marks": 1
    },

    # -------------------------------------------------------------
    # 5. WEEK 9 QUIZ: Graphs, Intro DP & Networks (10 Questions)
    # -------------------------------------------------------------
    {
        "id": "w9-q1",
        "assessment_id": "week-9-quiz",
        "question_number": 1,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Graphs",
        "difficulty": "EASY",
        "question": "What is the time complexity of Breadth-First Search (BFS) on an adjacency list graph with V vertices and E edges?",
        "options": ["O(V + E)", "O(V * E)", "O(V^2)", "O(E log V)"],
        "correct_answer": "O(V + E)",
        "explanation": "BFS visits every vertex once and explores every outgoing edge once, yielding O(V + E) linear time.",
        "marks": 1
    },
    {
        "id": "w9-q2",
        "assessment_id": "week-9-quiz",
        "question_number": 2,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Graphs",
        "difficulty": "MEDIUM",
        "question": "Topological Sort can be computed on which type of graph?",
        "options": [
            "Any Directed Graph",
            "Directed Acyclic Graph (DAG) only",
            "Undirected Connected Graph",
            "Complete Graph"
        ],
        "correct_answer": "Directed Acyclic Graph (DAG) only",
        "explanation": "A Topological Ordering requires directed edges without cycles (DAG); a cycle creates a circular dependency where no valid linear ordering exists.",
        "marks": 1
    },
    {
        "id": "w9-q3",
        "assessment_id": "week-9-quiz",
        "question_number": 3,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Graphs",
        "difficulty": "MEDIUM",
        "question": "Why does standard Dijkstra's algorithm fail on graphs with negative edge weights?",
        "options": [
            "Dijkstra assumes that adding an edge to a path never decreases total path distance (greedy assumption)",
            "Dijkstra can only run on undirected trees",
            "Priority queue cannot store negative numbers",
            "Dijkstra runs in O(V!) time on negative weights"
        ],
        "correct_answer": "Dijkstra assumes that adding an edge to a path never decreases total path distance (greedy assumption)",
        "explanation": "Dijkstra greedily marks visited nodes as final; negative edge weights invalidate the invariant that shortest path cannot be decreased later.",
        "marks": 1
    },
    {
        "id": "w9-q4",
        "assessment_id": "week-9-quiz",
        "question_number": 4,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Dynamic Programming",
        "difficulty": "EASY",
        "question": "What two core properties must a problem exhibit to be effectively solved by Dynamic Programming?",
        "options": [
            "Optimal Substructure and Overlapping Subproblems",
            "Greedy Choice Property and Divide-and-Conquer",
            "NP-Hardness and Polynomial Reducibility",
            "Randomized Steps and Monte Carlo Convergence"
        ],
        "correct_answer": "Optimal Substructure and Overlapping Subproblems",
        "explanation": "DP requires Optimal Substructure (global optimal solution contains optimal sub-solutions) and Overlapping Subproblems (subproblems recur repeatedly).",
        "marks": 1
    },
    {
        "id": "w9-q5",
        "assessment_id": "week-9-quiz",
        "question_number": 5,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Dynamic Programming",
        "difficulty": "MEDIUM",
        "question": "In the 0/1 Knapsack problem with N items and capacity W, what is the standard 2D DP state representation?",
        "options": [
            "dp[i][w]: Maximum value possible using a subset of first i items with capacity at most w",
            "dp[i]: Maximum weight of item i",
            "dp[w]: Total items fitting in weight w",
            "dp[i][j]: Value of item i minus weight of item j"
        ],
        "correct_answer": "dp[i][w]: Maximum value possible using a subset of first i items with capacity at most w",
        "explanation": "`dp[i][w]` captures the maximum value achievable considering the first `i` items with a remaining weight capacity of `w`.",
        "marks": 1
    },
    {
        "id": "w9-q6",
        "assessment_id": "week-9-quiz",
        "question_number": 6,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Dynamic Programming",
        "difficulty": "MEDIUM",
        "question": "For Longest Common Subsequence (LCS) of strings S1 and S2, if `S1[i-1] == S2[j-1]`, what is `dp[i][j]`?",
        "options": [
            "dp[i][j] = 1 + dp[i-1][j-1]",
            "dp[i][j] = max(dp[i-1][j], dp[i][j-1])",
            "dp[i][j] = dp[i-1][j-1]",
            "dp[i][j] = 1 + max(dp[i-1][j], dp[i][j-1])"
        ],
        "correct_answer": "dp[i][j] = 1 + dp[i-1][j-1]",
        "explanation": "When matching characters match, the LCS length increases by 1 plus the LCS of the prefixes `S1[0..i-2]` and `S2[0..j-2]`.",
        "marks": 1
    },
    {
        "id": "w9-q7",
        "assessment_id": "week-9-quiz",
        "question_number": 7,
        "question_type": "MCQ",
        "category": "CN",
        "topic": "TCP Handshake",
        "difficulty": "EASY",
        "question": "What is the correct sequence of packets in the TCP 3-Way Handshake?",
        "options": [
            "SYN -> SYN-ACK -> ACK",
            "ACK -> SYN -> SYN-ACK",
            "SYN -> ACK -> DATA",
            "CONNECT -> ACCEPT -> ESTABLISHED"
        ],
        "correct_answer": "SYN -> SYN-ACK -> ACK",
        "explanation": "Client sends SYN; Server responds with SYN-ACK; Client replies with ACK to establish a full-duplex connection.",
        "marks": 1
    },
    {
        "id": "w9-q8",
        "assessment_id": "week-9-quiz",
        "question_number": 8,
        "question_type": "MCQ",
        "category": "CN",
        "topic": "Application Layer",
        "difficulty": "EASY",
        "question": "What transport protocol does DNS predominantly use for standard query lookups?",
        "options": ["UDP on port 53", "TCP on port 80", "HTTP on port 443", "ICMP on port 0"],
        "correct_answer": "UDP on port 53",
        "explanation": "DNS queries use UDP on port 53 for fast, lightweight resolution without connection establishment overhead.",
        "marks": 1
    },
    {
        "id": "w9-q9",
        "assessment_id": "week-9-quiz",
        "question_number": 9,
        "question_type": "MCQ",
        "category": "CN",
        "topic": "HTTP Status Codes",
        "difficulty": "EASY",
        "question": "What is the difference between HTTP status code 401 Unauthorized and 403 Forbidden?",
        "options": [
            "401 means authentication is missing or invalid; 403 means identity is known but access to the resource is forbidden",
            "401 is a server crash; 403 is a client crash",
            "401 indicates expired SSL certificate; 403 indicates rate limit exceeded",
            "They are exact synonyms in RFC 9110"
        ],
        "correct_answer": "401 means authentication is missing or invalid; 403 means identity is known but access to the resource is forbidden",
        "explanation": "401 represents unauthenticated requests (login required), whereas 403 indicates authenticated user lacks authorization permissions.",
        "marks": 1
    },
    {
        "id": "w9-q10",
        "assessment_id": "week-9-quiz",
        "question_number": 10,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Disjoint Set Union (DSU)",
        "difficulty": "MEDIUM",
        "question": "With both Path Compression and Union by Rank optimizations, what is the nearly constant amortized time complexity per DSU operation?",
        "options": ["O(α(N)) (Inverse Ackermann function)", "O(log N)", "O(N)", "O(1/N)"],
        "correct_answer": "O(α(N)) (Inverse Ackermann function)",
        "explanation": "DSU with union by rank and path compression achieves O(α(N)) time per operation, where α(N) ≤ 4 for all practical inputs.",
        "marks": 1
    }
]

async def seed_assessments(db: AsyncIOMotorDatabase) -> None:
    """
    Idempotent deterministic seed for assessments and question bank.
    Safe to run repeatedly without creating duplicates.
    """
    now = datetime.now(timezone.utc)

    # 1. Seed Assessments
    for a in ASSESSMENTS_SEED:
        doc = {**a, "updated_at": now}
        await db["assessments"].update_one(
            {"id": a["id"]},
            {"$set": doc, "$setOnInsert": {"created_at": now}},
            upsert=True
        )

    # 2. Seed Questions
    for q in QUESTIONS_SEED:
        doc = {**q, "updated_at": now}
        await db["assessment_questions"].update_one(
            {"id": q["id"]},
            {"$set": doc, "$setOnInsert": {"created_at": now}},
            upsert=True
        )

    logger.info("Assessment seed completed: 5 assessments and 50 questions verified.")
