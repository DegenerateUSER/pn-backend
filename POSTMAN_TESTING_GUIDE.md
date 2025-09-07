# Proctoring Results API - Postman Testing Guide

## 🚀 Overview
This guide provides step-by-step instructions for testing the Proctoring Results API using Postman. The API retrieves proctoring session data from AWS DynamoDB, including session IDs, flags, risk scores, and timestamps.

## 📋 Prerequisites
- Django server running on `http://localhost:8000`
- Valid user account in the system
- Postman installed
- AWS DynamoDB table "ProctoringResults" with data

## 🔐 Step 1: Authentication (Get JWT Token)

### Login Request
```
POST http://localhost:8000/api/v1/login/
```

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "email": "your_email@example.com",
  "password": "your_password"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "your_email@example.com",
    "role": "admin"
  }
}
```

**⚠️ Important:** Copy the `access` token from the response - you'll need it for all subsequent requests.

## 📊 Step 2: Testing Proctoring Results Endpoints

### 2.1 Get All Proctoring Results

**Request:**
```
GET http://localhost:8000/api/v1/proctoring-results/
```

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Proctoring results retrieved successfully",
  "data": [
    {
      "session_id": "std03",
      "flags": [
        "MULTIPLE_FACES_DETECTED",
        "PROHIBITED_OBJECT_BOOK"
      ],
      "risk_score": 90,
      "timestamp": "2025-09-07T13:44:04.252893",
      "s3_key": "manual-test-123/std03.jpg",
      "rekognition_face_response": {...},
      "rekognition_label_response": {...}
    },
    {
      "session_id": "std02",
      "flags": [
        "MULTIPLE_FACES_DETECTED",
        "PROHIBITED_OBJECT_BOOK"
      ],
      "risk_score": 90,
      "timestamp": "2025-09-07T13:42:41.101883",
      "s3_key": "manual-test-123/std02.jpg",
      "rekognition_face_response": {...},
      "rekognition_label_response": {...}
    }
  ],
  "count": 2,
  "filters_applied": null
}
```

### 2.2 Get Specific Session by ID

**Request:**
```
GET http://localhost:8000/api/v1/proctoring-results/std03/
```

