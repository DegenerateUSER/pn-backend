# Test Cases API Documentation

**Base URL**: `http://localhost:8000/api/v1/`  
**Headers for authenticated requests:**
```
Content-Type: application/json
Authorization: Bearer <your_access_token>
```

---

## Test Case Management for Coding Questions

This document outlines the API requests for managing test cases (both normal/example test cases and hidden test cases) for coding questions in assessments.

---

## 1. Create Assessment with Normal and Hidden Test Cases

### Create Assessment with Comprehensive Test Cases
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Advanced Programming Test Cases",
  "assessment_type": "coding",
  "assessment_description": "Comprehensive coding assessment with extensive test case coverage",
  "passing_marks": 120,
  "num_of_sets": 1,
  "section_names": ["Algorithm Design", "Data Structures", "String Manipulation"],
  "section_descriptions": [
    "Advanced algorithm implementation and optimization",
    "Complex data structure operations and efficiency",
    "String processing and pattern matching"
  ],
  "start_time": "2025-12-15T09:00:00Z",
  "end_time": "2025-12-15T13:00:00Z",
  "is_electron_only": true,
  "is_proctored": true,
  "is_published": false,
  "num_of_ai_generated_questions": 0,
  "attachments": [],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Implement a function to find the longest palindromic substring in a given string",
      "description": "Write an efficient algorithm to find the longest contiguous palindromic substring. Handle edge cases like empty strings and single characters.",
      "constraints": [
        "Time complexity should be O(n^2) or better",
        "Space complexity should be O(1) if possible",
        "Handle Unicode characters",
        "String length can be up to 10,000 characters"
      ],
      "positive_marks": 50,
      "negative_marks": 0,
      "time_limit": 1800,
      "test_cases": {
        "examples": [
          {
            "input": "babad",
            "output": "bab",
            "explanation": "Both 'bab' and 'aba' are valid longest palindromes"
          },
          {
            "input": "cbbd",
            "output": "bb",
            "explanation": "The longest palindromic substring is 'bb'"
          },
          {
            "input": "racecar",
            "output": "racecar",
            "explanation": "The entire string is a palindrome"
          }
        ],
        "hidden": [
          {
            "input": "",
            "output": "",
            "explanation": "Empty string case"
          },
          {
            "input": "a",
            "output": "a",
            "explanation": "Single character case"
          },
          {
            "input": "abcdef",
            "output": "a",
            "explanation": "No palindrome longer than 1, return first character"
          },
          {
            "input": "abacabad",
            "output": "abacaba",
            "explanation": "Complex palindrome detection"
          },
          {
            "input": "forgeeksskeegfor",
            "output": "geeksskeeg",
            "explanation": "Embedded palindrome in longer string"
          },
          {
            "input": "Aabcdcba",
            "output": "abcdcba",
            "explanation": "Case sensitivity handling"
          }
        ]
      }
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Implement a Binary Search Tree with insertion, deletion, and search operations",
      "description": "Create a complete BST implementation with proper node management and tree balancing considerations.",
      "constraints": [
        "Support generic data types",
        "Handle duplicate values appropriately",
        "Implement iterative and recursive approaches",
        "Include tree traversal methods"
      ],
      "positive_marks": 50,
      "negative_marks": 0,
      "time_limit": 2400,
      "test_cases": {
        "examples": [
          {
            "input": "insert: [5, 3, 7, 2, 4, 6, 8]; search: 4",
            "output": "true",
            "explanation": "Basic insertion and search operation"
          },
          {
            "input": "insert: [10, 5, 15, 3]; delete: 5; search: 5",
            "output": "false",
            "explanation": "Deletion and verification"
          },
          {
            "input": "insert: [20, 10, 30]; inorder_traversal",
            "output": "[10, 20, 30]",
            "explanation": "Tree traversal after insertion"
          }
        ],
        "hidden": [
          {
            "input": "insert: []; search: 1",
            "output": "false",
            "explanation": "Empty tree case"
          },
          {
            "input": "insert: [1]; delete: 1; search: 1",
            "output": "false",
            "explanation": "Single node deletion"
          },
          {
            "input": "insert: [5, 5, 5]; search: 5",
            "output": "true",
            "explanation": "Duplicate value handling"
          },
          {
            "input": "insert: [50, 30, 70, 20, 40, 60, 80]; delete: 30; inorder",
            "output": "[20, 40, 50, 60, 70, 80]",
            "explanation": "Complex deletion with two children"
          },
          {
            "input": "insert: [1, 2, 3, 4, 5]; search: 3",
            "output": "true",
            "explanation": "Degenerate tree (linear) case"
          },
          {
            "input": "insert: [100, 50, 150, 25, 75, 125, 175]; delete: 100; root",
            "output": "75",
            "explanation": "Root deletion and replacement"
          }
        ]
      }
    },
    {
      "question_type": "coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "Implement a string pattern matching algorithm (KMP or similar)",
      "description": "Create an efficient pattern matching algorithm to find all occurrences of a pattern in a text string.",
      "constraints": [
        "Time complexity should be O(n + m) where n is text length, m is pattern length",
        "Handle overlapping patterns",
        "Support case-sensitive and case-insensitive matching",
        "Return all occurrence positions"
      ],
      "positive_marks": 50,
      "negative_marks": 0,
      "time_limit": 2100,
      "test_cases": {
        "examples": [
          {
            "input": "text: 'ABABDABACDABABCABCABCABCABC', pattern: 'ABABCABCAB'",
            "output": "[15]",
            "explanation": "Single pattern match"
          },
          {
            "input": "text: 'AAAAAA', pattern: 'AA'",
            "output": "[0, 1, 2, 3, 4]",
            "explanation": "Overlapping pattern matches"
          },
          {
            "input": "text: 'Hello World', pattern: 'o'",
            "output": "[4, 7]",
            "explanation": "Multiple single character matches"
          }
        ],
        "hidden": [
          {
            "input": "text: '', pattern: 'test'",
            "output": "[]",
            "explanation": "Empty text case"
          },
          {
            "input": "text: 'hello', pattern: ''",
            "output": "[]",
            "explanation": "Empty pattern case"
          },
          {
            "input": "text: 'ABCDEFGHIJKLMNOP', pattern: 'XYZ'",
            "output": "[]",
            "explanation": "No matches found"
          },
          {
            "input": "text: 'ABABABAB', pattern: 'ABAB'",
            "output": "[0, 2, 4]",
            "explanation": "Complex overlapping pattern"
          },
          {
            "input": "text: 'The quick brown fox jumps over the lazy dog', pattern: 'the'",
            "output": "[31]",
            "explanation": "Case sensitive matching (only lowercase 'the')"
          },
          {
            "input": "text: 'aaaabaaaabaaaab', pattern: 'aaaab'",
            "output": "[0, 5, 10]",
            "explanation": "Repeated pattern with prefix overlaps"
          }
        ]
      }
    }
  ]
}
```

---

## 2. String Reversal Test Cases

### Simple String Reversal Problem
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "String Reversal Test Cases",
  "assessment_type": "coding",
  "assessment_description": "Comprehensive string reversal implementation with edge cases",
  "passing_marks": 40,
  "num_of_sets": 1,
  "section_names": ["String Operations"],
  "section_descriptions": ["Basic string manipulation and reversal"],
  "start_time": "2025-12-10T10:00:00Z",
  "end_time": "2025-12-10T11:00:00Z",
  "is_electron_only": false,
  "is_proctored": false,
  "is_published": true,
  "num_of_ai_generated_questions": 0,
  "attachments": [],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Write a function to reverse a string without using built-in reverse methods",
      "description": "Implement string reversal using manual character manipulation. Handle various edge cases including empty strings, single characters, and Unicode characters.",
      "constraints": [
        "No built-in reverse functions allowed",
        "Handle empty strings gracefully",
        "Support Unicode characters",
        "Time complexity should be O(n)",
        "Space complexity should be O(1) for in-place reversal or O(n) for new string"
      ],
      "positive_marks": 50,
      "negative_marks": 0,
      "time_limit": 900,
      "test_cases": {
        "examples": [
          {
            "input": "hello",
            "output": "olleh",
            "explanation": "Basic string reversal"
          },
          {
            "input": "world",
            "output": "dlrow",
            "explanation": "Another basic case"
          },
          {
            "input": "Python",
            "output": "nohtyP",
            "explanation": "Mixed case string"
          }
        ],
        "hidden": [
          {
            "input": "",
            "output": "",
            "explanation": "Empty string should return empty string"
          },
          {
            "input": "a",
            "output": "a",
            "explanation": "Single character remains the same"
          },
          {
            "input": "12345",
            "output": "54321",
            "explanation": "Numeric string reversal"
          },
          {
            "input": "A man a plan a canal Panama",
            "output": "amanaP lanac a nalp a nam A",
            "explanation": "Long string with spaces"
          },
          {
            "input": "!@#$%^&*()",
            "output": ")(*&^%$#@!",
            "explanation": "Special characters"
          },
          {
            "input": "café",
            "output": "éfac",
            "explanation": "Unicode characters with accents"
          },
          {
            "input": "🚀🌟⭐",
            "output": "⭐🌟🚀",
            "explanation": "Emoji and Unicode symbols"
          }
        ]
      }
    }
  ]
}
```

