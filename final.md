# PN Academy API - Complete Testing Guide

**Base URL**: `http://localhost:8000/api/v1/`  
**Headers for authenticated requests:**
```
Content-Type: application/json
Authorization: Bearer <your_access_token>
```

---

## 1. Authentication Routes

### 1.1 User Registration
```http
POST /api/v1/register/
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "admin@pnacademy.com",
  "password": "securepassword123"
}
```

**Expected Success Response (201):**
```json
{
  "id": 1,
  "email": "admin@pnacademy.com",
  "role": "assessment_manager",
  "created_at": "2025-09-18T10:00:00Z",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 1.2 User Login
```http
POST /api/v1/login/
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "admin@pnacademy.com",
  "password": "securepassword123"
}
```

**Expected Success Response (201):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 1.3 Reset Password
```http
POST /api/v1/reset-password/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "new_password": "newsecurepassword456"
}
```

**Expected Success Response (200):**
```json
{
  "message": "Password updated successfully"
}
```

---

## 2. User Management Routes

### 2.1 Create User (Admin Only)
```http
POST /api/v1/users/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "manager@pnacademy.com",
  "password": "managerpass123",
  "role": "assessment_manager"
}
```

**Expected Success Response (201):**
```json
{
  "status": "success",
  "message": "User created successfully",
  "data": {
    "id": 2,
    "email": "manager@pnacademy.com",
    "role": "assessment_manager",
    "created_at": "2025-09-18T10:00:00Z"
  }
}
```

### 2.2 Get All Users
```http
GET /api/v1/users/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "email": "admin@pnacademy.com",
      "role": "assessment_manager",
      "created_at": "2025-09-18T10:00:00Z"
    },
    {
      "id": 2,
      "email": "manager@pnacademy.com",
      "role": "assessment_manager",
      "created_at": "2025-09-18T10:00:00Z"
    }
  ]
}
```

### 2.3 Get User by ID
```http
GET /api/v1/users/{id}/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "id": 1,
  "email": "admin@pnacademy.com",
  "role": "assessment_manager",
  "created_at": "2025-09-18T10:00:00Z",
  "updated_at": "2025-09-18T10:00:00Z"
}
```

### 2.4 Update User
```http
PUT /api/v1/users/{id}/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "updated@pnacademy.com",
  "role": "proctor"
}
```

**Expected Success Response (200):**
```json
{
  "id": 1,
  "email": "updated@pnacademy.com",
  "role": "proctor",
  "updated_at": "2025-09-18T10:30:00Z"
}
```

### 2.5 Partial Update User
```http
PATCH /api/v1/users/{id}/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "role": "admin"
}
```

**Expected Success Response (200):**
```json
{
  "id": 1,
  "email": "admin@pnacademy.com",
  "role": "admin",
  "updated_at": "2025-09-18T10:30:00Z"
}
```

### 2.6 Delete User
```http
DELETE /api/v1/users/{id}/
Authorization: Bearer <token>
```

**Expected Success Response (204):**
```
No Content
```

---

## 3. Assessment Management Routes

### 3.1 Create Assessment (Main Route)
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
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
    }
  ]
}
```

**Expected Success Response (201):**
```json
{
  "message": "Assessment created successfully",
  "assessment_id": 1,
  "data": {
    "id": 1,
    "title": "Full Stack Developer Assessment",
    "assessment_type": "mix",
    "passing_marks": 120,
    "is_published": false,
    "is_proctored": true,
    "created_at": "2025-09-18T10:00:00Z",
    "sections": [
      {
        "id": 1,
        "name": "Frontend Development",
        "description": "HTML, CSS, JavaScript, React.js, and modern frontend frameworks",
        "questions_count": 2
      }
    ]
  }
}
```

