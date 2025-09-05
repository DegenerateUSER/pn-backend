# PN Academy Backend API Documentation

A Django REST API for managing educational assessments, students, and related functionality.

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL (for production) or SQLite (for development)
- AWS account with S3 and SES configured

### Environment Setup

1. **Clone and navigate to the project:**
   ```bash
   cd server
   ```

2. **Create and configure environment variables:**
   Copy `.env.local` and update the following variables:
   ```bash
   # OAuth Configuration
   OAUTH_CLIENT_ID=your_google_oauth_client_id
   OAUTH_CLIENT_KEY=your_google_oauth_client_secret
   
   # Django Settings
   DEBUG=1
   SECRET_KEY=your_secret_key
   
   # Database (for production)
   POSTGRES_DB=pnacademy
   POSTGRES_USER=pnadmin
   POSTGRES_PASSWORD=supersecret
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   
   # AWS Configuration
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_REGION=eu-north-1
   AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name
   DEFAULT_FROM_EMAIL=your_email@domain.com
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```
   **Note:** If you encounter issues with superuser creation due to the custom User model, you can use the provided script:
   ```bash
   python create_superuser.py
   ```
   **Default Admin Credentials:**
   - Email: `admin@example.com`
   - Password: `admin`

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

The server will be available at `http://127.0.0.1:8000/`

### Using Docker

```bash
docker-compose up --build
```

## API Endpoints

### Base URL
- **Development:** `http://127.0.0.1:8000/`
- **API Base:** `http://127.0.0.1:8000/api/v1/`

### Authentication

All API endpoints (except registration, login, and OAuth) require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

---

## Authentication Endpoints

