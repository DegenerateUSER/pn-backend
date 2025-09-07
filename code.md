# Code Execution and Submission API Documentation

**Base URL**: `http://localhost:8000/api/v1/`  
**Headers for authenticated requests:**
```
Content-Type: application/json
Authorization: Bearer <your_access_token>
```

---

## Code Execution and Submission for Coding Assessments

This document provides Postman request examples for running and submitting code solutions for all test case scenarios defined in the assessment system.

---

## 1. Palindrome Problem - Code Execution and Submission

### Run Code for Palindrome Problem
```http
POST /api/v1/code/run
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "def longest_palindrome(s):\n    if not s:\n        return \"\"\n    \n    def expand_around_center(left, right):\n        while left >= 0 and right < len(s) and s[left] == s[right]:\n            left -= 1\n            right += 1\n        return s[left + 1:right]\n    \n    longest = \"\"\n    for i in range(len(s)):\n        # Odd length palindromes\n        palindrome1 = expand_around_center(i, i)\n        # Even length palindromes\n        palindrome2 = expand_around_center(i, i + 1)\n        \n        for p in [palindrome1, palindrome2]:\n            if len(p) > len(longest):\n                longest = p\n    \n    return longest\n\n# Test with sample input\nprint(longest_palindrome(\"babad\"))",
  "language": "python",
  "versionIndex": "3.9"
}
```

### Submit Code for Palindrome Problem
```http
POST /api/v1/code/submit
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "def longest_palindrome(s):\n    if not s:\n        return \"\"\n    \n    def expand_around_center(left, right):\n        while left >= 0 and right < len(s) and s[left] == s[right]:\n            left -= 1\n            right += 1\n        return s[left + 1:right]\n    \n    longest = \"\"\n    for i in range(len(s)):\n        # Odd length palindromes\n        palindrome1 = expand_around_center(i, i)\n        # Even length palindromes\n        palindrome2 = expand_around_center(i, i + 1)\n        \n        for p in [palindrome1, palindrome2]:\n            if len(p) > len(longest):\n                longest = p\n    \n    return longest\n\n# Read input and call function\ninput_str = input().strip()\nresult = longest_palindrome(input_str)\nprint(result)",
  "language": "python",
  "versionIndex": "3.9",
  "question_id": 1,
  "assessment_id": 1
}
```

---

## 2. Binary Search Tree - Code Execution and Submission

### Run Code for BST Implementation
```http
POST /api/v1/code/run
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "class TreeNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.left = None\n        self.right = None\n\nclass BST:\n    def __init__(self):\n        self.root = None\n    \n    def insert(self, val):\n        if not self.root:\n            self.root = TreeNode(val)\n        else:\n            self._insert_recursive(self.root, val)\n    \n    def _insert_recursive(self, node, val):\n        if val < node.val:\n            if node.left:\n                self._insert_recursive(node.left, val)\n            else:\n                node.left = TreeNode(val)\n        else:\n            if node.right:\n                self._insert_recursive(node.right, val)\n            else:\n                node.right = TreeNode(val)\n    \n    def search(self, val):\n        return self._search_recursive(self.root, val)\n    \n    def _search_recursive(self, node, val):\n        if not node:\n            return False\n        if node.val == val:\n            return True\n        elif val < node.val:\n            return self._search_recursive(node.left, val)\n        else:\n            return self._search_recursive(node.right, val)\n    \n    def delete(self, val):\n        self.root = self._delete_recursive(self.root, val)\n    \n    def _delete_recursive(self, node, val):\n        if not node:\n            return node\n        \n        if val < node.val:\n            node.left = self._delete_recursive(node.left, val)\n        elif val > node.val:\n            node.right = self._delete_recursive(node.right, val)\n        else:\n            # Node to be deleted found\n            if not node.left:\n                return node.right\n            elif not node.right:\n                return node.left\n            \n            # Node with two children\n            temp = self._find_min(node.right)\n            node.val = temp.val\n            node.right = self._delete_recursive(node.right, temp.val)\n        \n        return node\n    \n    def _find_min(self, node):\n        while node.left:\n            node = node.left\n        return node\n    \n    def inorder_traversal(self):\n        result = []\n        self._inorder_recursive(self.root, result)\n        return result\n    \n    def _inorder_recursive(self, node, result):\n        if node:\n            self._inorder_recursive(node.left, result)\n            result.append(node.val)\n            self._inorder_recursive(node.right, result)\n\n# Test the BST\nbst = BST()\nfor val in [5, 3, 7, 2, 4, 6, 8]:\n    bst.insert(val)\n\nprint(\"Search 4:\", bst.search(4))\nprint(\"Inorder traversal:\", bst.inorder_traversal())\nbst.delete(5)\nprint(\"After deleting 5:\", bst.inorder_traversal())",
  "language": "python",
  "versionIndex": "3.9"
}
```

