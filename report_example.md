# Report Generation Examples for Test Cases

**Base URL**: `http://localhost:8000/api/v1/`  
**Headers for authenticated requests:**
```
Content-Type: application/json
Authorization: Bearer <your_access_token>
```

---

## Report Generation for Coding Assessments

This document provides Postman request examples for generating student reports based on the various test case scenarios defined in the system.

---

## 1. Advanced Programming Test Cases Report

### Generate Report for Palindrome, BST, and Pattern Matching Assessment
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 1,
  "student_email": "john.doe@example.com",
  "started_at": "2025-12-15T09:00:00Z",
  "ended_at": "2025-12-15T13:00:00Z",
  "submitted_at": "2025-12-15T12:45:00Z",
  "window_switch_count": 1,
  "is_cheating": false,
  "sections": [
    {
      "section_id": 1,
      "set_number": 1,
      "time_spent": 1800,
      "questions": [
        {
          "question_id": 1,
          "is_attempted": true,
          "code_answer": "def longest_palindrome(s):\n    if not s:\n        return \"\"\n    \n    def expand_around_center(left, right):\n        while left >= 0 and right < len(s) and s[left] == s[right]:\n            left -= 1\n            right += 1\n        return s[left + 1:right]\n    \n    longest = \"\"\n    for i in range(len(s)):\n        # Odd length palindromes\n        palindrome1 = expand_around_center(i, i)\n        # Even length palindromes\n        palindrome2 = expand_around_center(i, i + 1)\n        \n        for p in [palindrome1, palindrome2]:\n            if len(p) > len(longest):\n                longest = p\n    \n    return longest",
          "is_correct": true,
          "marks_obtained": 50,
          "total_marks": 50,
          "time_spent": 1800
        }
      ]
    },
    {
      "section_id": 2,
      "set_number": 1,
      "time_spent": 2400,
      "questions": [
        {
          "question_id": 2,
          "is_attempted": true,
          "code_answer": "class TreeNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.left = None\n        self.right = None\n\nclass BST:\n    def __init__(self):\n        self.root = None\n    \n    def insert(self, val):\n        if not self.root:\n            self.root = TreeNode(val)\n        else:\n            self._insert_recursive(self.root, val)\n    \n    def _insert_recursive(self, node, val):\n        if val < node.val:\n            if node.left:\n                self._insert_recursive(node.left, val)\n            else:\n                node.left = TreeNode(val)\n        else:\n            if node.right:\n                self._insert_recursive(node.right, val)\n            else:\n                node.right = TreeNode(val)\n    \n    def search(self, val):\n        return self._search_recursive(self.root, val)\n    \n    def _search_recursive(self, node, val):\n        if not node:\n            return False\n        if node.val == val:\n            return True\n        elif val < node.val:\n            return self._search_recursive(node.left, val)\n        else:\n            return self._search_recursive(node.right, val)",
          "is_correct": true,
          "marks_obtained": 45,
          "total_marks": 50,
          "time_spent": 2400
        }
      ]
    },
    {
      "section_id": 3,
      "set_number": 1,
      "time_spent": 2100,
      "questions": [
        {
          "question_id": 3,
          "is_attempted": true,
          "code_answer": "def kmp_search(text, pattern):\n    if not pattern:\n        return []\n    if not text:\n        return []\n    \n    # Build failure function\n    def build_failure_function(pattern):\n        failure = [0] * len(pattern)\n        j = 0\n        for i in range(1, len(pattern)):\n            while j > 0 and pattern[i] != pattern[j]:\n                j = failure[j - 1]\n            if pattern[i] == pattern[j]:\n                j += 1\n            failure[i] = j\n        return failure\n    \n    failure = build_failure_function(pattern)\n    matches = []\n    j = 0\n    \n    for i in range(len(text)):\n        while j > 0 and text[i] != pattern[j]:\n            j = failure[j - 1]\n        if text[i] == pattern[j]:\n            j += 1\n        if j == len(pattern):\n            matches.append(i - j + 1)\n            j = failure[j - 1]\n    \n    return matches",
          "is_correct": true,
          "marks_obtained": 48,
          "total_marks": 50,
          "time_spent": 2100
        }
      ]
    }
  ]
}
```

---

## 2. String Reversal Assessment Report

### Generate Report for String Reversal Implementation
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 2,
  "student_email": "jane.smith@example.com",
  "started_at": "2025-12-10T10:00:00Z",
  "ended_at": "2025-12-10T11:00:00Z",
  "submitted_at": "2025-12-10T10:45:00Z",
  "window_switch_count": 0,
  "is_cheating": false,
  "sections": [
    {
      "section_id": 1,
      "set_number": 1,
      "time_spent": 900,
      "questions": [
        {
          "question_id": 4,
          "is_attempted": true,
          "code_answer": "def reverse_string(s):\n    if not s:\n        return \"\"\n    \n    # Convert to list for in-place reversal\n    chars = list(s)\n    left = 0\n    right = len(chars) - 1\n    \n    while left < right:\n        # Swap characters\n        chars[left], chars[right] = chars[right], chars[left]\n        left += 1\n        right -= 1\n    \n    return ''.join(chars)",
          "is_correct": true,
          "marks_obtained": 50,
          "total_marks": 50,
          "time_spent": 900
        }
      ]
    }
  ]
}
```

