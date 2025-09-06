# Assessment API Documentation - PN Academy Platform

## Overview
This document provides comprehensive API documentation for all assessment and student-related endpoints in the PN Academy Assessment Platform. The API uses Django REST Framework with JWT authentication.

---

## Base Configuration
- **Base URL**: `http://localhost:8000/api/v1/` (development)
- **Authentication**: JWT Bearer Token
- **Content-Type**: `application/json` (except file uploads: `multipart/form-data`)

---

## Authentication Endpoints

### 1. User Registration
```http
POST /api/v1/register/
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response**:
```json
{
  "email": "user@example.com",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 2. User Login
```http
POST /api/v1/login/
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response**:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 3. Reset Password
```http
POST /api/v1/reset-password/
```

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "new_password": "newsecurepassword123"
}
```

**Response**:
```json
{
  "message": "Password has been reset successfully"
}
```

---

## Assessment Management Endpoints

### 1. Create Assessment
```http
POST /api/v1/assessments/
```

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "assessment_name": "Full Stack Development Assessment",
  "assessment_type": "mix",
  "assessment_description": "A comprehensive test designed to assess aptitude, coding ability, logical reasoning, and general knowledge with diverse question formats.",
  "passing_marks": 60,
  "total_marks": 100,
  "num_of_sets": 2,
  "section_names": ["Aptitude", "Coding", "Logical Reasoning", "General Knowledge"],
  "section_descriptions": [
    "Numerical and analytical aptitude questions.",
    "Hands-on coding problems with visible and hidden test cases.",
    "Logical puzzles and sequence problems.",
    "General awareness and subject knowledge."
  ],
  "start_time": "2025-09-20T09:30:00Z",
  "end_time": "2025-09-20T12:30:00Z",
  "is_electron_only": false,
  "num_of_ai_generated_questions": 5,
  "is_proctored": true,
  "is_published": false,
  "attachments": [
    "https://example.com/docs/reference-material.pdf",
    "https://example.com/images/question-diagram.png"
  ],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "If 12 pens cost ₹144, what is the cost of 1 pen? $1",
      "options": [
        "₹10",
        "₹12",
        "₹14",
        "₹15"
      ],
      "correct_option_index": 1,
      "positive_marks": 4,
      "negative_marks": -1,
      "time_limit": 60
    },
    {
      "question_type": "non-coding",
      "section_id": 4,
      "set_number": 1,
      "question_text": "Which of the following are programming languages? $2",
      "options": [
        "Python",
        "HTML",
        "Java",
        "CSS"
      ],
      "correct_option_index": 0,
      "positive_marks": 4,
      "negative_marks": -1,
      "time_limit": 90
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Write a function to check if a number is prime. $1",
      "description": "Given an integer n, return true if it is prime, otherwise false.",
      "constraints": [
        "1 <= n <= 10^6",
        "Input is an integer"
      ],
      "positive_marks": 10,
      "negative_marks": 0,
      "time_limit": 900,
      "test_cases": {
        "examples": [
          {
            "input": "5",
            "output": "true"
          },
          {
            "input": "10",
            "output": "false"
          }
        ],
        "hidden": [
          {
            "input": "999983",
            "output": "true"
          }
        ]
      }
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Implement a function to count the number of vowels in a given string. $2",
      "description": "Return the total number of vowels (a, e, i, o, u) in the string, case-insensitive.",
      "constraints": [
        "1 <= length of string <= 10^5",
        "String contains only printable ASCII characters"
      ],
      "positive_marks": 8,
      "negative_marks": 0,
      "time_limit": 600,
      "test_cases": {
        "examples": [
          {
            "input": "Hello World",
            "output": "3"
          },
          {
            "input": "AI",
            "output": "2"
          }
        ],
        "hidden": [
          {
            "input": "Programming is fun",
            "output": "6"
          }
        ]
      }
    }
  ]
}
```

**Response**:
```json
{
  "message": "Assessment created successfully",
  "assessment_id": 1,
  "data": {
    "id": 1,
    "assessment_name": "Full Stack Development Assessment",
    "assessment_type": "mix",
    "total_marks": 26,
    "duration": 28,
    "sections": [...]
  }
}
```

**Field Descriptions**:
- `assessment_name`: Title of the assessment
- `assessment_type`: One of ["coding", "non-coding", "mix"]
- `assessment_description`: Optional description
- `passing_marks`: Minimum marks to pass
- `num_of_sets`: Number of question sets
- `section_names`: Array of section names (1-indexed with section_id)
- `section_descriptions`: Array of section descriptions
- `start_time`/`end_time`: UTC datetime in ISO format
- `is_electron_only`: Restrict to electron app only
- `num_of_ai_generated_questions`: Number of AI-generated questions
- `is_proctored`: Enable proctoring
- `is_published`: Publish status
- `attachments`: Array of attachment URLs (referenced as $1, $2, etc. in questions)
- `questions`: Array of question objects

**Question Types**:
- `"non-coding"`: Multiple choice, single answer
- `"coding"`: Programming problems with test cases

### 2. Get All Assessments
```http
GET /api/v1/assessments/
```

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `page`: Page number (default: 1)
- `page_size`: Items per page (max: 100)
- `type`: Filter by assessment_type ["coding", "non-coding", "mix"]
- `is_published`: Filter by published status [true, false]
- `is_active`: Filter by active status [true, false]
- `search`: Search in assessment titles
- `set_number`: Filter questions by set number

**Response**:
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/v1/assessments/?page=3",
  "previous": "http://localhost:8000/api/v1/assessments/?page=1",
  "results": [
    {
      "id": 1,
      "assessment_name": "Full Stack Development Assessment",
      "assessment_type": "mix",
      "total_marks": 100,
      "passing_marks": 60,
      "duration": 180,
      "is_published": false,
      "sections": [...]
    }
  ]
}
```