### Submit Code for BST Implementation
```http
POST /api/v1/code/submit
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "class TreeNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.left = None\n        self.right = None\n\nclass BST:\n    def __init__(self):\n        self.root = None\n    \n    def insert(self, val):\n        if not self.root:\n            self.root = TreeNode(val)\n        else:\n            self._insert_recursive(self.root, val)\n    \n    def _insert_recursive(self, node, val):\n        if val < node.val:\n            if node.left:\n                self._insert_recursive(node.left, val)\n            else:\n                node.left = TreeNode(val)\n        else:\n            if node.right:\n                self._insert_recursive(node.right, val)\n            else:\n                node.right = TreeNode(val)\n    \n    def search(self, val):\n        return self._search_recursive(self.root, val)\n    \n    def _search_recursive(self, node, val):\n        if not node:\n            return False\n        if node.val == val:\n            return True\n        elif val < node.val:\n            return self._search_recursive(node.left, val)\n        else:\n            return self._search_recursive(node.right, val)\n    \n    def delete(self, val):\n        self.root = self._delete_recursive(self.root, val)\n    \n    def _delete_recursive(self, node, val):\n        if not node:\n            return node\n        \n        if val < node.val:\n            node.left = self._delete_recursive(node.left, val)\n        elif val > node.val:\n            node.right = self._delete_recursive(node.right, val)\n        else:\n            if not node.left:\n                return node.right\n            elif not node.right:\n                return node.left\n            \n            temp = self._find_min(node.right)\n            node.val = temp.val\n            node.right = self._delete_recursive(node.right, temp.val)\n        \n        return node\n    \n    def _find_min(self, node):\n        while node.left:\n            node = node.left\n        return node\n    \n    def inorder_traversal(self):\n        result = []\n        self._inorder_recursive(self.root, result)\n        return result\n    \n    def _inorder_recursive(self, node, result):\n        if node:\n            self._inorder_recursive(node.left, result)\n            result.append(node.val)\n            self._inorder_recursive(node.right, result)",
  "language": "python",
  "versionIndex": "3.9",
  "question_id": 2,
  "assessment_id": 1
}
```

---

## 3. String Pattern Matching - Code Execution and Submission

### Run Code for KMP Algorithm
```http
POST /api/v1/code/run
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "def kmp_search(text, pattern):\n    if not pattern:\n        return []\n    if not text:\n        return []\n    \n    def build_failure_function(pattern):\n        failure = [0] * len(pattern)\n        j = 0\n        for i in range(1, len(pattern)):\n            while j > 0 and pattern[i] != pattern[j]:\n                j = failure[j - 1]\n            if pattern[i] == pattern[j]:\n                j += 1\n            failure[i] = j\n        return failure\n    \n    failure = build_failure_function(pattern)\n    matches = []\n    j = 0\n    \n    for i in range(len(text)):\n        while j > 0 and text[i] != pattern[j]:\n            j = failure[j - 1]\n        if text[i] == pattern[j]:\n            j += 1\n        if j == len(pattern):\n            matches.append(i - j + 1)\n            j = failure[j - 1]\n    \n    return matches\n\n# Test cases\nprint(kmp_search('ABABDABACDABABCABCABCABCABC', 'ABABCABCAB'))\nprint(kmp_search('AAAAAA', 'AA'))\nprint(kmp_search('Hello World', 'o'))",
  "language": "python",
  "versionIndex": "3.9"
}
```