---

## 3. Array Sorting Assessment Report

### Generate Report for Merge Sort Implementation
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 3,
  "student_email": "alice.johnson@example.com",
  "started_at": "2025-12-12T14:00:00Z",
  "ended_at": "2025-12-12T16:00:00Z",
  "submitted_at": "2025-12-12T15:30:00Z",
  "window_switch_count": 2,
  "is_cheating": false,
  "sections": [
    {
      "section_id": 1,
      "set_number": 1,
      "time_spent": 1800,
      "questions": [
        {
          "question_id": 5,
          "is_attempted": true,
          "code_answer": "def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    \n    # Divide\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    \n    # Conquer\n    return merge(left, right)\n\ndef merge(left, right):\n    result = []\n    i = j = 0\n    \n    # Merge the two sorted arrays\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            result.append(left[i])\n            i += 1\n        else:\n            result.append(right[j])\n            j += 1\n    \n    # Add remaining elements\n    result.extend(left[i:])\n    result.extend(right[j:])\n    \n    return result",
          "is_correct": true,
          "marks_obtained": 58,
          "total_marks": 60,
          "time_spent": 1800
        }
      ]
    }
  ]
}
```

---

## 4. Prime Number Algorithm Report

### Generate Report for Prime Number Detection
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 4,
  "student_email": "bob.wilson@example.com",
  "started_at": "2025-12-18T09:00:00Z",
  "ended_at": "2025-12-18T11:00:00Z",
  "submitted_at": "2025-12-18T10:20:00Z",
  "window_switch_count": 0,
  "is_cheating": false,
  "sections": [
    {
      "section_id": 1,
      "set_number": 1,
      "time_spent": 1200,
      "questions": [
        {
          "question_id": 6,
          "is_attempted": true,
          "code_answer": "import math\n\ndef is_prime(n):\n    # Handle edge cases\n    if n < 2:\n        return False\n    if n == 2:\n        return True\n    if n % 2 == 0:\n        return False\n    \n    # Check odd divisors up to sqrt(n)\n    for i in range(3, int(math.sqrt(n)) + 1, 2):\n        if n % i == 0:\n            return False\n    \n    return True",
          "is_correct": true,
          "marks_obtained": 55,
          "total_marks": 55,
          "time_spent": 1200
        }
      ]
    }
  ]
}
```

---

## 5. Linked List Implementation Report

