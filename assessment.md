# Complete Assessment API Testing Guide

This comprehensive guide covers ALL assessment-related APIs and routes in the PN Academy backend system, based on thorough analysis of the entire codebase. Use this guide to test every aspect of the assessment functionality from creation to management, student assignment, and file handling.

## Table of Contents
1. [System Architecture Overview](#system-architecture-overview)
2. [Authentication & Setup](#authentication--setup)
3. [Assessment Management APIs](#assessment-management-apis)
4. [Student & CSV Management APIs](#student--csv-management-apis)
5. [Test Code Management APIs](#test-code-management-apis)
6. [File Management & AWS S3 APIs](#file-management--aws-s3-apis)
7. [Email Management APIs](#email-management-apis)
8. [Proctoring APIs](#proctoring-apis)
9. [Advanced Testing Workflows](#advanced-testing-workflows)
10. [Error Handling & Edge Cases](#error-handling--edge-cases)

---

## System Architecture Overview

### Core Models Structure
The assessment system is built around these key models:
- **Assessment**: Main assessment container with metadata
- **Section**: Assessment sections (e.g., Math, Coding, Logic)
- **Question**: Individual questions within sections
- **Student**: Student records from CSV uploads
- **TestCode**: Unique access codes for students
- **CSVUpload**: Batch student upload tracking
- **AssessmentFile**: File attachments for assessments

### Base Configuration
- **Base URL**: `http://127.0.0.1:8000/api/v1/`
- **Authentication**: JWT Bearer tokens required for all APIs
- **Pagination**: Default 10 items per page, max 100
- **File Storage**: AWS S3 integration for attachments

---

## Authentication & Setup

### 1. Environment Setup
First, ensure your environment is configured properly:

```bash
# Start the server
python manage.py runserver

# Verify server is running
curl http://127.0.0.1:8000/
```

### 2. User Registration
```bash
curl -X POST http://127.0.0.1:8000/api/v1/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "securepassword123"
  }'
```

**Expected Response:**
```json
{
  "token": "your_jwt_token_here"
}
```

### 3. User Login
```bash
curl -X POST http://127.0.0.1:8000/api/v1/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "securepassword123"
  }'
```

### 4. Set Authentication Token
Export your token for subsequent requests:
```bash
export JWT_TOKEN="your_jwt_token_here"
```

### 5. Test Authentication
```bash
curl -X GET http://127.0.0.1:8000/api/v1/assessments/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

---

## Assessment Management APIs

The system provides two types of assessment APIs:
1. **AssessmentViewSet** - Full CRUD operations with advanced features
2. **AssessmentView** - Simple JSON storage for legacy support

### Core Assessment CRUD Operations

#### 1. Create Assessment - Basic Structure

**Endpoint:** `POST /api/v1/assessments/`

**Basic Non-Coding Assessment:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/assessments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_name": "Basic Mathematics Test",
    "assessment_type": "non-coding",
    "assessment_description": "Elementary mathematics assessment for grade 10",
    "passing_marks": 40,
    "num_of_sets": 1,
    "section_names": ["Arithmetic", "Algebra"],
    "section_descriptions": [
      "Basic arithmetic operations and calculations",
      "Simple algebraic expressions and equations"
    ],
    "start_time": "2025-02-01T09:00:00Z",
    "end_time": "2025-02-01T11:00:00Z",
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
        "question_text": "What is 25 + 17?",
        "options": ["40", "41", "42", "43"],
        "correct_option_index": 2,
        "positive_marks": 5,
        "negative_marks": -1,
        "time_limit": 60
      },
      {
        "question_type": "non-coding",
        "section_id": 2,
        "set_number": 1,
        "question_text": "Solve for x: 3x + 9 = 21",
        "options": ["3", "4", "5", "6"],
        "correct_option_index": 1,
        "positive_marks": 10,
        "negative_marks": -2,
        "time_limit": 120
      }
    ]
  }'
```

#### 2. Create Assessment - Advanced Coding Assessment

**Mixed Assessment with Coding Questions:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/assessments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_name": "Full Stack Developer Assessment",
    "assessment_type": "mix",
    "assessment_description": "Comprehensive evaluation for full stack developer position covering algorithms, system design, and problem-solving",
    "passing_marks": 70,
    "num_of_sets": 2,
    "section_names": ["Programming Logic", "Data Structures", "System Design"],
    "section_descriptions": [
      "Basic programming logic and algorithmic thinking",
      "Understanding of fundamental data structures",
      "System architecture and design principles"
    ],
    "start_time": "2025-02-15T10:00:00Z",
    "end_time": "2025-02-15T14:00:00Z",
    "is_electron_only": true,
    "num_of_ai_generated_questions": 5,
    "is_proctored": true,
    "is_published": false,
    "attachments": [
      "https://example.com/coding-standards.pdf",
      "https://example.com/api-reference.json"
    ],
    "questions": [
      {
        "question_type": "non-coding",
        "section_id": 1,
        "set_number": 1,
        "question_text": "What is the time complexity of binary search?",
        "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
        "correct_option_index": 1,
        "positive_marks": 5,
        "negative_marks": -1,
        "time_limit": 90
      },
      {
        "question_type": "coding",
        "section_id": 1,
        "set_number": 1,
        "question_text": "Implement a function to reverse a linked list",
        "description": "Given the head of a singly linked list, reverse the list and return the reversed list head.",
        "constraints": [
          "The number of nodes in the list is the range [0, 5000]",
          "-5000 <= Node.val <= 5000"
        ],
        "positive_marks": 15,
        "negative_marks": 0,
        "time_limit": 1800,
        "test_cases": {
          "examples": [
            {
              "input": "[1,2,3,4,5]",
              "output": "[5,4,3,2,1]"
            },
            {
              "input": "[1,2]",
              "output": "[2,1]"
            }
          ],
          "hidden": [
            {
              "input": "[1,2,3,4,5,6,7,8,9,10]",
              "output": "[10,9,8,7,6,5,4,3,2,1]"
            },
            {
              "input": "[]",
              "output": "[]"
            }
          ]
        }
      },
      {
        "question_type": "non-coding",
        "section_id": 3,
        "set_number": 2,
        "question_text": "Which architectural pattern is best for microservices communication?",
        "options": ["Monolithic", "Event-driven", "Layered", "MVC"],
        "correct_option_index": 1,
        "positive_marks": 8,
        "negative_marks": -2,
        "time_limit": 150
      }
    ]
  }'
```

**Expected Response:**
```json
{
  "message": "Assessment created successfully",
  "assessment_id": 1,
  "data": {
    "id": 1,
    "assessment_name": "Full Stack Developer Assessment",
    "assessment_type": "mix",
    "total_marks": 28,
    "duration": 32,
    "sections": [
      {
        "id": 1,
        "name": "Programming Logic",
        "total_marks": 20,
        "questions": [...]
      }
    ]
  }
}
```

#### 3. List All Assessments

**Basic Listing:**
```bash
curl -X GET http://127.0.0.1:8000/api/v1/assessments/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Advanced Filtering and Pagination:**
```bash
# Filter by type
curl -X GET "http://127.0.0.1:8000/api/v1/assessments/?type=coding" \
  -H "Authorization: Bearer $JWT_TOKEN"

# Filter by published status
curl -X GET "http://127.0.0.1:8000/api/v1/assessments/?is_published=true" \
  -H "Authorization: Bearer $JWT_TOKEN"

# Search by title
curl -X GET "http://127.0.0.1:8000/api/v1/assessments/?search=Developer" \
  -H "Authorization: Bearer $JWT_TOKEN"

# Pagination with page size
curl -X GET "http://127.0.0.1:8000/api/v1/assessments/?page=1&page_size=5" \
  -H "Authorization: Bearer $JWT_TOKEN"

# Combined filters
curl -X GET "http://127.0.0.1:8000/api/v1/assessments/?type=mix&is_published=false&search=Full&page=1" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

#### 4. Retrieve Specific Assessment

```bash
curl -X GET http://127.0.0.1:8000/api/v1/assessments/1/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected Response:**
```json
{
  "message": "Assessment retrieved successfully",
  "data": {
    "id": 1,
    "assessment_name": "Full Stack Developer Assessment",
    "assessment_description": "Comprehensive evaluation...",
    "assessment_type": "mix",
    "created_by": 1,
    "created_at": "2025-01-01T10:00:00Z",
    "is_published": false,
    "total_marks": 28,
    "passing_marks": 70,
    "duration": 32,
    "sections": [
      {
        "id": 1,
        "name": "Programming Logic",
        "description": "Basic programming logic...",
        "total_marks": 20,
        "duration": 30,
        "questions": [
          {
            "id": 1,
            "question_text": "What is the time complexity...",
            "question_type": "non-coding",
            "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
            "correct_answer": "O(log n)",
            "marks": 5,
            "negative_marks": -1,
            "time_limit": 90
          }
        ]
      }
    ]
  }
}
```

#### 5. Update Assessment

**Full Update (PUT):**
```bash
curl -X PUT http://127.0.0.1:8000/api/v1/assessments/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_name": "Updated Full Stack Assessment",
    "assessment_description": "Updated comprehensive evaluation",
    "passing_marks": 75,
    "is_proctored": true
  }'
```

**Partial Update (PATCH):**
```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/assessments/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_name": "Modified Assessment Title",
    "passing_marks": 80
  }'
```

#### 6. Assessment Publishing Operations

**Publish Assessment:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/assessments/1/publish/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected Response:**
```json
{
  "message": "Assessment published successfully",
  "data": {
    "id": 1,
    "is_published": true,
    "assessment_name": "Full Stack Developer Assessment"
  }
}
```

**Unpublish Assessment:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/assessments/1/unpublish/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

#### 7. Duplicate Assessment

```bash
curl -X POST http://127.0.0.1:8000/api/v1/assessments/1/duplicate/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected Response:**
```json
{
  "message": "Assessment duplicated successfully",
  "data": {
    "id": 2,
    "assessment_name": "Full Stack Developer Assessment (Copy)",
    "is_published": false,
    "total_marks": 28,
    "sections": [...]
  }
}
```

#### 8. Delete Assessment

```bash
curl -X DELETE http://127.0.0.1:8000/api/v1/assessments/1/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Note:** Cannot delete published assessments. Will return error if attempted.

#### 9. Assessment Statistics

```bash
curl -X GET http://127.0.0.1:8000/api/v1/assessments/statistics/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected Response:**
```json
{
  "message": "Statistics retrieved successfully",
  "data": {
    "total_assessments": 5,
    "published_assessments": 3,
    "draft_assessments": 2,
    "active_assessments": 5,
    "by_type": {
      "coding": 2,
      "non-coding": 1,
      "mix": 2
    },
    "proctored_assessments": 4,
    "recent_assessments": 3
  }
}
```

### Legacy Assessment APIs (JSON Storage)

These APIs provide simple JSON storage for backward compatibility:

#### 1. Create JSON Assessment

```bash
curl -X POST http://127.0.0.1:8000/api/v1/assessment \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_name": "Legacy Test",
    "assessment_type": "non-coding",
    "questions": []
  }'
```

#### 2. Get JSON Assessments

```bash
# Get all
curl -X GET http://127.0.0.1:8000/api/v1/assessment \
  -H "Authorization: Bearer $JWT_TOKEN"

# Get specific
curl -X GET "http://127.0.0.1:8000/api/v1/assessment?id=1" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

#### 3. Update JSON Assessment

```bash
curl -X PUT "http://127.0.0.1:8000/api/v1/assessment?id=1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_name": "Updated Legacy Test"
  }'
```

#### 4. Delete JSON Assessment

```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/assessment?id=1" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

---

## Student & CSV Management APIs

### 1. Upload Students via CSV

**Endpoint:** `POST /api/v1/uploadStudents/`

**Prepare CSV file (students.csv):**
```csv
name,email
John Doe,john.doe@example.com
Jane Smith,jane.smith@example.com
Alice Johnson,alice.johnson@example.com
Bob Williams,bob.williams@example.com
Sarah Davis,sarah.davis@example.com
```

**Upload the CSV:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/uploadStudents/ \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -F "file=@students.csv"
```

**Expected Response:**
```json
{
  "message": "CSV processing completed",
  "summary": {
    "total_processed": 5,
    "created": 5,
    "skipped": 0,
    "errors": 0
  },
  "created_students": [
    {
      "id": 1,
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "created_at": "2025-01-01T10:00:00Z"
    },
    {
      "id": 2,
      "full_name": "Jane Smith",
      "email": "jane.smith@example.com",
      "created_at": "2025-01-01T10:00:00Z"
    }
  ],
  "skipped_students": [],
  "errors": []
}
```

**Test with Invalid CSV (missing columns):**
```csv
name
John Doe
Jane Smith
```

```bash
curl -X POST http://127.0.0.1:8000/api/v1/uploadStudents/ \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -F "file=@invalid_students.csv"
```

**Expected Error Response:**
```json
{
  "error": "CSV must contain columns: name, email"
}
```

**Test with Duplicate Emails:**
```csv
name,email
John Doe,john.doe@example.com
John Smith,john.doe@example.com
```

**Expected Response (with skipped entries):**
```json
{
  "message": "CSV processing completed",
  "summary": {
    "total_processed": 2,
    "created": 1,
    "skipped": 1,
    "errors": 0
  },
  "created_students": [
    {
      "id": 1,
      "full_name": "John Doe",
      "email": "john.doe@example.com"
    }
  ],
  "skipped_students": [
    {
      "name": "John Smith",
      "email": "john.doe@example.com",
      "reason": "Email already exists"
    }
  ],
  "errors": []
}
```

### 2. List CSV Uploads

**Endpoint:** `GET /api/v1/students-list/`

```bash
curl -X GET http://127.0.0.1:8000/api/v1/students-list/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected Response:**
```json
[
  {
    "id": 1,
    "uploaded_by": 1,
    "uploaded_at": "2025-01-01T10:00:00Z",
    "file_name": "students.csv",
    "total_records": 5,
    "processed_records": 5,
    "status": "completed",
    "errors": null
  }
]
```

### 3. Get Specific CSV Upload

```bash
curl -X GET http://127.0.0.1:8000/api/v1/students-list/1/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

### 4. List All Students

**Endpoint:** `GET /api/v1/students/`

```bash
curl -X GET http://127.0.0.1:8000/api/v1/students/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

### 5. Get Students by CSV Upload (Preview)

**Endpoint:** `GET /api/v1/csv-uploads/{csv_upload_id}/students/`

```bash
curl -X GET http://127.0.0.1:8000/api/v1/csv-uploads/1/students/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected Response:**
```json
{
  "csv_upload_id": 1,
  "csv_upload_info": {
    "file_name": "students.csv",
    "uploaded_by": "testuser@example.com",
    "uploaded_at": "2025-01-01T10:00:00Z",
    "total_records": 5
  },
  "students": [
    {
      "id": 1,
      "email": "john.doe@example.com",
      "full_name": "John Doe",
      "created_at": "2025-01-01T10:00:00Z"
    }
  ],
  "total_students": 5
}
```

---

## Test Code Management APIs

### 1. Assign Assessment to CSV Upload Students

**Endpoint:** `POST /api/v1/assign-assessment/`

```bash
curl -X POST http://127.0.0.1:8000/api/v1/assign-assessment/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_id": 1,
    "csv_upload_id": 1
  }'
```

**Expected Response:**
```json
{
  "message": "Assessment assignment completed",
  "assessment": {
    "id": 1,
    "title": "Full Stack Developer Assessment",
    "universal_code": "UNIV-ABC123XYZ789"
  },
  "csv_upload": {
    "id": 1,
    "file_name": "students.csv",
    "total_students": 5
  },
  "summary": {
    "total_students": 5,
    "codes_created": 5,
    "codes_skipped": 0,
    "errors": 0
  },
  "created_test_codes": [
    {
      "id": 1,
      "code": "ABCD1234",
      "student_name": "John Doe",
      "student_email": "john.doe@example.com",
      "assessment_title": "Full Stack Developer Assessment",
      "created_at": "2025-01-01T10:00:00Z",
      "is_used": false
    }
  ],
  "skipped_codes": [],
  "errors": []
}
```

**Test Duplicate Assignment (should skip):**
```bash
# Run the same command again
curl -X POST http://127.0.0.1:8000/api/v1/assign-assessment/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_id": 1,
    "csv_upload_id": 1
  }'
```

**Expected Response:**
```json
{
  "error": "Assessment already assigned to students from this CSV upload"
}
```

### 2. Get Test Codes for Assessment

**Endpoint:** `GET /api/v1/assessments/{assessment_id}/test-codes/`

**Basic Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/v1/assessments/1/test-codes/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**With Filters:**
```bash
# Filter by CSV upload
curl -X GET "http://127.0.0.1:8000/api/v1/assessments/1/test-codes/?csv_upload_id=1" \
  -H "Authorization: Bearer $JWT_TOKEN"

# Filter by usage status
curl -X GET "http://127.0.0.1:8000/api/v1/assessments/1/test-codes/?is_used=false" \
  -H "Authorization: Bearer $JWT_TOKEN"

# Combined filters
curl -X GET "http://127.0.0.1:8000/api/v1/assessments/1/test-codes/?csv_upload_id=1&is_used=false" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected Response:**
```json
{
  "assessment": {
    "id": 1,
    "title": "Full Stack Developer Assessment",
    "universal_code": "UNIV-ABC123XYZ789"
  },
  "total_codes": 5,
  "test_codes": [
    {
      "id": 1,
      "code": "ABCD1234",
      "student_name": "John Doe",
      "student_email": "john.doe@example.com",
      "assessment_title": "Full Stack Developer Assessment",
      "created_at": "2025-01-01T10:00:00Z",
      "is_used": false,
      "used_at": null
    }
  ]
}
```

### 3. Get Test Codes for CSV Upload

**Endpoint:** `GET /api/v1/csv-uploads/{csv_upload_id}/test-codes/`

```bash
curl -X GET http://127.0.0.1:8000/api/v1/csv-uploads/1/test-codes/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**With Filters:**
```bash
# Filter by assessment
curl -X GET "http://127.0.0.1:8000/api/v1/csv-uploads/1/test-codes/?assessment_id=1" \
  -H "Authorization: Bearer $JWT_TOKEN"

# Filter by usage status
curl -X GET "http://127.0.0.1:8000/api/v1/csv-uploads/1/test-codes/?is_used=true" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected Response:**
```json
{
  "csv_upload": {
    "id": 1,
    "file_name": "students.csv",
    "uploaded_by": "testuser@example.com",
    "uploaded_at": "2025-01-01T10:00:00Z"
  },
  "total_codes": 5,
  "test_codes": [
    {
      "id": 1,
      "code": "ABCD1234",
      "student_name": "John Doe",
      "student_email": "john.doe@example.com",
      "assessment_title": "Full Stack Developer Assessment"
    }
  ]
}
```

---

## File Management & AWS S3 APIs

### 1. Generate Presigned URL for File Upload

**Endpoint:** `POST /api/v1/upload/`

**For PDF Document:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/upload/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_id": 1,
    "filename": "reference_guide.pdf"
  }'
```

**For Image File:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/upload/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_id": 1,
    "filename": "diagram.png"
  }'
```

**Expected Response:**
```json
{
  "message": "Presigned URL generated successfully",
  "presigned_url": "https://your-bucket.s3.region.amazonaws.com/assessments/1/reference_guide.pdf?AWSAccessKeyId=...&Expires=...&Signature=...",
  "expires_at": "2025-01-01T11:00:00Z",
  "expires_in_seconds": 3600,
  "assessment_file_id": 1,
  "s3_path": "assessments/1/reference_guide.pdf",
  "upload_instructions": {
    "method": "PUT",
    "url": "https://your-bucket.s3.region.amazonaws.com/...",
    "headers": {
      "Content-Type": "application/pdf"
    }
  }
}
```

### 2. Upload File to S3 (using presigned URL)

```bash
# Using the presigned URL from previous response
curl -X PUT "https://your-bucket.s3.region.amazonaws.com/assessments/1/reference_guide.pdf?AWSAccessKeyId=..." \
  -H "Content-Type: application/pdf" \
  --upload-file reference_guide.pdf
```

**Expected Response:** HTTP 200 OK (no body)

### 3. Check File Upload Status

**Endpoint:** `GET /api/v1/fileStatus/`

```bash
curl -X GET http://127.0.0.1:8000/api/v1/fileStatus/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_id": 1,
    "filename": "reference_guide.pdf"
  }'
```

**Expected Response (File Uploaded):**
```json
{
  "message": "File found and record updated",
  "file_uploaded": true,
  "file_size_bytes": 2548736,
  "file_size_mb": 2.43,
  "file_size_kb": 2489.00,
  "assessment_file_id": 1,
  "s3_url": "https://your-bucket.s3.region.amazonaws.com/assessments/1/reference_guide.pdf",
  "upload_status": "uploaded",
  "uploaded_at": "2025-01-01T10:30:00Z"
}
```

**Expected Response (File Not Found):**
```json
{
  "message": "File not found in S3",
  "file_uploaded": false,
  "file_size_bytes": 0,
  "upload_status": "pending",
  "presigned_url_expired": true
}
```

### 4. List Files for Assessment

**Endpoint:** `GET /api/v1/files/{assessment_id}`

```bash
curl -X GET http://127.0.0.1:8000/api/v1/files/1 \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected Response:**
```json
{
  "assessment_id": 1,
  "assessment_title": "Full Stack Developer Assessment",
  "files": [
    {
      "id": 1,
      "filename": "reference_guide.pdf",
      "s3_key": "assessments/1/reference_guide.pdf",
      "s3_url": "https://your-bucket.s3.region.amazonaws.com/assessments/1/reference_guide.pdf",
      "file_size": 2548736,
      "file_size_mb": 2.43,
      "upload_status": "uploaded",
      "created_at": "2025-01-01T10:00:00Z",
      "updated_at": "2025-01-01T10:30:00Z"
    },
    {
      "id": 2,
      "filename": "diagram.png",
      "upload_status": "pending",
      "file_size_mb": 0
    }
  ],
  "total_files": 2,
  "uploaded_files": 1,
  "pending_files": 1
}
```

### 5. Test File Management Error Cases

**Test Duplicate Filename:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/upload/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_id": 1,
    "filename": "reference_guide.pdf"
  }'
```

**Test Invalid Assessment ID:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/upload/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_id": 99999,
    "filename": "test.pdf"
  }'
```

---

## Email Management APIs

### 1. Send Bulk Emails to CSV Upload Students

**Endpoint:** `POST /api/v1/sendEmail/`

**Plain Text Email:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/sendEmail/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "csv_upload_id": 1,
    "subject": "Assessment Invitation - Full Stack Developer Position",
    "content": "Dear Candidate,\n\nYou have been invited to take the Full Stack Developer Assessment. Please use your unique test code to access the assessment.\n\nBest regards,\nPN Academy Team",
    "content_type": "text"
  }'
```

**HTML Email:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/sendEmail/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "csv_upload_id": 1,
    "subject": "Assessment Ready - Full Stack Developer Test",
    "content": "<html><body><h2>Assessment Invitation</h2><p>Dear Candidate,</p><p>You have been invited to take the <strong>Full Stack Developer Assessment</strong>.</p><p>Please use your unique test code to access the assessment.</p><br><p>Best regards,<br>PN Academy Team</p></body></html>",
    "content_type": "html"
  }'
```

**Expected Response:**
```json
{
  "message": "Email sending completed",
  "csv_upload_id": 1,
  "total_students": 5,
  "successful_sends": 5,
  "failed_sends": 0,
  "results": [
    {
      "student_email": "john.doe@example.com",
      "student_name": "John Doe",
      "status": "success",
      "error_message": ""
    },
    {
      "student_email": "jane.smith@example.com",
      "student_name": "Jane Smith",
      "status": "success",
      "error_message": ""
    }
  ]
}
```

**Test with Invalid CSV Upload ID:**
```bash
curl -X POST http://127.0.0.1:8000/api/v1/sendEmail/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "csv_upload_id": 99999,
    "subject": "Test",
    "content": "Test content",
    "content_type": "text"
  }'
```

**Expected Error Response:**
```json
{
  "error": "CSV Upload not found"
}
```

---

## Proctoring APIs

### 1. Upload Student Image for Proctoring

**Endpoint:** `POST /api/v1/uploadStudentImage/`

This endpoint requires a JWT token containing a test code and an image file.

**Prepare Test Data:**
```bash
# First, you would need to create a JWT token with test code
# This is typically done by your frontend application
# For testing, you can use a mock token or create one programmatically

curl -X POST http://127.0.0.1:8000/api/v1/uploadStudentImage/ \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -F "token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0ZXN0X2NvZGUiOiJBQkNEMTIzNCJ9.signature" \
  -F "image=@student_photo.jpg"
```

**Expected Success Response:**
```json
{
  "success": true,
  "message": "Image Sent Successfully!"
}
```

**Expected Error Responses:**
```json
{
  "success": false,
  "message": "Token has expired"
}
```

```json
{
  "success": false,
  "message": "Invalid test code"
}
```

---

## Advanced Testing Workflows

### Complete Assessment Creation and Management Workflow

This workflow demonstrates a complete end-to-end process:

#### Step 1: Create Assessment
```bash
ASSESSMENT_RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/api/v1/assessments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_name": "Complete Workflow Test",
    "assessment_type": "mix",
    "assessment_description": "End-to-end workflow testing assessment",
    "passing_marks": 60,
    "num_of_sets": 1,
    "section_names": ["Programming", "Logic"],
    "section_descriptions": ["Basic programming concepts", "Logical reasoning"],
    "start_time": "2025-02-01T09:00:00Z",
    "end_time": "2025-02-01T12:00:00Z",
    "is_electron_only": false,
    "num_of_ai_generated_questions": 0,
    "is_proctored": true,
    "is_published": false,
    "attachments": [],
    "questions": [
      {
        "question_type": "non-coding",
        "section_id": 1,
        "set_number": 1,
        "question_text": "What is object-oriented programming?",
        "options": ["A paradigm", "A language", "A framework", "A library"],
        "correct_option_index": 0,
        "positive_marks": 10,
        "negative_marks": -2,
        "time_limit": 120
      },
      {
        "question_type": "non-coding",
        "section_id": 2,
        "set_number": 1,
        "question_text": "Which comes next: 2, 4, 8, 16, ?",
        "options": ["20", "24", "32", "64"],
        "correct_option_index": 2,
        "positive_marks": 5,
        "negative_marks": -1,
        "time_limit": 90
      }
    ]
  }')

# Extract assessment ID
ASSESSMENT_ID=$(echo $ASSESSMENT_RESPONSE | grep -o '"assessment_id":[0-9]*' | cut -d':' -f2)
echo "Created Assessment ID: $ASSESSMENT_ID"
```

#### Step 2: Add File Attachments
```bash
# Generate presigned URL
UPLOAD_RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/api/v1/upload/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d "{
    \"assessment_id\": $ASSESSMENT_ID,
    \"filename\": \"programming_guide.pdf\"
  }")

# Extract presigned URL (in real scenario, you'd parse JSON properly)
echo "Upload response: $UPLOAD_RESPONSE"

# Upload a sample file (create a dummy PDF first)
echo "Sample PDF content" > programming_guide.pdf
PRESIGNED_URL=$(echo $UPLOAD_RESPONSE | grep -o '"presigned_url":"[^"]*' | cut -d':' -f2- | tr -d '"')
```

#### Step 3: Upload Students
```bash
# Create test CSV
cat > workflow_students.csv << EOF
name,email
Alice Johnson,alice@example.com
Bob Smith,bob@example.com
Carol Davis,carol@example.com
EOF

# Upload CSV
CSV_RESPONSE=$(curl -s -X POST http://127.0.0.1:8000/api/v1/uploadStudents/ \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -F "file=@workflow_students.csv")

echo "CSV Upload Response: $CSV_RESPONSE"
```

#### Step 4: Publish Assessment
```bash
curl -X POST http://127.0.0.1:8000/api/v1/assessments/$ASSESSMENT_ID/publish/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

#### Step 5: Assign Assessment to Students
```bash
# You'll need to extract CSV_UPLOAD_ID from the CSV_RESPONSE
# For this example, assuming it's 1
CSV_UPLOAD_ID=1

curl -X POST http://127.0.0.1:8000/api/v1/assign-assessment/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d "{
    \"assessment_id\": $ASSESSMENT_ID,
    \"csv_upload_id\": $CSV_UPLOAD_ID
  }"
```

#### Step 6: Send Notification Emails
```bash
curl -X POST http://127.0.0.1:8000/api/v1/sendEmail/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d "{
    \"csv_upload_id\": $CSV_UPLOAD_ID,
    \"subject\": \"Assessment Ready - Complete Workflow Test\",
    \"content\": \"Your assessment is now available. Please check your test code and start the assessment.\",
    \"content_type\": \"text\"
  }"
```

#### Step 7: Verify Test Codes Generated
```bash
curl -X GET http://127.0.0.1:8000/api/v1/assessments/$ASSESSMENT_ID/test-codes/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

#### Step 8: Get Assessment Statistics
```bash
curl -X GET http://127.0.0.1:8000/api/v1/assessments/statistics/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```

### Performance Testing Workflow

#### 1. Create Multiple Assessments
```bash
for i in {1..10}; do
  curl -X POST http://127.0.0.1:8000/api/v1/assessments/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $JWT_TOKEN" \
    -d "{
      \"assessment_name\": \"Performance Test Assessment $i\",
      \"assessment_type\": \"non-coding\",
      \"assessment_description\": \"Performance testing assessment number $i\",
      \"passing_marks\": 50,
      \"num_of_sets\": 1,
      \"section_names\": [\"General\"],
      \"section_descriptions\": [\"General questions\"],
      \"start_time\": \"2025-02-01T09:00:00Z\",
      \"end_time\": \"2025-02-01T11:00:00Z\",
      \"is_published\": false,
      \"questions\": [
        {
          \"question_type\": \"non-coding\",
          \"section_id\": 1,
          \"set_number\": 1,
          \"question_text\": \"Sample question $i\",
          \"options\": [\"A\", \"B\", \"C\", \"D\"],
          \"correct_option_index\": 0,
          \"positive_marks\": 5,
          \"negative_marks\": -1,
          \"time_limit\": 60
        }
      ]
    }" &
done
wait
echo "Created 10 assessments concurrently"
```

#### 2. Test Pagination Performance
```bash
# Test with different page sizes
for page_size in 5 10 20 50; do
  echo "Testing page size: $page_size"
  time curl -s "http://127.0.0.1:8000/api/v1/assessments/?page_size=$page_size" \
    -H "Authorization: Bearer $JWT_TOKEN" > /dev/null
done
```

#### 3. Upload Large CSV Files
```bash
# Create large CSV file
{
  echo "name,email"
  for i in {1..1000}; do
    echo "User$i,user$i@example.com"
  done
} > large_students.csv

time curl -X POST http://127.0.0.1:8000/api/v1/uploadStudents/ \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -F "file=@large_students.csv"
```

### Multi-Set Assessment Testing

```bash
curl -X POST http://127.0.0.1:8000/api/v1/assessments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_name": "Multi-Set Assessment Test",
    "assessment_type": "mix",
    "assessment_description": "Testing multiple sets functionality",
    "passing_marks": 60,
    "num_of_sets": 3,
    "section_names": ["Math", "Logic", "Programming"],
    "section_descriptions": ["Mathematical questions", "Logic puzzles", "Programming concepts"],
    "start_time": "2025-02-01T09:00:00Z",
    "end_time": "2025-02-01T12:00:00Z",
    "is_published": false,
    "questions": [
      {
        "question_type": "non-coding",
        "section_id": 1,
        "set_number": 1,
        "question_text": "Set 1 Math Question",
        "options": ["10", "20", "30", "40"],
        "correct_option_index": 1,
        "positive_marks": 5,
        "negative_marks": -1,
        "time_limit": 60
      },
      {
        "question_type": "non-coding",
        "section_id": 2,
        "set_number": 2,
        "question_text": "Set 2 Logic Question",
        "options": ["A", "B", "C", "D"],
        "correct_option_index": 2,
        "positive_marks": 8,
        "negative_marks": -2,
        "time_limit": 90
      },
      {
        "question_type": "coding",
        "section_id": 3,
        "set_number": 3,
        "question_text": "Set 3 Programming Question: Implement a simple function",
        "description": "Write a function that returns the sum of two numbers",
        "constraints": ["Both numbers will be integers", "-1000 <= numbers <= 1000"],
        "positive_marks": 15,
        "negative_marks": 0,
        "time_limit": 600,
        "test_cases": {
          "examples": [
            {"input": "5, 3", "output": "8"},
            {"input": "10, -2", "output": "8"}
          ],
          "hidden": [
            {"input": "100, 200", "output": "300"}
          ]
        }
      }
    ]
  }'
```

---

## Error Handling & Edge Cases

### Authentication Errors

#### 1. No Token Provided
```bash
curl -X GET http://127.0.0.1:8000/api/v1/assessments/
```
**Expected:** 401 Unauthorized

#### 2. Invalid Token
```bash
curl -X GET http://127.0.0.1:8000/api/v1/assessments/ \
  -H "Authorization: Bearer invalid_token"
```
**Expected:** 401 Unauthorized

#### 3. Expired Token
```bash
curl -X GET http://127.0.0.1:8000/api/v1/assessments/ \
  -H "Authorization: Bearer expired_token"
```
**Expected:** 401 Unauthorized

### Validation Errors

#### 1. Missing Required Fields
```bash
curl -X POST http://127.0.0.1:8000/api/v1/assessments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_name": ""
  }'
```
**Expected:** 400 Bad Request with validation details

#### 2. Invalid Assessment Type
```bash
curl -X POST http://127.0.0.1:8000/api/v1/assessments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_name": "Test",
    "assessment_type": "invalid_type",
    "passing_marks": 50,
    "num_of_sets": 1,
    "section_names": ["Section 1"],
    "section_descriptions": ["Description"],
    "questions": []
  }'
```

#### 3. Invalid Section ID in Questions
```bash
curl -X POST http://127.0.0.1:8000/api/v1/assessments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_name": "Test",
    "assessment_type": "non-coding",
    "passing_marks": 50,
    "num_of_sets": 1,
    "section_names": ["Section 1"],
    "section_descriptions": ["Description"],
    "questions": [
      {
        "question_type": "non-coding",
        "section_id": 5,
        "set_number": 1,
        "question_text": "Test question",
        "options": ["A", "B", "C", "D"],
        "correct_option_index": 0,
        "positive_marks": 5,
        "negative_marks": -1,
        "time_limit": 60
      }
    ]
  }'
```

### Resource Not Found Errors

#### 1. Non-existent Assessment
```bash
curl -X GET http://127.0.0.1:8000/api/v1/assessments/99999/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```
**Expected:** 404 Not Found

#### 2. Non-existent CSV Upload
```bash
curl -X GET http://127.0.0.1:8000/api/v1/csv-uploads/99999/test-codes/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```
**Expected:** 404 Not Found

### Business Logic Errors

#### 1. Deleting Published Assessment
```bash
# First publish an assessment
curl -X POST http://127.0.0.1:8000/api/v1/assessments/1/publish/ \
  -H "Authorization: Bearer $JWT_TOKEN"

# Then try to delete it
curl -X DELETE http://127.0.0.1:8000/api/v1/assessments/1/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```
**Expected:** 400 Bad Request - "Cannot delete a published assessment"

#### 2. Publishing Assessment Without Questions
```bash
# Create assessment without questions
EMPTY_ASSESSMENT=$(curl -s -X POST http://127.0.0.1:8000/api/v1/assessments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_name": "Empty Assessment",
    "assessment_type": "non-coding",
    "passing_marks": 50,
    "num_of_sets": 1,
    "section_names": ["Section 1"],
    "section_descriptions": ["Description"],
    "questions": []
  }')

EMPTY_ASSESSMENT_ID=$(echo $EMPTY_ASSESSMENT | grep -o '"assessment_id":[0-9]*' | cut -d':' -f2)

# Try to publish it
curl -X POST http://127.0.0.1:8000/api/v1/assessments/$EMPTY_ASSESSMENT_ID/publish/ \
  -H "Authorization: Bearer $JWT_TOKEN"
```
**Expected:** 400 Bad Request - "Cannot publish assessment without questions"

#### 3. Modifying Questions of Published Assessment
```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/assessments/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "questions": [
      {
        "question_type": "non-coding",
        "section_id": 1,
        "set_number": 1,
        "question_text": "Modified question",
        "options": ["A", "B", "C", "D"],
        "correct_option_index": 0,
        "positive_marks": 5,
        "negative_marks": -1,
        "time_limit": 60
      }
    ]
  }'
```
**Expected:** 400 Bad Request - "Cannot modify questions of a published assessment"

### File Upload Errors

#### 1. Invalid Assessment ID for File Upload
```bash
curl -X POST http://127.0.0.1:8000/api/v1/upload/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_id": 99999,
    "filename": "test.pdf"
  }'
```
**Expected:** 400 Bad Request - "Assessment not found"

#### 2. Duplicate Filename Upload
```bash
# Upload same filename twice
curl -X POST http://127.0.0.1:8000/api/v1/upload/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_id": 1,
    "filename": "duplicate.pdf"
  }'

# Try again with same filename
curl -X POST http://127.0.0.1:8000/api/v1/upload/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "assessment_id": 1,
    "filename": "duplicate.pdf"
  }'
```

### CSV Upload Errors

#### 1. Non-CSV File Upload
```bash
echo "This is not a CSV" > notcsv.txt
curl -X POST http://127.0.0.1:8000/api/v1/uploadStudents/ \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -F "file=@notcsv.txt"
```
**Expected:** 400 Bad Request - "File must be a CSV file"

#### 2. Empty CSV File
```bash
touch empty.csv
curl -X POST http://127.0.0.1:8000/api/v1/uploadStudents/ \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -F "file=@empty.csv"
```

#### 3. CSV with Invalid Email Addresses
```bash
cat > invalid_emails.csv << EOF
name,email
John Doe,invalid-email
Jane Smith,another-invalid@
EOF

curl -X POST http://127.0.0.1:8000/api/v1/uploadStudents/ \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -F "file=@invalid_emails.csv"
```

### Email Sending Errors

#### 1. Invalid CSV Upload ID for Email
```bash
curl -X POST http://127.0.0.1:8000/api/v1/sendEmail/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "csv_upload_id": 99999,
    "subject": "Test",
    "content": "Test content",
    "content_type": "text"
  }'
```
**Expected:** 404 Not Found - "CSV Upload not found"

#### 2. Empty Subject or Content
```bash
curl -X POST http://127.0.0.1:8000/api/v1/sendEmail/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -d '{
    "csv_upload_id": 1,
    "subject": "",
    "content": "",
    "content_type": "text"
  }'
```
**Expected:** 400 Bad Request with validation errors

---

## Testing Checklist

### Basic Functionality
- [ ] User registration and login
- [ ] JWT token authentication
- [ ] Assessment CRUD operations
- [ ] Assessment publishing/unpublishing
- [ ] Assessment duplication
- [ ] CSV student upload
- [ ] Test code generation
- [ ] Email sending
- [ ] File upload and management

### Advanced Features
- [ ] Multi-set assessments
- [ ] Coding questions with test cases
- [ ] Assessment statistics
- [ ] Pagination and filtering
- [ ] Concurrent operations
- [ ] Large dataset handling

### Error Scenarios
- [ ] Authentication failures
- [ ] Validation errors
- [ ] Resource not found
- [ ] Business logic violations
- [ ] File upload failures
- [ ] Email sending failures

### Performance Testing
- [ ] Large CSV uploads (1000+ students)
- [ ] Multiple concurrent assessment creations
- [ ] Assessment with many questions (50+)
- [ ] Pagination with large datasets
- [ ] File upload performance

### Security Testing
- [ ] Token expiration
- [ ] Invalid tokens
- [ ] Cross-user data access
- [ ] File upload security
- [ ] SQL injection attempts
- [ ] XSS prevention in email content

---

This comprehensive guide covers every aspect of the assessment system. Use it to thoroughly test all functionality, from basic CRUD operations to complex workflows involving multiple components working together.