### 1. User Registration
- **URL:** `POST /api/v1/register/`
- **Permission:** Public
- **Description:** Register a new user account

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "token": "jwt_token_here",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### 2. User Login
- **URL:** `POST /api/v1/login/`
- **Permission:** Public
- **Description:** Login with email and password

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "token": "jwt_token_here"
}
```

### 3. Google OAuth Callback
- **URL:** `GET /auth-receiver`
- **Permission:** Public
- **Description:** Handles Google OAuth authentication callback

### 4. Reset Password
- **URL:** `POST /api/v1/reset-password/`
- **Permission:** Authenticated
- **Description:** Reset user password

**Request Body:**
```json
{
  "new_password": "newSecurePassword"
}
```

---

## Assessment Management

### 5. Assessment CRUD Operations

#### List/Create Assessments
- **URL:** `GET/POST /api/v1/assessments/`
- **Permission:** Authenticated

**GET Response:**
```json
{
  "results": [
    {
      "id": 1,
      "title": "Mathematics Assessment",
      "description": "Basic math skills test",
      "created_at": "2025-01-01T00:00:00Z",
      "is_published": true
    }
  ]
}
```

**POST Request:**
```json
{
  "assessment_name": "Comprehensive Skill Evaluation",
  "assessment_type": "mix",
  "assessment_description": "A test designed to assess aptitude, coding ability, logical reasoning, and general knowledge with diverse question formats.",
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
      "question_type": "non-coding-single",
      "section_id": 1,
      "set_number": 1,
      "question_text": "If 12 pens cost ₹144, what is the cost of 1 pen?",
      "options": ["₹10", "₹12", "₹14", "₹15"],
      "correct_option_index": 1,
      "positive_marks": 4,
      "negative_marks": -1,
      "time_limit": 60
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Write a function to check if a number is prime.",
      "description": "Given an integer n, return true if it is prime, otherwise false.",
      "constraints": ["1 <= n <= 10^6", "Input is an integer"],
      "positive_marks": 10,
      "negative_marks": 0,
      "time_limit": 900,
      "test_cases": {
        "examples": [
          {"input": "5", "output": "true"},
          {"input": "10", "output": "false"}
        ],
        "hidden": [
          {"input": "999983", "output": "true"}
        ]
      }
    }
  ]
}
```

#### Retrieve/Update/Delete Assessment
- **URL:** `GET/PUT/PATCH/DELETE /api/v1/assessments/{id}/`
- **Permission:** Authenticated

#### Publish Assessment
- **URL:** `POST /api/v1/assessments/{id}/publish/`
- **Permission:** Authenticated
- **Description:** Publish an assessment to make it available for students

---

## User Management

### 6. User CRUD Operations
- **URL:** `GET/POST/PUT/DELETE /api/v1/users/`
- **Permission:** Authenticated (Admin for some operations)

### 7. Student Management
- **URL:** `GET /api/v1/students/`
- **Permission:** Authenticated
- **Description:** List students (read-only)

---

## Student Management & CSV Operations

### 8. Upload Students via CSV
- **URL:** `POST /api/v1/uploadStudents/`
- **Permission:** Authenticated
- **Description:** Upload student data via CSV file

**Request:**
- **Content-Type:** `multipart/form-data`
- **File:** CSV file with student data

**CSV Format:**
```csv
first_name,last_name,email,registration_number
John,Doe,john.doe@email.com,REG001
Jane,Smith,jane.smith@email.com,REG002
```

### 9. Assign Assessment to CSV Upload
- **URL:** `POST /api/v1/assign-assessment/`
- **Permission:** Authenticated
- **Description:** Assign an assessment to students from a CSV upload

**Request Body:**
```json
{
  "csv_upload_id": 1,
  "assessment_id": 2,
  "due_date": "2025-12-31T23:59:59Z"
}
```

### 10. Get Students List from CSV Uploads
- **URL:** `GET /api/v1/students-list/`
- **Permission:** Authenticated
- **Description:** List all CSV uploads containing student data

---

## Test Codes & Assessment Access

### 11. Get Assessment Test Codes
- **URL:** `GET /api/v1/assessments/{assessment_id}/test-codes/`
- **Permission:** Authenticated
- **Description:** Get test codes for accessing an assessment

**Response:**
```json
{
  "test_codes": [
    {
      "code": "ABC123",
      "student_email": "student@email.com",
      "used": false,
      "created_at": "2025-01-01T00:00:00Z"
    }
  ]
}
```

### 12. Get CSV Upload Test Codes
- **URL:** `GET /api/v1/csv-uploads/{csv_upload_id}/test-codes/`
- **Permission:** Authenticated
- **Description:** Get test codes for students from a specific CSV upload

---

## Email & Communication

### 13. Send Bulk Emails
- **URL:** `POST /api/v1/sendEmail/`
- **Permission:** Authenticated
- **Description:** Send bulk emails to students (uses AWS SES)

**Request Body:**
```json
{
  "recipients": ["student1@email.com", "student2@email.com"],
  "subject": "Assessment Invitation",
  "message": "You have been invited to take an assessment.",
  "assessment_id": 1
}
```

---

## File Management

### 14. Generate Presigned URL for File Upload
- **URL:** `POST /api/v1/upload/`
- **Permission:** Authenticated
- **Description:** Generate AWS S3 presigned URL for file uploads

**Request Body:**
```json
{
  "file_name": "document.pdf",
  "file_type": "application/pdf",
  "assessment_id": 1
}
```

**Response:**
```json
{
  "presigned_url": "https://s3.amazonaws.com/bucket/...",
  "file_key": "assessments/1/document.pdf"
}
```

### 15. Check File Status
- **URL:** `GET /api/v1/fileStatus/?file_key=<file_key>`
- **Permission:** Authenticated
- **Description:** Check if a file exists in S3 storage

### 16. List Assessment Files
- **URL:** `GET /api/v1/files/{assessment_id}`
- **Permission:** Authenticated
- **Description:** List all files associated with an assessment

---

## Proctoring Module

### 17. Upload Student Image
- **URL:** `POST /api/v1/uploadStudentImage/`
- **Permission:** Authenticated
- **Description:** Upload student image for proctoring and verification

**Request:**
- **Content-Type:** `multipart/form-data`
- **File:** Image file

---

## Error Responses

All endpoints return standard HTTP status codes:

- **200 OK:** Success
- **201 Created:** Resource created successfully
- **400 Bad Request:** Invalid request data
- **401 Unauthorized:** Authentication required
- **403 Forbidden:** Permission denied
- **404 Not Found:** Resource not found
- **500 Internal Server Error:** Server error

**Error Response Format:**
```json
{
  "error": "Error message description",
  "details": "Additional error details if available"
}
```

---

## Admin Panel

### 18. Django Admin
- **URL:** `GET /admin/`
- **Permission:** Superuser
- **Description:** Access Django admin interface for database management

---

## Additional Features

### Pagination
List endpoints support pagination with the following parameters:
- `page`: Page number
- `page_size`: Number of items per page (default: 20)

### CORS Configuration
The API supports CORS for frontend applications running on `http://localhost:3000`.

### Security Features
- JWT authentication with 7-day access token lifetime
- CSRF protection
- Secure password validation
- Google OAuth integration

---

## Development Notes

### Database Models
The API includes models for:
- **User:** Custom user model with authentication
- **Assessment:** Assessment structure with sections and questions
- **Student:** Student information and registration
- **CSVUpload:** Batch student data uploads
- **TestCode:** Access codes for assessments
- **Files:** File attachments and storage

### AWS Integration
- **S3:** File storage and presigned URL generation
- **SES:** Email sending functionality
- **Lambda:** Serverless function integration (configurable)

### Future Enhancements
- Assessment result reporting
- Advanced proctoring features
- Video call integration
- Sample report generation

---

## Troubleshooting

### Common Issues

1. **Database Connection Error:**
   - Check PostgreSQL service is running
   - Verify database credentials in `.env.local`
   - For development, ensure SQLite database is accessible

2. **AWS Configuration:**
   - Verify AWS credentials and permissions
   - Check S3 bucket exists and has proper permissions
   - Ensure SES is configured for your region

3. **Google OAuth Issues:**
   - Verify OAuth client ID and secret
   - Check redirect URLs in Google Console
   - Ensure proper CORS configuration

4. **File Upload Problems:**
   - Check AWS S3 permissions
   - Verify file size limits
   - Ensure proper content-type headers

For additional support, check the Django logs and ensure all environment variables are properly configured.