### Generate Report for Linked List Operations
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 5,
  "student_email": "carol.davis@example.com",
  "started_at": "2025-12-20T10:00:00Z",
  "ended_at": "2025-12-20T13:00:00Z",
  "submitted_at": "2025-12-20T12:45:00Z",
  "window_switch_count": 1,
  "is_cheating": false,
  "sections": [
    {
      "section_id": 1,
      "set_number": 1,
      "time_spent": 2700,
      "questions": [
        {
          "question_id": 7,
          "is_attempted": true,
          "code_answer": "class ListNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.next = None\n\nclass LinkedList:\n    def __init__(self):\n        self.head = None\n        self.size = 0\n    \n    def insert_head(self, val):\n        new_node = ListNode(val)\n        new_node.next = self.head\n        self.head = new_node\n        self.size += 1\n    \n    def insert_tail(self, val):\n        new_node = ListNode(val)\n        if not self.head:\n            self.head = new_node\n        else:\n            current = self.head\n            while current.next:\n                current = current.next\n            current.next = new_node\n        self.size += 1\n    \n    def delete_value(self, val):\n        if not self.head:\n            return False\n        \n        if self.head.val == val:\n            self.head = self.head.next\n            self.size -= 1\n            return True\n        \n        current = self.head\n        while current.next:\n            if current.next.val == val:\n                current.next = current.next.next\n                self.size -= 1\n                return True\n            current = current.next\n        return False\n    \n    def search(self, val):\n        current = self.head\n        while current:\n            if current.val == val:\n                return True\n            current = current.next\n        return False\n    \n    def reverse(self):\n        prev = None\n        current = self.head\n        \n        while current:\n            next_temp = current.next\n            current.next = prev\n            prev = current\n            current = next_temp\n        \n        self.head = prev\n    \n    def display(self):\n        result = []\n        current = self.head\n        while current:\n            result.append(current.val)\n            current = current.next\n        return result",
          "is_correct": true,
          "marks_obtained": 70,
          "total_marks": 75,
          "time_spent": 2700
        }
      ]
    }
  ]
}
```

---

## 6. Dynamic Programming Fibonacci Report

### Generate Report for Fibonacci Implementation
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 6,
  "student_email": "david.brown@example.com",
  "started_at": "2025-12-22T11:00:00Z",
  "ended_at": "2025-12-22T12:30:00Z",
  "submitted_at": "2025-12-22T12:25:00Z",
  "window_switch_count": 0,
  "is_cheating": false,
  "sections": [
    {
      "section_id": 1,
      "set_number": 1,
      "time_spent": 1500,
      "questions": [
        {
          "question_id": 8,
          "is_attempted": true,
          "code_answer": "def fibonacci(n, memo={}):\n    # Handle base cases\n    if n in memo:\n        return memo[n]\n    \n    if n <= 1:\n        return n\n    \n    # Memoized recursive approach\n    memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo)\n    return memo[n]\n\n# Alternative bottom-up approach for better space complexity\ndef fibonacci_optimized(n):\n    if n <= 1:\n        return n\n    \n    a, b = 0, 1\n    for i in range(2, n + 1):\n        a, b = b, a + b\n    \n    return b",
          "is_correct": true,
          "marks_obtained": 50,
          "total_marks": 50,
          "time_spent": 1500
        }
      ]
    }
  ]
}
```

---

## 7. Graph Algorithms Report