### Submit Code for Pattern Matching
```http
POST /api/v1/code/submit
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "def kmp_search(text, pattern):\n    if not pattern:\n        return []\n    if not text:\n        return []\n    \n    def build_failure_function(pattern):\n        failure = [0] * len(pattern)\n        j = 0\n        for i in range(1, len(pattern)):\n            while j > 0 and pattern[i] != pattern[j]:\n                j = failure[j - 1]\n            if pattern[i] == pattern[j]:\n                j += 1\n            failure[i] = j\n        return failure\n    \n    failure = build_failure_function(pattern)\n    matches = []\n    j = 0\n    \n    for i in range(len(text)):\n        while j > 0 and text[i] != pattern[j]:\n            j = failure[j - 1]\n        if text[i] == pattern[j]:\n            j += 1\n        if j == len(pattern):\n            matches.append(i - j + 1)\n            j = failure[j - 1]\n    \n    return matches",
  "language": "python",
  "versionIndex": "3.9",
  "question_id": 3,
  "assessment_id": 1
}
```

---

## 4. String Reversal - Code Execution and Submission

### Run Code for String Reversal
```http
POST /api/v1/code/run
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "def reverse_string(s):\n    if not s:\n        return \"\"\n    \n    # Convert to list for in-place reversal\n    chars = list(s)\n    left = 0\n    right = len(chars) - 1\n    \n    while left < right:\n        # Swap characters\n        chars[left], chars[right] = chars[right], chars[left]\n        left += 1\n        right -= 1\n    \n    return ''.join(chars)\n\n# Test cases\nprint(reverse_string(\"hello\"))\nprint(reverse_string(\"world\"))\nprint(reverse_string(\"Python\"))\nprint(reverse_string(\"\"))\nprint(reverse_string(\"a\"))",
  "language": "python",
  "versionIndex": "3.9"
}
```

### Submit Code for String Reversal
```http
POST /api/v1/code/submit
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "def reverse_string(s):\n    if not s:\n        return \"\"\n    \n    chars = list(s)\n    left = 0\n    right = len(chars) - 1\n    \n    while left < right:\n        chars[left], chars[right] = chars[right], chars[left]\n        left += 1\n        right -= 1\n    \n    return ''.join(chars)\n\n# Read input and call function\ninput_str = input().strip()\nresult = reverse_string(input_str)\nprint(result)",
  "language": "python",
  "versionIndex": "3.9",
  "question_id": 4,
  "assessment_id": 2
}
```

---

## 5. Merge Sort - Code Execution and Submission

### Run Code for Merge Sort
```http
POST /api/v1/code/run
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    \n    # Divide\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    \n    # Conquer\n    return merge(left, right)\n\ndef merge(left, right):\n    result = []\n    i = j = 0\n    \n    # Merge the two sorted arrays\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            result.append(left[i])\n            i += 1\n        else:\n            result.append(right[j])\n            j += 1\n    \n    # Add remaining elements\n    result.extend(left[i:])\n    result.extend(right[j:])\n    \n    return result\n\n# Test cases\nprint(merge_sort([64, 34, 25, 12, 22, 11, 90]))\nprint(merge_sort([5, 2, 4, 6, 1, 3]))\nprint(merge_sort([1, 2, 3, 4, 5]))\nprint(merge_sort([]))\nprint(merge_sort([42]))",
  "language": "python",
  "versionIndex": "3.9"
}
```

### Submit Code for Merge Sort
```http
POST /api/v1/code/submit
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    \n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    \n    return merge(left, right)\n\ndef merge(left, right):\n    result = []\n    i = j = 0\n    \n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            result.append(left[i])\n            i += 1\n        else:\n            result.append(right[j])\n            j += 1\n    \n    result.extend(left[i:])\n    result.extend(right[j:])\n    \n    return result",
  "language": "python",
  "versionIndex": "3.9",
  "question_id": 5,
  "assessment_id": 3
}
```

---

## 6. Prime Number Detection - Code Execution and Submission

### Run Code for Prime Number Algorithm
```http
POST /api/v1/code/run
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "import math\n\ndef is_prime(n):\n    # Handle edge cases\n    if n < 2:\n        return False\n    if n == 2:\n        return True\n    if n % 2 == 0:\n        return False\n    \n    # Check odd divisors up to sqrt(n)\n    for i in range(3, int(math.sqrt(n)) + 1, 2):\n        if n % i == 0:\n            return False\n    \n    return True\n\n# Test cases\nprint(is_prime(17))\nprint(is_prime(4))\nprint(is_prime(97))\nprint(is_prime(0))\nprint(is_prime(1))\nprint(is_prime(2))\nprint(is_prime(101))",
  "language": "python",
  "versionIndex": "3.9"
}
```

