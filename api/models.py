from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('assessment_manager', 'Assessment Manager'),
        ('proctor', 'Proctor'),
    ]

class EmailWhitelist(models.Model):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=128, choices=ROLE_CHOICES, default='candidate')

    def __str__(self):
        return self.email




# --------- USERS & ROLES ----------
class Role(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50, unique=True)
    permissions = models.JSONField() #to be updated

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=128, choices=ROLE_CHOICES, default='assessment_manager')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    username = None

    groups = models.ManyToManyField(
        Group,
        related_name='client_set',  
        blank=True,
        help_text='The groups this client belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='client_set',  
        blank=True,
        help_text='Specific permissions for this client.',
        verbose_name='user permissions'
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"

"""

{
    "assessment_name": "test",
    "assessment_type": enum("coding", "non-coding", "mix"),
    "passing_marks": 40,
    "total_sets": 3,
    "section_name": [<string>3] ["aptitude", ]
    "start_time": <UTC datetime format>,
    "end_time": <UTC datetime format>,
    "is_electron_only": <boolean>,
    "num_of_ai_generated_questions": <int>,
    "questions": [
     {
        "question_type": enum("coding", "non-coding")
        "section_id": <int> (less than equal to num_of_sections),
        "set_number": <int>,
        "question_text" <string> (any references should be starting from $1 and then number goes up)
        "options": [<string>,] (can add references as well)
        "positive_marks": <int>,
        "negative_marks": <int>,
        "time_limit": <UTC datetime format>,
        "test_cases":[
            {
                ""
            }
        ]

     }
    
    
    ]
}



"""




# --------- ASSESSMENTS ----------
ASSESSMENT_TYPE_CHOICES = [
    ('coding', 'Coding'),
    ('non-coding', 'Non-Coding'),
    ('mix', 'Mix'),
]

class Assessment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # maps to assessment_description
<<<<<<< Updated upstream
=======
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPE_CHOICES, default='mix')
>>>>>>> Stashed changes
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_assessments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)  # NEW
    total_marks = models.PositiveIntegerField()
    passing_marks = models.PositiveIntegerField()
<<<<<<< Updated upstream
=======
    total_sets = models.PositiveIntegerField(default=1)
>>>>>>> Stashed changes
    duration = models.PositiveIntegerField(help_text="Duration in minutes", null=True, blank=True)  
    set_number = models.PositiveIntegerField(default=1)
    is_proctored = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_electron_only = models.BooleanField(default=False)
    ai_generated_questions = models.PositiveIntegerField(default=0)  
    attachments = models.JSONField(blank=True, null=True)
    is_offline = models.BooleanField(default=False)
    universal_code = models.CharField(max_length=255,null=True, blank=True)



class SampleJSON(models.Model):
    data = models.JSONField()
"""
{
  "assessment_name": "test",
  "assessment_type": "mix", 
  "assessment_description": ""
  "passing_marks": 40,
  "total_sets": 3,
  "section_names": ["aptitude", "coding", "logical"], 
  "section_descriptions":["desc 1", "desc 2", "desc 3"]
  "start_time": "2025-08-10T09:00:00Z",
  "end_time": "2025-08-10T12:00:00Z",
  "is_electron_only": false,
  "num_of_ai_generated_questions": 5,
  "is_proctored": true,
  "is_published": <boolean>
  "attachments": [<url>]
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1, 
      "set_number": 1,
      "question_text": "What is the capital of France? $1",
      "options": [
        "Paris",
        "London",
        "Rome",
        "Berlin"
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
      "question_text": "Write a function to reverse a string. $1",
      "description": "You are given a string, reverse it without using built-in reverse methods.",
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
            "input": "abc",
            "output": "cba"
          }
        ],
        "hidden": [
          {
            "input": "OpenAI",
            "output": "IAnepO"
          }
        ]
      }
    }
  ]
}


"""