### 3.2 Create Assessment (Alternative Route)
```http
POST /api/v1/assessment
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:** (Same as above)

**Expected Success Response (201):** (Same as above)

### 3.3 Get All Assessments
```http
GET /api/v1/assessments/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Full Stack Developer Assessment",
      "assessment_type": "mix",
      "passing_marks": 120,
      "is_published": false,
      "is_proctored": true,
      "created_at": "2025-09-18T10:00:00Z",
      "sections_count": 3,
      "total_questions": 12
    }
  ]
}
```

### 3.4 Get All Assessments (Alternative Route)
```http
GET /api/v1/assessment
Authorization: Bearer <token>
```

**Expected Success Response (200):** (Same as above)

### 3.5 Get Assessments with Filtering
```http
GET /api/v1/assessments/?assessment_type=mix&is_published=true&search=Full&page=1
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Full Stack Developer Assessment",
      "assessment_type": "mix",
      "is_published": true,
      "matches_search": true
    }
  ]
}
```

### 3.6 Get Assessment by ID
```http
GET /api/v1/assessments/{id}/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "message": "Assessment retrieved successfully",
  "data": {
    "id": 1,
    "title": "Full Stack Developer Assessment",
    "assessment_type": "mix",
    "description": "Comprehensive assessment covering frontend, backend, and system design",
    "passing_marks": 120,
    "is_published": false,
    "is_proctored": true,
    "start_time": "2025-12-01T09:00:00Z",
    "end_time": "2025-12-01T13:00:00Z",
    "sections": [
      {
        "id": 1,
        "name": "Frontend Development",
        "description": "HTML, CSS, JavaScript, React.js, and modern frontend frameworks",
        "questions": [
          {
            "id": 1,
            "question_text": "According to the technical specifications in $1, which CSS framework is recommended?",
            "question_type": "non-coding",
            "options": ["Bootstrap", "Tailwind CSS", "Bulma", "Foundation"],
            "correct_option_index": 1,
            "positive_marks": 20,
            "negative_marks": -5,
            "time_limit": 120
          }
        ]
      }
    ]
  }
}
```

### 3.7 Get Assessment by ID (Alternative Route)
```http
GET /api/v1/assessment/{id}
Authorization: Bearer <token>
```

**Expected Success Response (200):** (Same as above)

### 3.8 Get Assessment with Specific Set
```http
GET /api/v1/assessments/{id}/?set_number=1
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "message": "Assessment retrieved successfully",
  "data": {
    "id": 1,
    "title": "Full Stack Developer Assessment",
    "sections": [
      {
        "id": 1,
        "name": "Frontend Development",
        "questions": [
          {
            "id": 1,
            "set_number": 1,
            "question_text": "According to the technical specifications in $1, which CSS framework is recommended?",
            "question_type": "non-coding"
          }
        ]
      }
    ]
  }
}
```

### 3.9 Update Assessment
```http
PUT /api/v1/assessments/{id}/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "assessment_name": "Updated Full Stack Assessment",
  "assessment_type": "mix",
  "assessment_description": "Updated comprehensive assessment with new features",
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
  "is_published": false
}
```

**Expected Success Response (200):**
```json
{
  "message": "Assessment updated successfully",
  "data": {
    "id": 1,
    "title": "Updated Full Stack Assessment",
    "assessment_type": "mix",
    "passing_marks": 140,
    "is_published": false,
    "updated_at": "2025-09-18T11:00:00Z"
  }
}
```

### 3.10 Update Assessment (Alternative Route)
```http
PUT /api/v1/assessment/{id}
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:** (Same as above)
**Expected Success Response (200):** (Same as above)

### 3.11 Partial Update Assessment
```http
PATCH /api/v1/assessments/{id}/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "assessment_name": "Updated Assessment Name",
  "passing_marks": 150,
  "is_published": true
}
```

**Expected Success Response (200):**
```json
{
  "message": "Assessment updated successfully",
  "data": {
    "id": 1,
    "title": "Updated Assessment Name",
    "passing_marks": 150,
    "is_published": true,
    "updated_at": "2025-09-18T11:30:00Z"
  }
}
```