### Submit Code for Prime Number Detection
```http
POST /api/v1/code/submit
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "import math\n\ndef is_prime(n):\n    if n < 2:\n        return False\n    if n == 2:\n        return True\n    if n % 2 == 0:\n        return False\n    \n    for i in range(3, int(math.sqrt(n)) + 1, 2):\n        if n % i == 0:\n            return False\n    \n    return True\n\n# Read input and call function\nn = int(input().strip())\nresult = is_prime(n)\nprint('true' if result else 'false')",
  "language": "python",
  "versionIndex": "3.9",
  "question_id": 6,
  "assessment_id": 4
}
```

---

## 7. Linked List Implementation - Code Execution and Submission

### Run Code for Linked List
```http
POST /api/v1/code/run
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "class ListNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.next = None\n\nclass LinkedList:\n    def __init__(self):\n        self.head = None\n        self.size = 0\n    \n    def insert_head(self, val):\n        new_node = ListNode(val)\n        new_node.next = self.head\n        self.head = new_node\n        self.size += 1\n    \n    def insert_tail(self, val):\n        new_node = ListNode(val)\n        if not self.head:\n            self.head = new_node\n        else:\n            current = self.head\n            while current.next:\n                current = current.next\n            current.next = new_node\n        self.size += 1\n    \n    def delete_value(self, val):\n        if not self.head:\n            return False\n        \n        if self.head.val == val:\n            self.head = self.head.next\n            self.size -= 1\n            return True\n        \n        current = self.head\n        while current.next:\n            if current.next.val == val:\n                current.next = current.next.next\n                self.size -= 1\n                return True\n            current = current.next\n        return False\n    \n    def search(self, val):\n        current = self.head\n        while current:\n            if current.val == val:\n                return True\n            current = current.next\n        return False\n    \n    def reverse(self):\n        prev = None\n        current = self.head\n        \n        while current:\n            next_temp = current.next\n            current.next = prev\n            prev = current\n            current = next_temp\n        \n        self.head = prev\n    \n    def display(self):\n        result = []\n        current = self.head\n        while current:\n            result.append(current.val)\n            current = current.next\n        return result\n\n# Test the linked list\nll = LinkedList()\nll.insert_head(5)\nll.insert_head(3)\nll.insert_tail(7)\nprint(\"After insertions:\", ll.display())\nprint(\"Search 3:\", ll.search(3))\nll.delete_value(3)\nprint(\"After deleting 3:\", ll.display())\nll.reverse()\nprint(\"After reverse:\", ll.display())",
  "language": "python",
  "versionIndex": "3.9"
}
```

### Submit Code for Linked List
```http
POST /api/v1/code/submit
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "class ListNode:\n    def __init__(self, val=0):\n        self.val = val\n        self.next = None\n\nclass LinkedList:\n    def __init__(self):\n        self.head = None\n        self.size = 0\n    \n    def insert_head(self, val):\n        new_node = ListNode(val)\n        new_node.next = self.head\n        self.head = new_node\n        self.size += 1\n    \n    def insert_tail(self, val):\n        new_node = ListNode(val)\n        if not self.head:\n            self.head = new_node\n        else:\n            current = self.head\n            while current.next:\n                current = current.next\n            current.next = new_node\n        self.size += 1\n    \n    def delete_value(self, val):\n        if not self.head:\n            return False\n        \n        if self.head.val == val:\n            self.head = self.head.next\n            self.size -= 1\n            return True\n        \n        current = self.head\n        while current.next:\n            if current.next.val == val:\n                current.next = current.next.next\n                self.size -= 1\n                return True\n            current = current.next\n        return False\n    \n    def search(self, val):\n        current = self.head\n        while current:\n            if current.val == val:\n                return True\n            current = current.next\n        return False\n    \n    def reverse(self):\n        prev = None\n        current = self.head\n        \n        while current:\n            next_temp = current.next\n            current.next = prev\n            prev = current\n            current = next_temp\n        \n        self.head = prev\n    \n    def display(self):\n        result = []\n        current = self.head\n        while current:\n            result.append(current.val)\n            current = current.next\n        return result",
  "language": "python",
  "versionIndex": "3.9",
  "question_id": 7,
  "assessment_id": 5
}
```

---

## 8. Fibonacci with Dynamic Programming - Code Execution and Submission