---

## 3. Array and Sorting Test Cases

### Array Manipulation with Comprehensive Test Cases
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Array Sorting and Manipulation",
  "assessment_type": "coding",
  "assessment_description": "Advanced array operations with comprehensive test coverage",
  "passing_marks": 60,
  "num_of_sets": 1,
  "section_names": ["Array Operations"],
  "section_descriptions": ["Sorting algorithms and array manipulation"],
  "start_time": "2025-12-12T14:00:00Z",
  "end_time": "2025-12-12T16:00:00Z",
  "is_electron_only": true,
  "is_proctored": true,
  "is_published": false,
  "num_of_ai_generated_questions": 0,
  "attachments": [],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Implement a merge sort algorithm that sorts an array of integers",
      "description": "Create an efficient merge sort implementation that handles various array configurations and edge cases.",
      "constraints": [
        "Time complexity must be O(n log n)",
        "Space complexity should be O(n)",
        "Handle duplicate elements correctly",
        "Implement stable sorting",
        "Handle negative numbers"
      ],
      "positive_marks": 60,
      "negative_marks": 0,
      "time_limit": 1800,
      "test_cases": {
        "examples": [
          {
            "input": "[64, 34, 25, 12, 22, 11, 90]",
            "output": "[11, 12, 22, 25, 34, 64, 90]",
            "explanation": "Basic unsorted array"
          },
          {
            "input": "[5, 2, 4, 6, 1, 3]",
            "output": "[1, 2, 3, 4, 5, 6]",
            "explanation": "Small array sorting"
          },
          {
            "input": "[1, 2, 3, 4, 5]",
            "output": "[1, 2, 3, 4, 5]",
            "explanation": "Already sorted array"
          }
        ],
        "hidden": [
          {
            "input": "[]",
            "output": "[]",
            "explanation": "Empty array case"
          },
          {
            "input": "[42]",
            "output": "[42]",
            "explanation": "Single element array"
          },
          {
            "input": "[5, 4, 3, 2, 1]",
            "output": "[1, 2, 3, 4, 5]",
            "explanation": "Reverse sorted array"
          },
          {
            "input": "[3, 3, 3, 3]",
            "output": "[3, 3, 3, 3]",
            "explanation": "All elements identical"
          },
          {
            "input": "[-5, -2, -10, -1, -8]",
            "output": "[-10, -8, -5, -2, -1]",
            "explanation": "Negative numbers only"
          },
          {
            "input": "[-3, 7, -1, 2, 0, -5, 4]",
            "output": "[-5, -3, -1, 0, 2, 4, 7]",
            "explanation": "Mixed positive and negative numbers"
          },
          {
            "input": "[1000, 999, 998, 997, 996, 995, 994, 993, 992, 991]",
            "output": "[991, 992, 993, 994, 995, 996, 997, 998, 999, 1000]",
            "explanation": "Large numbers in reverse order"
          },
          {
            "input": "[2, 1, 1, 2, 3, 3, 1, 2]",
            "output": "[1, 1, 1, 2, 2, 2, 3, 3]",
            "explanation": "Multiple duplicates stability test"
          }
        ]
      }
    }
  ]
}
```

---

## 4. Mathematical Algorithm Test Cases

### Prime Number Algorithm with Edge Cases
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Prime Number Algorithms",
  "assessment_type": "coding",
  "assessment_description": "Mathematical algorithms for prime number detection and generation",
  "passing_marks": 50,
  "num_of_sets": 1,
  "section_names": ["Mathematical Algorithms"],
  "section_descriptions": ["Prime numbers, factorization, and number theory"],
  "start_time": "2025-12-18T09:00:00Z",
  "end_time": "2025-12-18T11:00:00Z",
  "is_electron_only": false,
  "is_proctored": false,
  "is_published": true,
  "num_of_ai_generated_questions": 0,
  "attachments": [],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Implement an efficient algorithm to check if a number is prime",
      "description": "Create a function that determines whether a given positive integer is a prime number. Optimize for large numbers and handle edge cases.",
      "constraints": [
        "Time complexity should be O(√n) or better",
        "Handle numbers up to 10^12",
        "Return boolean true/false",
        "Handle edge cases (0, 1, 2, negative numbers)",
        "Consider optimization techniques like trial division"
      ],
      "positive_marks": 55,
      "negative_marks": 0,
      "time_limit": 1200,
      "test_cases": {
        "examples": [
          {
            "input": "17",
            "output": "true",
            "explanation": "17 is a prime number"
          },
          {
            "input": "4",
            "output": "false",
            "explanation": "4 is not prime (divisible by 2)"
          },
          {
            "input": "97",
            "output": "true",
            "explanation": "97 is a prime number"
          }
        ],
        "hidden": [
          {
            "input": "0",
            "output": "false",
            "explanation": "0 is not considered prime"
          },
          {
            "input": "1",
            "output": "false",
            "explanation": "1 is not considered prime by definition"
          },
          {
            "input": "2",
            "output": "true",
            "explanation": "2 is the only even prime number"
          },
          {
            "input": "-5",
            "output": "false",
            "explanation": "Negative numbers are not prime"
          },
          {
            "input": "9",
            "output": "false",
            "explanation": "9 = 3 × 3, composite number"
          },
          {
            "input": "101",
            "output": "true",
            "explanation": "101 is prime"
          },
          {
            "input": "121",
            "output": "false",
            "explanation": "121 = 11 × 11, perfect square"
          },
          {
            "input": "982451653",
            "output": "true",
            "explanation": "Large prime number test"
          },
          {
            "input": "982451654",
            "output": "false",
            "explanation": "Large composite number test"
          },
          {
            "input": "1000000007",
            "output": "true",
            "explanation": "Another large prime commonly used in programming contests"
          }
        ]
      }
    }
  ]
}
```

