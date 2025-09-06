# More Assessment API Requests - Advanced Examples & Edge Cases

## Overview
This document provides comprehensive examples of assessment-related API requests covering various edge cases, complex scenarios, and unique use cases. All examples show only request formats without responses.

## Important Field Explanations

### Assessment Sets Concept
- **`num_of_sets`**: Total number of question sets in the assessment (e.g., 3 means there are 3 different versions/sets)
- **`set_number`**: Which specific set each question belongs to (1, 2, 3, etc.)

**Example**: If `num_of_sets = 3`, you should have questions with `set_number: 1`, `set_number: 2`, and `set_number: 3`. This allows:
- **Randomization**: Students get different question sets
- **Security**: Prevents cheating by giving different questions to different students
- **Adaptive Testing**: Different difficulty levels for different student groups
- **A/B Testing**: Compare performance across different question variations

**Usage Scenarios**:
- Set 1: Beginner level questions
- Set 2: Intermediate level questions  
- Set 3: Advanced level questions

OR

- Set 1: Version A of questions
- Set 2: Version B of questions (same difficulty, different questions)
- Set 3: Version C of questions (same difficulty, different questions)

---

## Assessment Creation - Advanced Examples

### 1. Large-Scale Mixed Assessment (Maximum Complexity)
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Enterprise Software Engineering Comprehensive Evaluation 2025",
  "assessment_type": "mix",
  "assessment_description": "A comprehensive 4-hour assessment covering full-stack development, system design, algorithm optimization, database management, cloud architecture, and software engineering principles. Designed for senior-level software engineers with 3+ years of experience.",
  "passing_marks": 420,
  "total_marks": 600,
  "num_of_sets": 3,
  "section_names": [
    "Data Structures & Algorithms",
    "System Design & Architecture", 
    "Full-Stack Development",
    "Database Design & Optimization",
    "Cloud Computing & DevOps",
    "Software Engineering Principles",
    "Problem Solving & Critical Thinking"
  ],
  "section_descriptions": [
    "Advanced algorithmic problem solving, time complexity analysis, and optimization techniques including dynamic programming, graph algorithms, and advanced data structures.",
    "Large-scale system design, microservices architecture, load balancing, caching strategies, and distributed systems concepts with real-world scenarios.",
    "End-to-end application development covering React.js, Node.js, REST APIs, authentication, state management, and modern web development practices.",
    "Advanced SQL queries, database normalization, indexing strategies, NoSQL databases, query optimization, and transaction management.",
    "AWS/Azure cloud services, containerization with Docker, Kubernetes orchestration, CI/CD pipelines, infrastructure as code, and monitoring.",
    "SOLID principles, design patterns, code review practices, testing strategies, agile methodologies, and software lifecycle management.",
    "Analytical thinking, debugging skills, performance optimization, and creative problem-solving approaches to complex technical challenges."
  ],
  "start_time": "2025-09-25T08:00:00Z",
  "end_time": "2025-09-25T12:30:00Z",
  "is_electron_only": true,
  "num_of_ai_generated_questions": 25,
  "is_proctored": true,
  "is_published": false,
  "attachments": [
    "https://s3.amazonaws.com/assessments/system-design-diagrams.pdf",
    "https://s3.amazonaws.com/assessments/database-schema-reference.png",
    "https://s3.amazonaws.com/assessments/api-documentation.html",
    "https://s3.amazonaws.com/assessments/performance-requirements.pdf",
    "https://s3.amazonaws.com/assessments/cloud-architecture-template.svg"
  ],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Given the system architecture diagram in $1, what is the time complexity of the shortest path algorithm used in the microservice mesh routing? Consider the graph has V vertices and E edges.",
      "options": [
        "O(V + E) using BFS",
        "O(V²) using Floyd-Warshall", 
        "O((V + E) log V) using Dijkstra with priority queue",
        "O(VE) using Bellman-Ford",
        "O(E log E) using Kruskal's algorithm"
      ],
      "correct_option_index": 2,
      "positive_marks": 8,
      "negative_marks": -2,
      "time_limit": 180
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Implement a thread-safe LRU Cache with TTL (Time To Live) functionality. The cache should support get(), put(), and cleanup() operations. Refer to the performance requirements in $4 for optimization constraints.",
      "description": "Design and implement a Least Recently Used (LRU) cache that automatically expires entries after a specified time-to-live (TTL) period. The implementation must be thread-safe and optimized for high-concurrency scenarios with minimal lock contention.",
      "constraints": [
        "1 <= capacity <= 10^6",
        "1 <= key length <= 100 characters",
        "1 <= value size <= 1MB",
        "TTL range: 1 second to 24 hours",
        "Must handle 10^5 concurrent operations per second",
        "Memory usage should not exceed capacity * 1.2",
        "Cleanup operation should complete in O(expired_items) time"
      ],
      "positive_marks": 25,
      "negative_marks": 0,
      "time_limit": 2700,
      "test_cases": {
        "examples": [
          {
            "input": "LRUCache cache = new LRUCache(2, 5); cache.put('a', 1); cache.put('b', 2); sleep(6); cache.get('a');",
            "output": "null"
          },
          {
            "input": "LRUCache cache = new LRUCache(3, 10); cache.put('x', 100); cache.put('y', 200); cache.get('x'); cache.put('z', 300); cache.get('y');",
            "output": "200"
          }
        ],
        "hidden": [
          {
            "input": "Concurrent test with 1000 threads performing mixed operations",
            "output": "No race conditions, all operations complete successfully"
          },
          {
            "input": "Memory stress test with capacity 100000",
            "output": "Memory usage within bounds, no memory leaks"
          }
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 2,
      "question_text": "Based on the cloud architecture template in $5, if the system handles 1 million requests per day with 99.9% uptime requirement, and each request processes an average of 50KB data, what would be the minimum required specifications for the auto-scaling group?",
      "options": [
        "Min: 2 instances (t3.medium), Max: 10 instances, Target CPU: 70%",
        "Min: 3 instances (t3.large), Max: 15 instances, Target CPU: 60%", 
        "Min: 4 instances (c5.xlarge), Max: 20 instances, Target CPU: 50%",
        "Min: 5 instances (m5.large), Max: 25 instances, Target CPU: 80%",
        "Min: 6 instances (t3.xlarge), Max: 30 instances, Target CPU: 40%"
      ],
      "correct_option_index": 1,
      "positive_marks": 12,
      "negative_marks": -3,
      "time_limit": 300
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 3,
      "question_text": "Implement a distributed rate limiter using the Token Bucket algorithm that can handle 1M requests per second across multiple servers. The system should maintain consistency across all nodes and handle server failures gracefully. Refer to performance requirements in $4.",
      "description": "Design a horizontally scalable rate limiting system using token bucket algorithm with distributed coordination and fault tolerance.",
      "constraints": [
        "Support 1M+ requests per second globally",
        "Maintain consistency across 100+ servers",
        "Handle node failures without rate limit violations",
        "Token refill rate: configurable per client",
        "Burst capacity: configurable per client",
        "Response time: < 1ms for rate limit decisions",
        "Memory usage per server: < 2GB for 1M clients"
      ],
      "positive_marks": 35,
      "negative_marks": 0,
      "time_limit": 3600,
      "test_cases": {
        "examples": [
          {
            "input": "Configure limiter: 1000 tokens/sec, burst=5000; Send 5000 requests instantly",
            "output": "5000 requests allowed, subsequent requests blocked until refill"
          },
          {
            "input": "Simulate server failure during high load",
            "output": "Rate limiting continues with remaining servers, no violations"
          }
        ],
        "hidden": [
          {
            "input": "Stress test with 1M concurrent clients across 50 servers",
            "output": "All rate limits enforced correctly, sub-millisecond response times"
          },
          {
            "input": "Network partition scenario with split-brain prevention",
            "output": "Conservative rate limiting maintained, no double-allocation of tokens"
          }
        ]
      }
    }
  ]
}
```

### 2. Pure Coding Assessment (Programming Contest Style)
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Advanced Algorithm Programming Challenge - ICPC Style",
  "assessment_type": "coding",
  "assessment_description": "Competitive programming assessment featuring algorithmic challenges similar to ACM ICPC contests. Problems range from medium to extremely difficult, testing advanced problem-solving skills, mathematical reasoning, and implementation efficiency.",
  "passing_marks": 200,
  "total_marks": 500,
  "num_of_sets": 3,
  "section_names": [
    "Dynamic Programming & Optimization",
    "Graph Theory & Network Flows",
    "Number Theory & Combinatorics",
    "Geometry & Computational Mathematics"
  ],
  "section_descriptions": [
    "Complex dynamic programming problems including state-space optimization, digit DP, and advanced recurrence relations.",
    "Advanced graph algorithms, maximum flow problems, minimum cut, bipartite matching, and network optimization.",
    "Modular arithmetic, prime number theory, combinatorial mathematics, and discrete probability problems.",
    "Computational geometry, convex hull algorithms, line intersection, and spatial data structure problems."
  ],
  "start_time": "2025-10-15T09:00:00Z",
  "end_time": "2025-10-15T14:00:00Z",
  "is_electron_only": true,
  "num_of_ai_generated_questions": 0,
  "is_proctored": true,
  "is_published": false,
  "attachments": [
    "https://s3.amazonaws.com/contests/algorithm-reference-guide.pdf",
    "https://s3.amazonaws.com/contests/mathematical-formulas.pdf",
    "https://s3.amazonaws.com/contests/graph-theory-diagrams.png"
  ],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "The Matrix Chain Multiplication Optimization Problem: Given a sequence of matrices A₁, A₂, ..., Aₙ where matrix Aᵢ has dimensions pᵢ₋₁ × pᵢ, find the minimum number of scalar multiplications needed to compute the product A₁A₂...Aₙ. Additionally, reconstruct and output the optimal parenthesization. Refer to optimization techniques in $1.",
      "description": "Implement an efficient solution to find both the minimum cost and the optimal way to parenthesize matrix chain multiplication. Your solution should handle edge cases and provide the actual parenthesization string.",
      "constraints": [
        "2 ≤ n ≤ 500 (number of matrices)",
        "1 ≤ pᵢ ≤ 1000 (matrix dimensions)",
        "Time limit: 2 seconds",
        "Memory limit: 256 MB",
        "Output format: minimum cost on first line, parenthesization on second line"
      ],
      "positive_marks": 50,
      "negative_marks": 0,
      "time_limit": 3600,
      "test_cases": {
        "examples": [
          {
            "input": "4\n40 20 30 10 30",
            "output": "26000\n((A1(A2A3))A4)"
          },
          {
            "input": "3\n5 10 3 12",
            "output": "330\n((A1A2)A3)"
          }
        ],
        "hidden": [
          {
            "input": "100 matrices with random dimensions",
            "output": "Optimal cost and parenthesization"
          },
          {
            "input": "Edge case: 2 matrices",
            "output": "Single multiplication cost"
          }
        ]
      }
    },
    {
      "question_type": "coding", 
      "section_id": 2,
      "set_number": 1,
      "question_text": "Maximum Flow with Multiple Sources and Sinks: In a network with multiple source nodes S = {s₁, s₂, ..., sₖ} and multiple sink nodes T = {t₁, t₂, ..., tₘ}, find the maximum flow from any source to any sink. Each edge has a capacity constraint and each source has a supply limit. Implement using Push-Relabel algorithm for optimal performance.",
      "description": "Solve the multi-source multi-sink maximum flow problem with supply constraints. Your algorithm should efficiently handle large graphs and provide the actual flow values for each edge in the optimal solution.",
      "constraints": [
        "1 ≤ n ≤ 1000 (vertices)",
        "1 ≤ m ≤ 5000 (edges)", 
        "1 ≤ k, t ≤ 100 (sources, sinks)",
        "1 ≤ capacity ≤ 10^9",
        "1 ≤ supply ≤ 10^9",
        "Time complexity must be better than O(V²E)",
        "Output: maximum flow value and flow on each edge"
      ],
      "positive_marks": 60,
      "negative_marks": 0,
      "time_limit": 4500,
      "test_cases": {
        "examples": [
          {
            "input": "6 8 2 2\n1 2\n5 6\n1 3 10\n1 4 8\n2 3 5\n2 5 7\n3 4 3\n3 5 6\n4 6 15\n5 6 12",
            "output": "19\n1->3: 10\n1->4: 8\n2->5: 7\n3->5: 6\n4->6: 15\n5->6: 12"
          }
        ],
        "hidden": [
          {
            "input": "Large graph with 1000 vertices and multiple sources/sinks",
            "output": "Optimal flow distribution"
          },
          {
            "input": "Disconnected components test case",
            "output": "0 (no flow possible)"
          }
        ]
      }
    }
  ]
}
```

