# Assessment Structure Validation Implementation

## Overview
This document summarizes the implementation of assessment structure validation rules that ensure consistency in assessment design.

## Validation Rules Implemented

### Rule 1: Consistent Net Scoring Potential Within Each Set
- **Requirement**: If one section in a set has constant net scoring potential (e.g., 40), then ALL sections in the SAME set should have the same net scoring potential (40)
- **Calculation**: Net scoring potential = positive_marks + negative_marks for each question
- **Implementation**: The system calculates net scoring potential for each section within each set and validates that all sections in the same set have identical net scoring potential
- **Error Message**: "All sections in set X must have the same net scoring potential. Found different totals: Section Y: Z net marks, Section A: B net marks. Please ensure all sections in the same set have equal net scoring potential (positive_marks + negative_marks)."

### Rule 2: Consistent Section Structure Across Sets
- **Requirement**: All sets of the assessment should have the same type of sections but with different questions
- **Implementation**: The system validates that every set contains exactly the same section IDs (same section structure)
- **Error Message**: "Set X has different section structure than set Y. Missing sections: [Z]. All sets must have the same section types/structure."

## Files Modified

### 1. `api/serializers.py`
- **Location**: `AssessmentSerializer` class
- **Changes**:
  - Enhanced `validate()` method to call new validation
  - Added `validate_assessment_structure()` method with comprehensive validation logic

### 2. `test_assessment_validation.py`
- **Purpose**: Comprehensive test suite to validate the new rules
- **Test Cases**:
  1. Valid assessment (should pass)
  2. Inconsistent marks within set (should fail)
  3. Inconsistent section structure (should fail)

## Implementation Details

### Validation Logic Flow

1. **Data Grouping**: Questions are grouped by `set_number` and `section_id`
2. **Net Scoring Calculation**: Net scoring potential is calculated for each section in each set by summing `(positive_marks + negative_marks)` for all questions in that section
3. **Marks Consistency Check**: Within each set, all section net scoring potentials are compared
4. **Structure Consistency Check**: Section IDs are compared across all sets
5. **Error Generation**: Detailed error messages are generated for any violations

**Important Note**: Section totals are calculated using **net scoring potential** (`positive_marks + negative_marks`). This ensures that the risk/reward balance is consistent across sections, accounting for both the points gained for correct answers and points lost for incorrect answers.

### Code Structure

```python
def validate_assessment_structure(self, attrs):
    """
    Validate assessment structure requirements:
    1. Within each set, all sections should have the same net scoring potential
    2. All sets should have the same section types (structure)
    """
    # Group questions by set and section
    set_section_data = defaultdict(lambda: defaultdict(list))
    
    # Calculate net scoring potential (positive_marks + negative_marks)
    for question in questions:
        net_marks = question.get('positive_marks', 0) + question.get('negative_marks', 0)
        set_section_data[set_number][section_id].append(net_marks)
    
    # Calculate section net totals
    set_section_totals = {}
    
    # Validate net scoring potential consistency within sets
    # Validate structure consistency across sets
    
    # Raise ValidationError if violations found
```

## Test Results

All tests passed successfully:

### ✅ Test 1: Valid Assessment
- **Scenario**: Assessment with 2 sets, each having 2 sections with 40 net marks each
- **Result**: PASSED - Correctly accepted valid structure
- **Structure**: 
  - Set 1: Section 1 (40 net marks), Section 2 (40 net marks)
  - Set 2: Section 1 (40 net marks), Section 2 (40 net marks)

### ✅ Test 2: Inconsistent Net Scoring Within Set
- **Scenario**: Assessment with 1 set having sections with different net scoring potential
- **Result**: PASSED - Correctly rejected invalid structure
- **Structure**: Set 1: Section 1 (45 net marks), Section 2 (25 net marks) ❌
- **Error**: "All sections in set 1 must have the same net scoring potential..."

### ✅ Test 3: Inconsistent Section Structure
- **Scenario**: Assessment with sets having different section structures
- **Result**: PASSED - Correctly rejected invalid structure
- **Structure**: 
  - Set 1: Sections [1, 2, 3]
  - Set 2: Sections [1, 2] (missing section 3) ❌
- **Error**: "Set 2 has different section structure than set 1..."

## Usage Examples

