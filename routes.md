/api/v1/register/ — Signup
/api/v1/login/ — Login (returns JWT)
/api/v1/reset-password/ — Reset password (JWT required)

/api/v1/assessment — List or create assessments (alias)
/api/v1/assessment/{id} — Retrieve, update, or delete assessment (alias)

/api/v1/assessments/ — List or create assessments
/api/v1/assessments/{id}/ — Retrieve, update, or delete assessment

/api/v1/users/ — List or create users (admin only)
/api/v1/users/{id}/ — Retrieve, update, or delete user

/api/v1/students/ — List students
/api/v1/students/{id}/ — Retrieve student details

/api/v1/students-list/ — List uploaded student CSV batches
/api/v1/students-list/{id}/ — Retrieve CSV batch details

/api/v1/uploadStudents/ — Upload students via CSV
/api/v1/assign-assessment/ — Assign assessment to a CSV cohort

/api/v1/assessments/{assessment_id}/test-codes/ — List test codes for an assessment
/api/v1/csv-uploads/{csv_upload_id}/test-codes/ — List test codes for a CSV upload

/api/v1/sendEmail/ — Send bulk emails to cohort

/api/v1/upload/ — Generate S3 presigned upload URL
/api/v1/fileStatus/ — Check uploaded file status
/api/v1/files/{assessment_id} — List files for an assessment

/api/v1/uploadStudentImage/ — Upload student image for proctoring
/api/v1/reports/student — Generate a student report