**Headers:**
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
Content-Type: application/json
```

**Expected Response:**
```json
{
  "success": true,
  "message": "Proctoring result retrieved successfully",
  "data": {
    "session_id": "std03",
    "flags": [
      "MULTIPLE_FACES_DETECTED",
      "PROHIBITED_OBJECT_BOOK"
    ],
    "risk_score": 90,
    "timestamp": "2025-09-07T13:44:04.252893",
    "s3_key": "manual-test-123/std03.jpg",
    "rekognition_face_response": {...},
    "rekognition_label_response": {...}
  }
}
```

## 🔍 Step 3: Testing Filters

### 3.1 Filter by Session ID

**Request:**
```
GET http://localhost:8000/api/v1/proctoring-results/?session_id=std01
```

### 3.2 Filter by Risk Score (Exact)

**Request:**
```
GET http://localhost:8000/api/v1/proctoring-results/?risk_score=90
```

### 3.3 Filter by Minimum Risk Score

**Request:**
```
GET http://localhost:8000/api/v1/proctoring-results/?min_risk_score=80
```

### 3.4 Filter by Maximum Risk Score

**Request:**
```
GET http://localhost:8000/api/v1/proctoring-results/?max_risk_score=95
```

### 3.5 Filter Sessions with Flags

**Request:**
```
GET http://localhost:8000/api/v1/proctoring-results/?has_flags=true
```

### 3.6 Filter by Date Range

**Request:**
```
GET http://localhost:8000/api/v1/proctoring-results/?start_date=2025-09-07T13:00:00&end_date=2025-09-07T14:00:00
```

### 3.7 Combine Multiple Filters

**Request:**
```
GET http://localhost:8000/api/v1/proctoring-results/?min_risk_score=80&has_flags=true
```

**Expected Response (with filters):**
```json
{
  "success": true,
  "message": "Proctoring results retrieved successfully",
  "data": [
    {
      "session_id": "std03",
      "flags": ["MULTIPLE_FACES_DETECTED", "PROHIBITED_OBJECT_BOOK"],
      "risk_score": 90,
      "timestamp": "2025-09-07T13:44:04.252893",
      "s3_key": "manual-test-123/std03.jpg"
    }
  ],
  "count": 1,
  "filters_applied": {
    "min_risk_score": 80,
    "has_flags": true
  }
}
```

## 📝 Postman Collection Setup

### Create a New Collection
1. Open Postman
2. Click "New" → "Collection"
3. Name it "Proctoring Results API"

### Add Environment Variables
1. Click the gear icon → "Manage Environments"
2. Create new environment: "Local Development"
3. Add variables:
   ```
   base_url: http://localhost:8000/api/v1
   jwt_token: (leave empty - will be set after login)
   ```

### Setup Requests in Collection

#### 1. Login Request
- **Name:** "Login - Get JWT Token"
- **Method:** POST
- **URL:** `{{base_url}}/login/`
- **Body:** JSON with your credentials
- **Test Script:**
  ```javascript
  if (pm.response.code === 200) {
      const response = pm.response.json();
      pm.environment.set("jwt_token", response.access);
      pm.test("Login successful", function () {
          pm.expect(response.success).to.be.true;
      });
  }
  ```

#### 2. Get All Results
- **Name:** "Get All Proctoring Results"
- **Method:** GET
- **URL:** `{{base_url}}/proctoring-results/`
- **Headers:** `Authorization: Bearer {{jwt_token}}`

#### 3. Get Specific Result
- **Name:** "Get Specific Result"
- **Method:** GET
- **URL:** `{{base_url}}/proctoring-results/std03/`
- **Headers:** `Authorization: Bearer {{jwt_token}}`

#### 4. Filter Tests (create separate requests for each filter)
- **Filter by Session:** `{{base_url}}/proctoring-results/?session_id=std01`
- **Filter by Risk Score:** `{{base_url}}/proctoring-results/?min_risk_score=80`
- **Filter with Flags:** `{{base_url}}/proctoring-results/?has_flags=true`

## ⚠️ Common Issues & Solutions

### 1. 404 Not Found
**Problem:** URL not found
**Solution:** Make sure you're using `/api/v1/` prefix in the URL

### 2. 401 Unauthorized
**Problem:** Missing or invalid JWT token
**Solution:** 
- Get a fresh token using the login endpoint
- Ensure the Authorization header is properly set
- Check token expiration

### 3. 403 Forbidden
**Problem:** User doesn't have permission
**Solution:** Check user role and permissions

### 4. 500 Internal Server Error
**Problem:** Server-side error (like the Decimal issue we fixed)
**Solution:** Check Django server logs for detailed error messages

### 5. Empty Response
**Problem:** No data in DynamoDB or connection issues
**Solution:** 
- Verify AWS credentials are configured
- Check DynamoDB table exists and has data
- Verify region is set to eu-central-1

## 🧪 Test Scenarios

### Scenario 1: Basic Functionality Test
1. Login to get JWT token
2. Get all proctoring results
3. Verify response structure and data

### Scenario 2: Filtering Test
1. Test each filter parameter individually
2. Combine multiple filters
3. Verify filter logic works correctly

### Scenario 3: Edge Cases
1. Test with non-existent session ID (should return 404)
2. Test with invalid filter values (should return 400)
3. Test without authentication (should return 401)

### Scenario 4: Performance Test
1. Request all results and measure response time
2. Test with large date ranges
3. Verify pagination works for large datasets

## 📊 Sample Test Data

Based on your CSV data, you can test with these session IDs:
- `std01`
- `std02` 
- `std03`

Expected risk scores: `90`

Expected flags:
- `MULTIPLE_FACES_DETECTED`
- `PROHIBITED_OBJECT_BOOK`

## 🎯 Success Criteria

**✅ All tests pass if:**
- Login returns JWT token
- All endpoints return 200 status
- Response structure matches expected format
- Filters work correctly
- Data transformation is accurate (Decimal → int, Flags array parsing)
- Authentication is enforced

## 📞 Support

If you encounter issues:
1. Check Django server logs for detailed errors
2. Verify AWS DynamoDB connectivity
3. Ensure JWT token is not expired
4. Validate request format and headers

## 🔗 Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/login/` | POST | Get JWT token |
| `/api/v1/proctoring-results/` | GET | List all/filtered results |
| `/api/v1/proctoring-results/{session_id}/` | GET | Get specific result |

**Required Headers for API calls:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```