### 3.12 Partial Update Assessment (Alternative Route)
```http
PATCH /api/v1/assessment/{id}
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "is_proctored": true,
  "is_electron_only": true
}
```

**Expected Success Response (200):** (Similar to above)

### 3.13 Delete Assessment
```http
DELETE /api/v1/assessments/{id}/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "message": "Assessment \"Full Stack Developer Assessment\" deleted successfully"
}
```

### 3.14 Delete Assessment (Alternative Route)
```http
DELETE /api/v1/assessment/{id}
Authorization: Bearer <token>
```

**Expected Success Response (200):** (Same as above)

### 3.15 Publish Assessment
```http
POST /api/v1/assessments/{id}/publish/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "message": "Assessment published successfully",
  "data": {
    "id": 1,
    "title": "Full Stack Developer Assessment",
    "is_published": true,
    "updated_at": "2025-09-18T12:00:00Z"
  }
}
```

### 3.16 Unpublish Assessment
```http
POST /api/v1/assessments/{id}/unpublish/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "message": "Assessment unpublished successfully",
  "data": {
    "id": 1,
    "title": "Full Stack Developer Assessment",
    "is_published": false,
    "updated_at": "2025-09-18T12:30:00Z"
  }
}
```

### 3.17 Duplicate Assessment
```http
POST /api/v1/assessments/{id}/duplicate/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "message": "Assessment duplicated successfully",
  "data": {
    "id": 2,
    "title": "Copy of Full Stack Developer Assessment",
    "assessment_type": "mix",
    "is_published": false,
    "created_at": "2025-09-18T13:00:00Z",
    "original_assessment_id": 1
  }
}
```

### 3.18 Get Assessment Statistics
```http
GET /api/v1/assessments/statistics/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "message": "Statistics retrieved successfully",
  "data": {
    "total_assessments": 5,
    "published_assessments": 3,
    "draft_assessments": 2,
    "active_assessments": 4,
    "by_type": {
      "coding": 2,
      "non-coding": 1,
      "mix": 2
    },
    "proctored_assessments": 3,
    "recent_assessments": 2
  }
}
```

### 3.19 Get All Assessments (Admin View)
```http
GET /api/v1/assessments/all_assessments/
Authorization: Bearer <admin_token>
```

**Expected Success Response (200):**
```json
{
  "message": "All assessments retrieved successfully",
  "total_count": 10,
  "data": [
    {
      "id": 1,
      "title": "Full Stack Developer Assessment",
      "created_by": {
        "id": 1,
        "email": "admin@pnacademy.com"
      },
      "assessment_type": "mix",
      "is_published": true,
      "created_at": "2025-09-18T10:00:00Z"
    }
  ]
}
```

---

## 4. Student Management Routes

### 4.1 Upload Students CSV
```http
POST /api/v1/uploadStudents/
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Form Data:**
- `file`: (CSV file with headers: name, email)

**Sample CSV Content:**
```csv
name,email
John Doe,john.doe@example.com
Jane Smith,jane.smith@example.com
Alice Johnson,alice.johnson@example.com
```

**Expected Success Response (201):**
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
      "email": "john.doe@example.com",
      "csv_upload_id": 1,
      "created_at": "2025-09-18T14:00:00Z"
    },
    {
      "id": 2,
      "full_name": "Jane Smith",
      "email": "jane.smith@example.com",
      "csv_upload_id": 1,
      "created_at": "2025-09-18T14:00:00Z"
    },
    {
      "id": 3,
      "full_name": "Alice Johnson",
      "email": "alice.johnson@example.com",
      "csv_upload_id": 1,
      "created_at": "2025-09-18T14:00:00Z"
    }
  ],
  "skipped_students": [],
  "errors": []
}
```