"""
we've to create a serializer which will ingest data in this way

First we've to create the Assessment object where title is set as assessment_name of input json, description as assessment_description, type as assessment_type
created by is given the value of request.user, is_published is set as is_published, passing_marks is set as passing_marks, total_marks is calculated by going through the array of
questions in the input json and summing up the positive marks with common set_number, duration is also calculated by going through the questions array and summing up the time limit with common set_number of each entity,
total_sets is set from num_of_sets, is_proctored is set from is_proctored, start_time and end_time are set from start_time and end_time, is_electron is set from is_electron,
num_of_ai_generated_questions set from num_of_ai_generated_questions


then, we've to create single/multiple Section object, where assessment is set the assessment object that we just created, 
we'll have an array of section_name in the input json, we've to iterate through the array, and then create a Section for each, first name at that index will be set
as section_name of section object, we also a section_descriptions paramter with an array of objects, for this particular index we've to set the description paarameter of 
sectino object as value at this index of section_descriptions object, store the index as section_order of the section object, total_marks for a section_object is calculated by
going through the questions array and summing up positive_marks for common set_number, duration of set is also calculated from going through the questions array,

after this we've to create Question object, this is done by iterating through the questions array, which is an array of objects, now for each object, we've to create a question
question_type is set from question_type, section is set from section_id (we've to assign the section object created previously with section_order = section_id here), 
set_number is set from set_number, question_text is set from question_text, the array of options is set as options as JSONField, options[correct_option_index] is set as 
correct_answer again in JSONField, marks is set as positive_marks, negative_marks is set as negative_marks, question_order is set as index of the current question, 
constraints array is set as constraints JSONfield, test_cases json is set as test_cases JSONField, time_limit as set as time_limit
"""





# --------- SECTIONS ----------
class Section(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    num_of_questions = models.IntegerField(default=0)
    total_marks = models.PositiveIntegerField()
    negative_mark_per_question = models.PositiveIntegerField(default = 0)
    duration = models.PositiveIntegerField(help_text="Duration in minutes", null=True, blank=True)
    section_order = models.PositiveIntegerField(default=0)  # Added field for section ordering


# --------- QUESTIONS ----------
class Question(models.Model):
    QuestionTypeChoices = [
        ("coding", "Coding"),
        ("non-coding", "Non Coding"),
    ]
    
    
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="questions") #issue
    question_text = models.TextField()
    question_type = models.CharField(max_length=255, choices=QuestionTypeChoices, default="non-coding")
    options = models.JSONField(blank=True, null=True)  
    correct_answer = models.JSONField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # Problem description
    constraints = models.JSONField(blank=True, null=True)  # ["1 <= length <= 1000", ...]
    expected_output = models.TextField(blank=True, null=True)
    test_cases = models.JSONField(blank=True, null=True)  # { "examples": [...], "hidden": [...] }
<<<<<<< Updated upstream
=======
    # Added fields for question management
    set_number = models.PositiveIntegerField(default=1)  # Which set this question belongs to
    marks = models.PositiveIntegerField(default=0)  # Positive marks for correct answer
    negative_marks = models.IntegerField(default=0)  # Negative marks for wrong answer
    question_order = models.PositiveIntegerField(default=0)  # Order of question within section
    time_limit = models.PositiveIntegerField(default=0)  # Time limit in seconds
>>>>>>> Stashed changes

# --------- ASSESSMENT ASSIGNMENTS ----------
class AssessmentAssignment(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="assignments")
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="candidate_assignments")
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_assessments")
    assigned_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    unique_test_url = models.URLField(blank=True, null=True)
    email_sent = models.BooleanField(default=False)
    is_marked_for_assignment = models.BooleanField(default=False)


# --------- REPORT ----------
class Report(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    assignment = models.ForeignKey(AssessmentAssignment, on_delete=models.CASCADE, related_name="reports")
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="candidate_reports")
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50)
    total_marks = models.FloatField()
    obtained_marks = models.FloatField()
    percentage = models.FloatField()
    percentile = models.FloatField()
    position = models.PositiveIntegerField(null=True, blank=True)
    window_switch_count = models.PositiveIntegerField(default=0)
    is_kicked_out = models.BooleanField(default=False)
    kicked_out_reason = models.TextField(blank=True, null=True)
    is_cheating = models.BooleanField(default=False)
    cheating_reason = models.TextField(blank=True, null=True)
    proctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="proctored_reports")
    set_number = models.PositiveIntegerField(default=1)