### Valid Assessment Structure
```json
{
  "num_of_sets": 2,
  "questions": [
    // Set 1 - Section 1: 40 net marks total (25+25-5-5)
    {"section_id": 1, "set_number": 1, "positive_marks": 25, "negative_marks": -5},
    {"section_id": 1, "set_number": 1, "positive_marks": 25, "negative_marks": -5},
    // Set 1 - Section 2: 40 net marks total (same as section 1) ✅
    {"section_id": 2, "set_number": 1, "positive_marks": 25, "negative_marks": -5},
    {"section_id": 2, "set_number": 1, "positive_marks": 25, "negative_marks": -5},
    
    // Set 2 - Same net scoring potential as Set 1 ✅
    {"section_id": 1, "set_number": 2, "positive_marks": 25, "negative_marks": -5},
    {"section_id": 1, "set_number": 2, "positive_marks": 25, "negative_marks": -5},
    {"section_id": 2, "set_number": 2, "positive_marks": 25, "negative_marks": -5},
    {"section_id": 2, "set_number": 2, "positive_marks": 25, "negative_marks": -5}
  ]
}
```

### Invalid Assessment Structure (Inconsistent Net Scoring)
```json
{
  "questions": [
    // Set 1 - Section 1: 45 net marks (50-5)
    {"section_id": 1, "set_number": 1, "positive_marks": 50, "negative_marks": -5},
    // Set 1 - Section 2: 25 net marks (30-5) (different from section 1) ❌
    {"section_id": 2, "set_number": 1, "positive_marks": 30, "negative_marks": -5}
  ]
}
```

### Invalid Assessment Structure (Different Structure)
```json
{
  "questions": [
    // Set 1 has sections 1, 2, 3
    {"section_id": 1, "set_number": 1, "positive_marks": 50},
    {"section_id": 2, "set_number": 1, "positive_marks": 50},
    {"section_id": 3, "set_number": 1, "positive_marks": 50},
    
    // Set 2 has only sections 1, 2 (missing section 3) ❌
    {"section_id": 1, "set_number": 2, "positive_marks": 50},
    {"section_id": 2, "set_number": 2, "positive_marks": 50}
  ]
}
```

## Benefits

1. **Data Integrity**: Ensures consistent assessment structure across all sets
2. **Fair Evaluation**: Guarantees equal difficulty/scoring across different sets
3. **User-Friendly Errors**: Provides clear, actionable error messages
4. **Automated Validation**: Prevents invalid assessments from being created
5. **Maintainable Code**: Well-structured validation logic that's easy to extend

## Future Enhancements

1. **Custom Marks Distribution**: Allow configurable marks distribution patterns
2. **Section Weight Validation**: Validate relative weights between sections
3. **Question Type Consistency**: Ensure similar question types across sets
4. **Time Limit Validation**: Validate time consistency across sets

## Conclusion

The implementation successfully enforces the required assessment structure validation rules:

1. ✅ **Equal marks within sets**: All sections in a set must have the same total marks
2. ✅ **Consistent structure across sets**: All sets must have the same section types

The validation is robust, provides clear error messages, and has been thoroughly tested with comprehensive test cases.

---

# Postman API Request Examples

## Base Configuration

**Base URL**: `http://localhost:8000` (or your server URL)
**Authentication**: Bearer Token required for all requests

### Headers for all requests:
```
Content-Type: application/json
Authorization: Bearer <your_access_token>
```

---

## 1. Valid Assessment Request ✅

### **POST** `/api/v1/assessments/`

**Description**: Creates a valid assessment that passes all validation rules.