---

## 5. Data Structure Implementation Test Cases

### Linked List Operations with Comprehensive Testing
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Linked List Implementation",
  "assessment_type": "coding",
  "assessment_description": "Complete linked list implementation with various operations",
  "passing_marks": 70,
  "num_of_sets": 1,
  "section_names": ["Data Structures"],
  "section_descriptions": ["Linked lists, stacks, queues, and linear data structures"],
  "start_time": "2025-12-20T10:00:00Z",
  "end_time": "2025-12-20T13:00:00Z",
  "is_electron_only": true,
  "is_proctored": true,
  "is_published": false,
  "num_of_ai_generated_questions": 0,
  "attachments": [],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Implement a singly linked list with insert, delete, search, and reverse operations",
      "description": "Create a complete singly linked list implementation supporting various operations including insertion at different positions, deletion by value or position, searching, and list reversal.",
      "constraints": [
        "Implement proper node structure",
        "Handle empty list cases",
        "Support insertion at head, tail, and arbitrary positions",
        "Implement deletion by value and by position",
        "Include search functionality",
        "Implement iterative list reversal"
      ],
      "positive_marks": 75,
      "negative_marks": 0,
      "time_limit": 2700,
      "test_cases": {
        "examples": [
          {
            "input": "insert_head(5); insert_head(3); insert_tail(7); display()",
            "output": "[3, 5, 7]",
            "explanation": "Basic insertion operations"
          },
          {
            "input": "insert_head(1); insert_head(2); delete_value(1); display()",
            "output": "[2]",
            "explanation": "Insertion and deletion by value"
          },
          {
            "input": "insert_head(1); insert_head(2); insert_head(3); reverse(); display()",
            "output": "[1, 2, 3]",
            "explanation": "List reversal operation"
          }
        ],
        "hidden": [
          {
            "input": "display()",
            "output": "[]",
            "explanation": "Empty list display"
          },
          {
            "input": "delete_value(5)",
            "output": "false",
            "explanation": "Delete from empty list should return false"
          },
          {
            "input": "search(10)",
            "output": "false",
            "explanation": "Search in empty list"
          },
          {
            "input": "insert_head(1); search(1)",
            "output": "true",
            "explanation": "Search existing element in single-node list"
          },
          {
            "input": "insert_head(5); delete_value(5); display()",
            "output": "[]",
            "explanation": "Delete only element from list"
          },
          {
            "input": "insert_tail(1); insert_tail(2); insert_tail(3); delete_position(1); display()",
            "output": "[1, 3]",
            "explanation": "Delete by position (0-indexed)"
          },
          {
            "input": "insert_head(10); insert_head(20); insert_head(30); insert_position(1, 15); display()",
            "output": "[30, 15, 20, 10]",
            "explanation": "Insert at specific position"
          },
          {
            "input": "insert_head(1); insert_head(2); insert_head(3); size()",
            "output": "3",
            "explanation": "Get list size"
          },
          {
            "input": "for i in range(1000): insert_tail(i); search(999)",
            "output": "true",
            "explanation": "Large list performance test"
          },
          {
            "input": "insert_head(5); insert_head(3); insert_head(5); delete_all_occurrences(5); display()",
            "output": "[3]",
            "explanation": "Delete all occurrences of a value"
          }
        ]
      }
    }
  ]
}
```

---

## 6. Dynamic Programming Test Cases

### Fibonacci Sequence with Memoization
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Dynamic Programming - Fibonacci",
  "assessment_type": "coding",
  "assessment_description": "Efficient Fibonacci implementation using dynamic programming techniques",
  "passing_marks": 45,
  "num_of_sets": 1,
  "section_names": ["Dynamic Programming"],
  "section_descriptions": ["Optimization techniques, memoization, and recursive problem solving"],
  "start_time": "2025-12-22T11:00:00Z",
  "end_time": "2025-12-22T12:30:00Z",
  "is_electron_only": false,
  "is_proctored": false,
  "is_published": true,
  "num_of_ai_generated_questions": 0,
  "attachments": [],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Implement an efficient Fibonacci sequence calculator using dynamic programming",
      "description": "Create a function that calculates the nth Fibonacci number efficiently. Use memoization or bottom-up approach to avoid redundant calculations.",
      "constraints": [
        "Handle large values of n (up to 1000)",
        "Time complexity should be O(n)",
        "Space complexity should be O(n) for memoization or O(1) for optimized version",
        "Handle edge cases (n = 0, n = 1)",
        "Return results as integers (handle overflow appropriately)"
      ],
      "positive_marks": 50,
      "negative_marks": 0,
      "time_limit": 1500,
      "test_cases": {
        "examples": [
          {
            "input": "5",
            "output": "5",
            "explanation": "F(5) = F(4) + F(3) = 3 + 2 = 5"
          },
          {
            "input": "10",
            "output": "55",
            "explanation": "F(10) = 55 in the Fibonacci sequence"
          },
          {
            "input": "0",
            "output": "0",
            "explanation": "F(0) = 0 by definition"
          }
        ],
        "hidden": [
          {
            "input": "1",
            "output": "1",
            "explanation": "F(1) = 1 by definition"
          },
          {
            "input": "2",
            "output": "1",
            "explanation": "F(2) = F(1) + F(0) = 1 + 0 = 1"
          },
          {
            "input": "15",
            "output": "610",
            "explanation": "F(15) = 610"
          },
          {
            "input": "20",
            "output": "6765",
            "explanation": "F(20) = 6765"
          },
          {
            "input": "30",
            "output": "832040",
            "explanation": "F(30) = 832040, medium-sized Fibonacci number"
          },
          {
            "input": "50",
            "output": "12586269025",
            "explanation": "F(50) = 12586269025, large Fibonacci number"
          },
          {
            "input": "100",
            "output": "354224848179261915075",
            "explanation": "F(100) = very large Fibonacci number, tests efficiency"
          }
        ]
      }
    }
  ]
}
```