### Run Code for Fibonacci Algorithm
```http
POST /api/v1/code/run
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "def fibonacci(n, memo={}):\n    # Handle base cases\n    if n in memo:\n        return memo[n]\n    \n    if n <= 1:\n        return n\n    \n    # Memoized recursive approach\n    memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo)\n    return memo[n]\n\n# Alternative optimized approach\ndef fibonacci_optimized(n):\n    if n <= 1:\n        return n\n    \n    a, b = 0, 1\n    for i in range(2, n + 1):\n        a, b = b, a + b\n    \n    return b\n\n# Test cases\nprint(\"Fibonacci(5):\", fibonacci(5))\nprint(\"Fibonacci(10):\", fibonacci(10))\nprint(\"Fibonacci(0):\", fibonacci(0))\nprint(\"Fibonacci(1):\", fibonacci(1))\nprint(\"Fibonacci(15):\", fibonacci_optimized(15))\nprint(\"Fibonacci(20):\", fibonacci_optimized(20))",
  "language": "python",
  "versionIndex": "3.9"
}
```

### Submit Code for Fibonacci
```http
POST /api/v1/code/submit
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "def fibonacci(n):\n    if n <= 1:\n        return n\n    \n    a, b = 0, 1\n    for i in range(2, n + 1):\n        a, b = b, a + b\n    \n    return b\n\n# Read input and call function\nn = int(input().strip())\nresult = fibonacci(n)\nprint(result)",
  "language": "python",
  "versionIndex": "3.9",
  "question_id": 8,
  "assessment_id": 6
}
```

---

## 9. Graph Algorithms (DFS/BFS) - Code Execution and Submission

### Run Code for Graph Traversal
```http
POST /api/v1/code/run
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "from collections import defaultdict, deque\n\nclass Graph:\n    def __init__(self):\n        self.graph = defaultdict(list)\n        self.vertices = set()\n    \n    def add_edge(self, u, v):\n        self.graph[u].append(v)\n        self.graph[v].append(u)  # Undirected graph\n        self.vertices.add(u)\n        self.vertices.add(v)\n    \n    def dfs_recursive(self, start, visited=None):\n        if visited is None:\n            visited = set()\n        \n        visited.add(start)\n        result = [start]\n        \n        for neighbor in self.graph[start]:\n            if neighbor not in visited:\n                result.extend(self.dfs_recursive(neighbor, visited))\n        \n        return result\n    \n    def dfs_iterative(self, start):\n        visited = set()\n        stack = [start]\n        result = []\n        \n        while stack:\n            vertex = stack.pop()\n            if vertex not in visited:\n                visited.add(vertex)\n                result.append(vertex)\n                for neighbor in reversed(self.graph[vertex]):\n                    if neighbor not in visited:\n                        stack.append(neighbor)\n        \n        return result\n    \n    def bfs(self, start):\n        visited = set()\n        queue = deque([start])\n        result = []\n        \n        visited.add(start)\n        \n        while queue:\n            vertex = queue.popleft()\n            result.append(vertex)\n            \n            for neighbor in self.graph[vertex]:\n                if neighbor not in visited:\n                    visited.add(neighbor)\n                    queue.append(neighbor)\n        \n        return result\n\n# Test the graph\ng = Graph()\ng.add_edge(0, 1)\ng.add_edge(0, 2)\ng.add_edge(1, 3)\ng.add_edge(2, 3)\n\nprint(\"DFS from 0:\", g.dfs_recursive(0))\nprint(\"BFS from 0:\", g.bfs(0))\nprint(\"DFS iterative from 0:\", g.dfs_iterative(0))",
  "language": "python",
  "versionIndex": "3.9"
}
```

### Submit Code for Graph Algorithms
```http
POST /api/v1/code/submit
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "from collections import defaultdict, deque\n\nclass Graph:\n    def __init__(self):\n        self.graph = defaultdict(list)\n        self.vertices = set()\n    \n    def add_edge(self, u, v):\n        self.graph[u].append(v)\n        self.graph[v].append(u)\n        self.vertices.add(u)\n        self.vertices.add(v)\n    \n    def dfs_recursive(self, start, visited=None):\n        if visited is None:\n            visited = set()\n        \n        visited.add(start)\n        result = [start]\n        \n        for neighbor in self.graph[start]:\n            if neighbor not in visited:\n                result.extend(self.dfs_recursive(neighbor, visited))\n        \n        return result\n    \n    def bfs(self, start):\n        visited = set()\n        queue = deque([start])\n        result = []\n        \n        visited.add(start)\n        \n        while queue:\n            vertex = queue.popleft()\n            result.append(vertex)\n            \n            for neighbor in self.graph[vertex]:\n                if neighbor not in visited:\n                    visited.add(neighbor)\n                    queue.append(neighbor)\n        \n        return result",
  "language": "python",
  "versionIndex": "3.9",
  "question_id": 9,
  "assessment_id": 7
}
```