### Generate Report for DFS and BFS Implementation
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 7,
  "student_email": "eve.taylor@example.com",
  "started_at": "2025-12-25T14:00:00Z",
  "ended_at": "2025-12-25T17:00:00Z",
  "submitted_at": "2025-12-25T16:50:00Z",
  "window_switch_count": 3,
  "is_cheating": false,
  "sections": [
    {
      "section_id": 1,
      "set_number": 1,
      "time_spent": 3000,
      "questions": [
        {
          "question_id": 9,
          "is_attempted": true,
          "code_answer": "from collections import defaultdict, deque\n\nclass Graph:\n    def __init__(self):\n        self.graph = defaultdict(list)\n        self.vertices = set()\n    \n    def add_edge(self, u, v):\n        self.graph[u].append(v)\n        self.graph[v].append(u)  # Undirected graph\n        self.vertices.add(u)\n        self.vertices.add(v)\n    \n    def dfs_recursive(self, start, visited=None):\n        if visited is None:\n            visited = set()\n        \n        visited.add(start)\n        result = [start]\n        \n        for neighbor in self.graph[start]:\n            if neighbor not in visited:\n                result.extend(self.dfs_recursive(neighbor, visited))\n        \n        return result\n    \n    def dfs_iterative(self, start):\n        visited = set()\n        stack = [start]\n        result = []\n        \n        while stack:\n            vertex = stack.pop()\n            if vertex not in visited:\n                visited.add(vertex)\n                result.append(vertex)\n                # Add neighbors in reverse order for consistent traversal\n                for neighbor in reversed(self.graph[vertex]):\n                    if neighbor not in visited:\n                        stack.append(neighbor)\n        \n        return result\n    \n    def bfs(self, start):\n        visited = set()\n        queue = deque([start])\n        result = []\n        \n        visited.add(start)\n        \n        while queue:\n            vertex = queue.popleft()\n            result.append(vertex)\n            \n            for neighbor in self.graph[vertex]:\n                if neighbor not in visited:\n                    visited.add(neighbor)\n                    queue.append(neighbor)\n        \n        return result\n    \n    def find_all_components(self):\n        visited = set()\n        components = []\n        \n        for vertex in self.vertices:\n            if vertex not in visited:\n                component = self.dfs_recursive(vertex, visited)\n                components.append(component)\n        \n        return components\n    \n    def is_connected(self):\n        if not self.vertices:\n            return True\n        \n        start = next(iter(self.vertices))\n        visited = set()\n        self.dfs_recursive(start, visited)\n        \n        return len(visited) == len(self.vertices)",
          "is_correct": true,
          "marks_obtained": 80,
          "total_marks": 85,
          "time_spent": 3000
        }
      ]
    }
  ]
}
```

---

## 8. Partial Implementation Report

### Generate Report for Incomplete Solution
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 1,
  "student_email": "incomplete.student@example.com",
  "started_at": "2025-12-15T09:00:00Z",
  "ended_at": "2025-12-15T13:00:00Z",
  "submitted_at": "2025-12-15T13:00:00Z",
  "window_switch_count": 5,
  "is_cheating": false,
  "sections": [
    {
      "section_id": 1,
      "set_number": 1,
      "time_spent": 1800,
      "questions": [
        {
          "question_id": 1,
          "is_attempted": true,
          "code_answer": "def longest_palindrome(s):\n    # Partial implementation\n    if not s:\n        return \"\"\n    \n    # Only handles simple cases\n    for i in range(len(s), 0, -1):\n        for j in range(len(s) - i + 1):\n            substring = s[j:j+i]\n            if substring == substring[::-1]:\n                return substring\n    \n    return s[0]",
          "is_correct": false,
          "marks_obtained": 25,
          "total_marks": 50,
          "time_spent": 1800
        }
      ]
    },
    {
      "section_id": 2,
      "set_number": 1,
      "time_spent": 2400,
      "questions": [
        {
          "question_id": 2,
          "is_attempted": true,
          "code_answer": "# Incomplete BST implementation\nclass TreeNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.left = None\n        self.right = None\n\nclass BST:\n    def __init__(self):\n        self.root = None\n    \n    def insert(self, val):\n        # Basic insertion only\n        if not self.root:\n            self.root = TreeNode(val)\n    \n    def search(self, val):\n        # Incomplete search\n        return self.root and self.root.val == val",
          "is_correct": false,
          "marks_obtained": 15,
          "total_marks": 50,
          "time_spent": 2400
        }
      ]
    },
    {
      "section_id": 3,
      "set_number": 1,
      "time_spent": 1200,
      "questions": [
        {
          "question_id": 3,
          "is_attempted": false,
          "code_answer": "",
          "is_correct": false,
          "marks_obtained": 0,
          "total_marks": 50,
          "time_spent": 0
        }
      ]
    }
  ]
}
```

---

## 9. Time Management Issues Report

