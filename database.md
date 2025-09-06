# Database Documentation - PN Academy Assessment Platform

## Overview
This document provides a comprehensive overview of the database structure, migrations, and changes for the PN Academy Assessment Platform. The application uses Django ORM with SQLite3 for development and supports PostgreSQL for production through `dj-database-url`.

---

## Database Configuration

### Current Setup
- **Development Database**: SQLite3 (`db.sqlite3`)
- **Production Database**: PostgreSQL (configurable via `DATABASE_URL` environment variable)
- **ORM**: Django ORM
- **Migrations Directory**: `api/migrations/`

### Database Settings (settings.py)
```python
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR}/db.sqlite3"
    )
}
```

### Authentication Model
- **Custom User Model**: `api.User` (extends AbstractUser)
- **Username Field**: Email (username field disabled)

---

## Migration History

### Migration 1: Initial Schema (0001_initial.py)
**Generated**: September 4, 2025 at 17:41
**Description**: Initial database schema creation with all core models

### Migration 2: Question Enhancement (0002_question_marks_question_negative_marks_and_more.py)
**Generated**: September 5, 2025 at 08:07
**Description**: Added question management fields for better assessment control

**Changes Made**:
- Added `marks` field to Question model (PositiveIntegerField, default=0)
- Added `negative_marks` field to Question model (IntegerField, default=0)
- Added `question_order` field to Question model (PositiveIntegerField, default=0)
- Added `set_number` field to Question model (PositiveIntegerField, default=1)
- Added `time_limit` field to Question model (PositiveIntegerField, default=0)
- Added `section_order` field to Section model (PositiveIntegerField, default=0)

---

## Database Schema

### Core Models

#### 1. User Management

##### EmailWhitelist
```python
- id: BigAutoField (Primary Key)
- email: EmailField (Unique)
- role: CharField (choices: admin, assessment_manager, proctor, default: candidate)
```

##### Role
```python
- id: CharField (Primary Key, max_length=50)
- name: CharField (max_length=50, unique=True)
- permissions: JSONField
```

##### User (Custom AbstractUser)
```python
- id: BigAutoField (Primary Key)
- password: CharField (inherited)
- last_login: DateTimeField (inherited)
- is_superuser: BooleanField (inherited)
- first_name: CharField (inherited)
- last_name: CharField (inherited)
- is_staff: BooleanField (inherited)
- is_active: BooleanField (inherited)
- date_joined: DateTimeField (inherited)
- email: EmailField (unique=True) - USERNAME_FIELD
- role: CharField (choices: admin, assessment_manager, proctor, default: assessment_manager)
- created_at: DateTimeField (auto_now_add=True)
- updated_at: DateTimeField (auto_now=True)
- phone_number: CharField (max_length=20, nullable)
- groups: ManyToManyField (related_name='client_set')
- user_permissions: ManyToManyField (related_name='client_set')
```

#### 2. Assessment Structure

##### Assessment
```python
- id: BigAutoField (Primary Key)
- title: CharField (max_length=255)
- description: TextField (nullable)
- assessment_type: CharField (choices: coding, non-coding, mix, default: mix)
- created_by: ForeignKey (User, related_name='created_assessments')
- created_at: DateTimeField (auto_now_add=True)
- updated_at: DateTimeField (auto_now=True)
- is_active: BooleanField (default=True)
- is_published: BooleanField (default=False)
- total_marks: PositiveIntegerField
- passing_marks: PositiveIntegerField
- total_sets: PositiveIntegerField (default=1)
- duration: PositiveIntegerField (nullable, help_text="Duration in minutes")
- set_number: PositiveIntegerField (default=1)
- is_proctored: BooleanField (default=False)
- start_time: DateTimeField (nullable)
- end_time: DateTimeField (nullable)
- is_electron_only: BooleanField (default=False)
- ai_generated_questions: PositiveIntegerField (default=0)
- attachments: JSONField (nullable)
- is_offline: BooleanField (default=False)
- universal_code: CharField (max_length=255, nullable)
```

##### Section
```python
- id: BigAutoField (Primary Key)
- assessment: ForeignKey (Assessment, related_name='sections')
- name: CharField (max_length=255)
- description: TextField (nullable)
- num_of_questions: IntegerField (default=0)
- total_marks: PositiveIntegerField
- negative_mark_per_question: PositiveIntegerField (default=0)
- duration: PositiveIntegerField (nullable, help_text="Duration in minutes")
- section_order: PositiveIntegerField (default=0) [Added in Migration 2]
```

