CURRICULUM_VERSION = "1.0"

CURRICULUM = [
    {
        "week_number": 1,
        "title": "Foundations & Programming (Python & C++)",
        "description": "Establish your programming foundation, review core language syntax, and practice basic manipulation.",
        "tasks": [
            {"day_number": 1, "title": "Setup environment and review Git basics", "category": "Software Engineering", "estimated_minutes": 45, "description": "Ensure your local IDE is ready, and review Git add, commit, push, and branching."},
            {"day_number": 2, "title": "Practice Python data types, loops, and functions", "category": "Python", "estimated_minutes": 60, "description": "Write small scripts covering lists, dictionaries, list comprehensions, and functions."},
            {"day_number": 3, "title": "Practice C++ pointers, references, and memory", "category": "C++", "estimated_minutes": 60, "description": "Review pointer arithmetic, pass-by-reference, and dynamic memory allocation."},
            {"day_number": 4, "title": "Solve 3 basic string manipulation problems", "category": "Problem Solving", "estimated_minutes": 60, "description": "Focus on reversing strings, checking palindromes, and character counting."},
            {"day_number": 5, "title": "Solve 3 basic array manipulation problems", "category": "Problem Solving", "estimated_minutes": 60, "description": "Focus on finding max/min elements, reversing arrays, and basic shifting."},
            {"day_number": 6, "title": "Review Time & Space Complexity (Big-O)", "category": "DSA", "estimated_minutes": 45, "description": "Understand O(1), O(N), O(N^2), O(log N), and analyze your previous solutions."}
        ]
    },
    {
        "week_number": 2,
        "title": "Core DSA - Arrays, Strings, Hashing",
        "description": "Dive into the most frequently asked data structures in early interview rounds.",
        "tasks": [
            {"day_number": 1, "title": "Practice array traversal and prefix sums", "category": "DSA", "estimated_minutes": 90, "description": "Solve problems using prefix sum arrays to quickly find subarray sums."},
            {"day_number": 2, "title": "Practice hash maps for frequency counting", "category": "DSA", "estimated_minutes": 90, "description": "Use hash maps to solve pair-finding (e.g., Two Sum) and counting problems."},
            {"day_number": 3, "title": "Solve 3 two-pointer problems", "category": "DSA", "estimated_minutes": 60, "description": "Apply the two-pointer technique on sorted arrays (e.g., removing duplicates)."},
            {"day_number": 4, "title": "Solve 3 string matching and palindrome problems", "category": "DSA", "estimated_minutes": 60, "description": "Focus on valid palindrome variations and substring searching basic logic."},
            {"day_number": 5, "title": "Practice basic recursion on strings and arrays", "category": "DSA", "estimated_minutes": 60, "description": "Understand the call stack by reversing strings recursively and finding factorials."}
        ]
    },
    {
        "week_number": 3,
        "title": "Core DSA - Linked Lists, Stacks, Queues",
        "description": "Master sequential dynamic data structures and LIFO/FIFO patterns.",
        "tasks": [
            {"day_number": 1, "title": "Implement a singly linked list and reverse it", "category": "DSA", "estimated_minutes": 60, "description": "Write a node class and manually reverse the pointers iteratively."},
            {"day_number": 2, "title": "Solve cycle detection and middle element problems", "category": "DSA", "estimated_minutes": 60, "description": "Apply the slow/fast pointer (Tortoise and Hare) algorithm."},
            {"day_number": 3, "title": "Implement a stack and solve balanced parentheses", "category": "DSA", "estimated_minutes": 60, "description": "Use a list/array as a stack to validate parenthesis strings."},
            {"day_number": 4, "title": "Practice queue operations and monotonic stacks", "category": "DSA", "estimated_minutes": 90, "description": "Solve 'Next Greater Element' using a monotonic stack."},
            {"day_number": 5, "title": "Complete a timed 1-hour coding assessment", "category": "Assessment", "estimated_minutes": 60, "description": "Pick 2 easy and 1 medium question on Arrays/Strings/Linked Lists and solve them strictly within 60 minutes."}
        ]
    },
    {
        "week_number": 4,
        "title": "Advanced DSA - Trees, Heaps, Basic Graphs",
        "description": "Explore hierarchical data structures and network connectivity basics.",
        "tasks": [
            {"day_number": 1, "title": "Implement a BST and perform DFS traversals", "category": "DSA", "estimated_minutes": 90, "description": "Code In-order, Pre-order, and Post-order traversals recursively."},
            {"day_number": 2, "title": "Practice BFS (Level Order Traversal) on trees", "category": "DSA", "estimated_minutes": 60, "description": "Use a queue to traverse a binary tree level by level."},
            {"day_number": 3, "title": "Solve 3 heap/priority queue problems", "category": "DSA", "estimated_minutes": 90, "description": "Solve Top K Frequent Elements or Kth Largest Element using heaps."},
            {"day_number": 4, "title": "Implement basic graph representation", "category": "DSA", "estimated_minutes": 90, "description": "Represent a graph using an adjacency list and perform basic DFS/BFS."},
            {"day_number": 5, "title": "Solve 2 graph connectivity / island problems", "category": "DSA", "estimated_minutes": 60, "description": "Apply grid-based DFS to solve 'Number of Islands' type problems."}
        ]
    },
    {
        "week_number": 5,
        "title": "Object-Oriented Programming (OOP)",
        "description": "Understand core software design paradigms expected in technical interviews.",
        "tasks": [
            {"day_number": 1, "title": "Explain Classes, Objects, and Encapsulation", "category": "OOP", "estimated_minutes": 60, "description": "Write code examples demonstrating private variables and getters/setters."},
            {"day_number": 2, "title": "Practice Inheritance and Polymorphism", "category": "OOP", "estimated_minutes": 60, "description": "Create a base class and derived classes demonstrating method overriding."},
            {"day_number": 3, "title": "Review Abstraction, Interfaces, and Composition", "category": "OOP", "estimated_minutes": 60, "description": "Understand 'has-a' vs 'is-a' relationships in system design."},
            {"day_number": 4, "title": "Solve 3 common OOP interview design questions", "category": "OOP", "estimated_minutes": 90, "description": "E.g., Design a Parking Lot, Library Management System, or Deck of Cards."},
            {"day_number": 5, "title": "Review SOLID principles", "category": "OOP", "estimated_minutes": 60, "description": "Understand Single Responsibility, Open/Closed, Liskov, Interface Segregation, and Dependency Inversion."}
        ]
    },
    {
        "week_number": 6,
        "title": "Relational Databases & SQL",
        "description": "Master data storage, querying, and relational design concepts.",
        "tasks": [
            {"day_number": 1, "title": "Review normalization, ACID, and basic keys", "category": "DBMS", "estimated_minutes": 60, "description": "Understand 1NF/2NF/3NF, primary keys, and foreign keys."},
            {"day_number": 2, "title": "Write basic SELECT, filtering, and sorting queries", "category": "SQL", "estimated_minutes": 45, "description": "Practice WHERE, ORDER BY, IN, LIKE, and basic logical operators."},
            {"day_number": 3, "title": "Solve 3 SQL JOIN and subquery problems", "category": "SQL", "estimated_minutes": 90, "description": "Practice INNER JOIN, LEFT JOIN, and writing nested SELECT queries."},
            {"day_number": 4, "title": "Practice GROUP BY, HAVING, and aggregation", "category": "SQL", "estimated_minutes": 60, "description": "Use COUNT, SUM, AVG along with grouping clauses."},
            {"day_number": 5, "title": "Review indexing concepts and optimization", "category": "DBMS", "estimated_minutes": 60, "description": "Understand how B-Tree indexes speed up lookups and the cost of indexing."}
        ]
    },
    {
        "week_number": 7,
        "title": "Core CS - Operating Systems",
        "description": "Review fundamental low-level system concepts and concurrency.",
        "tasks": [
            {"day_number": 1, "title": "Explain process vs thread and memory layout", "category": "Operating Systems", "estimated_minutes": 60, "description": "Understand the heap, stack, data, and text segments of a process."},
            {"day_number": 2, "title": "Review CPU scheduling algorithms", "category": "Operating Systems", "estimated_minutes": 60, "description": "Review FCFS, Round Robin, SJF, and context switching overhead."},
            {"day_number": 3, "title": "Explain synchronization, mutexes, and deadlocks", "category": "Operating Systems", "estimated_minutes": 90, "description": "Understand race conditions, semaphores, and the 4 Coffman conditions for deadlocks."},
            {"day_number": 4, "title": "Review memory management and virtual memory", "category": "Operating Systems", "estimated_minutes": 60, "description": "Explain paging, segmentation, and page faults."},
            {"day_number": 5, "title": "Answer 10 rapid-fire OS interview questions", "category": "Mock Interviews", "estimated_minutes": 45, "description": "Test your active recall on core OS concepts without looking at notes."}
        ]
    },
    {
        "week_number": 8,
        "title": "Core CS - Computer Networks & Architecture",
        "description": "Understand how computers communicate and execute instructions.",
        "tasks": [
            {"day_number": 1, "title": "Explain OSI & TCP/IP models", "category": "Computer Networks", "estimated_minutes": 60, "description": "Understand the responsibilities of the 7 layers of OSI."},
            {"day_number": 2, "title": "Differentiate TCP vs UDP and the 3-way handshake", "category": "Computer Networks", "estimated_minutes": 60, "description": "Understand connection-oriented vs connectionless protocols."},
            {"day_number": 3, "title": "Review HTTP/HTTPS, DNS, and basic routing", "category": "Computer Networks", "estimated_minutes": 60, "description": "Explain what happens when you type a URL into a browser."},
            {"day_number": 4, "title": "Explain CPU pipeline, cache hierarchy, and registers", "category": "Computer Architecture", "estimated_minutes": 60, "description": "Understand L1/L2/L3 cache, memory latency, and instruction pipelining."},
            {"day_number": 5, "title": "Complete a timed 1-hour CS fundamentals assessment", "category": "Assessment", "estimated_minutes": 60, "description": "Answer a mix of DBMS, OS, CN, and Architecture MCQ/Short-answer questions."}
        ]
    },
    {
        "week_number": 9,
        "title": "Software Engineering & Backend Basics",
        "description": "Apply computer science to modern software development and API design.",
        "tasks": [
            {"day_number": 1, "title": "Review SDLC models, Git branching, and PRs", "category": "Software Engineering", "estimated_minutes": 60, "description": "Understand Agile/Scrum basics, Git merge vs rebase, and code review etiquette."},
            {"day_number": 2, "title": "Explain REST API principles and HTTP status codes", "category": "SDE / Backend", "estimated_minutes": 45, "description": "Understand GET/POST/PUT/PATCH/DELETE and the 200/300/400/500 code families."},
            {"day_number": 3, "title": "Review Authentication vs Authorization", "category": "SDE / Backend", "estimated_minutes": 60, "description": "Explain JWTs, session cookies, and basic RBAC concepts."},
            {"day_number": 4, "title": "Practice writing unit tests", "category": "Software Engineering", "estimated_minutes": 60, "description": "Write test cases for a simple function handling edge cases, nulls, and boundaries."},
            {"day_number": 5, "title": "Explain basic system design concepts", "category": "SDE / Backend", "estimated_minutes": 90, "description": "Understand load balancing, horizontal vs vertical scaling, and caching."}
        ]
    },
    {
        "week_number": 10,
        "title": "Data Science & AI/ML Fundamentals",
        "description": "Review baseline data manipulation and machine learning terminology.",
        "tasks": [
            {"day_number": 1, "title": "Practice basic NumPy and Pandas filtering", "category": "Data Science", "estimated_minutes": 90, "description": "Write code to manipulate arrays and filter DataFrames."},
            {"day_number": 2, "title": "Review missing value handling and merging in Pandas", "category": "Data Science", "estimated_minutes": 60, "description": "Practice fillna, dropna, groupby, and merge operations."},
            {"day_number": 3, "title": "Explain Supervised vs Unsupervised learning", "category": "AI/ML", "estimated_minutes": 60, "description": "Understand classification vs regression and clustering."},
            {"day_number": 4, "title": "Review evaluation metrics and Overfitting", "category": "AI/ML", "estimated_minutes": 60, "description": "Explain accuracy, precision, recall, F1 score, bias/variance tradeoff."},
            {"day_number": 5, "title": "Answer 5 basic ML conceptual interview questions", "category": "Mock Interviews", "estimated_minutes": 45, "description": "Test your ability to concisely explain ML concepts to a non-expert."}
        ]
    },
    {
        "week_number": 11,
        "title": "Portfolio Projects & Explanations",
        "description": "Prepare to defend your resume and articulate your technical decisions.",
        "tasks": [
            {"day_number": 1, "title": "Prepare a technical self-introduction", "category": "Projects", "estimated_minutes": 60, "description": "Draft a 90-second elevator pitch covering your education, skills, and top project."},
            {"day_number": 2, "title": "Draft a 2-minute architectural explanation of a project", "category": "Projects", "estimated_minutes": 60, "description": "Explain the tech stack, data flow, and why you chose specific tools."},
            {"day_number": 3, "title": "Document the database design of your project", "category": "Projects", "estimated_minutes": 45, "description": "Be ready to draw or explain your database schema, relationships, and queries."},
            {"day_number": 4, "title": "Identify and explain your most complex bug", "category": "Projects", "estimated_minutes": 45, "description": "Prepare a STAR method response detailing a bug, your debugging process, and the fix."},
            {"day_number": 5, "title": "Enhance a project README", "category": "Projects", "estimated_minutes": 60, "description": "Ensure at least one GitHub project has a stellar README with setup steps and architecture."}
        ]
    },
    {
        "week_number": 12,
        "title": "Final Revision & Mock Interviews",
        "description": "Consolidate your knowledge and polish your interview performance.",
        "tasks": [
            {"day_number": 1, "title": "Revise weak topics in DSA (Trees/Graphs/DP)", "category": "Revision", "estimated_minutes": 90, "description": "Re-solve 3 problems you previously struggled with."},
            {"day_number": 2, "title": "Revise weak topics in Core CS (OS/CN/SQL)", "category": "Revision", "estimated_minutes": 90, "description": "Review flashcards or summaries for theoretical subjects."},
            {"day_number": 3, "title": "Practice answering behavioral questions (STAR method)", "category": "Mock Interviews", "estimated_minutes": 60, "description": "Prepare answers for leadership, conflict resolution, and failure questions."},
            {"day_number": 4, "title": "Conduct a full 45-minute technical mock interview", "category": "Mock Interviews", "estimated_minutes": 60, "description": "Do a peer mock interview or record yourself solving a problem while talking out loud."},
            {"day_number": 5, "title": "Final review of project defense and technical communication", "category": "Revision", "estimated_minutes": 60, "description": "Review your resume top-to-bottom and ensure you can explain every bullet point."}
        ]
    }
]
