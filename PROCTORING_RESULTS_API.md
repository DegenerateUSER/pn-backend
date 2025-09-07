# Proctoring Results API Implementation

## Overview
Added new API endpoints to retrieve proctoring results from AWS DynamoDB table "ProctoringResults" located in the eu-central-1 region. The API returns the key fields: **session_id**, **flags**, **risk_score**, and **timestamp**.

## Table Schema
Based on the actual DynamoDB table structure:
- **SessionID** (Primary Key) - Session identifier (e.g., "std01", "std02")
- **Flags** - Array of flags with detected violations (e.g., MULTIPLE_FACES_DETECTED, PROHIBITED_OBJECT_BOOK)
- **RiskScore** - Numeric risk score (e.g., 90)
- **Timestamp** - ISO timestamp of the detection
- **RekognitionFaceResponse** - AWS Rekognition face detection response (JSON)
- **RekognitionLabelResponse** - AWS Rekognition label detection response (JSON)
- **S3Key** - S3 path to the analyzed image

## Files Modified

### 1. api/utils.py
- Added `ProctoringDynamoDBHandler` class
- Handles connection to DynamoDB in eu-central-1 region
- Provides methods for:
  - `get_all_proctoring_results()` - Retrieve all items with pagination support
  - `get_proctoring_result_by_session_id(session_id)` - Get specific item by SessionID
  - `query_proctoring_results_by_filter(filter_params)` - Filter results with parameters
- Transforms raw DynamoDB data to clean format with key fields
- Parses Flags array and JSON responses properly

### 2. api/views.py
- Added `ProctoringResultsView` class (APIView)
  - GET endpoint for retrieving all or filtered proctoring results
  - Supports comprehensive query parameters for filtering
  - JWT authentication required
- Added `ProctoringResultDetailView` class (APIView)
  - GET endpoint for retrieving specific proctoring result by SessionID
  - JWT authentication required

### 3. api/urls.py
- Added two new URL patterns:
  - `proctoring-results/` - List/filter proctoring results
  - `proctoring-results/<session_id>/` - Get specific result by SessionID

## API Endpoints

### Get All Proctoring Results
```
GET /api/proctoring-results/
```
**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Query Parameters (optional):**
- `session_id` - Filter by specific session ID (e.g., "std01")
- `risk_score` - Filter by exact risk score (e.g., 90)
- `min_risk_score` - Filter by minimum risk score (e.g., 50)
- `max_risk_score` - Filter by maximum risk score (e.g., 100)
- `start_date` - Filter by start date (ISO format: "2025-09-07T13:42:00")
- `end_date` - Filter by end date (ISO format: "2025-09-07T14:00:00")
- `has_flags` - Filter sessions with flags (true/false)

**Example Requests:**
```bash
# Get all results
GET /api/proctoring-results/

# Get results for specific session
GET /api/proctoring-results/?session_id=std01

# Get high-risk sessions
GET /api/proctoring-results/?min_risk_score=80

# Get sessions with flags
GET /api/proctoring-results/?has_flags=true

# Get sessions in date range
GET /api/proctoring-results/?start_date=2025-09-07T13:00:00&end_date=2025-09-07T14:00:00
```

**Response:**
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
    }
  ],
  "count": 1,
  "filters_applied": {
    "session_id": "std03"
  }
}
```

### Get Specific Proctoring Result
```
GET /api/proctoring-results/{session_id}/
```
**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Example:**
```bash
GET /api/proctoring-results/std01/
```

**Response:**
```json
{
  "success": true,
  "message": "Proctoring result retrieved successfully",
  "data": {
    "session_id": "std01",
    "flags": [
      "MULTIPLE_FACES_DETECTED",
      "PROHIBITED_OBJECT_BOOK"
    ],
    "risk_score": 90,
    "timestamp": "2025-09-07T13:44:04.252893",
    "s3_key": "manual-test-123/std01.jpg",
    "rekognition_face_response": {...},
    "rekognition_label_response": {...}
  }
}
```

## Data Transformation
The API transforms raw DynamoDB data to provide clean, structured responses:

### Input (DynamoDB format):
```json
{
  "SessionID": "std01",
  "Flags": [{"S": "MULTIPLE_FACES_DETECTED"}, {"S": "PROHIBITED_OBJECT_BOOK"}],
  "RiskScore": "90",
  "Timestamp": "2025-09-07T13:44:04.252893",
  "RekognitionFaceResponse": "{\"FaceDetails\": [...]}",
  "RekognitionLabelResponse": "{\"Labels\": [...]}"
}
```

### Output (API response):
```json
{
  "session_id": "std01",
  "flags": ["MULTIPLE_FACES_DETECTED", "PROHIBITED_OBJECT_BOOK"],
  "risk_score": 90,
  "timestamp": "2025-09-07T13:44:04.252893",
  "rekognition_face_response": {"FaceDetails": [...]},
  "rekognition_label_response": {"Labels": [...]}
}
```

## Authentication & Permissions
- Both endpoints require JWT authentication (`IsAuthenticated` permission)
- Uses existing authentication system from the project
- Follows the same authentication patterns as other endpoints

## Error Handling
- Proper HTTP status codes (200, 400, 404, 500)
- Structured error responses following project patterns
- DynamoDB client error handling
- Input validation for numeric parameters
- Generic exception handling for unexpected errors

## AWS Configuration
- Uses existing AWS credentials from project settings
- Specifically connects to eu-central-1 region for DynamoDB
- Leverages existing boto3 configuration

## Testing
To test the endpoints:

1. Ensure you have valid JWT token
2. Make GET request to `/api/proctoring-results/`
3. Try filtering with query parameters:
   ```bash
   curl -H "Authorization: Bearer <token>" \
        "http://localhost:8000/api/proctoring-results/?session_id=std01"
   ```
4. Test specific result retrieval:
   ```bash
   curl -H "Authorization: Bearer <token>" \
        "http://localhost:8000/api/proctoring-results/std01/"
   ```

## Key Features
- ✅ **Focused Data**: Returns the 4 key fields you requested (session_id, flags, risk_score, timestamp)
- ✅ **Flexible Filtering**: Multiple query parameters for different use cases
- ✅ **Risk Score Analysis**: Support for risk score range filtering
- ✅ **Date Range Queries**: Filter by timestamp ranges
- ✅ **Flag Detection**: Filter sessions that have violations
- ✅ **Clean Data Format**: Parsed and transformed responses
- ✅ **Additional Context**: Includes S3 keys and Rekognition responses for deeper analysis

## Future Enhancements
- Add aggregation endpoints (statistics, trends)
- Implement bulk export functionality
- Add real-time notifications for high-risk sessions
- Consider adding GraphQL support for complex queries