##### Question
```python
- id: BigAutoField (Primary Key)
- section: ForeignKey (Section, related_name='questions')
- question_text: TextField
- question_type: CharField (choices: coding, non-coding, default: non-coding)
- options: JSONField (nullable)
- correct_answer: JSONField (nullable)
- description: TextField (nullable)
- constraints: JSONField (nullable)
- expected_output: TextField (nullable)
- test_cases: JSONField (nullable)
- set_number: PositiveIntegerField (default=1) [Added in Migration 2]
- marks: PositiveIntegerField (default=0) [Added in Migration 2]
- negative_marks: IntegerField (default=0) [Added in Migration 2]
- question_order: PositiveIntegerField (default=0) [Added in Migration 2]
- time_limit: PositiveIntegerField (default=0) [Added in Migration 2]
```

#### 3. Assessment Assignment & Management

##### AssessmentAssignment
```python
- id: CharField (Primary Key, max_length=50)
- assessment: ForeignKey (Assessment, related_name='assignments')
- candidate: ForeignKey (User, related_name='candidate_assignments')
- assigned_by: ForeignKey (User, related_name='assigned_assessments')
- assigned_at: DateTimeField (auto_now_add=True)
- status: CharField (max_length=50)
- unique_test_url: URLField (nullable)
- email_sent: BooleanField (default=False)
- is_marked_for_assignment: BooleanField (default=False)
```

##### Student
```python
- id: BigAutoField (Primary Key)
- csv_upload: ForeignKey (CSVUpload, nullable)
- email: EmailField (unique=True)
- full_name: CharField (max_length=255)
- created_at: DateTimeField (auto_now_add=True)
- updated_at: DateTimeField (auto_now=True)
```

##### TestCode
```python
- id: BigAutoField (Primary Key)
- code: CharField (max_length=100, unique=True)
- student: ForeignKey (Student, related_name='test_codes')
- assessment: ForeignKey (Assessment, related_name='test_codes')
- created_at: DateTimeField (auto_now_add=True)
- is_used: BooleanField (default=False)
- is_active: BooleanField (default=False)
- used_at: DateTimeField (nullable)
- unique_together: (student, assessment)
```

#### 4. Assessment Results & Reports

##### Report
```python
- id: CharField (Primary Key, max_length=50)
- assignment: ForeignKey (AssessmentAssignment, related_name='reports')
- candidate: ForeignKey (User, related_name='candidate_reports')
- assessment: ForeignKey (Assessment)
- started_at: DateTimeField (nullable)
- ended_at: DateTimeField (nullable)
- submitted_at: DateTimeField (nullable)
- status: CharField (max_length=50)
- total_marks: FloatField
- obtained_marks: FloatField
- percentage: FloatField
- percentile: FloatField
- position: PositiveIntegerField (nullable)
- window_switch_count: PositiveIntegerField (default=0)
- is_kicked_out: BooleanField (default=False)
- kicked_out_reason: TextField (nullable)
- is_cheating: BooleanField (default=False)
- cheating_reason: TextField (nullable)
- proctor: ForeignKey (User, related_name='proctored_reports', nullable)
- set_number: PositiveIntegerField (default=1)
```

##### SectionReport
```python
- id: CharField (Primary Key, max_length=50)
- report: ForeignKey (Report, related_name='section_reports')
- section: ForeignKey (Section)
- started_at: DateTimeField (nullable)
- ended_at: DateTimeField (nullable)
- obtained_marks: FloatField
- total_questions: PositiveIntegerField
- attempted_questions: PositiveIntegerField
- correct_answers: PositiveIntegerField
- wrong_answers: PositiveIntegerField
```

##### QuestionAttempt
```python
- id: CharField (Primary Key, max_length=50)
- report: ForeignKey (Report, related_name='question_attempts')
- question: ForeignKey (Question)
- started_at: DateTimeField (nullable)
- ended_at: DateTimeField (nullable)
- selected_answer: JSONField (nullable)
- is_correct: BooleanField (default=False)
- marks_obtained: FloatField (default=0)
- time_taken: PositiveIntegerField (nullable)
- is_attempted: BooleanField (default=False)
```

