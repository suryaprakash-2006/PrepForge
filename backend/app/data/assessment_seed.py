from datetime import datetime, timezone
import logging
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)

ASSESSMENTS_SEED = [
    {
        "id": "baseline-assessment",
        "title": "Comprehensive Baseline Assessment",
        "description": "Evaluate foundational readiness across Core CS, Algorithms, SQL, and System Concepts before diving into the 12-week roadmap.",
        "week_number": 1,
        "assessment_type": "BASELINE",
        "duration_minutes": 30,
        "question_count": 10,
        "passing_score": 60,
        "status": "PUBLISHED"
    },
    {
        "id": "week-3-quiz",
        "title": "Week 3 Mastery Quiz: Sliding Window, Linked Lists, Stacks & Normalization",
        "description": "Evaluate mastery of sliding window techniques, binary search, linked structures, stacks, queues, SQL subqueries, and database normalization.",
        "week_number": 3,
        "assessment_type": "QUIZ",
        "duration_minutes": 30,
        "question_count": 10,
        "passing_score": 60,
        "status": "PUBLISHED"
    },
    {
        "id": "week-5-quiz",
        "title": "Week 5 Mastery Quiz: Trees, Window Functions, Indexing & OS Processes",
        "description": "Assess deep conceptual knowledge of Binary Trees, BSTs, SQL Window Functions, B+ Tree Indexing, and OS Process Scheduling.",
        "week_number": 5,
        "assessment_type": "QUIZ",
        "duration_minutes": 30,
        "question_count": 10,
        "passing_score": 60,
        "status": "PUBLISHED"
    },
    {
        "id": "week-7-quiz",
        "title": "Week 7 Mastery Quiz: Recursion, Backtracking, Networks & Architecture",
        "description": "Test recursion, backtracking, graph traversals, networking protocols (DNS/DHCP/ARP/HTTPS), pipelining, and Git/Testing.",
        "week_number": 7,
        "assessment_type": "QUIZ",
        "duration_minutes": 30,
        "question_count": 10,
        "passing_score": 60,
        "status": "PUBLISHED"
    },
    {
        "id": "week-9-quiz",
        "title": "Week 9 Mastery Quiz: Machine Learning Fundamentals & Algorithms",
        "description": "Assess core supervised and unsupervised algorithms, overfitting/underfitting, cross-validation, decision trees, ensemble methods, and ML evaluation metrics.",
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
    # 1. BASELINE ASSESSMENT (Week 1 — 10 Questions)
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
    # 2. WEEK 3 QUIZ: Sliding Window, Linked Lists, Stacks & Normalization (10 Questions)
    # -------------------------------------------------------------
    {
        "id": "w3-q1",
        "assessment_id": "week-3-quiz",
        "question_number": 1,
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
        "id": "w3-q2",
        "assessment_id": "week-3-quiz",
        "question_number": 2,
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
        "id": "w3-q3",
        "assessment_id": "week-3-quiz",
        "question_number": 3,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Linked Lists",
        "difficulty": "EASY",
        "question": "What is the space complexity of Floyd's Tortoise and Hare algorithm for detecting cycles in a singly linked list?",
        "options": ["O(1)", "O(N)", "O(log N)", "O(N^2)"],
        "correct_answer": "O(1)",
        "explanation": "Floyd's cycle detection algorithm uses only two pointer variables (slow and fast), requiring O(1) auxiliary memory.",
        "marks": 1
    },
    {
        "id": "w3-q4",
        "assessment_id": "week-3-quiz",
        "question_number": 4,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Linked Lists",
        "difficulty": "EASY",
        "question": "When iteratively reversing a singly linked list with pointers `prev`, `curr`, `next_node`, what is the correct pointer update sequence inside the loop?",
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
        "id": "w3-q5",
        "assessment_id": "week-3-quiz",
        "question_number": 5,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Stacks",
        "difficulty": "EASY",
        "question": "Which data structure is ideally suited to validate matched pairs of nested brackets like `{[()]}` in O(N) time?",
        "options": ["Queue", "Stack", "Min Heap", "Binary Search Tree"],
        "correct_answer": "Stack",
        "explanation": "A Stack matches open brackets against closing brackets by matching the most recently opened symbol first (LIFO property).",
        "marks": 1
    },
    {
        "id": "w3-q6",
        "assessment_id": "week-3-quiz",
        "question_number": 6,
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
        "id": "w3-q7",
        "assessment_id": "week-3-quiz",
        "question_number": 7,
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
        "id": "w3-q8",
        "assessment_id": "week-3-quiz",
        "question_number": 8,
        "question_type": "MCQ",
        "category": "SQL",
        "topic": "Subqueries",
        "difficulty": "MEDIUM",
        "question": "What distinguishes a Correlated Subquery from an independent subquery in SQL?",
        "options": [
            "A correlated subquery executes once for the entire query, while independent subqueries run per row",
            "A correlated subquery references columns from the outer query and re-evaluates for each candidate row",
            "A correlated subquery can only return scalar numeric constants",
            "A correlated subquery requires an explicit UNION operator"
        ],
        "correct_answer": "A correlated subquery references columns from the outer query and re-evaluates for each candidate row",
        "explanation": "A correlated subquery depends on the outer query for its values and must be evaluated repeatedly for each row processed by the outer query.",
        "marks": 1
    },
    {
        "id": "w3-q9",
        "assessment_id": "week-3-quiz",
        "question_number": 9,
        "question_type": "MCQ",
        "category": "DBMS",
        "topic": "Normalization",
        "difficulty": "MEDIUM",
        "question": "A table is in Second Normal Form (2NF) if it is in 1NF and satisfies which additional rule?",
        "options": [
            "Every non-prime attribute is fully functionally dependent on the entire primary key (no partial dependencies)",
            "There are no transitive dependencies between non-prime attributes",
            "Every determinant is a candidate key (BCNF condition)",
            "No multi-valued dependencies exist in the table"
        ],
        "correct_answer": "Every non-prime attribute is fully functionally dependent on the entire primary key (no partial dependencies)",
        "explanation": "2NF requires removing partial dependencies, meaning non-prime attributes must depend on the whole primary key, not just a subset of a composite key.",
        "marks": 1
    },
    {
        "id": "w3-q10",
        "assessment_id": "week-3-quiz",
        "question_number": 10,
        "question_type": "MCQ",
        "category": "DBMS",
        "topic": "Transactions & ACID",
        "difficulty": "EASY",
        "question": "In database transaction management, what does the 'Atomicity' property guarantee?",
        "options": [
            "All operations within a transaction execute completely or none are applied (all-or-nothing)",
            "Transactions execute concurrently without interfering with each other",
            "Database state strictly satisfies all schema integrity constraints after commit",
            "Committed data is immediately mirrored across multiple disk arrays"
        ],
        "correct_answer": "All operations within a transaction execute completely or none are applied (all-or-nothing)",
        "explanation": "Atomicity ensures that a transaction is treated as a single indivisible unit: either all its modifications take effect or none do.",
        "marks": 1
    },

    # -------------------------------------------------------------
    # 3. WEEK 5 QUIZ: Trees, Window Functions, Indexing & OS Processes (10 Questions)
    # -------------------------------------------------------------
    {
        "id": "w5-q1",
        "assessment_id": "week-5-quiz",
        "question_number": 1,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Binary Trees",
        "difficulty": "EASY",
        "question": "Which tree traversal produces keys in strictly ascending sorted order when executed on a valid Binary Search Tree (BST)?",
        "options": ["Preorder Traversal", "Inorder Traversal", "Postorder Traversal", "Level-order Traversal"],
        "correct_answer": "Inorder Traversal",
        "explanation": "Inorder traversal (Left -> Node -> Right) on a BST processes nodes in non-decreasing sorted order.",
        "marks": 1
    },
    {
        "id": "w5-q2",
        "assessment_id": "week-5-quiz",
        "question_number": 2,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Binary Trees",
        "difficulty": "MEDIUM",
        "question": "In a BST, if both target nodes `p` and `q` have values strictly smaller than `root.val`, where is their Lowest Common Ancestor (LCA)?",
        "options": [
            "At root itself",
            "In the root.left subtree",
            "In the root.right subtree",
            "Undefined"
        ],
        "correct_answer": "In the root.left subtree",
        "explanation": "By BST properties, all values strictly smaller than `root.val` reside exclusively in the left subtree, so the LCA must be in `root.left`.",
        "marks": 1
    },
    {
        "id": "w5-q3",
        "assessment_id": "week-5-quiz",
        "question_number": 3,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Binary Trees",
        "difficulty": "EASY",
        "question": "What is the recursive formula for calculating the maximum height (depth) of a binary tree rooted at `node`?",
        "options": [
            "height(node) = height(node.left) + height(node.right)",
            "height(node) = 1 + max(height(node.left), height(node.right))",
            "height(node) = 1 + min(height(node.left), height(node.right))",
            "height(node) = max(height(node.left), height(node.right))"
        ],
        "correct_answer": "height(node) = 1 + max(height(node.left), height(node.right))",
        "explanation": "The height of a tree node is 1 (for the current node) plus the maximum depth of its left and right subtrees.",
        "marks": 1
    },
    {
        "id": "w5-q4",
        "assessment_id": "week-5-quiz",
        "question_number": 4,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Binary Search Trees",
        "difficulty": "MEDIUM",
        "question": "What is the worst-case time complexity of searching for a value in an unbalanced Binary Search Tree with N nodes?",
        "options": ["O(1)", "O(log N)", "O(N)", "O(N log N)"],
        "correct_answer": "O(N)",
        "explanation": "In the worst case (e.g., skewed tree like a linked list), searching an unbalanced BST takes O(N) linear time.",
        "marks": 1
    },
    {
        "id": "w5-q5",
        "assessment_id": "week-5-quiz",
        "question_number": 5,
        "question_type": "MCQ",
        "category": "SQL",
        "topic": "Window Functions",
        "difficulty": "MEDIUM",
        "question": "How does `DENSE_RANK()` differ from `RANK()` when ranking rows with identical values in SQL?",
        "options": [
            "DENSE_RANK() skips rank numbers after a tie (e.g. 1, 2, 2, 4), while RANK() does not skip (1, 2, 2, 3)",
            "DENSE_RANK() does not skip rank numbers after a tie (e.g. 1, 2, 2, 3), while RANK() skips (1, 2, 2, 4)",
            "DENSE_RANK() only works on unique numeric columns",
            "RANK() is an aggregate function, whereas DENSE_RANK() cannot use OVER()"
        ],
        "correct_answer": "DENSE_RANK() does not skip rank numbers after a tie (e.g. 1, 2, 2, 3), while RANK() skips (1, 2, 2, 4)",
        "explanation": "`RANK()` leaves gaps in the ranking sequence following tied values, whereas `DENSE_RANK()` produces consecutive integers without gaps.",
        "marks": 1
    },
    {
        "id": "w5-q6",
        "assessment_id": "week-5-quiz",
        "question_number": 6,
        "question_type": "MCQ",
        "category": "SQL",
        "topic": "Window Functions",
        "difficulty": "EASY",
        "question": "Which SQL window function allows accessing data from a subsequent row without performing a self-join?",
        "options": ["LAG()", "LEAD()", "FIRST_VALUE()", "NTILE()"],
        "correct_answer": "LEAD()",
        "explanation": "`LEAD()` provides access to a subsequent row at a specified physical offset, while `LAG()` accesses preceding rows.",
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
        "question": "Why are B+ Trees preferred over standard Binary Search Trees for relational database disk indexing?",
        "options": [
            "B+ Trees have a high branching factor, keeping tree height shallow (3-4 levels) to minimize disk I/O reads",
            "B+ Trees only reside in memory and never persist to disk",
            "Binary Search Trees cannot support equality searches",
            "B+ Trees store duplicate keys without any pointer overhead"
        ],
        "correct_answer": "B+ Trees have a high branching factor, keeping tree height shallow (3-4 levels) to minimize disk I/O reads",
        "explanation": "A high fan-out keeps the B+ tree depth very low, dramatically reducing expensive disk page I/O operations.",
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
        "question": "How many Clustered Indexes can exist on a single table in a relational database?",
        "options": ["Exactly 1", "Up to 16", "Unlimited", "Zero"],
        "correct_answer": "Exactly 1",
        "explanation": "A Clustered Index defines the physical sorting order of table rows on disk. Since data can only be physically stored in one sequence, only 1 clustered index is permitted per table.",
        "marks": 1
    },
    {
        "id": "w5-q9",
        "assessment_id": "week-5-quiz",
        "question_number": 9,
        "question_type": "MCQ",
        "category": "OS",
        "topic": "Processes & Threads",
        "difficulty": "EASY",
        "question": "Which memory segment is shared among all threads belonging to the same process?",
        "options": ["Stack memory", "Registers and Program Counter", "Heap and Data/Code segment", "Thread Local Storage"],
        "correct_answer": "Heap and Data/Code segment",
        "explanation": "Threads of the same process share the virtual address space (Heap, global variables, code segment, and file descriptors), but maintain independent execution Stacks.",
        "marks": 1
    },
    {
        "id": "w5-q10",
        "assessment_id": "week-5-quiz",
        "question_number": 10,
        "question_type": "MCQ",
        "category": "OS",
        "topic": "CPU Scheduling & Context Switching",
        "difficulty": "MEDIUM",
        "question": "Where does the Operating System kernel store the CPU registers and Program Counter during a process context switch?",
        "options": ["Process Control Block (PCB)", "File Allocation Table (FAT)", "Translation Lookaside Buffer (TLB)", "Direct Memory Access (DMA) buffer"],
        "correct_answer": "Process Control Block (PCB)",
        "explanation": "The PCB (Process Control Block) preserves all state information (CPU registers, PC, stack pointer, priority) so the process can resume execution seamlessly.",
        "marks": 1
    },

    # -------------------------------------------------------------
    # 4. WEEK 7 QUIZ: Recursion, Backtracking, Networks & Architecture (10 Questions)
    # -------------------------------------------------------------
    {
        "id": "w7-q1",
        "assessment_id": "week-7-quiz",
        "question_number": 1,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Recursion",
        "difficulty": "EASY",
        "question": "What is the primary cause of a 'Stack Overflow' error during execution of a recursive function?",
        "options": [
            "Missing or unreachable base case causing infinite call frame allocations on the execution stack",
            "Exceeding allocated heap dynamic memory",
            "Accessing an array index out of bounds",
            "Failure to compile bytecode"
        ],
        "correct_answer": "Missing or unreachable base case causing infinite call frame allocations on the execution stack",
        "explanation": "Each recursive call allocates a stack frame; without a terminating base case, the recursion consumes all stack memory, triggering a stack overflow.",
        "marks": 1
    },
    {
        "id": "w7-q2",
        "assessment_id": "week-7-quiz",
        "question_number": 2,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Backtracking",
        "difficulty": "MEDIUM",
        "question": "In backtracking algorithms (e.g. generating all Subsets or Permutations), what is the purpose of the 'undo' / 'backtrack' step?",
        "options": [
            "To restore the state so sibling exploration paths evaluate correct candidate choices",
            "To double the recursion depth limit",
            "To sort the output array in ascending order",
            "To bypass base case verification"
        ],
        "correct_answer": "To restore the state so sibling exploration paths evaluate correct candidate choices",
        "explanation": "Backtracking explores choice trees by mutating state, recursing forward, and explicitly reverting (undoing) the change when returning so other branches see a clean state.",
        "marks": 1
    },
    {
        "id": "w7-q3",
        "assessment_id": "week-7-quiz",
        "question_number": 3,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Backtracking",
        "difficulty": "MEDIUM",
        "question": "In the N-Queens problem, what optimization is used to prune invalid search branches in O(1) time?",
        "options": [
            "Using boolean arrays / hash sets to track occupied columns, main diagonals, and anti-diagonals",
            "Sorting the chessboard rows before placing queens",
            "Running Floyd-Warshall on the board matrix",
            "Using Dijkstra's algorithm to find shortest queen paths"
        ],
        "correct_answer": "Using boolean arrays / hash sets to track occupied columns, main diagonals, and anti-diagonals",
        "explanation": "Tracking occupied columns (`col`), main diagonals (`row - col`), and anti-diagonals (`row + col`) allows constant-time safety verification before placing a queen.",
        "marks": 1
    },
    {
        "id": "w7-q4",
        "assessment_id": "week-7-quiz",
        "question_number": 4,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Graphs Revision",
        "difficulty": "EASY",
        "question": "What is the time complexity of Breadth-First Search (BFS) on an adjacency list graph with V vertices and E edges?",
        "options": ["O(V + E)", "O(V * E)", "O(V^2)", "O(E log V)"],
        "correct_answer": "O(V + E)",
        "explanation": "BFS visits every vertex once and explores every outgoing edge once, resulting in O(V + E) linear time.",
        "marks": 1
    },
    {
        "id": "w7-q5",
        "assessment_id": "week-7-quiz",
        "question_number": 5,
        "question_type": "MCQ",
        "category": "DSA",
        "topic": "Graphs Revision",
        "difficulty": "MEDIUM",
        "question": "A valid Topological Sort ordering can only be found for which class of graphs?",
        "options": [
            "Directed Acyclic Graphs (DAG)",
            "Any Directed Graph with cycles",
            "Undirected Complete Graphs",
            "Bipartite Graphs only"
        ],
        "correct_answer": "Directed Acyclic Graphs (DAG)",
        "explanation": "Topological Sort linearly orders vertices such that for every directed edge u -> v, u appears before v. If a cycle exists, no such linear order is mathematically possible.",
        "marks": 1
    },
    {
        "id": "w7-q6",
        "assessment_id": "week-7-quiz",
        "question_number": 6,
        "question_type": "MCQ",
        "category": "CN",
        "topic": "Networking Protocols",
        "difficulty": "MEDIUM",
        "question": "What protocol is used to map a known network-layer IP address to a physical data-link layer MAC address on a local area network?",
        "options": ["ARP (Address Resolution Protocol)", "DHCP", "DNS", "ICMP"],
        "correct_answer": "ARP (Address Resolution Protocol)",
        "explanation": "ARP broadcasts an IP query over Ethernet to discover the physical hardware MAC address corresponding to that target IP.",
        "marks": 1
    },
    {
        "id": "w7-q7",
        "assessment_id": "week-7-quiz",
        "question_number": 7,
        "question_type": "MCQ",
        "category": "CN",
        "topic": "Networking Protocols",
        "difficulty": "EASY",
        "question": "What core security mechanism differentiates HTTPS from plain HTTP?",
        "options": [
            "HTTPS encrypts communication using Transport Layer Security (TLS/SSL) with asymmetric and symmetric cryptography",
            "HTTPS uses UDP on port 80 to speed up page downloads",
            "HTTPS disables cookies and caching by default",
            "HTTPS compresses web payloads with Gzip at the router"
        ],
        "correct_answer": "HTTPS encrypts communication using Transport Layer Security (TLS/SSL) with asymmetric and symmetric cryptography",
        "explanation": "HTTPS runs standard HTTP over an encrypted TLS connection, providing confidentiality, data integrity, and server authentication.",
        "marks": 1
    },
    {
        "id": "w7-q8",
        "assessment_id": "week-7-quiz",
        "question_number": 8,
        "question_type": "MCQ",
        "category": "Computer Architecture",
        "topic": "Pipelining & Hazards",
        "difficulty": "MEDIUM",
        "question": "In CPU pipelining, what type of hazard occurs when an instruction depends on the result of a previous instruction that is still in execution?",
        "options": ["Data Hazard", "Structural Hazard", "Control Hazard", "Branch Penalty Hazard"],
        "correct_answer": "Data Hazard",
        "explanation": "A Data Hazard arises when instructions exhibit data dependencies (Read-After-Write, RAW) before the needed operand has been written back to registers.",
        "marks": 1
    },
    {
        "id": "w7-q9",
        "assessment_id": "week-7-quiz",
        "question_number": 9,
        "question_type": "MCQ",
        "category": "Computer Architecture",
        "topic": "RISC vs CISC",
        "difficulty": "EASY",
        "question": "Which characteristic is a hallmark of Reduced Instruction Set Computer (RISC) architectures like ARM?",
        "options": [
            "Fixed-length instructions executed in a single cycle with load/store memory access model",
            "Variable-length complex multi-cycle instructions with direct memory arithmetic",
            "Absence of general-purpose registers",
            "Microprogrammed complex control units"
        ],
        "correct_answer": "Fixed-length instructions executed in a single cycle with load/store memory access model",
        "explanation": "RISC focuses on simple, uniform fixed-length instructions executed rapidly via pipelining, allowing memory access exclusively through explicit LOAD and STORE instructions.",
        "marks": 1
    },
    {
        "id": "w7-q10",
        "assessment_id": "week-7-quiz",
        "question_number": 10,
        "question_type": "MCQ",
        "category": "Software Engineering",
        "topic": "Version Control",
        "difficulty": "EASY",
        "question": "What is the primary difference between `git merge` and `git rebase` when integrating feature branch changes?",
        "options": [
            "Git merge preserves complete commit history with a dedicated merge commit, while Git rebase rewrites project history linearly",
            "Git rebase deletes remote commits permanently",
            "Git merge is only used on local branches, while rebase is only used on origin/main",
            "There is no difference in Git commit topology"
        ],
        "correct_answer": "Git merge preserves complete commit history with a dedicated merge commit, while Git rebase rewrites project history linearly",
        "explanation": "`git merge` creates a non-destructive merge commit preserving exact branch history, whereas `git rebase` reapplies commits atop the base branch for a clean linear history.",
        "marks": 1
    },

    # -------------------------------------------------------------
    # 5. WEEK 9 QUIZ: Machine Learning Fundamentals & Algorithms (10 Questions)
    # -------------------------------------------------------------
    {
        "id": "w9-q1",
        "assessment_id": "week-9-quiz",
        "question_number": 1,
        "question_type": "MCQ",
        "category": "Machine Learning",
        "topic": "Learning Paradigms",
        "difficulty": "EASY",
        "question": "What distinguishes Supervised Learning from Unsupervised Learning?",
        "options": [
            "Supervised learning trains on labeled input-output pairs; unsupervised learning finds patterns/clusters in unlabeled data",
            "Supervised learning requires neural networks, whereas unsupervised learning only uses linear models",
            "Supervised learning does not use feature vectors",
            "Unsupervised learning always produces higher prediction accuracy"
        ],
        "correct_answer": "Supervised learning trains on labeled input-output pairs; unsupervised learning finds patterns/clusters in unlabeled data",
        "explanation": "Supervised learning maps features X to known ground-truth labels Y, whereas Unsupervised learning discovers intrinsic groupings without target labels.",
        "marks": 1
    },
    {
        "id": "w9-q2",
        "assessment_id": "week-9-quiz",
        "question_number": 2,
        "question_type": "MCQ",
        "category": "Machine Learning",
        "topic": "Bias-Variance Tradeoff",
        "difficulty": "MEDIUM",
        "question": "A machine learning model with high training accuracy (99%) but low validation accuracy (62%) is suffering from which problem?",
        "options": ["High Bias (Underfitting)", "High Variance (Overfitting)", "Data Leakage", "Vanishing Gradient"],
        "correct_answer": "High Variance (Overfitting)",
        "explanation": "Overfitting occurs when a model memorizes training noise rather than learning generalizable patterns, resulting in high variance and poor validation performance.",
        "marks": 1
    },
    {
        "id": "w9-q3",
        "assessment_id": "week-9-quiz",
        "question_number": 3,
        "question_type": "MCQ",
        "category": "Machine Learning",
        "topic": "Model Validation",
        "difficulty": "EASY",
        "question": "Why is K-Fold Cross-Validation preferred over a single train/test split on moderate-sized datasets?",
        "options": [
            "It trains and tests on all K partitions to produce a reliable, low-variance estimate of model generalization",
            "It guarantees zero training error on any model",
            "It converts non-linear datasets into linear relationships",
            "It eliminates the need for test data collection"
        ],
        "correct_answer": "It trains and tests on all K partitions to produce a reliable, low-variance estimate of model generalization",
        "explanation": "K-Fold evaluates model performance across K distinct folds, ensuring every sample is used for validation once, reducing evaluation variance.",
        "marks": 1
    },
    {
        "id": "w9-q4",
        "assessment_id": "week-9-quiz",
        "question_number": 4,
        "question_type": "MCQ",
        "category": "Machine Learning",
        "topic": "Regression & Classification",
        "difficulty": "MEDIUM",
        "question": "Which loss function is standard for training a binary Logistic Regression classifier?",
        "options": [
            "Binary Cross-Entropy (Log Loss)",
            "Mean Squared Error (MSE)",
            "Hinge Loss",
            "Mean Absolute Error (MAE)"
        ],
        "correct_answer": "Binary Cross-Entropy (Log Loss)",
        "explanation": "Binary Cross-Entropy (`- [y log(p) + (1-y) log(1-p)]`) is the convex maximum likelihood loss function for logistic probability outputs.",
        "marks": 1
    },
    {
        "id": "w9-q5",
        "assessment_id": "week-9-quiz",
        "question_number": 5,
        "question_type": "MCQ",
        "category": "Machine Learning",
        "topic": "Decision Trees",
        "difficulty": "MEDIUM",
        "question": "Which metric measures the impurity of a dataset node when building a classification Decision Tree?",
        "options": ["Gini Impurity / Entropy", "R-squared Score", "Euclidean Distance", "Cosine Similarity"],
        "correct_answer": "Gini Impurity / Entropy",
        "explanation": "Decision trees evaluate split quality using Gini Impurity or Information Gain (Entropy reduction) to create homogeneous child leaves.",
        "marks": 1
    },
    {
        "id": "w9-q6",
        "assessment_id": "week-9-quiz",
        "question_number": 6,
        "question_type": "MCQ",
        "category": "Machine Learning",
        "topic": "Ensemble Methods",
        "difficulty": "MEDIUM",
        "question": "How does Random Forest reduce model variance compared to an individual deep Decision Tree?",
        "options": [
            "By training multiple decorrelated trees on bootstrap samples and random feature subsets, then averaging their predictions (Bagging)",
            "By boosting sequential residuals with gradient descent",
            "By pruning all tree branches to depth 1",
            "By converting trees into neural layers"
        ],
        "correct_answer": "By training multiple decorrelated trees on bootstrap samples and random feature subsets, then averaging their predictions (Bagging)",
        "explanation": "Random Forest uses Bootstrap Aggregation (Bagging) plus feature sub-sampling to decorrelate individual trees; averaging their outputs significantly reduces variance without increasing bias.",
        "marks": 1
    },
    {
        "id": "w9-q7",
        "assessment_id": "week-9-quiz",
        "question_number": 7,
        "question_type": "MCQ",
        "category": "Machine Learning",
        "topic": "KNN",
        "difficulty": "EASY",
        "question": "Why is feature scaling (e.g. StandardScaler / MinMaxScaler) critical before running K-Nearest Neighbors (KNN)?",
        "options": [
            "KNN relies on distance metrics (e.g. Euclidean distance), so unscaled large-magnitude features will dominate neighbor calculations",
            "KNN cannot compute gradients without scaling",
            "KNN only accepts input values between 0 and 1",
            "Scaling prevents matrix inversion singularity"
        ],
        "correct_answer": "KNN relies on distance metrics (e.g. Euclidean distance), so unscaled large-magnitude features will dominate neighbor calculations",
        "explanation": "Distance-based algorithms like KNN measure spatial proximity; features with larger numeric scales disproportionately dictate distance calculations if not normalized.",
        "marks": 1
    },
    {
        "id": "w9-q8",
        "assessment_id": "week-9-quiz",
        "question_number": 8,
        "question_type": "MCQ",
        "category": "Machine Learning",
        "topic": "Naive Bayes",
        "difficulty": "EASY",
        "question": "What is the core 'naive' independence assumption in the Naive Bayes classifier?",
        "options": [
            "All input features are conditionally independent of each other given the class label",
            "All classes have an equal prior probability of 0.5",
            "The data distribution is strictly linear and separable",
            "The model ignores outliers automatically"
        ],
        "correct_answer": "All input features are conditionally independent of each other given the class label",
        "explanation": "Naive Bayes simplifies Bayes theorem by assuming features are conditionally independent given class y: `P(X|y) = ∏ P(x_i|y)`.",
        "marks": 1
    },
    {
        "id": "w9-q9",
        "assessment_id": "week-9-quiz",
        "question_number": 9,
        "question_type": "MCQ",
        "category": "Machine Learning",
        "topic": "Evaluation Metrics",
        "difficulty": "MEDIUM",
        "question": "In medical disease detection where missing a sick patient (False Negative) is catastrophic, which metric should be prioritized?",
        "options": ["Recall (Sensitivity)", "Precision", "Accuracy", "Specificity"],
        "correct_answer": "Recall (Sensitivity)",
        "explanation": "Recall is `TP / (TP + FN)`. Maximizing recall minimizes False Negatives (missed positive cases).",
        "marks": 1
    },
    {
        "id": "w9-q10",
        "assessment_id": "week-9-quiz",
        "question_number": 10,
        "question_type": "MCQ",
        "category": "Data Science",
        "topic": "EDA & Outliers",
        "difficulty": "MEDIUM",
        "question": "In Exploratory Data Analysis (EDA), what is the standard Tukey boxplot formula for identifying outlier boundaries using Interquartile Range (IQR = Q3 - Q1)?",
        "options": [
            "Values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR",
            "Values below Mean - 1.5*IQR or above Mean + 1.5*IQR",
            "Values below Q1 - 3*IQR or above Q3 + 3*IQR only",
            "Values strictly exceeding 2 standard deviations"
        ],
        "correct_answer": "Values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR",
        "explanation": "Tukey's IQR method defines standard outlier fences at `[Q1 - 1.5 * IQR, Q3 + 1.5 * IQR]`.",
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
