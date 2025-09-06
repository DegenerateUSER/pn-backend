# Assessment API Requests

## 1. Create Assessment

```http
POST /api/v1/assessments/
Authorization: Bearer your_token_here
Content-Type: application/json
```

```json
{
  "assessment_name": "Basic Math Test",
  "assessment_type": "coding",
  "assessment_description": "Simple math problems for beginners",
  "passing_marks": 50,
  "num_of_sets": 2,
  "section_names": ["Addition", "Subtraction"],
  "section_descriptions": ["Basic addition problems", "Basic subtraction problems"],
  "start_time": "2025-12-01T10:00:00Z",
  "end_time": "2025-12-01T11:00:00Z",
  "is_electron_only": false,
  "is_proctored": false,
  "is_published": false,
  "num_of_ai_generated_questions": 0,
  "attachments": [
    "https://example.com/math_rules.pdf",
    "https://example.com/calculator_guide.pdf"
  ],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Write a function to add two numbers. Use the math rules ($1) for reference.",
      "description": "Create a simple addition function",
      "constraints": ["Use only basic math", "No external libraries"],
      "positive_marks": 25,
      "negative_marks": 0,
      "time_limit": 600
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "What is 5 - 3? Check the calculator guide ($2) if needed.",
      "options": ["1", "2", "3", "4"],
      "correct_option_index": 1,
      "positive_marks": 25,
      "negative_marks": -5,
      "time_limit": 300
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 2,
      "question_text": "Write a function to add three numbers. Use the math rules ($1) for reference.",
      "description": "Create an addition function for three numbers",
      "constraints": ["Use only basic math"],
      "positive_marks": 25,
      "negative_marks": 0,
      "time_limit": 600
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 2,
      "question_text": "What is 10 - 7? Check the calculator guide ($2) if needed.",
      "options": ["2", "3", "4", "5"],
      "correct_option_index": 1,
      "positive_marks": 25,
      "negative_marks": -5,
      "time_limit": 300
    }
  ]
}
```

## 2. Get All Assessments

```http
GET /api/v1/assessments/
Authorization: Bearer your_token_here
```

## 3. Get Assessment by ID
```http
GET /api/v1/assessments/123/
Authorization: Bearer your_token_here
```

## 4. Update Assessment (PUT - Full Update)

```http
PUT /api/v1/assessments/123/
Authorization: Bearer your_token_here
Content-Type: application/json
```

```json
{
  "assessment_name": "Basic Math Test - Updated",
  "assessment_type": "mix",
  "assessment_description": "Updated simple math problems",
  "passing_marks": 60,
  "num_of_sets": 2,
  "section_names": ["Addition", "Subtraction", "Multiplication"],
  "section_descriptions": ["Basic addition", "Basic subtraction", "Basic multiplication"],
  "start_time": "2025-12-01T10:00:00Z",
  "end_time": "2025-12-01T12:00:00Z",
  "is_electron_only": true,
  "is_proctored": true,
  "is_published": false,
  "num_of_ai_generated_questions": 1,
  "attachments": [
    "https://example.com/math_rules_v2.pdf"
  ],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Write a function to add two numbers. Use the updated math rules ($1).",
      "description": "Simple addition function",
      "constraints": ["Basic math only"],
      "positive_marks": 30,
      "negative_marks": 0,
      "time_limit": 600
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "What is 2 × 3?",
      "options": ["5", "6", "7", "8"],
      "correct_option_index": 1,
      "positive_marks": 30,
      "negative_marks": -5,
      "time_limit": 300
    }
  ]
}
```

## 5. Update Assessment (PATCH - Partial Update)

### Publish Assessment
```http
PATCH /api/v1/assessments/123/
Authorization: Bearer your_token_here
Content-Type: application/json
```

```json
{
  "is_published": true
}
```

### Unpublish Assessment
```http
PATCH /api/v1/assessments/123/
Authorization: Bearer your_token_here
Content-Type: application/json
```

```json
{
  "is_published": false
}
```

### Update Name and Marks
```http
PATCH /api/v1/assessments/123/
Authorization: Bearer your_token_here
Content-Type: application/json
```

```json
{
  "assessment_name": "Easy Math Test",
  "passing_marks": 40
}
```

### Update Schedule
```http
PATCH /api/v1/assessments/123/
Authorization: Bearer your_token_here
Content-Type: application/json
```

```json
{
  "start_time": "2025-12-02T09:00:00Z",
  "end_time": "2025-12-02T10:00:00Z"
}
```

### Enable Proctoring
```http
PATCH /api/v1/assessments/123/
Authorization: Bearer your_token_here
Content-Type: application/json
```

```json
{
  "is_proctored": true,
  "is_electron_only": true
}
```

## 6. Delete Assessment

```http
DELETE /api/v1/assessments/123/
Authorization: Bearer your_token_here
```

## 7. Get Assessments with Filtering

### Filter by Type
```http
GET /api/v1/assessments/?assessment_type=coding
Authorization: Bearer your_token_here
```

### Filter by Published Status
```http
GET /api/v1/assessments/?is_published=true
Authorization: Bearer your_token_here
```

### Multiple Filters
```http
GET /api/v1/assessments/?assessment_type=mix&is_published=true&limit=10
Authorization: Bearer your_token_here
```

## 8. Search Assessments and Sets

### Search by Keywords
```http
GET /api/v1/assessments/search/?q=math
Authorization: Bearer your_token_here
```

### Get Assessment with Set 1 Questions Only
```http
GET /api/v1/assessments/123/?set_number=1
Authorization: Bearer your_token_here
```

### Get Assessment with Set 2 Questions Only
```http
GET /api/v1/assessments/123/?set_number=2
Authorization: Bearer your_token_here
```

### Get All Assessments with Set 1 Questions
```http
GET /api/v1/assessments/?set_number=1
Authorization: Bearer your_token_here
```

### Get Published Assessments with Set 2 Questions
```http
GET /api/v1/assessments/?set_number=2&is_published=true
Authorization: Bearer your_token_here
```

## 9. Copy/Clone Assessment

```http
POST /api/v1/assessments/123/clone/
Authorization: Bearer your_token_here
Content-Type: application/json
```

```json
{
  "assessment_name": "Basic Math Test - Copy",
  "include_questions": true,
  "modify_dates": true,
  "new_start_time": "2025-12-10T10:00:00Z",
  "new_end_time": "2025-12-10T11:00:00Z"
}
```

## 10. Bulk Update Assessments

```http
POST /api/v1/assessments/bulk-update/
Authorization: Bearer your_token_here
Content-Type: application/json
```

```json
{
  "assessment_ids": [123, 124, 125],
  "updates": {
    "is_proctored": true,
    "passing_marks": 50
  }
}
```

## 11. Get Assessment Statistics

```http
GET /api/v1/assessments/123/statistics/
Authorization: Bearer your_token_here
```

## 12. Export Assessment

```http
GET /api/v1/assessments/123/export/?format=json&include_questions=true
Authorization: Bearer your_token_here
```

## 13. Import Assessment

```http
POST /api/v1/assessments/import/
Authorization: Bearer your_token_here
Content-Type: multipart/form-data
```

## 14. Validate Assessment

```http
POST /api/v1/assessments/validate/
Authorization: Bearer your_token_here
Content-Type: application/json
```

```json
{
  "assessment_name": "Test Validation",
  "assessment_type": "coding",
  "passing_marks": 30,
  "num_of_sets": 1,
  "section_names": ["Basic"],
  "section_descriptions": ["Basic test"]
}
```