##### AssessmentReport
```python
- id: CharField (Primary Key, max_length=50)
- assessment: ForeignKey (Assessment, related_name='assessment_reports')
- generated_at: DateTimeField (auto_now_add=True)
- total_candidates: PositiveIntegerField
- attempted_candidates: PositiveIntegerField
- not_attempted_candidates: PositiveIntegerField
- passed_candidates: PositiveIntegerField
- failed_candidates: PositiveIntegerField
- average_score: FloatField
- highest_score: FloatField
- lowest_score: FloatField
- report_data: JSONField
- is_published: BooleanField (default=False)
```

##### CandidateReport
```python
- id: CharField (Primary Key, max_length=50)
- report: ForeignKey (Report, related_name='candidate_reports')
- candidate: ForeignKey (User)
- assessment: ForeignKey (Assessment)
- generated_at: DateTimeField (auto_now_add=True)
- published_at: DateTimeField (nullable)
- email_sent: BooleanField (default=False)
- report_data: JSONField
- feedback: TextField (nullable)
- is_published: BooleanField (default=False)
```

#### 5. Proctoring System

##### ProctoringSession
```python
- id: CharField (Primary Key, max_length=50)
- report: ForeignKey (Report, related_name='proctoring_sessions')
- proctor: ForeignKey (User, related_name='proctoring_sessions', nullable)
- started_at: DateTimeField
- ended_at: DateTimeField (nullable)
- status: CharField (max_length=50)
- recordings: JSONField (nullable)
- incidents: JSONField (nullable)
- notes: TextField (nullable)
```

##### ProctoringSnapshot
```python
- id: CharField (Primary Key, max_length=50)
- session: ForeignKey (ProctoringSession, related_name='snapshots')
- report: ForeignKey (Report)
- question: ForeignKey (Question, nullable)
- timestamp: DateTimeField
- image_url: URLField
- suspicious_activity: BooleanField (default=False)
- activity_type: CharField (max_length=100, nullable)
```

#### 6. File Management & Notifications

##### AssessmentFile
```python
- id: BigAutoField (Primary Key)
- assessment: ForeignKey (Assessment, related_name='files')
- filename: CharField (max_length=255)
- s3_key: CharField (max_length=500)
- s3_url: URLField (nullable)
- file_size: PositiveIntegerField (default=0)
- upload_status: CharField (choices: pending, uploaded, failed, default: pending)
- presigned_url: URLField (max_length=500, nullable)
- presigned_url_expires: DateTimeField (nullable)
- created_at: DateTimeField (auto_now_add=True)
- updated_at: DateTimeField (auto_now=True)
- unique_together: (assessment, filename)
```

##### CSVUpload
```python
- id: BigAutoField (Primary Key)
- uploaded_by: ForeignKey (User)
- uploaded_at: DateTimeField (auto_now_add=True)
- file_name: CharField (max_length=255)
- total_records: PositiveIntegerField
- processed_records: PositiveIntegerField
- status: CharField (max_length=50)
- errors: JSONField (nullable)
```

##### Notification
```python
- id: CharField (Primary Key, max_length=50)
- user: ForeignKey (User, related_name='notifications')
- type: CharField (max_length=100)
- title: CharField (max_length=255)
- message: TextField
- is_read: BooleanField (default=False)
- created_at: DateTimeField (auto_now_add=True)
- related_entity_id: CharField (max_length=50, nullable)
- related_entity_type: CharField (max_length=100, nullable)
```

#### 7. Utility Models

##### SampleJSON
```python
- id: BigAutoField (Primary Key)
- data: JSONField
```

---

## Database Relationships

### Key Foreign Key Relationships

1. **Assessment → User (created_by)**
   - One assessment is created by one user
   - One user can create multiple assessments

2. **Section → Assessment**
   - One section belongs to one assessment
   - One assessment can have multiple sections

3. **Question → Section**
   - One question belongs to one section
   - One section can have multiple questions

4. **AssessmentAssignment → Assessment, User (candidate), User (assigned_by)**
   - Links candidates to assessments with assignment metadata

5. **Report → AssessmentAssignment, User (candidate), Assessment**
   - Stores assessment attempt results

6. **TestCode → Student, Assessment**
   - Unique codes for student access to assessments

7. **Proctoring System**
   - ProctoringSession → Report
   - ProctoringSnapshot → ProctoringSession, Report, Question

---

## JSON Schema Examples