### 4.2 Get All Students
```http
GET /api/v1/students/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "csv_upload": {
        "id": 1,
        "file_name": "students.csv",
        "uploaded_at": "2025-09-18T14:00:00Z"
      },
      "created_at": "2025-09-18T14:00:00Z"
    },
    {
      "id": 2,
      "full_name": "Jane Smith",
      "email": "jane.smith@example.com",
      "csv_upload": {
        "id": 1,
        "file_name": "students.csv",
        "uploaded_at": "2025-09-18T14:00:00Z"
      },
      "created_at": "2025-09-18T14:00:00Z"
    }
  ]
}
```

### 4.3 Get Student by ID
```http
GET /api/v1/students/{id}/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "id": 1,
  "full_name": "John Doe",
  "email": "john.doe@example.com",
  "csv_upload": {
    "id": 1,
    "file_name": "students.csv",
    "uploaded_by": "admin@pnacademy.com",
    "uploaded_at": "2025-09-18T14:00:00Z"
  },
  "created_at": "2025-09-18T14:00:00Z",
  "updated_at": "2025-09-18T14:00:00Z"
}
```

### 4.4 Update Student
```http
PUT /api/v1/students/{id}/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "full_name": "Updated John Doe",
  "email": "updated.john@example.com"
}
```

**Expected Success Response (200):**
```json
{
  "id": 1,
  "full_name": "Updated John Doe",
  "email": "updated.john@example.com",
  "updated_at": "2025-09-18T15:00:00Z"
}
```

### 4.5 Partial Update Student
```http
PATCH /api/v1/students/{id}/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "full_name": "John D. Smith"
}
```

**Expected Success Response (200):**
```json
{
  "id": 1,
  "full_name": "John D. Smith",
  "email": "john.doe@example.com",
  "updated_at": "2025-09-18T15:30:00Z"
}
```

### 4.6 Delete Student
```http
DELETE /api/v1/students/{id}/
Authorization: Bearer <token>
```

**Expected Success Response (204):**
```
No Content
```

### 4.7 Get CSV Upload History
```http
GET /api/v1/students-list/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
[
  {
    "id": 1,
    "file_name": "students.csv",
    "uploaded_by": {
      "id": 1,
      "email": "admin@pnacademy.com"
    },
    "uploaded_at": "2025-09-18T14:00:00Z",
    "total_records": 3,
    "processed_records": 3,
    "status": "completed",
    "errors": null
  }
]
```

### 4.8 Get CSV Upload by ID
```http
GET /api/v1/students-list/{id}/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "id": 1,
  "file_name": "students.csv",
  "uploaded_by": {
    "id": 1,
    "email": "admin@pnacademy.com"
  },
  "uploaded_at": "2025-09-18T14:00:00Z",
  "total_records": 3,
  "processed_records": 3,
  "status": "completed",
  "errors": null,
  "students": [
    {
      "id": 1,
      "full_name": "John Doe",
      "email": "john.doe@example.com"
    },
    {
      "id": 2,
      "full_name": "Jane Smith",
      "email": "jane.smith@example.com"
    }
  ]
}
```

---

## 5. Assessment Assignment Routes

### 5.1 Assign Assessment to CSV Upload
```http
POST /api/v1/assign-assessment/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "assessment_id": 1,
  "csv_upload_id": 1
}
```

**Expected Success Response (200):**
```json
{
  "message": "Assessment assigned successfully to all students",
  "assessment": {
    "id": 1,
    "title": "Full Stack Developer Assessment"
  },
  "csv_upload": {
    "id": 1,
    "file_name": "students.csv",
    "total_students": 3
  },
  "test_codes_generated": 3,
  "test_codes": [
    {
      "student_id": 1,
      "student_email": "john.doe@example.com",
      "test_code": "TC-ABC123",
      "is_active": true
    },
    {
      "student_id": 2,
      "student_email": "jane.smith@example.com",
      "test_code": "TC-DEF456",
      "is_active": true
    },
    {
      "student_id": 3,
      "student_email": "alice.johnson@example.com",
      "test_code": "TC-GHI789",
      "is_active": true
    }
  ]
}
```