### 3. Non-Coding Assessment (Knowledge-Based)
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Software Architecture & System Design Knowledge Assessment",
  "assessment_type": "non-coding",
  "assessment_description": "Comprehensive knowledge assessment covering software architecture patterns, system design principles, cloud technologies, security practices, and engineering best practices. Suitable for technical leads and senior architects.",
  "passing_marks": 280,
  "total_marks": 400,
  "num_of_sets": 2,
  "section_names": [
    "Software Architecture Patterns",
    "System Design & Scalability",
    "Cloud Technologies & Services",
    "Security & Compliance",
    "Engineering Best Practices"
  ],
  "section_descriptions": [
    "Design patterns, architectural styles, microservices, event-driven architecture, and pattern selection criteria.",
    "Scalability patterns, load balancing, caching strategies, database sharding, and performance optimization.",
    "AWS/Azure/GCP services, serverless computing, containerization, and cloud-native application design.",
    "Security protocols, authentication, authorization, data protection, and compliance frameworks.",
    "Code quality, testing strategies, continuous integration, monitoring, and operational excellence."
  ],
  "start_time": "2025-11-10T10:00:00Z",
  "end_time": "2025-11-10T13:00:00Z",
  "is_electron_only": false,
  "num_of_ai_generated_questions": 50,
  "is_proctored": false,
  "is_published": false,
  "attachments": [
    "https://s3.amazonaws.com/assessments/architecture-patterns-reference.pdf",
    "https://s3.amazonaws.com/assessments/aws-services-comparison.xlsx",
    "https://s3.amazonaws.com/assessments/security-frameworks-guide.pdf"
  ],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "According to the architecture patterns reference in $1, which combination of patterns would be most appropriate for a real-time financial trading system that requires sub-millisecond latency, high availability, and strict consistency?",
      "options": [
        "Event Sourcing + CQRS + Actor Model + Circuit Breaker",
        "Microservices + API Gateway + Database per Service + Saga Pattern", 
        "Layered Architecture + Repository Pattern + Unit of Work + Decorator",
        "Hexagonal Architecture + Domain Events + Event Bus + Retry Pattern",
        "Pipeline Architecture + Streaming + In-Memory Grid + Leader Election"
      ],
      "correct_option_index": 0,
      "positive_marks": 15,
      "negative_marks": -4,
      "time_limit": 240
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "For a globally distributed e-commerce platform handling 100M daily active users, which caching strategy would provide the optimal balance between consistency, performance, and cost?",
      "options": [
        "Multi-tier caching: Browser cache (5min) → CDN (1hr) → Application cache (30min) → Database query cache (15min)",
        "Single-tier Redis cluster with write-through policy and 2-hour TTL",
        "Distributed cache with eventual consistency and region-based partitioning",
        "In-memory cache with write-behind policy and manual invalidation",
        "Database-only caching with materialized views and scheduled refresh"
      ],
      "correct_option_index": 2,
      "positive_marks": 12,
      "negative_marks": -3,
      "time_limit": 180
    }
  ]
}
```

### 4. Minimal Assessment (Edge Case)
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Quick Skills Check",
  "assessment_type": "mix",
  "assessment_description": "",
  "passing_marks": 5,
  "total_marks": 10,
  "num_of_sets": 1,
  "section_names": ["General"],
  "section_descriptions": ["Basic assessment"],
  "start_time": "2025-09-20T10:00:00Z",
  "end_time": "2025-09-20T10:15:00Z",
  "is_electron_only": false,
  "num_of_ai_generated_questions": 0,
  "is_proctored": false,
  "is_published": false,
  "attachments": [],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "What is 2 + 2?",
      "options": ["3", "4", "5", "6"],
      "correct_option_index": 1,
      "positive_marks": 5,
      "negative_marks": 0,
      "time_limit": 30
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Write a function that returns 'Hello World'",
      "description": "Simple hello world function",
      "constraints": ["Return type: string"],
      "positive_marks": 5,
      "negative_marks": 0,
      "time_limit": 300,
      "test_cases": {
        "examples": [{"input": "", "output": "Hello World"}],
        "hidden": [{"input": "", "output": "Hello World"}]
      }
    }
  ]
}
```