# --------- SECTION REPORT ----------
class SectionReport(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="section_reports")
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    obtained_marks = models.FloatField()
    total_questions = models.PositiveIntegerField()
    attempted_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField()
    wrong_answers = models.PositiveIntegerField()


# --------- QUESTION ATTEMPTS ----------
class QuestionAttempt(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="question_attempts")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    selected_answer = models.JSONField(blank=True, null=True)
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.FloatField(default=0)
    time_taken = models.PositiveIntegerField(null=True, blank=True)
    is_attempted = models.BooleanField(default=False)


# --------- PROCTORING SESSIONS ----------
class ProctoringSession(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="proctoring_sessions")
    proctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="proctoring_sessions")
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50)
    recordings = models.JSONField(blank=True, null=True)
    incidents = models.JSONField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)


# --------- PROCTORING SNAPSHOTS ----------
class ProctoringSnapshot(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    session = models.ForeignKey(ProctoringSession, on_delete=models.CASCADE, related_name="snapshots")
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField()
    image_url = models.URLField()
    suspicious_activity = models.BooleanField(default=False)
    activity_type = models.CharField(max_length=100, blank=True, null=True)


# --------- ASSESSMENT REPORTS ----------
class AssessmentReport(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="assessment_reports")
    generated_at = models.DateTimeField(auto_now_add=True)
    total_candidates = models.PositiveIntegerField()
    attempted_candidates = models.PositiveIntegerField()
    not_attempted_candidates = models.PositiveIntegerField()
    passed_candidates = models.PositiveIntegerField()
    failed_candidates = models.PositiveIntegerField()
    average_score = models.FloatField()
    highest_score = models.FloatField()
    lowest_score = models.FloatField()
    report_data = models.JSONField()
    is_published = models.BooleanField(default=False)


# --------- CANDIDATE REPORTS ----------
class CandidateReport(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="candidate_reports")
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    email_sent = models.BooleanField(default=False)
    report_data = models.JSONField()
    feedback = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)


# --------- NOTIFICATIONS ----------
class Notification(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_entity_id = models.CharField(max_length=50, blank=True, null=True)
    related_entity_type = models.CharField(max_length=100, blank=True, null=True)


# --------- CSV UPLOADS ----------
class CSVUpload(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    total_records = models.PositiveIntegerField()
    processed_records = models.PositiveIntegerField()
    status = models.CharField(max_length=50)
    errors = models.JSONField(blank=True, null=True)
    
class Student(models.Model):
    csv_upload = models.ForeignKey(CSVUpload, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email
    
class TestCode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='test_codes')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='test_codes')
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    used_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.code} - {self.student.email}"
    
    class Meta:
        unique_together = ('student', 'assessment')
        
        
class AssessmentFile(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='files')
    filename = models.CharField(max_length=255)
    s3_key = models.CharField(max_length=500)  # Full S3 path
    s3_url = models.URLField(blank=True, null=True)  # Full S3 URL
    file_size = models.PositiveIntegerField(default=0)  # File size in bytes
    upload_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Upload'),
            ('uploaded', 'Uploaded'),
            ('failed', 'Upload Failed')
        ],
        default='pending'
    )
    presigned_url = models.URLField(max_length=500,blank=True, null=True)  # For upload
    presigned_url_expires = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('assessment', 'filename')  # Ensure filename is unique per assessment
    
    def __str__(self):
        return f"{self.assessment.title} - {self.filename}"
    
    @property
    def s3_full_url(self):
        """Generate full S3 URL"""
        from django.conf import settings
        if self.s3_key:
            return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_REGION_NAME}.amazonaws.com/{self.s3_key}"
        return None
    