### 5.2 Get Test Codes for Assessment
```http
GET /api/v1/assessments/{assessment_id}/test-codes/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "assessment": {
    "id": 1,
    "title": "Full Stack Developer Assessment",
    "universal_code": "ASSESS-001"
  },
  "total_codes": 3,
  "test_codes": [
    {
      "id": 1,
      "code": "TC-ABC123",
      "student": {
        "id": 1,
        "full_name": "John Doe",
        "email": "john.doe@example.com"
      },
      "is_used": false,
      "is_active": true,
      "created_at": "2025-09-18T16:00:00Z"
    },
    {
      "id": 2,
      "code": "TC-DEF456",
      "student": {
        "id": 2,
        "full_name": "Jane Smith",
        "email": "jane.smith@example.com"
      },
      "is_used": false,
      "is_active": true,
      "created_at": "2025-09-18T16:00:00Z"
    }
  ]
}
```

### 5.3 Get Test Codes for Assessment with Filters
```http
GET /api/v1/assessments/{assessment_id}/test-codes/?csv_upload_id=1&is_used=false
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "assessment": {
    "id": 1,
    "title": "Full Stack Developer Assessment"
  },
  "total_codes": 2,
  "test_codes": [
    {
      "id": 1,
      "code": "TC-ABC123",
      "student": {
        "id": 1,
        "full_name": "John Doe",
        "email": "john.doe@example.com"
      },
      "is_used": false,
      "is_active": true,
      "csv_upload_id": 1
    }
  ]
}
```

### 5.4 Get Test Codes for CSV Upload
```http
GET /api/v1/csv-uploads/{csv_upload_id}/test-codes/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "csv_upload": {
    "id": 1,
    "file_name": "students.csv",
    "uploaded_at": "2025-09-18T14:00:00Z"
  },
  "total_codes": 3,
  "test_codes": [
    {
      "id": 1,
      "code": "TC-ABC123",
      "student": {
        "id": 1,
        "full_name": "John Doe",
        "email": "john.doe@example.com"
      },
      "assessment": {
        "id": 1,
        "title": "Full Stack Developer Assessment"
      },
      "is_used": false,
      "is_active": true
    }
  ]
}
```

### 5.5 Get Test Codes for CSV Upload with Filters
```http
GET /api/v1/csv-uploads/{csv_upload_id}/test-codes/?assessment_id=1&is_used=true
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "csv_upload": {
    "id": 1,
    "file_name": "students.csv"
  },
  "total_codes": 1,
  "test_codes": [
    {
      "id": 1,
      "code": "TC-ABC123",
      "student": {
        "id": 1,
        "full_name": "John Doe",
        "email": "john.doe@example.com"
      },
      "assessment": {
        "id": 1,
        "title": "Full Stack Developer Assessment"
      },
      "is_used": true,
      "used_at": "2025-09-18T17:00:00Z"
    }
  ]
}
```

---

## 6. Communication Routes

### 6.1 Send Bulk Email (Text)
```http
POST /api/v1/sendEmail/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "csv_upload_id": 1,
  "subject": "Assessment Invitation - Full Stack Developer Test",
  "content": "Dear {{student_name}},\n\nYou have been invited to take the Full Stack Developer Assessment.\n\nYour unique test code: {{test_code}}\nAssessment link: {{assessment_link}}\n\nPlease complete the assessment before the deadline.\n\nBest regards,\nAssessment Team",
  "content_type": "text"
}
```

**Expected Success Response (200):**
```json
{
  "message": "Email sending completed",
  "csv_upload_id": 1,
  "total_students": 3,
  "successful_sends": 3,
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
    },
    {
      "student_email": "alice.johnson@example.com",
      "student_name": "Alice Johnson",
      "status": "success",
      "error_message": ""
    }
  ]
}
```

