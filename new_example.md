
# PN Academy API Postman Requests

**Base URL**: `http://localhost:8000/api/v1/`  
**Headers for authenticated requests:**
```
Content-Type: application/json
Authorization: Bearer <your_access_token>
```

---

## 1. Authentication

### User Registration
```http
POST /api/v1/register/
Content-Type: application/json
```

```json
{
  "email": "admin@pnacademy.com",
  "password": "securepassword123"
}
```

### User Login
```http
POST /api/v1/login/
Content-Type: application/json
```

```json
{
  "email": "admin@pnacademy.com",
  "password": "securepassword123"
}
```

### Reset Password
```http
POST /api/v1/reset-password/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "new_password": "newsecurepassword456"
}
```

---

## 2. User Management

### Create User (Admin Only)
```http
POST /api/v1/users/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "email": "manager@pnacademy.com",
  "password": "managerpass123",
  "role": "assessment_manager"
}
```

### Get All Users
```http
GET /api/v1/users/
Authorization: Bearer <token>
```

### Get User by ID
```http
GET /api/v1/users/{id}/
Authorization: Bearer <token>
```

### Update User
```http
PUT /api/v1/users/{id}/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "email": "updated@pnacademy.com",
  "role": "proctor"
}
```

### Partial Update User
```http
PATCH /api/v1/users/{id}/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "role": "admin"
}
```

### Delete User
```http
DELETE /api/v1/users/{id}/
Authorization: Bearer <token>
```

---

## 3. Assessment Management