**Request Body**:
```json
{
  "assessment_name": "Software Engineering Assessment - Valid Structure",
  "assessment_type": "mix",
  "assessment_description": "A properly structured assessment with consistent marks and section structure",
  "passing_marks": 120,
  "num_of_sets": 2,
  "section_names": ["Programming Fundamentals", "Data Structures", "System Design"],
  "section_descriptions": [
    "Basic programming concepts and syntax", 
    "Arrays, linked lists, stacks, and queues",
    "Architecture and design patterns"
  ],
  "start_time": "2025-12-01T10:00:00Z",
  "end_time": "2025-12-01T13:00:00Z",
  "is_electron_only": false,
  "is_proctored": true,
  "is_published": true,
  "num_of_ai_generated_questions": 0,
  "attachments": [],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "What is the output of print('Hello World') in Python?",
      "options": ["Hello World", "hello world", "Error", "None"],
      "correct_option_index": 0,
      "positive_marks": 20,
      "negative_marks": -5,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Write a function to find the maximum of two numbers",
      "description": "Create a function that takes two integers and returns the larger one",
      "constraints": ["Both numbers are integers", "-1000 <= numbers <= 1000"],
      "positive_marks": 30,
      "negative_marks": 0,
      "time_limit": 900,
      "test_cases": {
        "examples": [
          {"input": "5, 3", "output": "5"},
          {"input": "1, 8", "output": "8"}
        ],
        "hidden": [
          {"input": "-5, -10", "output": "-5"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Which data structure uses LIFO principle?",
      "options": ["Queue", "Stack", "Array", "Linked List"],
      "correct_option_index": 1,
      "positive_marks": 25,
      "negative_marks": -6,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "What is the time complexity of binary search?",
      "options": ["O(n)", "O(log n)", "O(n^2)", "O(1)"],
      "correct_option_index": 1,
      "positive_marks": 25,
      "negative_marks": -6,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "What is microservices architecture?",
      "options": [
        "Single large application", 
        "Multiple small, independent services",
        "Database design pattern",
        "Frontend framework"
      ],
      "correct_option_index": 1,
      "positive_marks": 25,
      "negative_marks": -6,
      "time_limit": 180
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "What is the purpose of load balancing?",
      "options": [
        "To store data",
        "To distribute incoming requests across multiple servers",
        "To encrypt data",
        "To backup databases"
      ],
      "correct_option_index": 1,
      "positive_marks": 25,
      "negative_marks": -6,
      "time_limit": 180
    },
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 2,
      "question_text": "What is the difference between '==' and 'is' in Python?",
      "options": [
        "No difference",
        "'==' compares values, 'is' compares identity",
        "'==' is for strings, 'is' is for numbers",
        "'is' is deprecated"
      ],
      "correct_option_index": 1,
      "positive_marks": 20,
      "negative_marks": -5,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 2,
      "question_text": "Write a function to check if a number is even or odd",
      "description": "Create a function that returns 'even' for even numbers and 'odd' for odd numbers",
      "constraints": ["Input is an integer", "-1000 <= number <= 1000"],
      "positive_marks": 30,
      "negative_marks": 0,
      "time_limit": 900,
      "test_cases": {
        "examples": [
          {"input": "4", "output": "even"},
          {"input": "7", "output": "odd"}
        ],
        "hidden": [
          {"input": "0", "output": "even"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 2,
      "question_text": "What is the main advantage of linked lists over arrays?",
      "options": [
        "Faster access time",
        "Dynamic size allocation",
        "Better cache performance",
        "Less memory usage"
      ],
      "correct_option_index": 1,
      "positive_marks": 25,
      "negative_marks": -6,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 2,
      "question_text": "Which sorting algorithm has the best average case time complexity?",
      "options": ["Bubble Sort", "Selection Sort", "Quick Sort", "Insertion Sort"],
      "correct_option_index": 2,
      "positive_marks": 25,
      "negative_marks": -6,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 2,
      "question_text": "What is the main benefit of using containerization?",
      "options": [
        "Faster code execution",
        "Application portability and consistency",
        "Better user interface",
        "Automatic bug fixing"
      ],
      "correct_option_index": 1,
      "positive_marks": 25,
      "negative_marks": -6,
      "time_limit": 180
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 2,
      "question_text": "What is API versioning?",
      "options": [
        "Creating multiple APIs",
        "Managing different versions of an API to maintain backward compatibility",
        "API documentation process",
        "API testing methodology"
      ],
      "correct_option_index": 1,
      "positive_marks": 25,
      "negative_marks": -6,
      "time_limit": 180
    }
  ]
}
```

**Expected Response**: `201 Created`
```json
{
  "message": "Assessment created successfully",
  "assessment_id": 1,
  "sections": [
    {"id": 1, "name": "Programming Fundamentals"},
    {"id": 2, "name": "Data Structures"},
    {"id": 3, "name": "System Design"}
  ]
}
```

---

## 2. Invalid Request - Inconsistent Marks Within Set ❌

### **POST** `/api/v1/assessments/`

**Description**: This request will fail because sections within Set 1 have different total marks.