### 3. Get Specific Assessment
```http
GET /api/v1/assessments/{id}/
```

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `set_number`: Filter questions by specific set number

**Response**:
```json
{
  "message": "Assessment retrieved successfully",
  "data": {
    "id": 1,
    "assessment_name": "Full Stack Development Assessment",
    "assessment_description": "A comprehensive test...",
    "assessment_type": "mix",
    "total_marks": 100,
    "passing_marks": 60,
    "duration": 180,
    "sections": [
      {
        "id": 1,
        "name": "Aptitude",
        "description": "Numerical and analytical aptitude questions.",
        "total_marks": 20,
        "duration": 30,
        "questions": [...]
      }
    ]
  }
}
```

### 4. Update Assessment
```http
PUT /api/v1/assessments/{id}/
```

**Headers**: `Authorization: Bearer <token>`

**Request Body**: Same as create assessment

**Note**: Cannot modify questions of published assessments

**Response**:
```json
{
  "message": "Assessment updated successfully",
  "data": {
    "id": 1,
    "assessment_name": "Updated Assessment Name",
    ...
  }
}
```

### 5. Partial Update Assessment
```http
PATCH /api/v1/assessments/{id}/
```

**Headers**: `Authorization: Bearer <token>`

**Request Body**: Any subset of assessment fields

**Response**:
```json
{
  "message": "Assessment updated successfully",
  "data": {...}
}
```

### 6. Delete Assessment
```http
DELETE /api/v1/assessments/{id}/
```

**Headers**: `Authorization: Bearer <token>`

**Note**: Cannot delete published assessments

**Response**:
```json
{
  "message": "Assessment \"Full Stack Development Assessment\" deleted successfully"
}
```

### 7. Publish Assessment
```http
POST /api/v1/assessments/{id}/publish/
```

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "message": "Assessment published successfully",
  "data": {
    "id": 1,
    "is_published": true,
    ...
  }
}
```

### 8. Unpublish Assessment
```http
POST /api/v1/assessments/{id}/unpublish/
```

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "message": "Assessment unpublished successfully",
  "data": {
    "id": 1,
    "is_published": false,
    ...
  }
}
```