### Create Assessment
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Full Stack Developer Assessment",
  "assessment_type": "mix",
  "assessment_description": "Comprehensive assessment covering frontend, backend, and system design with consistent scoring across all sets. Refer to technical specifications in $1 and coding standards in $2.",
  "passing_marks": 120,
  "num_of_sets": 2,
  "section_names": ["Frontend Development", "Backend Development", "System Design"],
  "section_descriptions": [
    "HTML, CSS, JavaScript, React.js, and modern frontend frameworks",
    "Node.js, Python, API development, and server-side technologies", 
    "Architecture patterns, scalability, and distributed systems"
  ],
  "start_time": "2025-12-01T09:00:00Z",
  "end_time": "2025-12-01T13:00:00Z",
  "is_electron_only": false,
  "is_proctored": true,
  "is_published": false,
  "num_of_ai_generated_questions": 5,
  "attachments": [
    "https://s3.amazonaws.com/assessments/technical-specifications.pdf",
    "https://s3.amazonaws.com/assessments/coding-standards.pdf"
  ],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "According to the technical specifications in $1, which CSS framework is recommended for responsive design?",
      "options": ["Bootstrap", "Tailwind CSS", "Bulma", "Foundation"],
      "correct_option_index": 1,
      "positive_marks": 20,
      "negative_marks": -5,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Create a React component that implements the form validation patterns described in $1. Follow the coding standards from $2.",
      "description": "Build a reusable form component with validation, error handling, and accessibility features",
      "constraints": ["Use React hooks", "Implement proper error handling", "Follow WCAG guidelines"],
      "positive_marks": 35,
      "negative_marks": 0,
      "time_limit": 1800,
      "test_cases": {
        "examples": [
          {"input": "Valid form data", "output": "Form submits successfully"},
          {"input": "Invalid email", "output": "Validation error displayed"}
        ],
        "hidden": [
          {"input": "Edge case inputs", "output": "Proper error handling"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Based on the backend architecture guidelines in $1, what is the recommended approach for handling authentication?",
      "options": ["Session-based auth", "JWT tokens", "OAuth 2.0", "API keys"],
      "correct_option_index": 1,
      "positive_marks": 20,
      "negative_marks": -5,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Implement a REST API endpoint following the standards outlined in $2 and architecture patterns from $1.",
      "description": "Create a secure API endpoint with proper validation, error handling, and documentation",
      "constraints": ["Use Express.js or Django", "Implement JWT authentication", "Add proper validation"],
      "positive_marks": 35,
      "negative_marks": 0,
      "time_limit": 1800,
      "test_cases": {
        "examples": [
          {"input": "GET /api/users", "output": "Returns paginated user list"},
          {"input": "POST /api/users with invalid data", "output": "Returns 400 with validation errors"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "According to the system design principles in $1, which pattern is best for handling high-traffic scenarios?",
      "options": ["Monolithic architecture", "Microservices", "Serverless", "Event-driven architecture"],
      "correct_option_index": 3,
      "positive_marks": 20,
      "negative_marks": -5,
      "time_limit": 180
    },
    {
      "question_type": "coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "Design a caching strategy implementation based on the guidelines in $1 and performance requirements in $2.",
      "description": "Implement a multi-tier caching solution with TTL and invalidation strategies",
      "constraints": ["Support Redis and in-memory caching", "Handle cache misses gracefully", "Implement cache warming"],
      "positive_marks": 35,
      "negative_marks": 0,
      "time_limit": 2400,
      "test_cases": {
        "examples": [
          {"input": "Cache miss scenario", "output": "Fetches from database and caches result"},
          {"input": "Cache hit scenario", "output": "Returns cached data quickly"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 2,
      "question_text": "Following the frontend best practices in $1, which state management solution is recommended for complex applications?",
      "options": ["useState only", "Redux Toolkit", "Zustand", "Context API"],
      "correct_option_index": 1,
      "positive_marks": 20,
      "negative_marks": -5,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 2,
      "question_text": "Build a performance-optimized React application following the optimization techniques described in $1 and coding standards in $2.",
      "description": "Create a React app with lazy loading, memoization, and bundle optimization",
      "constraints": ["Use React.memo and useMemo", "Implement code splitting", "Optimize bundle size"],
      "positive_marks": 35,
      "negative_marks": 0,
      "time_limit": 1800,
      "test_cases": {
        "examples": [
          {"input": "Large component tree", "output": "Renders efficiently without unnecessary re-renders"},
          {"input": "Route navigation", "output": "Lazy loads components on demand"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 2,
      "question_text": "According to the API design patterns in $1, what is the recommended approach for handling pagination?",
      "options": ["Offset-based", "Cursor-based", "Page-based", "Time-based"],
      "correct_option_index": 1,
      "positive_marks": 20,
      "negative_marks": -5,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 2,
      "question_text": "Implement a database optimization solution following the performance guidelines in $1 and coding standards from $2.",
      "description": "Create optimized database queries with proper indexing and caching",
      "constraints": ["Use proper indexing strategies", "Implement query optimization", "Add connection pooling"],
      "positive_marks": 35,
      "negative_marks": 0,
      "time_limit": 1800,
      "test_cases": {
        "examples": [
          {"input": "Complex join query", "output": "Executes efficiently with proper indexes"},
          {"input": "Large dataset query", "output": "Returns results within acceptable time limits"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 2,
      "question_text": "Based on the scalability patterns in $1, which approach is best for handling distributed transactions?",
      "options": ["Two-phase commit", "Saga pattern", "Event sourcing", "CQRS"],
      "correct_option_index": 1,
      "positive_marks": 20,
      "negative_marks": -5,
      "time_limit": 180
    },
    {
      "question_type": "coding",
      "section_id": 3,
      "set_number": 2,
      "question_text": "Design a distributed system architecture following the principles outlined in $1 and meeting the requirements in $2.",
      "description": "Create a fault-tolerant distributed system with proper service discovery and load balancing",
      "constraints": ["Handle service failures gracefully", "Implement circuit breakers", "Add health checks"],
      "positive_marks": 35,
      "negative_marks": 0,
      "time_limit": 2400,
      "test_cases": {
        "examples": [
          {"input": "Service failure scenario", "output": "System continues operating with degraded functionality"},
          {"input": "High load scenario", "output": "Load balancer distributes traffic effectively"}
        ]
      }
    }
  ]
}
```

### Create Assessment (Alternative)
```http
POST /api/v1/assessment
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Quick Programming Test",
  "assessment_type": "coding",
  "assessment_description": "Short coding assessment",
  "passing_marks": 40,
  "num_of_sets": 1,
  "section_names": ["Programming Basics"],
  "section_descriptions": ["Basic programming concepts"],
  "start_time": "2025-12-01T10:00:00Z",
  "end_time": "2025-12-01T11:00:00Z",
  "is_electron_only": true,
  "is_proctored": false,
  "is_published": false,
  "num_of_ai_generated_questions": 0,
  "attachments": [],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Write a function to reverse a string",
      "description": "Implement string reversal without using built-in methods",
      "constraints": ["No built-in reverse functions", "Handle empty strings"],
      "positive_marks": 50,
      "negative_marks": 0,
      "time_limit": 900,
      "test_cases": {
        "examples": [
          {"input": "hello", "output": "olleh"},
          {"input": "world", "output": "dlrow"}
        ],
        "hidden": [
          {"input": "", "output": ""},
          {"input": "a", "output": "a"}
        ]
      }
    }
  ]
}
```

### Get All Assessments
```http
GET /api/v1/assessments/
Authorization: Bearer <token>
```

### Get All Assessments (Alternative)
```http
GET /api/v1/assessment
Authorization: Bearer <token>
```

### Get Assessments with Filtering
```http
GET /api/v1/assessments/?assessment_type=mix&is_published=true&page=1&page_size=10
Authorization: Bearer <token>
```

### Get Assessment by ID
```http
GET /api/v1/assessments/{id}/
Authorization: Bearer <token>
```

### Get Assessment by ID (Alternative)
```http
GET /api/v1/assessment/{id}
Authorization: Bearer <token>
```

### Get Assessment with Specific Set
```http
GET /api/v1/assessments/{id}/?set_number=1
Authorization: Bearer <token>
```

### Update Assessment
```http
PUT /api/v1/assessments/{id}/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Updated Full Stack Assessment",
  "assessment_type": "mix",
  "assessment_description": "Updated comprehensive assessment with new features and improved validation",
  "passing_marks": 140,
  "num_of_sets": 3,
  "section_names": ["Frontend Development", "Backend Development", "System Design", "DevOps"],
  "section_descriptions": [
    "Modern frontend technologies and best practices",
    "Backend development and API design",
    "System architecture and scalability",
    "CI/CD, containerization, and deployment"
  ],
  "start_time": "2025-12-05T09:00:00Z",
  "end_time": "2025-12-05T14:00:00Z",
  "is_electron_only": true,
  "is_proctored": true,
  "is_published": false,
  "num_of_ai_generated_questions": 10,
  "attachments": [
    "https://s3.amazonaws.com/assessments/updated-technical-specs.pdf"
  ],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Implement a component based on the updated specifications in $1",
      "description": "Create a modern React component with TypeScript",
      "constraints": ["Use TypeScript", "Implement proper error boundaries"],
      "positive_marks": 40,
      "negative_marks": 0,
      "time_limit": 1200,
      "test_cases": {
        "examples": [
          {"input": "Component props", "output": "Rendered component"}
        ]
      }
    }
  ]
}
```

### Update Assessment (Alternative)
```http
PUT /api/v1/assessment/{id}
Authorization: Bearer <token>
Content-Type: application/json
```

### Partial Update Assessment
```http
PATCH /api/v1/assessments/{id}/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Updated Assessment Name",
  "passing_marks": 150,
  "is_published": true
}
```

### Partial Update Assessment (Alternative)
```http
PATCH /api/v1/assessment/{id}
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "is_proctored": true,
  "is_electron_only": true
}
```

### Delete Assessment
```http
DELETE /api/v1/assessments/{id}/
Authorization: Bearer <token>
```

### Delete Assessment (Alternative)
```http
DELETE /api/v1/assessment/{id}
Authorization: Bearer <token>
```

---

## 4. Question Search

### Get All Questions from Assessment
```http
GET /api/v1/assessments/{assessment_id}/
Authorization: Bearer <token>
```

**Response includes all questions nested within sections:**
```json
{
  "id": 1,
  "title": "Python Programming Assessment",
  "sections": [
    {
      "id": 1,
      "name": "Programming Fundamentals",
      "questions": [
        {
          "id": 1,
          "question_text": "What is Python?",
          "question_type": "non-coding",
          "section_id": 1,
          "set_number": 1,
          "marks": 2,
          "negative_marks": 0,
          "time_limit": 60,
          "options": ["A scripting language", "A programming language", "Both", "None"],
          "correct_answer": 2
        }
      ]
    }
  ]
}
```

### Filter Questions by Set Number
```http
GET /api/v1/assessments/{assessment_id}/?set_number={set_id}
Authorization: Bearer <token>
```

**Example:**
```http
GET /api/v1/assessments/1/?set_number=2
Authorization: Bearer <token>
```


### Search Assessments
```http
GET /api/v1/assessments/?search={keyword}
Authorization: Bearer <token>
```

**Example:**
```http
GET /api/v1/assessments/?search=Python
Authorization: Bearer <token>
```

### Filter Assessments by Type
```http
GET /api/v1/assessments/?type={assessment_type}
Authorization: Bearer <token>
```

**Example:**
```http
GET /api/v1/assessments/?type=technical
Authorization: Bearer <token>
```

### Get Published Assessments
```http
GET /api/v1/assessments/?is_published=true
Authorization: Bearer <token>
```

### Advanced Query Combinations
```http
GET /api/v1/assessments/?type=technical&is_published=true&set_number=1
Authorization: Bearer <token>
```

## 5. Student Management

### Upload Students CSV
```http
POST /api/v1/uploadStudents/
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Form Data:**
- `file`: (CSV file with headers: full_name, email, phone)

**Sample CSV:**
```csv
full_name,email,phone
John Doe,john.doe@example.com,+1234567890
Jane Smith,jane.smith@example.com,+1234567891
Alice Johnson,alice.johnson@example.com,+1234567892
```

### Get All Students
```http
GET /api/v1/students/
Authorization: Bearer <token>
```

### Get Student by ID
```http
GET /api/v1/students/{id}/
Authorization: Bearer <token>
```

### Update Student
```http
PUT /api/v1/students/{id}/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "full_name": "Updated John Doe",
  "email": "updated.john@example.com"
}
```

### Partial Update Student
```http
PATCH /api/v1/students/{id}/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "full_name": "John D. Smith"
}
```

### Delete Student
```http
DELETE /api/v1/students/{id}/
Authorization: Bearer <token>
```

### Get CSV Upload History
```http
GET /api/v1/students-list/
Authorization: Bearer <token>
```

### Get CSV Upload by ID
```http
GET /api/v1/students-list/{id}/
Authorization: Bearer <token>
```

---

## 6. Assessment Assignment

### Assign Assessment to CSV Upload
```http
POST /api/v1/assign-assessment/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 1,
  "csv_upload_id": 1
}
```

### Get Test Codes for Assessment
```http
GET /api/v1/assessments/{assessment_id}/test-codes/
Authorization: Bearer <token>
```

### Get Test Codes for Assessment with Filters
```http
GET /api/v1/assessments/{assessment_id}/test-codes/?csv_upload_id=1&is_used=false
Authorization: Bearer <token>
```

### Get Test Codes for CSV Upload
```http
GET /api/v1/csv-uploads/{csv_upload_id}/test-codes/
Authorization: Bearer <token>
```

### Get Test Codes for CSV Upload with Filters
```http
GET /api/v1/csv-uploads/{csv_upload_id}/test-codes/?assessment_id=1&is_used=true
Authorization: Bearer <token>
```

---

## 7. Communication

### Send Bulk Email
```http
POST /api/v1/sendEmail/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "csv_upload_id": 1,
  "subject": "Assessment Invitation - Full Stack Developer Test",
  "content": "Dear {{student_name}},\n\nYou have been invited to take the Full Stack Developer Assessment.\n\nYour unique test code: {{test_code}}\nAssessment link: {{assessment_link}}\n\nPlease complete the assessment before the deadline.\n\nBest regards,\nAssessment Team",
  "content_type": "text"
}
```

### Send HTML Email
```http
POST /api/v1/sendEmail/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "csv_upload_id": 1,
  "subject": "Assessment Invitation - HTML Format",
  "content": "<html><body><h2>Assessment Invitation</h2><p>Dear <strong>{{student_name}}</strong>,</p><p>You have been invited to take the assessment.</p><p><strong>Test Code:</strong> {{test_code}}</p><p><a href='{{assessment_link}}'>Start Assessment</a></p></body></html>",
  "content_type": "html"
}
```

---

## 8. File Management

### Generate Presigned URL for File Upload
```http
POST /api/v1/upload/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 1,
  "filename": "technical-specifications.pdf"
}
```

### Check File Upload Status
```http
POST /api/v1/fileStatus/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 1,
  "filename": "technical-specifications.pdf"
}
```

### List Assessment Files
```http
GET /api/v1/files/{assessment_id}
Authorization: Bearer <token>
```

---

## 9. Report Generation

### Generate Student Report
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 1,
  "student_email": "john.doe@example.com",
  "started_at": "2025-12-01T09:00:00Z",
  "ended_at": "2025-12-01T12:30:00Z",
  "submitted_at": "2025-12-01T12:25:00Z",
  "window_switch_count": 2,
  "is_cheating": false,
  "sections": [
    {
      "section_id": 1,
      "set_number": 1,
      "time_spent": 3600,
      "questions": [
        {
          "question_id": 1,
          "is_attempted": true,
          "selected_option_index": 1,
          "is_correct": true,
          "marks_obtained": 20,
          "total_marks": 20,
          "time_spent": 120
        },
        {
          "question_id": 2,
          "is_attempted": true,
          "code_answer": "import React from 'react';\n\nconst FormComponent = () => {\n  // Implementation\n  return <div>Form</div>;\n};\n\nexport default FormComponent;",
          "is_correct": true,
          "marks_obtained": 35,
          "total_marks": 35,
          "time_spent": 1800
        }
      ]
    },
    {
      "section_id": 2,
      "set_number": 1,
      "time_spent": 3600,
      "questions": [
        {
          "question_id": 3,
          "is_attempted": true,
          "selected_option_index": 1,
          "is_correct": true,
          "marks_obtained": 20,
          "total_marks": 20,
          "time_spent": 120
        },
        {
          "question_id": 4,
          "is_attempted": true,
          "code_answer": "const express = require('express');\nconst app = express();\n\napp.get('/api/users', (req, res) => {\n  // Implementation\n  res.json({ users: [] });\n});\n\nmodule.exports = app;",
          "is_correct": false,
          "marks_obtained": 20,
          "total_marks": 35,
          "time_spent": 1800
        }
      ]
    },
    {
      "section_id": 3,
      "set_number": 1,
      "time_spent": 2400,
      "questions": [
        {
          "question_id": 5,
          "is_attempted": false,
          "is_correct": false,
          "marks_obtained": 0,
          "total_marks": 20,
          "time_spent": 0
        },
        {
          "question_id": 6,
          "is_attempted": true,
          "code_answer": "// Partial implementation\nclass CacheManager {\n  constructor() {\n    this.cache = new Map();\n  }\n  \n  get(key) {\n    return this.cache.get(key);\n  }\n}",
          "is_correct": false,
          "marks_obtained": 10,
          "total_marks": 35,
          "time_spent": 2400
        }
      ]
    }
  ]
}
```

### Generate Report by Candidate Email
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_id": 1,
  "candidate_email": "candidate@example.com",
  "started_at": "2025-12-01T09:00:00Z",
  "ended_at": "2025-12-01T12:00:00Z",
  "submitted_at": "2025-12-01T11:55:00Z",
  "window_switch_count": 0,
  "is_cheating": false,
  "cheating_reason": "",
  "sections": [
    {
      "section_id": 1,
      "set_number": 2,
      "time_spent": 1800,
      "questions": [
        {
          "question_id": 7,
          "is_attempted": true,
          "selected_option_index": 0,
          "is_correct": false,
          "marks_obtained": -5,
          "total_marks": 20,
          "time_spent": 180
        }
      ]
    }
  ]
}
```

---

## 10. Proctoring

### Upload Student Image for Proctoring
```http
POST /api/v1/uploadStudentImage/
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Form Data:**
- `token`: (JWT token containing test code)
- `image`: (Image file for identity verification)

---

## 11. Assessment Statistics

### Get Assessment Statistics
```http
GET /api/v1/assessments/statistics/
Authorization: Bearer <token>
```
````
```

---

## Important Notes

### Assessment Validation Rules
1. **Net Scoring Consistency**: All sections within the same set must have equal net scoring potential (positive_marks + negative_marks)
2. **Structure Consistency**: All sets must have identical section structures
3. **Cross-Set Scoring**: Each section must have the same net scoring potential across all sets

### Attachment References
- Use `$1`, `$2`, etc. in question_text to reference attachments array (1-indexed)
- Attachments array length must be ≥ highest reference number used

### Question Types
- `"non-coding"`: Multiple choice questions with options and correct_option_index
- `"coding"`: Programming questions with description, constraints, and test_cases

### Required Fields
- All questions must have: question_type, section_id, set_number, question_text, positive_marks, negative_marks, time_limit
- Non-coding questions need: options, correct_option_index
- Coding questions need: description, constraints, test_cases

### Time Limits
- time_limit is in seconds
- Assessment duration is calculated automatically from question time limits

### Section IDs
- section_id values must be 1-indexed (1, 2, 3, etc.)
- Must correspond to section_names array indices + 1

### Set Numbers
- set_number values must be positive integers (1, 2, 3, etc.)
- Must not exceed num_of_sets value