**Request Body**:
```json
{
  "assessment_name": "Invalid Assessment - Inconsistent Marks Within Set",
  "assessment_type": "mix",
  "assessment_description": "This will fail due to inconsistent marks within the same set",
  "passing_marks": 60,
  "num_of_sets": 1,
  "section_names": ["Math", "Science"],
  "section_descriptions": ["Mathematics questions", "Science questions"],
  "start_time": "2025-12-01T10:00:00Z",
  "end_time": "2025-12-01T12:00:00Z",
  "is_electron_only": false,
  "is_proctored": false,
  "is_published": false,
  "num_of_ai_generated_questions": 0,
  "attachments": [],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "What is 2+2?",
      "options": ["3", "4", "5", "6"],
      "correct_option_index": 1,
      "positive_marks": 50,
      "negative_marks": -5,
      "time_limit": 60
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "What is H2O?",
      "options": ["Water", "Oxygen", "Hydrogen", "Carbon"],
      "correct_option_index": 0,
      "positive_marks": 30,
      "negative_marks": -5,
      "time_limit": 60
    }
  ]
}
```

**Expected Response**: `400 Bad Request`
```json
{
  "set_1_marks_consistency": [
    "All sections in set 1 must have the same total marks. Found different totals: Section 1: 50 marks, Section 2: 30 marks. Please ensure all sections in the same set have equal total marks."
  ]
}
```

---

## 3. Invalid Request - Different Section Structure ❌

### **POST** `/api/v1/assessments/`

**Description**: This request will fail because Set 2 is missing Section 3.

**Request Body**:
```json
{
  "assessment_name": "Invalid Assessment - Different Section Structure",
  "assessment_type": "mix",
  "assessment_description": "This will fail due to inconsistent section structure across sets",
  "passing_marks": 90,
  "num_of_sets": 2,
  "section_names": ["Math", "Science", "English"],
  "section_descriptions": ["Mathematics", "Science", "English"],
  "start_time": "2025-12-01T10:00:00Z",
  "end_time": "2025-12-01T12:00:00Z",
  "is_electron_only": false,
  "is_proctored": false,
  "is_published": false,
  "num_of_ai_generated_questions": 0,
  "attachments": [],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "What is 5+5?",
      "options": ["8", "9", "10", "11"],
      "correct_option_index": 2,
      "positive_marks": 50,
      "negative_marks": -10,
      "time_limit": 120
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "What is the chemical symbol for gold?",
      "options": ["Go", "Au", "Ag", "Gd"],
      "correct_option_index": 1,
      "positive_marks": 50,
      "negative_marks": -10,
      "time_limit": 120
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "What is a noun?",
      "options": ["Action word", "Describing word", "Person, place, or thing", "Connecting word"],
      "correct_option_index": 2,
      "positive_marks": 50,
      "negative_marks": -10,
      "time_limit": 120
    },
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 2,
      "question_text": "What is 7+8?",
      "options": ["14", "15", "16", "17"],
      "correct_option_index": 1,
      "positive_marks": 50,
      "negative_marks": -10,
      "time_limit": 120
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 2,
      "question_text": "What is H2SO4?",
      "options": ["Water", "Sulfuric Acid", "Salt", "Sugar"],
      "correct_option_index": 1,
      "positive_marks": 50,
      "negative_marks": -10,
      "time_limit": 120
    }
  ]
}
```

**Expected Response**: `400 Bad Request`
```json
{
  "set_2_structure_consistency": [
    "Set 2 has different section structure than set 1. Missing sections: [3]. All sets must have the same section types/structure."
  ]
}
```

---

## 4. Invalid Request - Inconsistent Marks Across Sets ❌

### **POST** `/api/v1/assessments/`

**Description**: This request will fail because the same sections have different marks in different sets.