---

## 10. JavaScript Code Examples

### Run JavaScript Code - Array Manipulation
```http
POST /api/v1/code/run
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "function quickSort(arr) {\n    if (arr.length <= 1) {\n        return arr;\n    }\n    \n    const pivot = arr[Math.floor(arr.length / 2)];\n    const left = arr.filter(x => x < pivot);\n    const middle = arr.filter(x => x === pivot);\n    const right = arr.filter(x => x > pivot);\n    \n    return [...quickSort(left), ...middle, ...quickSort(right)];\n}\n\n// Test cases\nconsole.log(quickSort([64, 34, 25, 12, 22, 11, 90]));\nconsole.log(quickSort([5, 2, 4, 6, 1, 3]));\nconsole.log(quickSort([1, 2, 3, 4, 5]));",
  "language": "javascript",
  "versionIndex": "18.x"
}
```

### Submit JavaScript Code
```http
POST /api/v1/code/submit
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "function quickSort(arr) {\n    if (arr.length <= 1) {\n        return arr;\n    }\n    \n    const pivot = arr[Math.floor(arr.length / 2)];\n    const left = arr.filter(x => x < pivot);\n    const middle = arr.filter(x => x === pivot);\n    const right = arr.filter(x => x > pivot);\n    \n    return [...quickSort(left), ...middle, ...quickSort(right)];\n}",
  "language": "javascript",
  "versionIndex": "18.x",
  "question_id": 10,
  "assessment_id": 8
}
```

---

## 11. Java Code Examples

### Run Java Code - Palindrome Check
```http
POST /api/v1/code/run
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "public class Solution {\n    public static String longestPalindrome(String s) {\n        if (s == null || s.length() == 0) {\n            return \"\";\n        }\n        \n        String longest = \"\";\n        for (int i = 0; i < s.length(); i++) {\n            // Odd length palindromes\n            String palindrome1 = expandAroundCenter(s, i, i);\n            // Even length palindromes\n            String palindrome2 = expandAroundCenter(s, i, i + 1);\n            \n            if (palindrome1.length() > longest.length()) {\n                longest = palindrome1;\n            }\n            if (palindrome2.length() > longest.length()) {\n                longest = palindrome2;\n            }\n        }\n        \n        return longest;\n    }\n    \n    private static String expandAroundCenter(String s, int left, int right) {\n        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {\n            left--;\n            right++;\n        }\n        return s.substring(left + 1, right);\n    }\n    \n    public static void main(String[] args) {\n        System.out.println(longestPalindrome(\"babad\"));\n        System.out.println(longestPalindrome(\"cbbd\"));\n        System.out.println(longestPalindrome(\"racecar\"));\n    }\n}",
  "language": "java",
  "versionIndex": "11"
}
```

### Submit Java Code
```http
POST /api/v1/code/submit
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "public class Solution {\n    public static String longestPalindrome(String s) {\n        if (s == null || s.length() == 0) {\n            return \"\";\n        }\n        \n        String longest = \"\";\n        for (int i = 0; i < s.length(); i++) {\n            String palindrome1 = expandAroundCenter(s, i, i);\n            String palindrome2 = expandAroundCenter(s, i, i + 1);\n            \n            if (palindrome1.length() > longest.length()) {\n                longest = palindrome1;\n            }\n            if (palindrome2.length() > longest.length()) {\n                longest = palindrome2;\n            }\n        }\n        \n        return longest;\n    }\n    \n    private static String expandAroundCenter(String s, int left, int right) {\n        while (left >= 0 && right < s.length() && s.charAt(left) == s.charAt(right)) {\n            left--;\n            right++;\n        }\n        return s.substring(left + 1, right);\n    }\n}",
  "language": "java",
  "versionIndex": "11",
  "question_id": 11,
  "assessment_id": 9
}
```

---

## 12. C++ Code Examples

