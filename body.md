# API Request Body Documentation

Complete guide for all API endpoints with request body formats, headers, and authentication requirements.

**Base URL:** `http://127.0.0.1:8000/api/` or `https://your-domain.com/api/`

**Date:** October 24, 2025

---

## ⚠️ CRITICAL: Section Marking Safety Rules

**READ THIS FIRST** before creating assessments. The backend enforces strict validation to ensure fair testing:

### 🔒 Automatic Validation Rules

When creating assessments with multiple sets, the system automatically validates:

| Rule | Description | Impact |
|------|-------------|--------|
| **1. Equal Section Marks** | All sections within the same set must have equal net scoring potential | Request will be **REJECTED** if sections have different total marks |
| **2. Same Section Structure** | All sets must have identical section IDs | Request will be **REJECTED** if sets have different sections |
| **3. Cross-Set Consistency** | Each section must have identical marks across all sets | Request will be **REJECTED** if same section has different marks in different sets |

### 📐 Net Scoring Potential Formula

```
Net Scoring Potential = SUM(positive_marks + negative_marks) for all questions
```

**Example Calculation:**
```
Section 1 Questions:
- Q1: positive_marks=4, negative_marks=-1  → Net = 3
- Q2: positive_marks=4, negative_marks=-1  → Net = 3
- Q3: positive_marks=6, negative_marks=0   → Net = 6
Total Section Net Marks = 3 + 3 + 6 = 12 marks
```

### ✅ Quick Validation Checklist

Before sending assessment creation request, verify:

- [ ] All sections in Set 1 have the **same total net marks**
- [ ] All sections in Set 2 have the **same total net marks** (and same as Set 1)
- [ ] All sets have the **same section IDs** (e.g., if Set 1 has sections 1,2,3 then Set 2 must also have 1,2,3)
- [ ] Section 1 has the **same net marks** in all sets
- [ ] Section 2 has the **same net marks** in all sets (and so on...)

### 🚫 Common Mistakes

**❌ WRONG - Inconsistent section marks within a set:**
```json
{
  "questions": [
    {"set_number": 1, "section_id": 1, "positive_marks": 10, "negative_marks": 0},  // 10 marks
    {"set_number": 1, "section_id": 2, "positive_marks": 5, "negative_marks": 0}   // 5 marks ❌ Different!
  ]
}
```

**✅ CORRECT - Equal section marks:**
```json
{
  "questions": [
    {"set_number": 1, "section_id": 1, "positive_marks": 10, "negative_marks": 0},  // 10 marks
    {"set_number": 1, "section_id": 2, "positive_marks": 10, "negative_marks": 0}   // 10 marks ✅ Same!
  ]
}
```

**❌ WRONG - Same section has different marks across sets:**
```json
{
  "questions": [
    {"set_number": 1, "section_id": 1, "positive_marks": 10, "negative_marks": 0},  // Set 1: 10 marks
    {"set_number": 2, "section_id": 1, "positive_marks": 12, "negative_marks": 0}   // Set 2: 12 marks ❌ Different!
  ]
}
```

**✅ CORRECT - Same section has same marks across sets:**
```json
{
  "questions": [
    {"set_number": 1, "section_id": 1, "positive_marks": 10, "negative_marks": 0},  // Set 1: 10 marks
    {"set_number": 2, "section_id": 1, "positive_marks": 10, "negative_marks": 0}   // Set 2: 10 marks ✅ Same!
  ]
}
```

### 🔴 Error Response Example

If validation fails, you'll receive a detailed error:

```json
{
  "error": {
    "set_1_marks_consistency": "All sections in set 1 must have the same net scoring potential. Found different totals: Section 1: 20 net marks, Section 2: 30 net marks. Please ensure all sections in the same set have equal net scoring potential (positive_marks + negative_marks).",
    "section_1_cross_set_consistency": "Section 1 has inconsistent net scoring potential across sets. Set 1: 20 net marks, Set 2: 25 net marks. Each section must have the same net scoring potential in every set."
  }
}
```

### 💡 Why These Rules Exist

1. **Fairness**: Ensures all students face equivalent difficulty regardless of which set they receive
2. **Consistency**: Maintains uniform scoring across all test variants
3. **Validity**: Prevents accidental marking scheme errors that could invalidate results

---

> **⚡ TIP:** Use a spreadsheet to calculate section totals before creating the JSON to avoid validation errors!

---