### 5. Multi-Set Assessment (Different Difficulty Levels)
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Adaptive Programming Assessment - Multi-Level",
  "assessment_type": "coding",
  "assessment_description": "Adaptive assessment with multiple sets of increasing difficulty. Set 1: Beginner level, Set 2: Intermediate level, Set 3: Advanced level. Students are assigned sets based on their initial screening results.",
  "passing_marks": 150,
  "total_marks": 300,
  "num_of_sets": 3,
  "section_names": [
    "Basic Programming",
    "Data Structures",
    "Advanced Algorithms"
  ],
  "section_descriptions": [
    "Fundamental programming concepts and basic problem solving",
    "Implementation and usage of common data structures", 
    "Complex algorithmic challenges and optimization problems"
  ],
  "start_time": "2025-12-01T09:00:00Z",
  "end_time": "2025-12-01T12:00:00Z",
  "is_electron_only": true,
  "num_of_ai_generated_questions": 15,
  "is_proctored": true,
  "is_published": false,
  "attachments": [
    "https://s3.amazonaws.com/assessments/programming-reference.pdf"
  ],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Write a function to find the maximum element in an array. Refer to basic concepts in $1.",
      "description": "Implement a simple function to find the largest number in an array of integers.",
      "constraints": [
        "1 ≤ array length ≤ 1000",
        "Array elements are integers",
        "Array is not empty"
      ],
      "positive_marks": 20,
      "negative_marks": 0,
      "time_limit": 600,
      "test_cases": {
        "examples": [
          {"input": "[1, 3, 2, 5, 4]", "output": "5"},
          {"input": "[-1, -3, -2]", "output": "-1"}
        ],
        "hidden": [
          {"input": "[100]", "output": "100"},
          {"input": "Large array with 1000 elements", "output": "Maximum value"}
        ]
      }
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 2,
      "question_text": "Implement a balanced binary search tree with insert, delete, and search operations.",
      "description": "Create a self-balancing BST (AVL or Red-Black tree) with all basic operations.",
      "constraints": [
        "Support up to 10^5 operations",
        "Each operation should be O(log n)",
        "Handle duplicate values appropriately"
      ],
      "positive_marks": 50,
      "negative_marks": 0,
      "time_limit": 2400,
      "test_cases": {
        "examples": [
          {"input": "insert(5), insert(3), insert(7), search(3)", "output": "true"},
          {"input": "insert(1), delete(1), search(1)", "output": "false"}
        ],
        "hidden": [
          {"input": "Stress test with 50000 operations", "output": "All operations complete in time"},
          {"input": "Edge case: delete root with two children", "output": "Tree remains balanced"}
        ]
      }
    },
    {
      "question_type": "coding",
      "section_id": 3,
      "set_number": 3,
      "question_text": "Solve the Traveling Salesman Problem using dynamic programming with bitmasks for graphs up to 20 vertices.",
      "description": "Implement an exact solution for TSP using Held-Karp algorithm with memoization.",
      "constraints": [
        "4 ≤ n ≤ 20 vertices",
        "Edge weights are positive integers ≤ 1000",
        "Graph is complete (all pairs connected)",
        "Return minimum tour cost and the actual path"
      ],
      "positive_marks": 80,
      "negative_marks": 0,
      "time_limit": 3600,
      "test_cases": {
        "examples": [
          {"input": "4 vertices with distance matrix", "output": "Minimum cost and optimal path"},
          {"input": "5 vertices symmetric graph", "output": "Optimal tour"}
        ],
        "hidden": [
          {"input": "15 vertices random graph", "output": "Exact optimal solution"},
          {"input": "20 vertices worst-case input", "output": "Solution within time limit"}
        ]
      }
    }
  ]
}
```

---

## Assessment Update Requests

### 1. Partial Update - Change Only Basic Information
```http
PATCH /api/v1/assessments/15/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Updated: Enterprise Software Engineering Evaluation 2025",
  "assessment_description": "Updated comprehensive assessment with new industry standards and best practices for 2025.",
  "passing_marks": 450,
  "start_time": "2025-10-01T09:00:00Z",
  "end_time": "2025-10-01T13:30:00Z"
}
```

### 2. Full Update - Replace Entire Assessment
```http
PUT /api/v1/assessments/23/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Completely Redesigned Algorithm Challenge",
  "assessment_type": "coding",
  "assessment_description": "Completely revamped algorithmic assessment focusing on competitive programming and advanced problem-solving techniques.",
  "passing_marks": 300,
  "total_marks": 500,
  "num_of_sets": 2,
  "section_names": [
    "Advanced Data Structures",
    "Complex Algorithms",
    "Mathematical Programming"
  ],
  "section_descriptions": [
    "Segment trees, Fenwick trees, persistent data structures",
    "Advanced graph algorithms, string algorithms, computational geometry", 
    "Number theory, combinatorics, game theory problems"
  ],
  "start_time": "2025-11-15T08:00:00Z",
  "end_time": "2025-11-15T13:00:00Z",
  "is_electron_only": true,
  "num_of_ai_generated_questions": 0,
  "is_proctored": true,
  "is_published": false,
  "attachments": [
    "https://s3.amazonaws.com/contests/advanced-algorithms-reference.pdf",
    "https://s3.amazonaws.com/contests/mathematical-formulas-extended.pdf"
  ],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Implement a persistent segment tree that supports range updates and point queries across multiple versions.",
      "description": "Build a persistent data structure that maintains all previous versions while supporting efficient updates and queries.",
      "constraints": [
        "1 ≤ n ≤ 100,000 (array size)",
        "1 ≤ q ≤ 100,000 (queries)",
        "Memory limit: 512 MB",
        "Time limit: 3 seconds per test case"
      ],
      "positive_marks": 75,
      "negative_marks": 0,
      "time_limit": 4800,
      "test_cases": {
        "examples": [
          {"input": "Array and sequence of update/query operations", "output": "Query results for each version"},
          {"input": "Edge case with single element", "output": "Correct handling"}
        ],
        "hidden": [
          {"input": "Maximum constraints stress test", "output": "All operations within limits"},
          {"input": "Random operations on large dataset", "output": "Consistent results across versions"}
        ]
      }
    }
  ]
}
```

### 3. Update Published Assessment (Should Fail)
```http
PATCH /api/v1/assessments/45/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "This should fail since assessment is published",
      "description": "Attempting to modify questions of published assessment",
      "constraints": ["This update should be rejected"],
      "positive_marks": 10,
      "negative_marks": 0,
      "time_limit": 300,
      "test_cases": {
        "examples": [{"input": "test", "output": "test"}],
        "hidden": [{"input": "test", "output": "test"}]
      }
    }
  ]
}
```

---

## Assessment Filtering & Search Requests

### 1. Get Assessments with Complex Filtering
```http
GET /api/v1/assessments/?type=mix&is_published=true&is_active=true&search=algorithm&page=2&page_size=5&set_number=1
Authorization: Bearer <token>
```

### 2. Get Specific Assessment with Set Filtering
```http
GET /api/v1/assessments/42/?set_number=3
Authorization: Bearer <token>
```

### 3. Get All Unpublished Drafts
```http
GET /api/v1/assessments/?is_published=false&is_active=true&page_size=50
Authorization: Bearer <token>
```

### 4. Search by Keyword in Title
```http
GET /api/v1/assessments/?search=enterprise%20software&type=mix&page=1&page_size=10
Authorization: Bearer <token>
```

### 5. Get Only Coding Assessments
```http
GET /api/v1/assessments/?type=coding&page_size=100
Authorization: Bearer <token>
```

---

## Assessment Lifecycle Management Requests

### 1. Publish Assessment
```http
POST /api/v1/assessments/67/publish/
Authorization: Bearer <token>
```

### 2. Unpublish Assessment
```http
POST /api/v1/assessments/67/unpublish/
Authorization: Bearer <token>
```

### 3. Duplicate Assessment
```http
POST /api/v1/assessments/89/duplicate/
Authorization: Bearer <token>
```

### 4. Delete Draft Assessment
```http
DELETE /api/v1/assessments/123/
Authorization: Bearer <token>
```

### 5. Attempt to Delete Published Assessment (Should Fail)
```http
DELETE /api/v1/assessments/456/
Authorization: Bearer <token>
```

---

## Assessment Statistics Request

### 1. Get Overall Statistics
```http
GET /api/v1/assessments/statistics/
Authorization: Bearer <token>
```

---

## Edge Cases & Special Scenarios

### 1. Assessment with Maximum Attachments (5 files)
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Multi-Media Assessment with All Attachment Types",
  "assessment_type": "mix",
  "assessment_description": "Assessment utilizing all possible attachment types for comprehensive evaluation.",
  "passing_marks": 80,
  "total_marks": 120,
  "num_of_sets": 1,
  "section_names": ["Multi-Media Comprehension"],
  "section_descriptions": ["Questions based on various media types and documents"],
  "start_time": "2025-12-15T10:00:00Z",
  "end_time": "2025-12-15T12:00:00Z",
  "is_electron_only": false,
  "num_of_ai_generated_questions": 0,
  "is_proctored": false,
  "is_published": false,
  "attachments": [
    "https://s3.amazonaws.com/assessments/technical-specification.pdf",
    "https://s3.amazonaws.com/assessments/workflow-diagram.png", 
    "https://s3.amazonaws.com/assessments/data-samples.csv",
    "https://s3.amazonaws.com/assessments/api-endpoints.json",
    "https://s3.amazonaws.com/assessments/system-requirements.docx"
  ],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Based on the technical specification in $1, workflow diagram in $2, data samples in $3, API endpoints in $4, and system requirements in $5, what is the optimal database design approach?",
      "options": [
        "Relational database with normalized schema",
        "NoSQL document store with denormalized data",
        "Hybrid approach with RDBMS for transactions and NoSQL for analytics",
        "In-memory database with persistent backup",
        "Distributed database with horizontal sharding"
      ],
      "correct_option_index": 2,
      "positive_marks": 20,
      "negative_marks": -5,
      "time_limit": 600
    }
  ]
}
```