### Run C++ Code - Binary Search
```http
POST /api/v1/code/run
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "#include <iostream>\n#include <vector>\nusing namespace std;\n\nint binarySearch(vector<int>& arr, int target) {\n    int left = 0;\n    int right = arr.size() - 1;\n    \n    while (left <= right) {\n        int mid = left + (right - left) / 2;\n        \n        if (arr[mid] == target) {\n            return mid;\n        }\n        else if (arr[mid] < target) {\n            left = mid + 1;\n        }\n        else {\n            right = mid - 1;\n        }\n    }\n    \n    return -1;\n}\n\nint main() {\n    vector<int> arr = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};\n    \n    cout << \"Search for 5: \" << binarySearch(arr, 5) << endl;\n    cout << \"Search for 8: \" << binarySearch(arr, 8) << endl;\n    cout << \"Search for 11: \" << binarySearch(arr, 11) << endl;\n    \n    return 0;\n}",
  "language": "cpp",
  "versionIndex": "17"
}
```

### Submit C++ Code
```http
POST /api/v1/code/submit
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "#include <vector>\nusing namespace std;\n\nint binarySearch(vector<int>& arr, int target) {\n    int left = 0;\n    int right = arr.size() - 1;\n    \n    while (left <= right) {\n        int mid = left + (right - left) / 2;\n        \n        if (arr[mid] == target) {\n            return mid;\n        }\n        else if (arr[mid] < target) {\n            left = mid + 1;\n        }\n        else {\n            right = mid - 1;\n        }\n    }\n    \n    return -1;\n}",
  "language": "cpp",
  "versionIndex": "17",
  "question_id": 12,
  "assessment_id": 10
}
```

---

## 13. Error Handling Examples

### Run Code with Syntax Error
```http
POST /api/v1/code/run
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "def reverse_string(s):\n    # Syntax error: missing colon\n    if not s\n        return \"\"\n    \n    result = \"\"\n    for i in range(len(s), 0, -1):\n        result += s[i]  # Index error\n    \n    return result\n\nprint(reverse_string(\"hello\"))",
  "language": "python",
  "versionIndex": "3.9"
}
```

### Run Code with Logic Error
```http
POST /api/v1/code/run
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "def fibonacci(n):\n    # Logic error: incorrect base case\n    if n <= 0:\n        return 1  # Should return 0 for n=0\n    if n == 1:\n        return 1\n    \n    return fibonacci(n-1) + fibonacci(n-2)\n\n# Test to see the error\nprint(\"Fibonacci(0):\", fibonacci(0))\nprint(\"Fibonacci(5):\", fibonacci(5))",
  "language": "python",
  "versionIndex": "3.9"
}
```

---

## 14. Performance Testing Examples

### Run Performance Test - Large Dataset
```http
POST /api/v1/code/run
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "import time\nimport random\n\ndef merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    \n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    \n    return merge(left, right)\n\ndef merge(left, right):\n    result = []\n    i = j = 0\n    \n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            result.append(left[i])\n            i += 1\n        else:\n            result.append(right[j])\n            j += 1\n    \n    result.extend(left[i:])\n    result.extend(right[j:])\n    return result\n\n# Performance test with large dataset\ntest_data = [random.randint(1, 10000) for _ in range(1000)]\n\nstart_time = time.time()\nsorted_data = merge_sort(test_data)\nend_time = time.time()\n\nprint(f\"Sorted {len(test_data)} elements in {end_time - start_time:.4f} seconds\")\nprint(f\"First 10 elements: {sorted_data[:10]}\")\nprint(f\"Last 10 elements: {sorted_data[-10:]}\")\nprint(f\"Is sorted: {sorted_data == sorted(test_data)}\")",
  "language": "python",
  "versionIndex": "3.9"
}
```

---

## 15. Multi-Language Support Examples

### Python with Libraries
```http
POST /api/v1/code/run
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "script": "import numpy as np\nimport json\n\ndef matrix_multiplication(a, b):\n    \"\"\"Efficient matrix multiplication using NumPy\"\"\"\n    return np.dot(a, b)\n\n# Test with sample matrices\nmatrix_a = np.array([[1, 2], [3, 4]])\nmatrix_b = np.array([[5, 6], [7, 8]])\n\nresult = matrix_multiplication(matrix_a, matrix_b)\nprint(\"Matrix A:\")\nprint(matrix_a)\nprint(\"Matrix B:\")\nprint(matrix_b)\nprint(\"Result:\")\nprint(result)\n\n# Convert to JSON for API response\nresult_json = {\n    \"matrix_a\": matrix_a.tolist(),\n    \"matrix_b\": matrix_b.tolist(),\n    \"result\": result.tolist()\n}\n\nprint(\"\\nJSON Output:\")\nprint(json.dumps(result_json, indent=2))",
  "language": "python",
  "versionIndex": "3.9"
}
```