### 9. Duplicate Assessment
```http
POST /api/v1/assessments/{id}/duplicate/
```

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "message": "Assessment duplicated successfully",
  "data": {
    "id": 2,
    "assessment_name": "Full Stack Development Assessment (Copy)",
    "is_published": false,
    ...
  }
}
```

### 10. Assessment Statistics
```http
GET /api/v1/assessments/statistics/
```

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "message": "Statistics retrieved successfully",
  "data": {
    "total_assessments": 15,
    "published_assessments": 8,
    "draft_assessments": 7,
    "active_assessments": 12,
    "by_type": {
      "coding": 5,
      "non-coding": 4,
      "mix": 6
    },
    "proctored_assessments": 10,
    "recent_assessments": 3
  }
}
```

---

## Student Management Endpoints

### 1. Upload Student CSV
```http
POST /api/v1/uploadStudents/
```

**Headers**: 
- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data`

**Request Body**:
```
file: <CSV file>
```

**CSV Format**:
```csv
name,email
John Doe,john@example.com
Jane Smith,jane@example.com
Alice Johnson,alice@example.com
```

**Response**:
```json
{
  "message": "CSV processing completed",
  "summary": {
    "total_processed": 3,
    "created": 3,
    "skipped": 0,
    "errors": 0
  },
  "created_students": [
    {
      "id": 1,
      "full_name": "John Doe",
      "email": "john@example.com",
      "created_at": "2025-09-06T10:30:00Z"
    }
  ],
  "skipped_students": [],
  "errors": []
}
```

### 2. Get All Students
```http
GET /api/v1/students/
```

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
[
  {
    "id": 1,
    "full_name": "John Doe",
    "email": "john@example.com",
    "created_at": "2025-09-06T10:30:00Z"
  }
]
```

### 3. Get CSV Upload History
```http
GET /api/v1/students-list/
```

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
[
  {
    "id": 1,
    "uploaded_by": 1,
    "uploaded_at": "2025-09-06T10:30:00Z",
    "file_name": "students_batch_1.csv",
    "total_records": 50,
    "processed_records": 48,
    "status": "completed",
    "errors": []
  }
]
```

### 4. Get Students by CSV Upload
```http
GET /api/v1/csv-uploads/{csv_upload_id}/students/
```

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "csv_upload_id": 1,
  "csv_upload_info": {
    "file_name": "students_batch_1.csv",
    "uploaded_by": "admin@example.com",
    "uploaded_at": "2025-09-06T10:30:00Z",
    "total_records": 50
  },
  "students": [
    {
      "id": 1,
      "email": "john@example.com",
      "full_name": "John Doe",
      "created_at": "2025-09-06T10:30:00Z"
    }
  ],
  "total_students": 50
}
```

---

## Assessment Assignment Endpoints