## Table of Contents
1. [Authentication](#authentication)
2. [Assessment Management](#assessment-management)
3. [User Management](#user-management)
4. [Student Management](#student-management)
5. [File Management](#file-management)
6. [Code Execution](#code-execution)
7. [Reports & Analytics](#reports--analytics)
8. [Proctoring](#proctoring)
9. [Email](#email)

---

## Authentication

### 1. Register User
**Endpoint:** `POST /api/register/`  
**Permission:** Public (AllowAny)  
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (201):**
```json
{
  "email": "user@example.com",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 2. Login
**Endpoint:** `POST /api/login/`  
**Permission:** Public (AllowAny)  
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (201):**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 3. Reset Password
**Endpoint:** `POST /api/reset-password/`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Request Body:**
```json
{
  "new_password": "NewSecurePassword456!"
}
```

**Response (200):**
```json
{
  "message": "Password has been reset successfully"
}
```

---

## Assessment Management

### 4. Create Assessment
**Endpoint:** `POST /api/assessment`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Request Body:**
```json
{
  "assessment_name": "Python Programming Test",
  "assessment_description": "Comprehensive Python assessment covering basics to advanced topics",
  "assessment_type": "mix",
  "passing_marks": 40,
  "num_of_sets": 2,
  "section_names": ["Programming Basics", "Data Structures", "Algorithms"],
  "section_descriptions": [
    "Basic programming concepts and syntax",
    "Arrays, Linked Lists, Trees, and Graphs",
    "Sorting, searching, and problem-solving"
  ],
  "start_time": "2025-01-15T10:00:00Z",
  "end_time": "2025-01-15T12:00:00Z",
  "is_electron_only": false,
  "is_proctored": true,
  "is_published": false,
  "num_of_ai_generated_questions": 0,
  "attachments": [],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "What is the output of print(type([]))?",
      "options": [
        "<class 'list'>",
        "<class 'dict'>",
        "<class 'tuple'>",
        "<class 'set'>"
      ],
      "correct_option_index": 0,
      "positive_marks": 4,
      "negative_marks": -1,
      "time_limit": 60
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Write a function to reverse a string without using built-in methods.",
      "description": "Implement a function that takes a string and returns its reverse.",
      "constraints": [
        "1 <= length of string <= 1000",
        "String contains only ASCII characters"
      ],
      "positive_marks": 10,
      "negative_marks": 0,
      "time_limit": 900,
      "test_cases": {
        "examples": [
          {
            "input": "hello",
            "output": "olleh"
          },
          {
            "input": "python",
            "output": "nohtyp"
          }
        ],
        "hidden": [
          {
            "input": "OpenAI",
            "output": "IAnepO"
          },
          {
            "input": "algorithm",
            "output": "mhtirogla"
          }
        ]
      }
    }
  ]
}
```

**Important Notes:**
- Only **two question types** are supported: `"coding"` and `"non-coding"` (MCQ)
- **Subjective questions are NOT allowed**
- `section_id` is 1-based (matches the index in section_names + 1)
- `set_number` starts from 1
- `time_limit` is in seconds
- `assessment_type` can be: `"coding"`, `"non-coding"`, or `"mix"`
- For non-coding questions: provide `options` array and `correct_option_index`
- For coding questions: provide `test_cases` with `examples` and `hidden` test cases

**⚠️ SECTION MARKING SAFETY VALIDATIONS:**

The backend automatically validates the following to ensure fair assessment:

1. **Within-Set Section Consistency**: All sections within the same set must have equal net scoring potential
   - Net scoring potential = `positive_marks + negative_marks` for all questions in a section
   - Example: If Set 1 has 3 sections, each section must have the same total net marks (e.g., all 50 marks)
   
2. **Cross-Set Structure Consistency**: All sets must have the same section structure
   - If Set 1 has sections [1, 2, 3], Set 2 must also have sections [1, 2, 3]
   - You cannot add or remove sections in different sets
   
3. **Cross-Set Section Marks Consistency**: Each section must have identical net scoring potential across all sets
   - If Section 1 has 50 net marks in Set 1, it must have 50 net marks in Set 2 as well
   - This ensures all students get equivalent difficulty regardless of which set they receive

**Example of Valid Structure:**
```json
{
  "num_of_sets": 2,
  "questions": [
    // Set 1, Section 1: Total = 20 net marks
    {"set_number": 1, "section_id": 1, "positive_marks": 10, "negative_marks": -2},
    {"set_number": 1, "section_id": 1, "positive_marks": 10, "negative_marks": -2},
    
    // Set 1, Section 2: Total = 20 net marks (same as Section 1)
    {"set_number": 1, "section_id": 2, "positive_marks": 12, "negative_marks": -4},
    {"set_number": 1, "section_id": 2, "positive_marks": 10, "negative_marks": -2},
    
    // Set 2, Section 1: Total = 20 net marks (same as Set 1, Section 1)
    {"set_number": 2, "section_id": 1, "positive_marks": 10, "negative_marks": -2},
    {"set_number": 2, "section_id": 1, "positive_marks": 10, "negative_marks": -2},
    
    // Set 2, Section 2: Total = 20 net marks (same as Set 1, Section 2)
    {"set_number": 2, "section_id": 2, "positive_marks": 10, "negative_marks": -2},
    {"set_number": 2, "section_id": 2, "positive_marks": 12, "negative_marks": -4}
  ]
}
```

**Validation Error Examples:**

**Error 1: Within-Set Inconsistency**
```json
{
  "error": {
    "set_1_marks_consistency": "All sections in set 1 must have the same net scoring potential. Found different totals: Section 1: 20 net marks, Section 2: 30 net marks. Please ensure all sections in the same set have equal net scoring potential (positive_marks + negative_marks)."
  }
}
```

**Error 2: Missing Sections**
```json
{
  "error": {
    "set_2_structure_consistency": "Set 2 has different section structure than set 1. Missing sections: [3]. All sets must have the same section types/structure."
  }
}
```

**Error 3: Cross-Set Marks Inconsistency**
```json
{
  "error": {
    "section_1_cross_set_consistency": "Section 1 has inconsistent net scoring potential across sets. Set 1: 20 net marks, Set 2: 25 net marks. Each section must have the same net scoring potential (positive_marks + negative_marks) in every set."
  }
}
```

**Response (201):**
```json
{
  "id": 1,
  "assessment_name": "Python Programming Test",
  "assessment_type": "mix",
  "total_marks": 28,
  "duration": 16,
  "sections": [...]
}
```

---

### 5. Get All Assessments
**Endpoint:** `GET /api/assessments/`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Query Parameters (Optional):**
- `type`: Filter by assessment type (`coding`, `non-coding`, `mix`)
- `is_published`: Filter by published status (`true`, `false`)
- `set_number`: Get questions for specific set
- `page`: Page number for pagination
- `page_size`: Results per page (default: 10, max: 100)

**Example:** `GET /api/assessments/?type=coding&is_published=true&page=1&page_size=20`

**Response (200):**
```json
{
  "count": 45,
  "next": "http://127.0.0.1:8000/api/assessments/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "assessment_name": "Python Test",
      "assessment_type": "mix",
      "total_marks": 100,
      "passing_marks": 40,
      "duration": 120,
      "is_published": true,
      "sections": [...]
    }
  ]
}
```

---

### 6. Get Single Assessment
**Endpoint:** `GET /api/assessment/<id>`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Query Parameters (Optional):**
- `set_number`: Get questions for specific set only

**Example:** `GET /api/assessment/1?set_number=1`

**Response (200):**
```json
{
  "id": 1,
  "assessment_name": "Python Programming Test",
  "assessment_description": "Comprehensive Python assessment",
  "assessment_type": "mix",
  "total_marks": 100,
  "passing_marks": 40,
  "duration": 120,
  "is_proctored": true,
  "start_time": "2025-01-15T10:00:00Z",
  "end_time": "2025-01-15T12:00:00Z",
  "sections": [
    {
      "id": 1,
      "name": "Programming Basics",
      "description": "Basic programming concepts",
      "total_marks": 40,
      "duration": 40,
      "questions": [...]
    }
  ]
}
```

---

### 7. Update Assessment
**Endpoint:** `PUT /api/assessment/<id>`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Request Body:** (Same structure as Create Assessment)

---

### 8. Delete Assessment
**Endpoint:** `DELETE /api/assessment/<id>`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Response (200):**
```json
{
  "message": "Assessment deleted successfully"
}
```

---

## User Management

### 9. Create User (Admin Only)
**Endpoint:** `POST /api/users/`  
**Permission:** Authenticated + Admin  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Request Body:**
```json
{
  "email": "proctor@example.com",
  "password": "SecurePass123!",
  "role": "proctor"
}
```

**Valid Roles:**
- `"admin"`
- `"assessment_manager"`
- `"proctor"`

**Response (201):**
```json
{
  "status": "success",
  "message": "User created successfully",
  "user": {
    "id": 5,
    "email": "proctor@example.com",
    "role": "proctor"
  }
}
```

---

### 10. List Users
**Endpoint:** `GET /api/users/`  
**Permission:** Authenticated + Admin  
**Headers:**
```json
{
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Query Parameters:**
- `role`: Filter by role (`assessment_manager`, `proctor`)

**Example:** `GET /api/users/?role=proctor`

---

## Student Management

### 11. Upload Students CSV
**Endpoint:** `POST /api/uploadStudents/`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Request Body:** (multipart/form-data)
```
file: <CSV file>
```

**CSV Format:**
```csv
name,email
John Doe,john@example.com
Jane Smith,jane@example.com
Alice Johnson,alice@example.com
```

**Response (201):**
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
      "created_at": "2025-01-15T10:00:00Z"
    }
  ],
  "skipped_students": [],
  "errors": []
}
```

---

### 12. List Students
**Endpoint:** `GET /api/students/`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Response (200):**
```json
[
  {
    "id": 1,
    "full_name": "John Doe",
    "email": "john@example.com",
    "created_at": "2025-01-15T10:00:00Z"
  }
]
```

---

### 13. Get CSV Upload Details
**Endpoint:** `GET /api/students-list/<id>/`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Response (200):**
```json
{
  "id": 1,
  "uploaded_by": 2,
  "uploaded_at": "2025-01-15T10:00:00Z",
  "file_name": "students.csv",
  "total_records": 50,
  "processed_records": 50,
  "status": "completed",
  "errors": null
}
```

---

### 14. Assign Assessment to Students
**Endpoint:** `POST /api/assign-assessment/`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Request Body:**
```json
{
  "assessment_id": 1,
  "csv_upload_id": 1
}
```

**Response (201):**
```json
{
  "message": "Assessment assignment completed",
  "assessment": {
    "id": 1,
    "title": "Python Programming Test",
    "universal_code": "UNIV-ABC123XYZ456"
  },
  "csv_upload": {
    "id": 1,
    "file_name": "students.csv",
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
      "code": "ABCD1234",
      "student_name": "John Doe",
      "student_email": "john@example.com",
      "assessment_title": "Python Programming Test",
      "created_at": "2025-01-15T10:00:00Z",
      "is_used": false,
      "used_at": null
    }
  ]
}
```

---

### 15. Get Test Codes for Assessment
**Endpoint:** `GET /api/assessments/<assessment_id>/test-codes/`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Query Parameters:**
- `csv_upload_id`: Filter by CSV upload
- `is_used`: Filter by usage status (`true`, `false`)

**Example:** `GET /api/assessments/1/test-codes/?is_used=false`

**Response (200):**
```json
{
  "assessment": {
    "id": 1,
    "title": "Python Programming Test",
    "universal_code": "UNIV-ABC123XYZ456"
  },
  "total_codes": 50,
  "test_codes": [
    {
      "id": 1,
      "code": "ABCD1234",
      "student_name": "John Doe",
      "student_email": "john@example.com",
      "is_used": false,
      "used_at": null
    }
  ]
}
```

---

### 16. Get Test Codes by CSV Upload
**Endpoint:** `GET /api/csv-uploads/<csv_upload_id>/test-codes/`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Authorization": "Bearer <your_jwt_token>"
}
```

---

## Email

### 17. Send Bulk Email
**Endpoint:** `POST /api/sendEmail/`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Request Body:**
```json
{
  "csv_upload_id": 1,
  "subject": "Assessment Invitation - Python Programming Test",
  "content": "Dear Student,\n\nYou have been invited to take the Python Programming Test.\n\nTest Details:\n- Date: January 15, 2025\n- Time: 10:00 AM UTC\n- Duration: 2 hours\n\nYour unique test code: {{test_code}}\n\nBest regards,\nExam Team",
  "content_type": "text"
}
```

**Content Types:**
- `"text"`: Plain text email
- `"html"`: HTML formatted email

**HTML Example:**
```json
{
  "csv_upload_id": 1,
  "subject": "Assessment Invitation",
  "content": "<html><body><h2>Assessment Invitation</h2><p>Dear Student,</p><p>You have been invited...</p></body></html>",
  "content_type": "html"
}
```

**Response (200):**
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

## File Management

### 18. Generate Presigned URL for File Upload
**Endpoint:** `POST /api/upload/`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Request Body:**
```json
{
  "assessment_id": 1,
  "filename": "problem_diagram.png"
}
```

**Response (201):**
```json
{
  "message": "Presigned URL generated successfully",
  "presigned_url": "https://your-bucket.s3.amazonaws.com/...",
  "expires_at": "2025-01-15T11:00:00Z",
  "expires_in_seconds": 3600,
  "assessment_file_id": 1,
  "s3_path": "assessments/1/problem_diagram.png",
  "upload_instructions": {
    "method": "PUT",
    "url": "https://your-bucket.s3.amazonaws.com/...",
    "headers": {
      "Content-Type": "image/png"
    }
  }
}
```

**How to Upload:**
```javascript
// Frontend code to upload file using presigned URL
const uploadFile = async (file, presignedUrl, contentType) => {
  const response = await fetch(presignedUrl, {
    method: 'PUT',
    body: file,
    headers: {
      'Content-Type': contentType
    }
  });
  return response.ok;
};
```

---

### 19. Check File Upload Status
**Endpoint:** `GET /api/fileStatus/`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Request Body:**
```json
{
  "assessment_id": 1,
  "filename": "problem_diagram.png"
}
```

**Response (200):**
```json
{
  "message": "File found and record updated",
  "file_uploaded": true,
  "file_size_bytes": 245678,
  "file_size_mb": 0.23,
  "file_size_kb": 239.92,
  "assessment_file_id": 1,
  "s3_url": "https://your-bucket.s3.amazonaws.com/assessments/1/problem_diagram.png",
  "upload_status": "uploaded",
  "uploaded_at": "2025-01-15T10:30:00Z"
}
```

---

### 20. List Assessment Files
**Endpoint:** `GET /api/files/<assessment_id>`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Response (200):**
```json
{
  "assessment_id": 1,
  "assessment_title": "Python Programming Test",
  "total_files": 5,
  "uploaded_files": 5,
  "pending_files": 0,
  "files": [
    {
      "id": 1,
      "filename": "problem_diagram.png",
      "s3_url": "https://...",
      "file_size": 245678,
      "file_size_mb": 0.23,
      "upload_status": "uploaded",
      "created_at": "2025-01-15T10:00:00Z",
      "updated_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

---

## Code Execution

### 21. Run Code (Test/Debug)
**Endpoint:** `POST /api/runCode/`  
**Permission:** Public (AllowAny)  
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
  "script": "print('Hello, World!')\nfor i in range(5):\n    print(i)",
  "language": "python3",
  "versionIndex": "3",
  "stdin": ""
}
```

**Supported Languages:**
- `"python3"` - Python 3
- `"java"` - Java
- `"cpp"` - C++
- `"c"` - C
- `"javascript"` - Node.js
- `"go"` - Go
- `"ruby"` - Ruby
- `"php"` - PHP
- `"swift"` - Swift
- `"kotlin"` - Kotlin
- And many more...

**With Input:**
```json
{
  "script": "name = input()\nprint(f'Hello, {name}!')",
  "language": "python3",
  "versionIndex": "3",
  "stdin": "John"
}
```

**Response (200):**
```json
{
  "output": "Hello, World!\n0\n1\n2\n3\n4\n",
  "statusCode": 200,
  "memory": "9216",
  "cpuTime": "0.02",
  "isExecutionSuccess": true
}
```

**Error Response:**
```json
{
  "output": "",
  "statusCode": 200,
  "memory": "0",
  "cpuTime": "0",
  "isExecutionSuccess": false,
  "error": "SyntaxError: invalid syntax"
}
```

---

### 22. Submit Code (Validate Against Test Cases)
**Endpoint:** `POST /api/submitCode/?type=example`  
**Permission:** Public (AllowAny)  
**Headers:**
```json
{
  "Content-Type": "application/json"
}
```

**Query Parameters:**
- `type`: `"example"` (runs example test cases) or `"all"` (runs hidden test cases)

**Request Body:**
```json
{
  "question_id": 5,
  "script": "def reverse_string(s):\n    return s[::-1]\n\nif __name__ == '__main__':\n    input_str = input()\n    print(reverse_string(input_str))",
  "language": "python3",
  "versionIndex": "3"
}
```

**Response (200):**
```json
{
  "total_test_cases": 2,
  "passed": 2,
  "failed": 0,
  "success_rate": 100.0,
  "test_results": [
    {
      "test_case_number": 1,
      "input": "hello",
      "expected_output": "olleh",
      "actual_output": "olleh",
      "passed": true,
      "error": null,
      "execution_time": "0.02",
      "memory_used": "9216"
    },
    {
      "test_case_number": 2,
      "input": "python",
      "expected_output": "nohtyp",
      "actual_output": "nohtyp",
      "passed": true,
      "error": null,
      "execution_time": "0.01",
      "memory_used": "9216"
    }
  ]
}
```

**Failed Test Case Example:**
```json
{
  "total_test_cases": 2,
  "passed": 1,
  "failed": 1,
  "success_rate": 50.0,
  "test_results": [
    {
      "test_case_number": 1,
      "input": "hello",
      "expected_output": "olleh",
      "actual_output": "olleh",
      "passed": true
    },
    {
      "test_case_number": 2,
      "input": "python",
      "expected_output": "nohtyp",
      "actual_output": "Python",
      "passed": false,
      "execution_time": "0.01",
      "memory_used": "9216"
    }
  ]
}
```

---

## Reports & Analytics

### 23. Generate Student Report
**Endpoint:** `POST /api/reports/student`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Request Body (Enhanced Format):**
```json
{
  "assessment_id": 1,
  "student_email": "john@example.com",
  "started_at": "2025-01-15T10:00:00Z",
  "ended_at": "2025-01-15T11:45:00Z",
  "submitted_at": "2025-01-15T11:45:00Z",
  "window_switch_count": 3,
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
          "selected_option_index": 0,
          "is_correct": true,
          "marks_obtained": 4,
          "total_marks": 4,
          "time_spent": 45
        },
        {
          "question_id": 2,
          "is_attempted": true,
          "selected_option_index": 2,
          "is_correct": false,
          "marks_obtained": -1,
          "total_marks": 4,
          "time_spent": 60
        },
        {
          "question_id": 3,
          "is_attempted": true,
          "code_answer": "def reverse(s):\n    return s[::-1]",
          "is_correct": true,
          "marks_obtained": 10,
          "total_marks": 10,
          "time_spent": 450
        },
        {
          "question_id": 4,
          "is_attempted": false,
          "is_correct": false,
          "marks_obtained": 0,
          "total_marks": 4,
          "time_spent": 0
        }
      ]
    },
    {
      "section_id": 2,
      "set_number": 1,
      "time_spent": 2400,
      "questions": [...]
    }
  ]
}
```

**Response (201):**
```json
{
  "message": "Student report generated successfully",
  "report_id": "REPORT-123ABC",
  "participant_type": "student",
  "student": {
    "email": "john@example.com",
    "name": "John Doe"
  },
  "assessment": {
    "id": 1,
    "title": "Python Programming Test",
    "total_marks": 100,
    "passing_marks": 40
  },
  "performance": {
    "obtained_marks": 78,
    "total_marks": 100,
    "percentage": 78.0,
    "result": "PASS",
    "total_questions": 25,
    "attempted": 23,
    "correct": 19,
    "wrong": 4,
    "unattempted": 2
  },
  "section_wise_performance": [
    {
      "section_name": "Programming Basics",
      "obtained_marks": 32,
      "total_marks": 40,
      "percentage": 80.0,
      "attempted": 9,
      "correct": 8,
      "wrong": 1
    }
  ],
  "time_analysis": {
    "total_time_seconds": 6300,
    "total_time_minutes": 105,
    "time_per_question_avg": 252
  },
  "proctoring": {
    "window_switches": 3,
    "is_flagged": false
  }
}
```

---

## Proctoring

### 24. Upload Student Image (Proctoring)
**Endpoint:** `POST /api/uploadStudentImage/`  
**Permission:** Public (AllowAny)  
**Headers:**
```json
{
  "Authorization": "Bearer <jwt_with_test_code>"
}
```

**Request Body:** (multipart/form-data)
```
token: <JWT token with test code>
image: <Image file>
```

---

### 25. Get Proctoring Results
**Endpoint:** `GET /api/proctoring-results/`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Query Parameters:**
- `assessment_id`: Filter by assessment
- `student_email`: Filter by student

**Response (200):**
```json
{
  "count": 10,
  "results": [
    {
      "session_id": "SESSION-123",
      "student_email": "john@example.com",
      "assessment_title": "Python Test",
      "suspicious_activity_count": 2,
      "snapshots_count": 45
    }
  ]
}
```

---

### 26. Get Proctoring Result Detail
**Endpoint:** `GET /api/proctoring-results/<session_id>/`  
**Permission:** Authenticated  
**Headers:**
```json
{
  "Authorization": "Bearer <your_jwt_token>"
}
```

**Response (200):**
```json
{
  "session_id": "SESSION-123",
  "student": {
    "email": "john@example.com",
    "name": "John Doe"
  },
  "assessment": {
    "id": 1,
    "title": "Python Programming Test"
  },
  "snapshots": [
    {
      "timestamp": "2025-01-15T10:15:00Z",
      "image_url": "https://...",
      "suspicious_activity": true,
      "activity_type": "multiple_faces_detected"
    }
  ],
  "summary": {
    "total_snapshots": 45,
    "suspicious_count": 2,
    "started_at": "2025-01-15T10:00:00Z",
    "ended_at": "2025-01-15T11:45:00Z"
  }
}
```

---

## Common Headers

### For All Authenticated Requests:
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer <your_jwt_token>",
  "ngrok-skip-browser-warning": "true"
}
```

**Note:** Add `"ngrok-skip-browser-warning": "true"` when using ngrok tunneling.

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid data",
  "details": {
    "email": ["This field is required"],
    "password": ["This field may not be blank"]
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
  "error": "Assessment not found",
  "assessment_id": 999
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "details": "Database connection failed"
}
```

---

## Important Notes

### Question Types
⚠️ **IMPORTANT:** Only two question types are supported:
1. **`"coding"`** - For programming questions with test cases
2. **`"non-coding"`** - For Multiple Choice Questions (MCQs)

**Subjective/Essay/Descriptive questions are NOT supported and will be rejected.**

### Section Marking Safety

The system enforces **strict validation rules** to ensure fair and consistent assessments across all sets:

**📋 Quick Rules:**
1. ✅ All sections in a set must have **equal net marks**
2. ✅ All sets must have the **same section structure**
3. ✅ Each section must have **identical marks across all sets**
4. ⚠️ Net marks = `positive_marks + negative_marks` (per question)

---

#### 1. Within-Set Section Consistency
All sections within the same set must have **equal net scoring potential**.

**Formula:** `Net Scoring Potential = SUM(positive_marks + negative_marks)` for all questions in a section

**Example:**
- Set 1, Section 1: 4 questions × (4 marks + (-1) mark) = 12 net marks
- Set 1, Section 2: 3 questions × (4 marks + 0 marks) = 12 net marks ✅ VALID
- Set 1, Section 3: 2 questions × (6 marks + 0 marks) = 12 net marks ✅ VALID

**Why?** This ensures students aren't disadvantaged by attempting harder sections with different scoring.

#### 2. Cross-Set Structure Consistency
All sets must have the **same section structure** (same section IDs).

**Example:**
- Set 1: Sections [1, 2, 3] ✅
- Set 2: Sections [1, 2, 3] ✅ VALID
- Set 3: Sections [1, 2] ❌ INVALID (missing section 3)

**Why?** This ensures all students take the same types of sections regardless of set assignment.

#### 3. Cross-Set Section Marks Consistency
Each section must have **identical net scoring potential across all sets**.

**Example:**
- Set 1, Section 1: 20 net marks
- Set 2, Section 1: 20 net marks ✅ VALID
- Set 3, Section 1: 25 net marks ❌ INVALID

**Why?** This ensures equivalent difficulty and fairness across all sets.

#### Validation Example

**✅ VALID Assessment (2 Sets, 2 Sections):**
```json
{
  "questions": [
    // Set 1, Section 1: 4+(-1) + 4+(-1) = 6 net marks
    {"set_number": 1, "section_id": 1, "positive_marks": 4, "negative_marks": -1},
    {"set_number": 1, "section_id": 1, "positive_marks": 4, "negative_marks": -1},
    
    // Set 1, Section 2: 3+0 + 3+0 = 6 net marks (matches Section 1 ✅)
    {"set_number": 1, "section_id": 2, "positive_marks": 3, "negative_marks": 0},
    {"set_number": 1, "section_id": 2, "positive_marks": 3, "negative_marks": 0},
    
    // Set 2, Section 1: 4+(-1) + 4+(-1) = 6 net marks (matches Set 1, Section 1 ✅)
    {"set_number": 2, "section_id": 1, "positive_marks": 4, "negative_marks": -1},
    {"set_number": 2, "section_id": 1, "positive_marks": 4, "negative_marks": -1},
    
    // Set 2, Section 2: 3+0 + 3+0 = 6 net marks (matches Set 1, Section 2 ✅)
    {"set_number": 2, "section_id": 2, "positive_marks": 3, "negative_marks": 0},
    {"set_number": 2, "section_id": 2, "positive_marks": 3, "negative_marks": 0}
  ]
}
```

**❌ INVALID Assessment (Inconsistent Marks):**
```json
{
  "questions": [
    // Set 1, Section 1: 4+(-1) + 4+(-1) = 6 net marks
    {"set_number": 1, "section_id": 1, "positive_marks": 4, "negative_marks": -1},
    {"set_number": 1, "section_id": 1, "positive_marks": 4, "negative_marks": -1},
    
    // Set 1, Section 2: 5+0 + 5+0 = 10 net marks ❌ (doesn't match Section 1)
    {"set_number": 1, "section_id": 2, "positive_marks": 5, "negative_marks": 0},
    {"set_number": 1, "section_id": 2, "positive_marks": 5, "negative_marks": 0}
  ]
}
// Error: "All sections in set 1 must have the same net scoring potential. Found different totals: Section 1: 6 net marks, Section 2: 10 net marks."
```

### Authentication
- All authenticated endpoints require JWT token in Authorization header
- Token format: `Bearer <token>`
- Get token from `/api/login/` or `/api/register/` endpoints
- Token expires after 24 hours (configurable)

### Pagination
Default pagination for list endpoints:
- `page_size`: 10 (default)
- `max_page_size`: 100
- Use `page` and `page_size` query parameters

### File Uploads
1. Generate presigned URL using `/api/upload/`
2. Upload file directly to S3 using presigned URL (PUT request)
3. Verify upload status using `/api/fileStatus/`

### CORS
If using ngrok or accessing from different domain, include:
```json
{
  "ngrok-skip-browser-warning": "true"
}
```

---

## Complete Frontend Example

### React/JavaScript Complete Flow

```javascript
// 1. Login
const login = async (email, password) => {
  const response = await fetch('http://127.0.0.1:8000/api/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'ngrok-skip-browser-warning': 'true'
    },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  localStorage.setItem('token', data.token);
  return data;
};

// 2. Create Assessment
const createAssessment = async (assessmentData) => {
  const token = localStorage.getItem('token');
  const response = await fetch('http://127.0.0.1:8000/api/assessment', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      'ngrok-skip-browser-warning': 'true'
    },
    body: JSON.stringify(assessmentData)
  });
  return response.json();
};

// 3. Upload Students CSV
const uploadStudents = async (file) => {
  const token = localStorage.getItem('token');
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://127.0.0.1:8000/api/uploadStudents/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'ngrok-skip-browser-warning': 'true'
    },
    body: formData
  });
  return response.json();
};

// 4. Assign Assessment to Students
const assignAssessment = async (assessmentId, csvUploadId) => {
  const token = localStorage.getItem('token');
  const response = await fetch('http://127.0.0.1:8000/api/assign-assessment/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      'ngrok-skip-browser-warning': 'true'
    },
    body: JSON.stringify({
      assessment_id: assessmentId,
      csv_upload_id: csvUploadId
    })
  });
  return response.json();
};

// 5. Upload File to Assessment
const uploadAssessmentFile = async (assessmentId, file) => {
  const token = localStorage.getItem('token');
  
  // Step 1: Get presigned URL
  const urlResponse = await fetch('http://127.0.0.1:8000/api/upload/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      'ngrok-skip-browser-warning': 'true'
    },
    body: JSON.stringify({
      assessment_id: assessmentId,
      filename: file.name
    })
  });
  const urlData = await urlResponse.json();
  
  // Step 2: Upload file to S3
  await fetch(urlData.presigned_url, {
    method: 'PUT',
    body: file,
    headers: {
      'Content-Type': file.type
    }
  });
  
  // Step 3: Verify upload
  const statusResponse = await fetch('http://127.0.0.1:8000/api/fileStatus/', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      'ngrok-skip-browser-warning': 'true'
    },
    body: JSON.stringify({
      assessment_id: assessmentId,
      filename: file.name
    })
  });
  return statusResponse.json();
};

// 6. Run Code
const runCode = async (code, language, input = '') => {
  const response = await fetch('http://127.0.0.1:8000/api/runCode/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'ngrok-skip-browser-warning': 'true'
    },
    body: JSON.stringify({
      script: code,
      language: language,
      versionIndex: '3',
      stdin: input
    })
  });
  return response.json();
};

// 7. Submit Code for Validation
const submitCode = async (questionId, code, language, testType = 'example') => {
  const response = await fetch(`http://127.0.0.1:8000/api/submitCode/?type=${testType}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'ngrok-skip-browser-warning': 'true'
    },
    body: JSON.stringify({
      question_id: questionId,
      script: code,
      language: language,
      versionIndex: '3'
    })
  });
  return response.json();
};
```

---

## Version Information
- **Django Version:** 5.1.5
- **Django REST Framework:** 3.16.0
- **API Version:** 1.0
- **Last Updated:** October 24, 2025

---

## Support
For issues or questions, contact the development team or refer to the project documentation.