---

## 7. Graph Algorithm Test Cases

### Graph Traversal Implementation
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Graph Algorithms - DFS and BFS",
  "assessment_type": "coding",
  "assessment_description": "Implementation of fundamental graph traversal algorithms",
  "passing_marks": 80,
  "num_of_sets": 1,
  "section_names": ["Graph Algorithms"],
  "section_descriptions": ["Graph traversal, shortest path, and connectivity algorithms"],
  "start_time": "2025-12-25T14:00:00Z",
  "end_time": "2025-12-25T17:00:00Z",
  "is_electron_only": true,
  "is_proctored": true,
  "is_published": false,
  "num_of_ai_generated_questions": 0,
  "attachments": [],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Implement both Depth-First Search (DFS) and Breadth-First Search (BFS) for an undirected graph",
      "description": "Create a graph class with DFS and BFS traversal methods. Support both recursive and iterative implementations of DFS. Handle disconnected components.",
      "constraints": [
        "Use adjacency list representation",
        "Handle disconnected graphs",
        "Return traversal order as a list",
        "Implement both recursive and iterative DFS",
        "Support starting from any vertex",
        "Handle empty graphs and single vertex graphs"
      ],
      "positive_marks": 85,
      "negative_marks": 0,
      "time_limit": 3000,
      "test_cases": {
        "examples": [
          {
            "input": "edges: [(0,1), (0,2), (1,3), (2,3)]; dfs_from(0)",
            "output": "[0, 1, 3, 2]",
            "explanation": "DFS traversal starting from vertex 0"
          },
          {
            "input": "edges: [(0,1), (0,2), (1,3), (2,3)]; bfs_from(0)",
            "output": "[0, 1, 2, 3]",
            "explanation": "BFS traversal starting from vertex 0"
          },
          {
            "input": "edges: [(0,1), (2,3)]; dfs_all_components()",
            "output": "[[0, 1], [2, 3]]",
            "explanation": "DFS on disconnected graph returns all components"
          }
        ],
        "hidden": [
          {
            "input": "edges: []; dfs_from(0)",
            "output": "[]",
            "explanation": "Empty graph case"
          },
          {
            "input": "edges: []; add_vertex(0); dfs_from(0)",
            "output": "[0]",
            "explanation": "Single vertex graph"
          },
          {
            "input": "edges: [(0,1)]; dfs_from(1)",
            "output": "[1, 0]",
            "explanation": "Simple two-vertex graph starting from vertex 1"
          },
          {
            "input": "edges: [(0,1), (1,2), (2,3), (3,4)]; dfs_from(2)",
            "output": "[2, 1, 0, 3, 4]",
            "explanation": "Linear graph DFS from middle vertex"
          },
          {
            "input": "edges: [(0,1), (0,2), (0,3), (0,4)]; bfs_from(0)",
            "output": "[0, 1, 2, 3, 4]",
            "explanation": "Star graph BFS from center"
          },
          {
            "input": "edges: [(0,1), (1,2), (2,0), (3,4), (4,5), (5,3)]; count_components()",
            "output": "2",
            "explanation": "Two disconnected triangular components"
          },
          {
            "input": "edges: [(0,1), (1,2), (2,3), (3,0), (1,3)]; is_connected()",
            "output": "true",
            "explanation": "Cycle graph connectivity check"
          },
          {
            "input": "edges: [(i, (i+1)%100) for i in range(100)]; dfs_from(0); length",
            "output": "100",
            "explanation": "Large cycle graph performance test"
          }
        ]
      }
    }
  ]
}
```

---

## 8. API Usage Examples

### Get Test Cases for Specific Assessment
```http
GET /api/v1/assessments/{assessment_id}/
Authorization: Bearer <token>
```

**Response will include questions with test_cases:**
```json
{
  "id": 1,
  "title": "Advanced Programming Test Cases",
  "questions": [
    {
      "id": 1,
      "question_text": "Implement a function to find the longest palindromic substring",
      "test_cases": {
        "examples": [
          {
            "input": "babad",
            "output": "bab",
            "explanation": "Both 'bab' and 'aba' are valid longest palindromes"
          }
        ],
        "hidden": [
          {
            "input": "",
            "output": "",
            "explanation": "Empty string case"
          }
        ]
      }
    }
  ]
}
```

### Filter Questions by Test Case Complexity
```http
GET /api/v1/assessments/{assessment_id}/?include_hidden_tests=true
Authorization: Bearer <token>
```

### Get Only Example Test Cases (Exclude Hidden)
```http
GET /api/v1/assessments/{assessment_id}/?include_hidden_tests=false
Authorization: Bearer <token>
```

---

## 9. Test Case Validation Guidelines

### Normal/Example Test Cases
- **Purpose**: Help candidates understand the problem and expected format
- **Visibility**: Shown to candidates during the assessment
- **Count**: Usually 2-4 examples per question
- **Coverage**: Basic scenarios and typical use cases

### Hidden Test Cases
- **Purpose**: Comprehensive evaluation including edge cases
- **Visibility**: Not shown to candidates, used for final scoring
- **Count**: 5-10+ test cases per question
- **Coverage**: Edge cases, boundary conditions, performance tests, error conditions

### Test Case Categories
1. **Empty/Null Input**: Handle edge cases with no data
2. **Single Element**: Minimal valid input cases
3. **Boundary Values**: Maximum/minimum valid inputs
4. **Error Conditions**: Invalid inputs that should be handled gracefully
5. **Performance Tests**: Large datasets to test efficiency
6. **Special Cases**: Domain-specific edge cases

### Best Practices
- Include explanation for each test case
- Cover both positive and negative scenarios
- Test algorithm correctness and efficiency
- Include unicode/special character tests for string problems
- Test with large datasets for performance validation
- Ensure hidden tests are comprehensive but fair

---

## Important Notes

1. **Test Case Structure**: All test cases must have `input`, `output`, and optional `explanation` fields
2. **Data Types**: Ensure input/output formats match expected function signatures
3. **Edge Cases**: Always include edge cases in hidden test cases
4. **Performance**: Include large input tests to validate algorithmic efficiency
5. **Consistency**: Maintain consistent formatting across all test cases
6. **Coverage**: Aim for 100% code path coverage through test cases