### 1. Assign Assessment to CSV Upload
```http
POST /api/v1/assign-assessment/
```

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "assessment_id": 1,
  "csv_upload_id": 1
}
```

**Response**:
```json
{
  "message": "Assessment assignment completed",
  "assessment": {
    "id": 1,
    "title": "Full Stack Development Assessment",
    "universal_code": "UNIV-ABC123DEF456"
  },
  "csv_upload": {
    "id": 1,
    "file_name": "students_batch_1.csv",
    "total_students": 50
  },
  "summary": {
    "total_students": 50,
    "codes_created": 50,
    "codes_skipped": 0,
    "errors": 0
  },
  "created_test_codes": [
    {
      "id": 1,
      "code": "AB12CD34",
      "student_name": "John Doe",
      "student_email": "john@example.com",
      "assessment_title": "Full Stack Development Assessment",
      "created_at": "2025-09-06T10:30:00Z",
      "is_used": false
    }
  ]
}
```

### 2. Get Test Codes for Assessment
```http
GET /api/v1/assessments/{assessment_id}/test-codes/
```

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `csv_upload_id`: Filter by specific CSV upload
- `is_used`: Filter by usage status [true, false]

**Response**:
```json
{
  "assessment": {
    "id": 1,
    "title": "Full Stack Development Assessment",
    "universal_code": "UNIV-ABC123DEF456"
  },
  "total_codes": 50,
  "test_codes": [
    {
      "id": 1,
      "code": "AB12CD34",
      "student_name": "John Doe",
      "student_email": "john@example.com",
      "assessment_title": "Full Stack Development Assessment",
      "created_at": "2025-09-06T10:30:00Z",
      "is_used": false,
      "used_at": null
    }
  ]
}
```

### 3. Get Test Codes for CSV Upload
```http
GET /api/v1/csv-uploads/{csv_upload_id}/test-codes/
```

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `assessment_id`: Filter by specific assessment
- `is_used`: Filter by usage status [true, false]

**Response**:
```json
{
  "csv_upload": {
    "id": 1,
    "file_name": "students_batch_1.csv",
    "uploaded_by": "admin",
    "uploaded_at": "2025-09-06T10:30:00Z"
  },
  "total_codes": 50,
  "test_codes": [...]
}
```

---

## Communication Endpoints

### 1. Send Bulk Email
```http
POST /api/v1/sendEmail/
```

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "csv_upload_id": 1,
  "subject": "Assessment Invitation - Full Stack Development Test",
  "content": "Dear {{student_name}},\n\nYou have been invited to take the Full Stack Development Assessment.\n\nYour test code: {{test_code}}\nAssessment link: {{assessment_link}}\n\nBest regards,\nAssessment Team",
  "content_type": "text"
}
```

**Content Types**:
- `"text"`: Plain text email
- `"html"`: HTML formatted email

**Response**:
```json
{
  "message": "Email sending completed",
  "csv_upload_id": 1,
  "total_students": 50,
  "successful_sends": 48,
  "failed_sends": 2,
  "results": [
    {
      "student_email": "john@example.com",
      "student_name": "John Doe",
      "status": "success",
      "error_message": ""
    },
    {
      "student_email": "invalid@domain",
      "student_name": "Invalid User",
      "status": "failed",
      "error_message": "Invalid email address"
    }
  ]
}
```

---

## File Management Endpoints

### 1. Generate Presigned URL for File Upload
```http
POST /api/v1/upload/
```

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "assessment_id": 1,
  "filename": "reference-document.pdf"
}
```

**Response**:
```json
{
  "message": "Presigned URL generated successfully",
  "presigned_url": "https://s3.amazonaws.com/bucket/path/file.pdf?...",
  "expires_at": "2025-09-06T11:30:00Z",
  "expires_in_seconds": 3600,
  "assessment_file_id": 1,
  "s3_path": "assessments/1/reference-document.pdf",
  "upload_instructions": {
    "method": "PUT",
    "url": "https://s3.amazonaws.com/bucket/path/file.pdf?...",
    "headers": {
      "Content-Type": "application/octet-stream"
    }
  }
}
```

### 2. Check File Upload Status
```http
POST /api/v1/fileStatus/
```

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "assessment_id": 1,
  "filename": "reference-document.pdf"
}
```

**Response**:
```json
{
  "assessment_id": 1,
  "filename": "reference-document.pdf",
  "upload_status": "uploaded",
  "file_size": 1048576,
  "file_size_mb": 1.0,
  "s3_url": "https://s3.amazonaws.com/bucket/path/file.pdf",
  "created_at": "2025-09-06T10:30:00Z"
}
```

**Upload Statuses**:
- `"pending"`: File record created, awaiting upload
- `"uploaded"`: File successfully uploaded to S3
- `"failed"`: Upload failed