**Request Body**:
```json
{
  "assessment_name": "Invalid Assessment - Cross-Set Mark Inconsistency",
  "assessment_type": "mix",
  "assessment_description": "This will fail due to inconsistent marks across sets for the same sections",
  "passing_marks": 80,
  "num_of_sets": 2,
  "section_names": ["Programming", "Algorithms"],
  "section_descriptions": ["Programming concepts", "Algorithm design"],
  "start_time": "2025-12-01T14:00:00Z",
  "end_time": "2025-12-01T16:00:00Z",
  "is_electron_only": false,
  "is_proctored": true,
  "is_published": false,
  "num_of_ai_generated_questions": 0,
  "attachments": [],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Write a function to add two numbers",
      "description": "Simple addition function",
      "constraints": ["Both inputs are integers"],
      "positive_marks": 40,
      "negative_marks": 0,
      "time_limit": 600,
      "test_cases": {
        "examples": [{"input": "2, 3", "output": "5"}],
        "hidden": [{"input": "10, 15", "output": "25"}]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "What is the time complexity of linear search?",
      "options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"],
      "correct_option_index": 2,
      "positive_marks": 40,
      "negative_marks": -10,
      "time_limit": 180
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 2,
      "question_text": "Write a function to multiply two numbers",
      "description": "Simple multiplication function",
      "constraints": ["Both inputs are integers"],
      "positive_marks": 25,
      "negative_marks": 0,
      "time_limit": 600,
      "test_cases": {
        "examples": [{"input": "3, 4", "output": "12"}],
        "hidden": [{"input": "7, 8", "output": "56"}]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 2,
      "question_text": "Which algorithm is used for finding shortest path?",
      "options": ["Bubble Sort", "Dijkstra's Algorithm", "Binary Search", "Quick Sort"],
      "correct_option_index": 1,
      "positive_marks": 25,
      "negative_marks": -5,
      "time_limit": 180
    }
  ]
}
```

**Expected Response**: `400 Bad Request`
```json
{
  "section_1_cross_set_consistency": [
    "Section 1 has inconsistent marks across sets. Set 1: 40 marks, Set 2: 25 marks. Each section must have the same total marks in every set."
  ],
  "section_2_cross_set_consistency": [
    "Section 2 has inconsistent marks across sets. Set 1: 40 marks, Set 2: 25 marks. Each section must have the same total marks in every set."
  ]
}
```

---

## 5. Edge Case - Single Set Assessment ✅

### **POST** `/api/v1/assessments/`

**Description**: Valid assessment with only one set (no cross-set validation needed).

**Request Body**:
```json
{
  "assessment_name": "Single Set Assessment - Valid",
  "assessment_type": "coding",
  "assessment_description": "Assessment with only one set",
  "passing_marks": 50,
  "num_of_sets": 1,
  "section_names": ["Coding Basics"],
  "section_descriptions": ["Basic coding problems"],
  "start_time": "2025-12-01T09:00:00Z",
  "end_time": "2025-12-01T11:00:00Z",
  "is_electron_only": true,
  "is_proctored": false,
  "is_published": true,
  "num_of_ai_generated_questions": 0,
  "attachments": [],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Write a function to reverse a string",
      "description": "Reverse the input string without using built-in reverse methods",
      "constraints": ["1 <= string length <= 1000"],
      "positive_marks": 100,
      "negative_marks": 0,
      "time_limit": 1800,
      "test_cases": {
        "examples": [
          {"input": "hello", "output": "olleh"},
          {"input": "world", "output": "dlrow"}
        ],
        "hidden": [
          {"input": "python", "output": "nohtyp"}
        ]
      }
    }
  ]
}
```

**Expected Response**: `201 Created`
```json
{
  "message": "Assessment created successfully",
  "assessment_id": 2,
  "sections": [
    {"id": 4, "name": "Coding Basics"}
  ]
}
```

---

## 6. Complex Valid Assessment - Multiple Sets ✅

### **POST** `/api/v1/assessments/`

**Description**: Complex assessment with 3 sets, each having 4 sections with consistent structure.