### 2. Assessment with No Attachments but Reference Attempt (Should Fail)
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Invalid Reference Assessment",
  "assessment_type": "non-coding",
  "assessment_description": "This should fail due to invalid attachment reference",
  "passing_marks": 10,
  "total_marks": 20,
  "num_of_sets": 1,
  "section_names": ["Test"],
  "section_descriptions": ["Invalid test"],
  "start_time": "2025-09-20T10:00:00Z",
  "end_time": "2025-09-20T11:00:00Z",
  "is_electron_only": false,
  "num_of_ai_generated_questions": 0,
  "is_proctored": false,
  "is_published": false,
  "attachments": [],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Refer to document $1 for the answer to this question.",
      "options": ["A", "B", "C", "D"],
      "correct_option_index": 0,
      "positive_marks": 10,
      "negative_marks": 0,
      "time_limit": 60
    }
  ]
}
```

### 3. Assessment with Invalid Section Reference (Should Fail)
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Invalid Section Reference",
  "assessment_type": "mix",
  "assessment_description": "This should fail due to invalid section_id reference",
  "passing_marks": 10,
  "total_marks": 20,
  "num_of_sets": 1,
  "section_names": ["Section 1"],
  "section_descriptions": ["Only one section"],
  "start_time": "2025-09-20T10:00:00Z",
  "end_time": "2025-09-20T11:00:00Z",
  "is_electron_only": false,
  "num_of_ai_generated_questions": 0,
  "is_proctored": false,
  "is_published": false,
  "attachments": [],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 5,
      "set_number": 1,
      "question_text": "This question references section 5 but only section 1 exists",
      "options": ["A", "B", "C", "D"],
      "correct_option_index": 0,
      "positive_marks": 10,
      "negative_marks": 0,
      "time_limit": 60
    }
  ]
}
```