### Assessment Creation JSON Structure
```json
{
  "assessment_name": "Sample Assessment",
  "assessment_type": "mix",
  "assessment_description": "Description of the assessment",
  "passing_marks": 40,
  "total_sets": 3,
  "section_names": ["Aptitude", "Coding", "Logical"],
  "section_descriptions": ["Aptitude questions", "Programming problems", "Logic puzzles"],
  "start_time": "2025-08-10T09:00:00Z",
  "end_time": "2025-08-10T12:00:00Z",
  "is_electron_only": false,
  "num_of_ai_generated_questions": 5,
  "is_proctored": true,
  "is_published": false,
  "attachments": ["url1", "url2"],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "What is the capital of France?",
      "options": ["Paris", "London", "Rome", "Berlin"],
      "correct_option_index": 0,
      "positive_marks": 4,
      "negative_marks": -1,
      "time_limit": 60
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Write a function to reverse a string",
      "description": "You are given a string, reverse it without using built-in reverse methods",
      "constraints": ["1 <= length of string <= 1000"],
      "positive_marks": 10,
      "negative_marks": 0,
      "time_limit": 900,
      "test_cases": {
        "examples": [
          {"input": "hello", "output": "olleh"}
        ],
        "hidden": [
          {"input": "OpenAI", "output": "IAnepO"}
        ]
      }
    }
  ]
}
```

---

## Database Indexes and Constraints

### Unique Constraints
- `EmailWhitelist.email` - Unique
- `Role.name` - Unique
- `User.email` - Unique
- `TestCode.code` - Unique
- `Student.email` - Unique
- `(TestCode.student, TestCode.assessment)` - Unique Together
- `(AssessmentFile.assessment, AssessmentFile.filename)` - Unique Together

### Primary Keys
- Most models use Django's default `BigAutoField`
- Some models use custom `CharField` primary keys (50 characters max):
  - AssessmentAssignment
  - Report
  - SectionReport
  - QuestionAttempt
  - ProctoringSession
  - ProctoringSnapshot
  - AssessmentReport
  - CandidateReport
  - Notification

---

## AWS Integration

### S3 File Storage
- **Bucket Configuration**: Via `AWS_STORAGE_BUCKET_NAME` environment variable
- **Region**: Configurable via `AWS_REGION` (default: eu-north-1)
- **File Models**: AssessmentFile for managing uploaded files

### SES Email Service
- **Email Backend**: django-ses
- **Configuration**: AWS credentials via environment variables
- **Default From Email**: Configurable via `DEFAULT_FROM_EMAIL`

### Lambda Integration
- **Region**: Configurable via `AWS_LAMBDA_REGION_NAME`
- **Function**: Configurable via `AWS_LAMBDA_FUNCTION_NAME`

---

## Deployment Considerations for AWS

### Database Migration for Production
1. **Switch to PostgreSQL**:
   ```bash
   export DATABASE_URL="postgresql://username:password@host:port/database"
   ```

2. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

### Environment Variables Required
```bash
# Database
DATABASE_URL=postgresql://...

# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=eu-north-1
AWS_STORAGE_BUCKET_NAME=your_bucket_name
AWS_LAMBDA_REGION_NAME=eu-north-1
AWS_LAMBDA_FUNCTION_NAME=your_function_name

# Email
DEFAULT_FROM_EMAIL=your_email@domain.com

# Security
SECRET_KEY=your_production_secret_key
DEBUG=0
```

### Security Considerations
- Custom User model with email-based authentication
- JWT token authentication configured
- CORS settings for frontend integration
- AWS credentials securely managed via environment variables

---

## Data Flow Architecture

### Assessment Creation Flow
1. **Assessment Object Creation** - Basic assessment metadata
2. **Section Creation** - Multiple sections per assessment
3. **Question Creation** - Questions assigned to sections with set numbers
4. **File Attachment** - Optional files stored in S3

### Assessment Taking Flow
1. **Assignment Creation** - Candidate assigned to assessment
2. **Test Code Generation** - Unique access codes for students
3. **Report Initialization** - Assessment attempt tracking
4. **Question Attempts** - Individual question responses
5. **Proctoring** - Session monitoring and snapshots

### Reporting Flow
1. **Section Reports** - Performance per section
2. **Assessment Reports** - Overall assessment analytics
3. **Candidate Reports** - Individual results with feedback
4. **Notifications** - System-generated alerts

---

*This documentation reflects the database state as of September 6, 2025, including all migrations and current schema structure.*