### 6.2 Send Bulk Email (HTML)
```http
POST /api/v1/sendEmail/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "csv_upload_id": 1,
  "subject": "Assessment Invitation - HTML Format",
  "content": "<html><body><h2>Assessment Invitation</h2><p>Dear <strong>{{student_name}}</strong>,</p><p>You have been invited to take the assessment.</p><p><strong>Test Code:</strong> {{test_code}}</p><p><a href='{{assessment_link}}'>Start Assessment</a></p></body></html>",
  "content_type": "html"
}
```

**Expected Success Response (200):** (Similar to text email response)

---

## 7. File Management Routes

### 7.1 Generate Presigned URL for File Upload
```http
POST /api/v1/upload/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "assessment_id": 1,
  "filename": "technical-specifications.pdf"
}
```

**Expected Success Response (201):**
```json
{
  "message": "Presigned URL generated successfully",
  "presigned_url": "https://s3.amazonaws.com/bucket/assessments/1/technical-specifications.pdf?...",
  "s3_key": "assessments/1/technical-specifications.pdf",
  "expires_in_seconds": 3600,
  "assessment_file_id": 1,
  "upload_instructions": {
    "method": "PUT",
    "url": "https://s3.amazonaws.com/bucket/assessments/1/technical-specifications.pdf?...",
    "headers": {
      "Content-Type": "application/pdf"
    }
  }
}
```

### 7.2 Check File Upload Status
```http
POST /api/v1/fileStatus/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "assessment_id": 1,
  "filename": "technical-specifications.pdf"
}
```

**Expected Success Response (200):**
```json
{
  "assessment_id": 1,
  "filename": "technical-specifications.pdf",
  "upload_status": "uploaded",
  "file_exists": true,
  "file_size": 2048576,
  "s3_key": "assessments/1/technical-specifications.pdf",
  "uploaded_at": "2025-09-18T18:00:00Z",
  "presigned_url_expired": true
}
```

### 7.3 List Assessment Files
```http
GET /api/v1/files/{assessment_id}
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "assessment_id": 1,
  "assessment_title": "Full Stack Developer Assessment",
  "files": [
    {
      "id": 1,
      "filename": "technical-specifications.pdf",
      "s3_key": "assessments/1/technical-specifications.pdf",
      "upload_status": "uploaded",
      "file_size": 2048576,
      "content_type": "application/pdf",
      "uploaded_at": "2025-09-18T18:00:00Z"
    },
    {
      "id": 2,
      "filename": "coding-standards.pdf",
      "s3_key": "assessments/1/coding-standards.pdf",
      "upload_status": "pending",
      "file_size": null,
      "content_type": "application/pdf",
      "uploaded_at": null
    }
  ],
  "total_files": 2,
  "uploaded_files": 1,
  "pending_files": 1
}
```

---

## 8. Code Execution Routes

### 8.1 Run Code
```http
POST /api/v1/runCode/
Content-Type: application/json
```

**Request Body:**
```json
{
  "language": "python3",
  "code": "print('Hello, World!')\nprint(2 + 3)",
  "input": ""
}
```

**Expected Success Response (200):**
```json
{
  "success": true,
  "output": "Hello, World!\n5\n",
  "error": "",
  "execution_time": "0.12",
  "memory_used": "9216",
  "language": "python3",
  "status": "success"
}
```

### 8.2 Submit Code for Validation
```http
POST /api/v1/submitCode/
Content-Type: application/json
```

**Request Body:**
```json
{
  "language": "python3",
  "code": "def add_numbers(a, b):\n    return a + b\n\nprint(add_numbers(2, 3))",
  "test_cases": {
    "examples": [
      {"input": "2 3", "expected_output": "5"},
      {"input": "10 15", "expected_output": "25"}
    ],
    "hidden": [
      {"input": "0 0", "expected_output": "0"},
      {"input": "-5 5", "expected_output": "0"}
    ]
  }
}
```