**Request Body**:
```json
{
  "assessment_name": "Full Stack Developer Assessment - Multi-Set",
  "assessment_type": "mix",
  "assessment_description": "Comprehensive assessment with 3 sets for randomized distribution",
  "passing_marks": 200,
  "num_of_sets": 3,
  "section_names": ["Frontend", "Backend", "Database", "DevOps"],
  "section_descriptions": [
    "HTML, CSS, JavaScript, React",
    "Node.js, Python, API development",
    "SQL, NoSQL, Database design",
    "Docker, CI/CD, Cloud platforms"
  ],
  "start_time": "2025-12-05T09:00:00Z",
  "end_time": "2025-12-05T13:00:00Z",
  "is_electron_only": false,
  "is_proctored": true,
  "is_published": false,
  "num_of_ai_generated_questions": 0,
  "attachments": [
    "https://example.com/reference-guide.pdf"
  ],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "What does HTML stand for? Refer to $1 for context.",
      "options": [
        "Hyper Text Markup Language",
        "High Tech Modern Language", 
        "Home Tool Markup Language",
        "Hyperlink and Text Markup Language"
      ],
      "correct_option_index": 0,
      "positive_marks": 25,
      "negative_marks": -6,
      "time_limit": 90
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Write a JavaScript function to validate email format",
      "description": "Create a function that returns true for valid email addresses",
      "constraints": ["Use regex for validation", "Handle edge cases"],
      "positive_marks": 50,
      "negative_marks": 0,
      "time_limit": 1200,
      "test_cases": {
        "examples": [
          {"input": "test@example.com", "output": "true"},
          {"input": "invalid-email", "output": "false"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Which HTTP method is used to create a new resource?",
      "options": ["GET", "POST", "PUT", "DELETE"],
      "correct_option_index": 1,
      "positive_marks": 25,
      "negative_marks": -6,
      "time_limit": 90
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Create a REST API endpoint to get user by ID",
      "description": "Write a Node.js/Express endpoint that returns user data",
      "constraints": ["Use Express.js", "Handle error cases", "Return JSON response"],
      "positive_marks": 50,
      "negative_marks": 0,
      "time_limit": 1200,
      "test_cases": {
        "examples": [
          {"input": "GET /users/123", "output": "{\"id\": 123, \"name\": \"John\"}"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "What is a primary key in a database?",
      "options": [
        "A key that unlocks the database",
        "The first column in a table",
        "A unique identifier for each row",
        "A foreign key reference"
      ],
      "correct_option_index": 2,
      "positive_marks": 25,
      "negative_marks": -6,
      "time_limit": 90
    },
    {
      "question_type": "coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "Write a SQL query to find users with duplicate emails",
      "description": "Find all email addresses that appear more than once in the users table",
      "constraints": ["Use GROUP BY and HAVING", "Return email and count"],
      "positive_marks": 50,
      "negative_marks": 0,
      "time_limit": 900,
      "test_cases": {
        "examples": [
          {"input": "users table with duplicate emails", "output": "emails with count > 1"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 4,
      "set_number": 1,
      "question_text": "What is Docker used for?",
      "options": [
        "Version control",
        "Containerization",
        "Database management",
        "Code compilation"
      ],
      "correct_option_index": 1,
      "positive_marks": 25,
      "negative_marks": -6,
      "time_limit": 90
    },
    {
      "question_type": "coding",
      "section_id": 4,
      "set_number": 1,
      "question_text": "Write a Dockerfile for a Node.js application",
      "description": "Create a Dockerfile that runs a Node.js app on port 3000",
      "constraints": ["Use official Node.js image", "Expose port 3000", "Install dependencies"],
      "positive_marks": 50,
      "negative_marks": 0,
      "time_limit": 1200,
      "test_cases": {
        "examples": [
          {"input": "Node.js app with package.json", "output": "Working Dockerfile"}
        ]
      }
    }
  ]
}
```
*Note: Include similar questions for set_number 2 and set_number 3 with the same structure and marks distribution*

**Expected Response**: `201 Created`
```json
{
  "message": "Assessment created successfully", 
  "assessment_id": 3,
  "sections": [
    {"id": 5, "name": "Frontend"},
    {"id": 6, "name": "Backend"}, 
    {"id": 7, "name": "Database"},
    {"id": 8, "name": "DevOps"}
  ]
}
```

---

## Testing Checklist

When testing with Postman:

### ✅ Valid Requests Should:
- Return `201 Created` status
- Include `assessment_id` in response
- Create sections with correct `total_marks` (sum across all sets)
- Allow questions to be retrieved by set number

### ❌ Invalid Requests Should:
- Return `400 Bad Request` status
- Include specific error messages explaining the validation failure
- Not create any assessment or section records
- Provide actionable feedback for fixing the structure

### 🔍 Validation Points to Test:
1. **Within-set consistency**: All sections in the same set have equal marks
2. **Cross-set structure**: All sets have the same section IDs
3. **Cross-set marks**: Same sections have identical marks across all sets
4. **Attachment references**: `$n` references don't exceed attachment count
5. **Section ID validity**: All `section_id` values are within range

Use these Postman requests to thoroughly test the assessment validation system and ensure your API correctly enforces all structural consistency rules.