### Generate Report for Student with Time Management Problems
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 5,
  "student_email": "slow.student@example.com",
  "started_at": "2025-12-20T10:00:00Z",
  "ended_at": "2025-12-20T13:00:00Z",
  "submitted_at": "2025-12-20T13:00:00Z",
  "window_switch_count": 0,
  "is_cheating": false,
  "sections": [
    {
      "section_id": 1,
      "set_number": 1,
      "time_spent": 10800,
      "questions": [
        {
          "question_id": 7,
          "is_attempted": true,
          "code_answer": "class ListNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.next = None\n\nclass LinkedList:\n    def __init__(self):\n        self.head = None\n    \n    def insert_head(self, val):\n        new_node = ListNode(val)\n        new_node.next = self.head\n        self.head = new_node\n    \n    def display(self):\n        result = []\n        current = self.head\n        while current:\n            result.append(current.val)\n            current = current.next\n        return result\n    \n    # Missing other required methods due to time constraints",
          "is_correct": false,
          "marks_obtained": 30,
          "total_marks": 75,
          "time_spent": 10800
        }
      ]
    }
  ]
}
```

---

## 10. Perfect Score Report

### Generate Report for Excellent Performance
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 6,
  "student_email": "excellent.student@example.com",
  "started_at": "2025-12-22T11:00:00Z",
  "ended_at": "2025-12-22T12:30:00Z",
  "submitted_at": "2025-12-22T12:00:00Z",
  "window_switch_count": 0,
  "is_cheating": false,
  "sections": [
    {
      "section_id": 1,
      "set_number": 1,
      "time_spent": 900,
      "questions": [
        {
          "question_id": 8,
          "is_attempted": true,
          "code_answer": "def fibonacci(n):\n    \"\"\"Optimized Fibonacci with O(n) time and O(1) space complexity.\"\"\"\n    if n <= 1:\n        return n\n    \n    # Iterative approach with constant space\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    \n    return b\n\n# Alternative matrix exponentiation for O(log n) solution\ndef fibonacci_matrix(n):\n    \"\"\"Matrix exponentiation approach for very large n.\"\"\"\n    if n <= 1:\n        return n\n    \n    def matrix_mult(a, b):\n        return [[a[0][0]*b[0][0] + a[0][1]*b[1][0],\n                 a[0][0]*b[0][1] + a[0][1]*b[1][1]],\n                [a[1][0]*b[0][0] + a[1][1]*b[1][0],\n                 a[1][0]*b[0][1] + a[1][1]*b[1][1]]]\n    \n    def matrix_power(matrix, power):\n        if power == 1:\n            return matrix\n        if power % 2 == 0:\n            half = matrix_power(matrix, power // 2)\n            return matrix_mult(half, half)\n        else:\n            return matrix_mult(matrix, matrix_power(matrix, power - 1))\n    \n    base_matrix = [[1, 1], [1, 0]]\n    result_matrix = matrix_power(base_matrix, n)\n    return result_matrix[0][1]",
          "is_correct": true,
          "marks_obtained": 50,
          "total_marks": 50,
          "time_spent": 900
        }
      ]
    }
  ]
}
```

---

## 11. Multiple Coding Questions Assessment Report