### 4. Assessment with Empty Question Arrays (Edge Case)
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Empty Assessment",
  "assessment_type": "mix",
  "assessment_description": "Assessment with no questions for testing edge cases",
  "passing_marks": 0,
  "total_marks": 0,
  "num_of_sets": 1,
  "section_names": ["Empty Section"],
  "section_descriptions": ["Section with no questions"],
  "start_time": "2025-09-20T10:00:00Z",
  "end_time": "2025-09-20T11:00:00Z",
  "is_electron_only": false,
  "num_of_ai_generated_questions": 0,
  "is_proctored": false,
  "is_published": false,
  "attachments": [],
  "questions": []
}
```

### 5. Assessment with Maximum Negative Marks
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "High Risk Assessment",
  "assessment_type": "non-coding",
  "assessment_description": "Assessment with significant negative marking to discourage guessing",
  "passing_marks": 50,
  "total_marks": 100,
  "num_of_sets": 1,
  "section_names": ["High Stakes Questions"],
  "section_descriptions": ["Questions with high negative marking"],
  "start_time": "2025-09-20T10:00:00Z",
  "end_time": "2025-09-20T12:00:00Z",
  "is_electron_only": true,
  "num_of_ai_generated_questions": 0,
  "is_proctored": true,
  "is_published": false,
  "attachments": [],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "This question has severe negative marking. What is the capital of France?",
      "options": ["London", "Berlin", "Paris", "Madrid", "Rome"],
      "correct_option_index": 2,
      "positive_marks": 20,
      "negative_marks": -15,
      "time_limit": 120
    }
  ]
}
```