---

## API Response Examples

### Successful Code Execution Response
```json
{
  "status": "success",
  "execution_time": 0.245,
  "memory_usage": 12.5,
  "output": "bab\nbb\nracecar\n",
  "error": null,
  "test_cases_passed": 3,
  "total_test_cases": 6
}
```

### Code Execution with Error Response
```json
{
  "status": "error",
  "execution_time": 0.012,
  "memory_usage": 2.1,
  "output": "",
  "error": {
    "type": "SyntaxError",
    "message": "invalid syntax",
    "line": 3,
    "column": 12
  },
  "test_cases_passed": 0,
  "total_test_cases": 6
}
```

### Code Submission Response
```json
{
  "status": "success",
  "submission_id": "sub_12345",
  "question_id": 1,
  "assessment_id": 1,
  "marks_obtained": 48,
  "total_marks": 50,
  "test_cases_passed": 9,
  "total_test_cases": 10,
  "execution_time": 0.156,
  "memory_usage": 8.3,
  "feedback": "Excellent solution! Minor optimization possible for edge cases."
}
```

---

## Important Notes

### Key Difference Between Run and Submit

#### Code Run Endpoint (`/api/v1/code/run`)
- **Purpose**: Test your code with custom inputs and see output
- **Input Handling**: You can include test inputs directly in your script with `print()` statements
- **Usage**: For debugging and testing your logic

#### Code Submit Endpoint (`/api/v1/code/submit`)
- **Purpose**: Submit final solution for evaluation against test cases
- **Input Handling**: Must read input using `input()` and print output using `print()`
- **Test Case Flow**: 
  1. System passes test case input via `stdin`
  2. Your code reads it using `input()`
  3. Your code processes and prints result
  4. System compares your output with expected output

#### Critical Submit Code Requirements
1. **Must read input**: Use `input()` to read test data
2. **Must produce output**: Use `print()` to output result
3. **Exact output match**: Output must exactly match expected result (including format)
4. **No extra output**: Don't print debug information or extra text

#### Example: Correct Submit Format
```python
def solve_problem(input_data):
    # Your solution logic here
    return result

# Read input from test case
input_data = input().strip()
result = solve_problem(input_data)
print(result)  # This output will be compared with expected
```

#### Example: Incorrect Submit Format (Won't Work)
```python
def solve_problem(input_data):
    # Your solution logic here
    return result

# This won't work - no input reading or output printing
```

### Required Fields for Code Execution
1. **script**: The complete source code to execute
2. **language**: Programming language (python, javascript, java, cpp, etc.)
3. **versionIndex**: Language version (3.9 for Python, 18.x for Node.js, etc.)

### Required Fields for Code Submission
1. **script**: The source code solution
2. **language**: Programming language
3. **versionIndex**: Language version
4. **question_id**: ID of the question being answered
5. **assessment_id**: ID of the assessment

### Supported Languages and Versions
- **Python**: 3.8, 3.9, 3.10, 3.11
- **JavaScript**: 16.x, 18.x, 20.x
- **Java**: 8, 11, 17, 21
- **C++**: 14, 17, 20
- **C**: 99, 11, 17
- **Go**: 1.19, 1.20, 1.21
- **Rust**: 1.70, 1.71, 1.72

### Performance Guidelines
- **Execution Time Limit**: 30 seconds for most problems
- **Memory Limit**: 512MB for standard problems, 1GB for complex algorithms
- **Output Limit**: 64KB maximum output size
- **Test Case Timeout**: 5 seconds per test case

### Best Practices
1. **Code Quality**: Write clean, well-commented code
2. **Error Handling**: Include proper error handling for edge cases
3. **Performance**: Optimize for both time and space complexity
4. **Testing**: Test with various input sizes and edge cases
5. **Documentation**: Include docstrings and comments for complex logic

### Security Considerations
- **Input Validation**: All code is executed in sandboxed environments
- **Resource Limits**: Strict limits on CPU, memory, and execution time
- **File Access**: Limited file system access for security
- **Network Access**: No external network access during code execution