**Expected Success Response (200):**
```json
{
  "success": true,
  "overall_result": "passed",
  "test_results": {
    "examples": [
      {
        "test_case": 1,
        "input": "2 3",
        "expected_output": "5",
        "actual_output": "5\n",
        "status": "passed",
        "execution_time": "0.08"
      },
      {
        "test_case": 2,
        "input": "10 15",
        "expected_output": "25",
        "actual_output": "25\n",
        "status": "passed",
        "execution_time": "0.07"
      }
    ],
    "hidden": [
      {
        "test_case": 1,
        "status": "passed",
        "execution_time": "0.06"
      },
      {
        "test_case": 2,
        "status": "passed",
        "execution_time": "0.08"
      }
    ]
  },
  "summary": {
    "total_tests": 4,
    "passed_tests": 4,
    "failed_tests": 0,
    "success_rate": "100%"
  }
}
```

---

## 9. Proctoring Routes

### 9.1 Upload Student Image for Proctoring
```http
POST /api/v1/uploadStudentImage/
Content-Type: multipart/form-data
```

**Form Data:**
- `token`: JWT token containing test code
- `image`: Image file for identity verification

**Expected Success Response (201):**
```json
{
  "success": true,
  "message": "Image Sent Successfully!"
}
```

### 9.2 Get All Proctoring Results
```http
GET /api/v1/proctoring-results/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "session_id": "std01",
      "flags": [
        "MULTIPLE_FACES_DETECTED",
        "PROHIBITED_OBJECT_BOOK"
      ],
      "risk_score": 90,
      "timestamp": "2025-09-18T13:44:04.252893Z",
      "s3_key": "proctoring/std01.jpg"
    },
    {
      "session_id": "std02",
      "flags": [],
      "risk_score": 10,
      "timestamp": "2025-09-18T14:15:20.123456Z",
      "s3_key": "proctoring/std02.jpg"
    }
  ],
  "count": 2
}
```

### 9.3 Get Proctoring Results with Filters
```http
GET /api/v1/proctoring-results/?session_id=std01&min_risk_score=50&has_flags=true
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "session_id": "std01",
      "flags": [
        "MULTIPLE_FACES_DETECTED",
        "PROHIBITED_OBJECT_BOOK"
      ],
      "risk_score": 90,
      "timestamp": "2025-09-18T13:44:04.252893Z",
      "s3_key": "proctoring/std01.jpg"
    }
  ],
  "count": 1
}
```

### 9.4 Get Specific Proctoring Result
```http
GET /api/v1/proctoring-results/{session_id}/
Authorization: Bearer <token>
```

**Expected Success Response (200):**
```json
{
  "success": true,
  "data": {
    "session_id": "std01",
    "flags": [
      "MULTIPLE_FACES_DETECTED",
      "PROHIBITED_OBJECT_BOOK"
    ],
    "risk_score": 90,
    "timestamp": "2025-09-18T13:44:04.252893Z",
    "s3_key": "proctoring/std01.jpg",
    "rekognition_face_response": {
      "FaceDetails": [
        {
          "BoundingBox": {
            "Width": 0.4,
            "Height": 0.6,
            "Left": 0.3,
            "Top": 0.2
          },
          "Confidence": 95.5
        }
      ]
    },
    "rekognition_label_response": {
      "Labels": [
        {
          "Name": "Book",
          "Confidence": 87.3,
          "Categories": ["Education"]
        }
      ]
    }
  }
}
```

---

## 10. Report Generation Routes

### 10.1 Generate Student Report
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
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

