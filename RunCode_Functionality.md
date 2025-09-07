# RunCode Functionality Documentation

## Overview

This document provides complete documentation for the **RunCode functionality** in the PN Academy Django application. This feature allows users to execute code snippets and validate them against test cases using the JDoodle API.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [API Endpoints](#api-endpoints)
- [Setup Instructions](#setup-instructions)
- [Code Components](#code-components)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)
- [Security Considerations](#security-considerations)
- [Limitations](#limitations)

## Features

### 1. Code Execution (`RunCodeView`)
- Execute code in multiple programming languages
- Support for stdin input
- Real-time execution with timeout handling
- Comprehensive error reporting

### 2. Code Validation (`SubmitCodeView`)
- Validate code against predefined test cases
- Support for example and hidden test cases
- Detailed test results with pass/fail status
- Performance metrics (execution time, memory usage)

### 3. Supported Languages
- Python (2.x, 3.x)
- Java
- C/C++ (multiple versions)
- JavaScript/Node.js
- C#, PHP, Ruby, Go, Scala
- And many more...

## Architecture

```
Frontend Request
    ↓
Django API View (RunCodeView/SubmitCodeView)
    ↓
Input Validation (Serializers)
    ↓
JDoodle API Integration
    ↓
Response Processing
    ↓
Formatted Response to Frontend
```

## API Endpoints

### 1. Execute Code
**Endpoint:** `POST /api/runCode/`

**Description:** Execute code snippet with optional input

**Request Body:**
```json
{
    "script": "print('Hello World')",
    "language": "python3",
    "versionIndex": "3",
    "stdin": ""
}
```

**Response:**
```json
{
    "output": "Hello World\n",
    "statusCode": 200,
    "memory": "9676",
    "cpuTime": "0.05",
    "error": null
}
```

### 2. Submit Code for Validation
**Endpoint:** `POST /api/submitCode/?type=example`

**Description:** Validate code against test cases

**Query Parameters:**
- `type`: `example` (for example test cases) or `all` (for hidden test cases)

**Request Body:**
```json
{
    "script": "x = int(input())\nprint(x * 2)",
    "language": "python3",
    "versionIndex": "3",
    "question_id": 1
}
```

**Response:**
```json
{
    "total_test_cases": 2,
    "passed_count": 2,
    "failed_count": 0,
    "success_rate": "100.0%",
    "overall_result": "PASSED",
    "test_results": [
        {
            "test_case_number": 1,
            "input": "5",
            "expected_output": "10",
            "actual_output": "10",
            "passed": true,
            "error": null,
            "execution_time": "0.05",
            "memory_used": "9676"
        }
    ]
}
```

### 3. Admin Assessment Management
**Endpoint:** `GET /api/v1/assessments/all_assessments/`

**Description:** Admin endpoint to view all assessments in the system (regardless of creator)

**Permission Requirements:**
- User must be authenticated
- User role must be `admin` or `assessment_manager`

**Query Parameters (Optional):**
- `type`: Filter by assessment type (`coding`, `non-coding`, `mix`)
- `is_published`: Filter by published status (`true`, `false`)
- `search`: Search in assessment titles

**Request:**
```http
GET /api/v1/assessments/all_assessments/
Authorization: Bearer <your_jwt_token>
```

**Request with Filters:**
```http
GET /api/v1/assessments/all_assessments/?type=coding&is_published=true&search=python
Authorization: Bearer <your_jwt_token>
```

**Response:**
```json
{
    "message": "All assessments retrieved successfully",
    "total_count": 5,
    "data": [
        {
            "id": 1,
            "title": "Python Programming Assessment",
            "description": "Basic Python skills test",
            "assessment_type": "coding",
            "created_by": {
                "id": 1,
                "email": "teacher1@example.com",
                "role": "assessment_manager"
            },
            "created_at": "2025-09-07T10:00:00Z",
            "updated_at": "2025-09-07T10:30:00Z",
            "is_published": true,
            "is_active": true,
            "total_marks": 100,
            "passing_marks": 60,
            "duration": 120,
            "is_proctored": true,
            "sections": [
                {
                    "id": 1,
                    "name": "Programming Fundamentals",
                    "questions_count": 5
                }
            ]
        },
        {
            "id": 2,
            "title": "Data Structures Quiz",
            "description": "Advanced data structures concepts",
            "assessment_type": "mix",
            "created_by": {
                "id": 2,
                "email": "teacher2@example.com",
                "role": "assessment_manager"
            },
            "created_at": "2025-09-06T14:00:00Z",
            "updated_at": "2025-09-06T15:00:00Z",
            "is_published": false,
            "is_active": true,
            "total_marks": 150,
            "passing_marks": 90,
            "duration": 180,
            "is_proctored": false,
            "sections": [
                {
                    "id": 2,
                    "name": "Theory",
                    "questions_count": 8
                },
                {
                    "id": 3,
                    "name": "Coding Problems",
                    "questions_count": 3
                }
            ]
        }
    ]
}
```

**Error Response (Permission Denied):**
```json
{
    "error": "Permission denied. Admin access required."
}
```

## Setup Instructions

### 1. Environment Variables

Create a `.env` file in your project root and add:

```env
# JDoodle API Credentials
JDOODLE_CLIENT_ID=your_jdoodle_client_id
JDOODLE_SECRET_KEY=your_jdoodle_secret_key
```

### 2. JDoodle API Setup

1. Visit [JDoodle.com](https://www.jdoodle.com)
2. Create a free account
3. Navigate to your dashboard
4. Copy the Client ID and Secret Key
5. Add them to your environment variables

### 3. Install Dependencies

```bash
pip install requests
```

### 4. Database Requirements

Ensure your `Question` model has the following field:

```python
class Question(models.Model):
    # ... other fields ...
    test_cases = models.JSONField(blank=True, null=True)
    # Expected format: {"examples": [...], "hidden": [...]}
```

## Code Components

### 1. URL Configuration (`api/urls.py`)

```python
from django.urls import path
from . import views

urlpatterns = [
    # ... other URLs ...
    path('runCode/', views.RunCodeView.as_view(), name="run code"),
    path('submitCode/', views.SubmitCodeView.as_view(), name="submit code"),
]
```

### 2. Views (`api/views.py`)

#### RunCodeView
```python
class RunCodeView(APIView):
    """
    API endpoint to execute code using JDoodle API
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Implementation details in the main code file
        pass
```

#### SubmitCodeView
```python
class SubmitCodeView(APIView):
    """
    API endpoint to submit code and validate against test cases
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        # Implementation details in the main code file
        pass
```

### 3. Serializers (`api/serializers.py`)

#### RunCodeSerializer
```python
class RunCodeSerializer(serializers.Serializer):
    script = serializers.CharField()
    language = serializers.CharField()
    versionIndex = serializers.CharField()
    stdin = serializers.CharField(required=False, allow_blank=True, default="")
    
    def validate(self, attrs):
        # Validates JDoodle credentials and input data
        pass
```

#### SubmitCodeSerializer
```python
class SubmitCodeSerializer(serializers.Serializer):
    script = serializers.CharField()
    language = serializers.CharField()
    versionIndex = serializers.CharField()
    question_id = serializers.IntegerField()
    
    def validate_question_id(self, value):
        # Validates question exists and is a coding question
        pass
```

### 4. Required Imports

Add these imports to your files:

**views.py:**
```python
import os
import requests as req
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
```

**serializers.py:**
```python
import os
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
```

## Usage Examples

### Example 1: Simple Python Code Execution

```python
import requests

url = "http://localhost:8000/api/runCode/"
data = {
    "script": "print('Hello, World!')",
    "language": "python3",
    "versionIndex": "3",
    "stdin": ""
}

response = requests.post(url, json=data)
print(response.json())
```

### Example 2: Code with Input

```python
import requests

url = "http://localhost:8000/api/runCode/"
data = {
    "script": "name = input('Enter your name: ')\nprint(f'Hello, {name}!')",
    "language": "python3",
    "versionIndex": "3",
    "stdin": "Alice"
}

response = requests.post(url, json=data)
print(response.json())
```

### Example 3: Code Validation Against Test Cases

```python
import requests

url = "http://localhost:8000/api/submitCode/?type=example"
data = {
    "script": "a, b = map(int, input().split())\nprint(a + b)",
    "language": "python3",
    "versionIndex": "3",
    "question_id": 1
}

response = requests.post(url, json=data)
print(response.json())
```

## Test Cases Format

Questions should have test cases in the following JSON format:

```json
{
    "examples": [
        {
            "input": "5 3",
            "output": "8"
        },
        {
            "input": "10 20",
            "output": "30"
        }
    ],
    "hidden": [
        {
            "input": "100 200",
            "output": "300"
        },
        {
            "input": "0 0",
            "output": "0"
        }
    ]
}
```

## Error Handling

### Common Error Responses

1. **Invalid Input:**
```json
{
    "errors": {
        "script": ["Script cannot be empty or contain only whitespace"]
    }
}
```

2. **Missing Credentials:**
```json
{
    "errors": {
        "configuration_error": "JDOODLE_CLIENT_ID not found in environment variables"
    }
}
```

3. **Execution Error:**
```json
{
    "error": "Internal server error"
}
```

4. **Question Not Found:**
```json
{
    "error": "Question with ID 999 not found"
}
```

### Error Types in Code Execution

- **Compilation Errors:** Syntax errors in the code
- **Runtime Errors:** Errors during code execution
- **Timeout Errors:** Code execution exceeds time limit
- **API Errors:** Issues with JDoodle API communication

## Security Considerations

### 1. Input Validation
- All inputs are validated using Django serializers
- Script length is limited to 50KB
- Input (stdin) is limited to 10KB

### 2. API Rate Limiting
- JDoodle API has rate limits based on your plan
- Free tier: 200 API calls per day
- Paid tiers: Higher limits available

### 3. Timeout Protection
- 30-second timeout on all API calls
- Prevents infinite loops and hanging requests

### 4. Environment Variables
- Sensitive credentials stored in environment variables
- Never expose API keys in code or version control

### 5. Assessment Access Control
- Standard assessments endpoint (`GET /api/v1/assessments/`) shows only user-created assessments
- Admin endpoint (`GET /api/v1/assessments/all_assessments/`) provides system-wide visibility
- Proper role-based permissions required for admin access
- User isolation maintained for regular operations

## Limitations

### 1. JDoodle API Limitations
- Daily execution limits based on plan
- Internet access not available in execution environment
- File system access is restricted
- Limited execution time per request

### 2. Language Versions
- Specific language versions available through JDoodle
- Version indices may change over time
- Some newer language features may not be available

### 3. Resource Constraints
- Memory usage is limited
- CPU time is restricted
- No persistent storage between executions

## Supported Languages and Version Indices

| Language | Version Index | Description |
|----------|---------------|-------------|
| python3 | 3 | Python 3.x |
| python2 | 2 | Python 2.x |
| java | 0 | Java 8+ |
| cpp | 0 | C++ (GCC) |
| cpp14 | 0 | C++14 |
| cpp17 | 0 | C++17 |
| c | 0 | C (GCC) |
| csharp | 0 | C# |
| javascript | 0 | JavaScript |
| nodejs | 0 | Node.js |

*Note: Version indices may vary. Check JDoodle documentation for the latest information.*

## Troubleshooting

### Common Issues

1. **"JDOODLE_CLIENT_ID not found"**
   - Ensure environment variables are properly set
   - Restart your Django development server

2. **"Unsupported language"**
   - Check the supported languages list
   - Verify the language string is correct

3. **"API Error: timeout"**
   - Check your internet connection
   - Verify JDoodle API is accessible

4. **"Question with ID X not found"**
   - Ensure the question exists in your database
   - Verify the question_id is correct

### Debug Mode

To enable debug mode, set the following in your settings:

```python
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'api.views': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Performance Optimization

### 1. Caching
Consider implementing caching for:
- Language validation
- Question data
- JDoodle API responses (for identical code)

### 2. Async Processing
For high-volume applications:
- Implement asynchronous code execution
- Use Celery for background task processing
- Queue management for API rate limiting

### 3. Database Optimization
- Index frequently queried fields
- Use select_related for foreign key relationships
- Implement pagination for large result sets

## Contributing

When contributing to this functionality:

1. Follow the existing code style and patterns
2. Add comprehensive tests for new features
3. Update documentation for any API changes
4. Ensure proper error handling and validation
5. Test with various programming languages

## License

This functionality is part of the PN Academy project. Please refer to the main project license for usage terms.

---

**Last Updated:** September 7, 2025  
**Version:** 1.0  
**Maintainer:** PN Academy Development Team