### 3. List Assessment Files
```http
GET /api/v1/files/{assessment_id}/
```

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "assessment_id": 1,
  "assessment_title": "Full Stack Development Assessment",
  "total_files": 3,
  "files": [
    {
      "id": 1,
      "filename": "reference-document.pdf",
      "file_size": 1048576,
      "file_size_mb": 1.0,
      "upload_status": "uploaded",
      "s3_full_url": "https://s3.amazonaws.com/bucket/path/file.pdf",
      "created_at": "2025-09-06T10:30:00Z",
      "updated_at": "2025-09-06T10:35:00Z"
    }
  ]
}
```

---

## User Management Endpoints

### 1. Create User (Admin Only)
```http
POST /api/v1/users/
```

**Headers**: `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "email": "manager@example.com",
  "password": "securepassword123",
  "role": "assessment_manager"
}
```

**Roles**:
- `"admin"`: Full system access
- `"assessment_manager"`: Can create and manage assessments
- `"proctor"`: Can monitor assessments

**Response**:
```json
{
  "status": "success",
  "message": "User created successfully",
  "data": {
    "email": "manager@example.com",
    "role": "assessment_manager"
  }
}
```

### 2. Get Users (Admin Only)
```http
GET /api/v1/users/
```

**Headers**: `Authorization: Bearer <token>`

**Query Parameters**:
- `role`: Filter by role ["assessment_manager", "proctor"]

**Response**:
```json
[
  {
    "id": 1,
    "email": "manager@example.com",
    "role": "assessment_manager",
    "phone_number": null,
    "created_at": "2025-09-06T10:30:00Z"
  }
]
```

---

## Reports Endpoints

### 1. Generate Student Report
```http
POST /api/v1/reports/student/
```

**Headers**: `Authorization: Bearer <token>`

**Request Body** (Option 1 - By Report ID):
```json
{
  "report_id": "RPT123456"
}
```

**Request Body** (Option 2 - By Assessment and Candidate):
```json
{
  "assessment_id": 1,
  "candidate_email": "student@example.com"
}
```

**Response**:
```json
{
  "message": "Student report generated successfully",
  "report": {
    "report_id": "RPT123456",
    "candidate_name": "John Doe",
    "candidate_email": "john@example.com",
    "assessment_title": "Full Stack Development Assessment",
    "total_marks": 100,
    "obtained_marks": 85,
    "percentage": 85.0,
    "status": "passed",
    "sections": [
      {
        "section_name": "Aptitude",
        "obtained_marks": 18,
        "total_marks": 20,
        "attempted_questions": 5,
        "correct_answers": 4
      }
    ]
  }
}
```

---

## Error Responses

### Common Error Format
```json
{
  "error": "Error message",
  "details": "Detailed error information"
}
```

### HTTP Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (missing/invalid token)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `500`: Internal Server Error

### Common Validation Errors

**Assessment Creation**:
```json
{
  "error": "Validation failed",
  "details": {
    "questions": {
      "0": "question_text references $3 but attachments length is 2. Valid range is $1..$2."
    }
  }
}
```

**File Upload**:
```json
{
  "error": "Invalid data",
  "details": {
    "assessment_id": ["Assessment not found."],
    "filename": ["File with this name already exists for this assessment."]
  }
}
```

---

## Notes

### Question Reference System
- Use `$1`, `$2`, etc. in question text to reference attachments
- References are 1-indexed and must not exceed attachments array length
- Example: "Refer to diagram $1 for the circuit layout"

### Assessment Publishing Rules
- Assessments must have sections and questions before publishing
- Published assessments cannot have their questions modified
- Published assessments cannot be deleted

### Test Code System
- Each student gets a unique test code per assessment
- Universal codes are generated for assessments when first assigned
- Test codes track usage status and timestamps

### File Upload Process
1. Generate presigned URL with `POST /api/v1/upload/`
2. Upload file directly to S3 using the presigned URL
3. Check upload status with `POST /api/v1/fileStatus/`
4. Files are automatically linked to assessments

### Pagination
- Most list endpoints support pagination
- Use `page` and `page_size` query parameters
- Maximum page size is 100 items

---

*This documentation covers all assessment and student management endpoints as of September 6, 2025.*