**Expected Success Response (201):**
```json
{
  "message": "Student report generated successfully",
  "report_id": 1,
  "participant_type": "student",
  "assessment": {
    "id": 1,
    "title": "Full Stack Developer Assessment",
    "total_marks": 130,
    "passing_marks": 120
  },
  "participant": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "test_session": {
    "started_at": "2025-12-01T09:00:00Z",
    "ended_at": "2025-12-01T12:30:00Z",
    "submitted_at": "2025-12-01T12:25:00Z",
    "duration_minutes": 210,
    "time_taken_minutes": 205,
    "window_switch_count": 2,
    "is_cheating": false,
    "status": "submitted"
  },
  "performance": {
    "total_marks": 130,
    "obtained_marks": 105,
    "percentage": 80.77,
    "result": "FAIL",
    "passing_marks": 120,
    "deficit": 15
  },
  "section_wise_performance": [
    {
      "section_id": 1,
      "section_name": "Frontend Development",
      "total_marks": 55,
      "obtained_marks": 55,
      "percentage": 100.0,
      "time_spent_minutes": 60,
      "questions_attempted": 2,
      "total_questions": 2,
      "attempt_rate": 100.0
    },
    {
      "section_id": 2,
      "section_name": "Backend Development",
      "total_marks": 55,
      "obtained_marks": 40,
      "percentage": 72.73,
      "time_spent_minutes": 60,
      "questions_attempted": 2,
      "total_questions": 2,
      "attempt_rate": 100.0
    },
    {
      "section_id": 3,
      "section_name": "System Design",
      "total_marks": 55,
      "obtained_marks": 10,
      "percentage": 18.18,
      "time_spent_minutes": 40,
      "questions_attempted": 1,
      "total_questions": 2,
      "attempt_rate": 50.0
    }
  ],
  "insights": {
    "strengths": [
      "Perfect performance in Frontend Development",
      "Consistent high performance in coding questions"
    ],
    "weaknesses": [
      "Poor performance in System Design section",
      "Low attempt rate in System Design (50%)"
    ],
    "recommendations": [
      "Focus more on System Design concepts",
      "Practice time management for complex sections",
      "Review caching and distributed systems patterns"
    ]
  },
  "ai_analysis": {
    "available": true,
    "summary": "Strong frontend skills with room for improvement in system design",
    "detailed_feedback": "The candidate demonstrates excellent frontend development skills..."
  }
}
```

### 10.2 Generate Report by Candidate Email
```http
POST /api/v1/reports/student
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
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

**Expected Success Response (201):** (Similar structure but for candidate instead of student)

---

## 11. Home Route

### 11.1 Home Page
```http
GET /
```

**Expected Success Response (200):**
```
Django is working!
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "Invalid data provided",
  "details": {
    "field_name": ["This field is required."]
  }
}
```

### 401 Unauthorized
```json
{
  "error": "Authentication credentials were not provided"
}
```

### 403 Forbidden
```json
{
  "error": "You do not have permission to perform this action"
}
```

### 404 Not Found
```json
{
  "error": "Assessment not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "details": "Specific error message"
}
```

---

## Testing Notes

1. **Authentication**: Most endpoints require a valid JWT token in the Authorization header
2. **File Uploads**: Use `multipart/form-data` content type for file uploads
3. **Pagination**: List endpoints support pagination with `page` and `page_size` parameters
4. **Filtering**: Many list endpoints support filtering via query parameters
5. **CSRF**: CSRF protection is disabled for API endpoints
6. **Permissions**: Different user roles have different access levels (admin, assessment_manager, proctor)

## Rate Limiting

Some endpoints may have rate limiting applied:
- Email sending: Limited to prevent spam
- File uploads: Limited by file size and frequency
- Code execution: Limited by execution time and frequency

## Data Validation

All endpoints perform strict data validation:
- Email formats are validated
- Required fields are enforced
- Data types are checked
- Business logic constraints are applied (e.g., assessment publishing rules)

This completes the comprehensive testing guide for all PN Academy API routes.