### Generate Report for Complex Multi-Section Assessment
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 8,
  "student_email": "comprehensive.student@example.com",
  "started_at": "2025-12-30T09:00:00Z",
  "ended_at": "2025-12-30T15:00:00Z",
  "submitted_at": "2025-12-30T14:45:00Z",
  "window_switch_count": 2,
  "is_cheating": false,
  "sections": [
    {
      "section_id": 1,
      "set_number": 1,
      "time_spent": 3600,
      "questions": [
        {
          "question_id": 10,
          "is_attempted": true,
          "code_answer": "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    \n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    \n    return quicksort(left) + middle + quicksort(right)",
          "is_correct": true,
          "marks_obtained": 45,
          "total_marks": 50,
          "time_spent": 1800
        },
        {
          "question_id": 11,
          "is_attempted": true,
          "code_answer": "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    \n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    \n    return -1",
          "is_correct": true,
          "marks_obtained": 50,
          "total_marks": 50,
          "time_spent": 1800
        }
      ]
    },
    {
      "section_id": 2,
      "set_number": 1,
      "time_spent": 7200,
      "questions": [
        {
          "question_id": 12,
          "is_attempted": true,
          "code_answer": "def validate_parentheses(s):\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    \n    for char in s:\n        if char in mapping:\n            if not stack or stack.pop() != mapping[char]:\n                return False\n        else:\n            stack.append(char)\n    \n    return not stack",
          "is_correct": true,
          "marks_obtained": 48,
          "total_marks": 50,
          "time_spent": 3600
        },
        {
          "question_id": 13,
          "is_attempted": true,
          "code_answer": "class Queue:\n    def __init__(self):\n        self.items = []\n    \n    def enqueue(self, item):\n        self.items.append(item)\n    \n    def dequeue(self):\n        if self.is_empty():\n            return None\n        return self.items.pop(0)\n    \n    def is_empty(self):\n        return len(self.items) == 0\n    \n    def size(self):\n        return len(self.items)",
          "is_correct": true,
          "marks_obtained": 47,
          "total_marks": 50,
          "time_spent": 3600
        }
      ]
    },
    {
      "section_id": 3,
      "set_number": 1,
      "time_spent": 10800,
      "questions": [
        {
          "question_id": 14,
          "is_attempted": true,
          "code_answer": "def longest_common_subsequence(text1, text2):\n    m, n = len(text1), len(text2)\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    \n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            if text1[i-1] == text2[j-1]:\n                dp[i][j] = dp[i-1][j-1] + 1\n            else:\n                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n    \n    return dp[m][n]",
          "is_correct": true,
          "marks_obtained": 50,
          "total_marks": 50,
          "time_spent": 5400
        },
        {
          "question_id": 15,
          "is_attempted": true,
          "code_answer": "def coin_change(coins, amount):\n    dp = [float('inf')] * (amount + 1)\n    dp[0] = 0\n    \n    for coin in coins:\n        for i in range(coin, amount + 1):\n            dp[i] = min(dp[i], dp[i - coin] + 1)\n    \n    return dp[amount] if dp[amount] != float('inf') else -1",
          "is_correct": true,
          "marks_obtained": 49,
          "total_marks": 50,
          "time_spent": 5400
        }
      ]
    }
  ]
}
```

---

## 12. Error-Prone Student Report

### Generate Report for Student with Syntax Errors
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 2,
  "student_email": "error.prone@example.com",
  "started_at": "2025-12-10T10:00:00Z",
  "ended_at": "2025-12-10T11:00:00Z",
  "submitted_at": "2025-12-10T11:00:00Z",
  "window_switch_count": 8,
  "is_cheating": false,
  "sections": [
    {
      "section_id": 1,
      "set_number": 1,
      "time_spent": 3600,
      "questions": [
        {
          "question_id": 4,
          "is_attempted": true,
          "code_answer": "def reverse_string(s):\n    # Multiple syntax and logic errors\n    if not s\n        return \"\"\n    \n    result = \"\"\n    for i in range(len(s), 0, -1):  # Off-by-one error\n        result += s[i]  # Index error\n    \n    return result",
          "is_correct": false,
          "marks_obtained": 10,
          "total_marks": 50,
          "time_spent": 3600
        }
      ]
    }
  ]
}
```

---

## 13. Late Submission Report

### Generate Report for Student Who Submitted After Deadline
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 4,
  "student_email": "late.student@example.com",
  "started_at": "2025-12-18T09:00:00Z",
  "ended_at": "2025-12-18T11:00:00Z",
  "submitted_at": "2025-12-18T11:15:00Z",
  "window_switch_count": 1,
  "is_cheating": false,
  "cheating_reason": "",
  "sections": [
    {
      "section_id": 1,
      "set_number": 1,
      "time_spent": 4500,
      "questions": [
        {
          "question_id": 6,
          "is_attempted": true,
          "code_answer": "def is_prime(n):\n    if n < 2:\n        return False\n    \n    for i in range(2, n):\n        if n % i == 0:\n            return False\n    \n    return True",
          "is_correct": false,
          "marks_obtained": 35,
          "total_marks": 55,
          "time_spent": 4500
        }
      ]
    }
  ]
}
```

---

## Important Notes

### Report Data Structure
1. **assessment_id**: Must match an existing assessment in the system
2. **Timing Fields**: Use ISO 8601 format for all datetime fields
3. **Code Answers**: Include actual code submissions for coding questions
4. **Marks**: Ensure marks_obtained ≤ total_marks for each question
5. **Time Tracking**: time_spent should be realistic for the complexity

### Performance Indicators
- **High Performance**: Quick completion time, correct solutions, minimal window switches
- **Average Performance**: Partial solutions, reasonable time usage, some errors
- **Poor Performance**: Incomplete solutions, time management issues, syntax errors

### Cheating Detection
- **Window Switches**: High count may indicate tab switching
- **Submission Patterns**: Unusually fast perfect solutions may be suspicious
- **Code Similarity**: Identical solutions across students should be flagged

### AI Tips Generation
Reports with this data will trigger AI analysis providing:
- **Strengths**: Areas where the student performed well
- **Weaknesses**: Topics needing improvement
- **Study Recommendations**: Specific actionable advice
- **Motivational Messages**: Encouraging feedback based on performance level