### 6. Assessment with Very Long Time Limits
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Extended Duration Research Assessment",
  "assessment_type": "coding",
  "assessment_description": "Long-form assessment allowing extensive research and implementation time",
  "passing_marks": 200,
  "total_marks": 400,
  "num_of_sets": 1,
  "section_names": ["Research & Implementation"],
  "section_descriptions": ["Deep research problems requiring extensive time"],
  "start_time": "2025-09-20T09:00:00Z",
  "end_time": "2025-09-22T18:00:00Z",
  "is_electron_only": false,
  "num_of_ai_generated_questions": 0,
  "is_proctored": false,
  "is_published": false,
  "attachments": [],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Design and implement a complete distributed consensus algorithm with Byzantine fault tolerance.",
      "description": "Implement a complete blockchain-style consensus mechanism that can handle Byzantine failures.",
      "constraints": [
        "Support up to 100 nodes",
        "Handle up to 33% Byzantine failures",
        "Implement leader election",
        "Provide formal proof of correctness"
      ],
      "positive_marks": 400,
      "negative_marks": 0,
      "time_limit": 172800,
      "test_cases": {
        "examples": [
          {"input": "Network simulation with 7 nodes, 2 Byzantine", "output": "Consensus achieved with correct value"},
          {"input": "Network partition scenario", "output": "Recovery after partition heals"}
        ],
        "hidden": [
          {"input": "Stress test with maximum Byzantine nodes", "output": "System remains functional"},
          {"input": "Complex attack scenarios", "output": "Consensus maintained despite attacks"}
        ]
      }
    }
  ]
}
```

---

*This document covers advanced assessment creation scenarios, edge cases, complex filtering, and various update patterns without response examples.*
