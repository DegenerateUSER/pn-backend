# Assessment Examples Collection

This document contains various assessment examples with different structures, topics, and complexities that can be used for creating assessments via POST requests.

---

## 1. Data Science Assessment

```json
{
  "assessment_name": "Data Science Professional Assessment",
  "assessment_type": "mix",
  "assessment_description": "Comprehensive data science assessment covering statistics, machine learning, and data visualization. Reference the data science handbook in $1 and coding best practices in $2.",
  "passing_marks": 150,
  "num_of_sets": 2,
  "section_names": ["Statistics & Mathematics", "Machine Learning", "Data Visualization"],
  "section_descriptions": [
    "Probability, statistics, linear algebra, and mathematical foundations",
    "Supervised learning, unsupervised learning, model evaluation and selection",
    "Data visualization tools, chart types, and storytelling with data"
  ],
  "start_time": "2025-12-15T09:00:00Z",
  "end_time": "2025-12-15T14:00:00Z",
  "is_electron_only": false,
  "is_proctored": true,
  "is_published": false,
  "num_of_ai_generated_questions": 3,
  "attachments": [
    "https://s3.amazonaws.com/assessments/data-science-handbook.pdf",
    "https://s3.amazonaws.com/assessments/python-ml-standards.pdf"
  ],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "According to the statistical methods in $1, which test should be used to compare means of two independent groups?",
      "options": ["Chi-square test", "T-test", "ANOVA", "Mann-Whitney U test"],
      "correct_option_index": 1,
      "positive_marks": 25,
      "negative_marks": -5,
      "time_limit": 180
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Implement a statistical analysis function following the guidelines in $1 and coding standards from $2.",
      "description": "Create a function that performs hypothesis testing and returns statistical significance",
      "constraints": ["Use scipy.stats library", "Return p-value and test statistic", "Handle edge cases"],
      "positive_marks": 50,
      "negative_marks": 0,
      "time_limit": 2400,
      "test_cases": {
        "examples": [
          {"input": "[1,2,3,4,5], [2,3,4,5,6]", "output": "{'p_value': 0.347, 'statistic': -1.0}"},
          {"input": "[10,20,30], [15,25,35]", "output": "{'p_value': 0.423, 'statistic': -1.5}"}
        ],
        "hidden": [
          {"input": "[], [1,2,3]", "output": "Error handling for empty arrays"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Based on the ML algorithms covered in $1, which algorithm is best for handling non-linear relationships?",
      "options": ["Linear Regression", "Random Forest", "Logistic Regression", "Naive Bayes"],
      "correct_option_index": 1,
      "positive_marks": 25,
      "negative_marks": -5,
      "time_limit": 180
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Build a machine learning pipeline following the architecture patterns described in $1 and coding standards in $2.",
      "description": "Create a complete ML pipeline with preprocessing, training, and evaluation",
      "constraints": ["Use scikit-learn", "Include cross-validation", "Handle missing values"],
      "positive_marks": 50,
      "negative_marks": 0,
      "time_limit": 3000,
      "test_cases": {
        "examples": [
          {"input": "Training dataset with missing values", "output": "Trained model with accuracy > 0.8"},
          {"input": "Test dataset", "output": "Predictions with confidence scores"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "According to the visualization principles in $1, which chart type is best for showing correlation between variables?",
      "options": ["Bar chart", "Scatter plot", "Pie chart", "Line chart"],
      "correct_option_index": 1,
      "positive_marks": 25,
      "negative_marks": -5,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "Create interactive data visualizations following the guidelines in $1 and standards from $2.",
      "description": "Build a dashboard with multiple chart types and interactive features",
      "constraints": ["Use matplotlib or plotly", "Include at least 3 chart types", "Add interactive elements"],
      "positive_marks": 50,
      "negative_marks": 0,
      "time_limit": 2400,
      "test_cases": {
        "examples": [
          {"input": "Sample dataset", "output": "Interactive dashboard with multiple visualizations"},
          {"input": "Time series data", "output": "Line charts with zoom and pan features"}
        ]
      }
    }
  ]
}
```

---

## 2. Cybersecurity Assessment

```json
{
  "assessment_name": "Cybersecurity Specialist Evaluation",
  "assessment_type": "mix",
  "assessment_description": "Advanced cybersecurity assessment covering network security, cryptography, and ethical hacking. Refer to security frameworks in $1.",
  "passing_marks": 120,
  "num_of_sets": 1,
  "section_names": ["Network Security", "Cryptography", "Penetration Testing"],
  "section_descriptions": [
    "Network protocols, firewalls, intrusion detection systems",
    "Encryption algorithms, digital signatures, key management",
    "Vulnerability assessment, ethical hacking techniques"
  ],
  "start_time": "2025-12-20T10:00:00Z",
  "end_time": "2025-12-20T15:00:00Z",
  "is_electron_only": true,
  "is_proctored": true,
  "is_published": false,
  "num_of_ai_generated_questions": 2,
  "attachments": [
    "https://s3.amazonaws.com/assessments/nist-cybersecurity-framework.pdf"
  ],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "According to the NIST framework in $1, which layer is most vulnerable to DDoS attacks?",
      "options": ["Physical Layer", "Network Layer", "Application Layer", "Data Link Layer"],
      "correct_option_index": 2,
      "positive_marks": 20,
      "negative_marks": -3,
      "time_limit": 150
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Implement a network security scanner following the guidelines in $1.",
      "description": "Create a port scanner that identifies open ports and running services",
      "constraints": ["Use Python socket library", "Handle timeouts gracefully", "Scan common ports"],
      "positive_marks": 40,
      "negative_marks": 0,
      "time_limit": 2700,
      "test_cases": {
        "examples": [
          {"input": "localhost, [22,80,443]", "output": "{'22': 'closed', '80': 'open', '443': 'closed'}"},
          {"input": "192.168.1.1, [21,22,23]", "output": "Port scan results with service detection"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Based on cryptographic standards in $1, which algorithm provides the highest security for data encryption?",
      "options": ["DES", "AES-128", "AES-256", "3DES"],
      "correct_option_index": 2,
      "positive_marks": 20,
      "negative_marks": -3,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Develop an encryption/decryption system following the security standards outlined in $1.",
      "description": "Implement AES encryption with secure key generation and management",
      "constraints": ["Use cryptography library", "Generate secure random keys", "Handle padding correctly"],
      "positive_marks": 40,
      "negative_marks": 0,
      "time_limit": 2400,
      "test_cases": {
        "examples": [
          {"input": "plaintext: 'Hello World'", "output": "Encrypted data and decryption verification"},
          {"input": "plaintext: 'Sensitive Data'", "output": "Secure encryption with key management"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "According to penetration testing methodologies in $1, what is the first phase of ethical hacking?",
      "options": ["Exploitation", "Reconnaissance", "Scanning", "Maintaining Access"],
      "correct_option_index": 1,
      "positive_marks": 20,
      "negative_marks": -3,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "Create a vulnerability assessment tool based on the methodologies described in $1.",
      "description": "Build a tool that identifies common web application vulnerabilities",
      "constraints": ["Scan for SQL injection", "Check for XSS vulnerabilities", "Test for authentication bypass"],
      "positive_marks": 40,
      "negative_marks": 0,
      "time_limit": 3000,
      "test_cases": {
        "examples": [
          {"input": "http://example.com/login", "output": "Vulnerability report with severity ratings"},
          {"input": "http://testsite.com/search", "output": "XSS and injection vulnerability assessment"}
        ]
      }
    }
  ]
}
```

---

## 3. Mobile App Development Assessment

```json
{
  "assessment_name": "Mobile Development Expert Assessment",
  "assessment_type": "coding",
  "assessment_description": "Advanced mobile development assessment focusing on React Native and native mobile development patterns.",
  "passing_marks": 80,
  "num_of_sets": 2,
  "section_names": ["React Native Development", "Mobile UI/UX"],
  "section_descriptions": [
    "React Native components, navigation, state management, and native integrations",
    "Mobile design patterns, responsive layouts, and user experience optimization"
  ],
  "start_time": "2025-12-25T09:00:00Z",
  "end_time": "2025-12-25T12:00:00Z",
  "is_electron_only": false,
  "is_proctored": false,
  "is_published": false,
  "num_of_ai_generated_questions": 0,
  "attachments": [],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Create a React Native component with navigation and state management.",
      "description": "Build a user profile screen with navigation between tabs and local state management",
      "constraints": ["Use React Navigation", "Implement useState and useEffect", "Handle async operations"],
      "positive_marks": 40,
      "negative_marks": 0,
      "time_limit": 2400,
      "test_cases": {
        "examples": [
          {"input": "User data object", "output": "Rendered profile screen with navigation"},
          {"input": "Navigation params", "output": "Proper screen transitions"}
        ]
      }
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Design a responsive mobile layout with accessibility features.",
      "description": "Create a mobile-first design that adapts to different screen sizes and includes accessibility support",
      "constraints": ["Use Flexbox for layout", "Add accessibility labels", "Support both iOS and Android"],
      "positive_marks": 40,
      "negative_marks": 0,
      "time_limit": 2100,
      "test_cases": {
        "examples": [
          {"input": "Small screen device", "output": "Optimized layout for mobile"},
          {"input": "Large screen device", "output": "Adapted layout for tablets"}
        ]
      }
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 2,
      "question_text": "Implement offline functionality and data synchronization.",
      "description": "Build a feature that works offline and syncs data when connection is restored",
      "constraints": ["Use AsyncStorage", "Implement network detection", "Handle sync conflicts"],
      "positive_marks": 40,
      "negative_marks": 0,
      "time_limit": 2700,
      "test_cases": {
        "examples": [
          {"input": "Offline mode", "output": "Data stored locally and accessible"},
          {"input": "Online mode", "output": "Data synchronized with server"}
        ]
      }
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 2,
      "question_text": "Create an animated mobile interface with gesture handling.",
      "description": "Build an interactive interface with smooth animations and touch gestures",
      "constraints": ["Use React Native Animated", "Implement pan gestures", "Add haptic feedback"],
      "positive_marks": 40,
      "negative_marks": 0,
      "time_limit": 2400,
      "test_cases": {
        "examples": [
          {"input": "Swipe gesture", "output": "Smooth animation response"},
          {"input": "Long press", "output": "Haptic feedback and action menu"}
        ]
      }
    }
  ]
}
```

---

## 4. DevOps Engineer Assessment

```json
{
  "assessment_name": "DevOps Engineering Assessment",
  "assessment_type": "mix",
  "assessment_description": "Comprehensive DevOps assessment covering containerization, CI/CD, infrastructure as code, and monitoring. Reference the DevOps handbook in $1 and automation guidelines in $2.",
  "passing_marks": 140,
  "num_of_sets": 1,
  "section_names": ["Containerization & Orchestration", "CI/CD Pipelines", "Infrastructure as Code", "Monitoring & Logging"],
  "section_descriptions": [
    "Docker, Kubernetes, container security and orchestration patterns",
    "Jenkins, GitLab CI, automated testing and deployment strategies",
    "Terraform, CloudFormation, infrastructure provisioning and management",
    "Prometheus, Grafana, ELK stack, observability and alerting"
  ],
  "start_time": "2025-12-28T08:00:00Z",
  "end_time": "2025-12-28T14:00:00Z",
  "is_electron_only": true,
  "is_proctored": true,
  "is_published": false,
  "num_of_ai_generated_questions": 4,
  "attachments": [
    "https://s3.amazonaws.com/assessments/devops-handbook.pdf",
    "https://s3.amazonaws.com/assessments/automation-best-practices.pdf"
  ],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "According to the containerization best practices in $1, which approach is recommended for multi-stage Docker builds?",
      "options": ["Single large image", "Multi-stage with slim base", "Separate images per service", "Monolithic containers"],
      "correct_option_index": 1,
      "positive_marks": 17,
      "negative_marks": -3,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Create a Kubernetes deployment configuration following the guidelines in $1 and automation standards from $2.",
      "description": "Build a complete K8s deployment with service, ingress, and resource management",
      "constraints": ["Include health checks", "Set resource limits", "Configure rolling updates"],
      "positive_marks": 35,
      "negative_marks": 0,
      "time_limit": 2400,
      "test_cases": {
        "examples": [
          {"input": "Application specs", "output": "Complete K8s YAML with best practices"},
          {"input": "Scaling requirements", "output": "HPA configuration for auto-scaling"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Based on the CI/CD patterns described in $1, what is the recommended strategy for zero-downtime deployments?",
      "options": ["Blue-Green deployment", "Recreate deployment", "Rolling deployment", "Canary deployment"],
      "correct_option_index": 0,
      "positive_marks": 17,
      "negative_marks": -3,
      "time_limit": 150
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Implement a CI/CD pipeline following the automation guidelines in $2 and best practices from $1.",
      "description": "Create a complete pipeline with testing, security scanning, and deployment",
      "constraints": ["Include automated tests", "Add security scanning", "Implement rollback mechanism"],
      "positive_marks": 35,
      "negative_marks": 0,
      "time_limit": 2700,
      "test_cases": {
        "examples": [
          {"input": "Source code changes", "output": "Automated pipeline execution with quality gates"},
          {"input": "Failed tests", "output": "Pipeline stops with detailed error reporting"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "According to the IaC principles in $1, which tool is best for managing multi-cloud infrastructure?",
      "options": ["CloudFormation", "Terraform", "Pulumi", "Azure ARM"],
      "correct_option_index": 1,
      "positive_marks": 17,
      "negative_marks": -3,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "Design infrastructure as code following the patterns outlined in $1 and automation standards from $2.",
      "description": "Create Terraform configuration for a scalable web application infrastructure",
      "constraints": ["Use modules for reusability", "Include security groups", "Configure auto-scaling"],
      "positive_marks": 35,
      "negative_marks": 0,
      "time_limit": 2400,
      "test_cases": {
        "examples": [
          {"input": "Application requirements", "output": "Complete Terraform configuration with modules"},
          {"input": "Multi-environment setup", "output": "Environment-specific variable configurations"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 4,
      "set_number": 1,
      "question_text": "Based on the monitoring strategies in $1, which metric is most important for application performance?",
      "options": ["CPU usage", "Response time", "Memory usage", "Network throughput"],
      "correct_option_index": 1,
      "positive_marks": 17,
      "negative_marks": -3,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 4,
      "set_number": 1,
      "question_text": "Implement a monitoring and alerting solution following the observability guidelines in $1 and automation practices from $2.",
      "description": "Create a comprehensive monitoring setup with metrics, logs, and alerts",
      "constraints": ["Use Prometheus for metrics", "Configure Grafana dashboards", "Set up alert rules"],
      "positive_marks": 35,
      "negative_marks": 0,
      "time_limit": 2700,
      "test_cases": {
        "examples": [
          {"input": "Application metrics", "output": "Prometheus configuration with custom metrics"},
          {"input": "Alert conditions", "output": "Alert manager rules with notification channels"}
        ]
      }
    }
  ]
}
```

---

## 5. UI/UX Design Assessment

```json
{
  "assessment_name": "UI/UX Design Professional Assessment",
  "assessment_type": "non-coding",
  "assessment_description": "Comprehensive UI/UX assessment covering design principles, user research, prototyping, and accessibility.",
  "passing_marks": 100,
  "num_of_sets": 2,
  "section_names": ["Design Principles", "User Research", "Prototyping & Tools"],
  "section_descriptions": [
    "Visual design, typography, color theory, and design systems",
    "User research methods, persona development, and usability testing",
    "Wireframing, prototyping tools, and design workflow"
  ],
  "start_time": "2025-12-30T10:00:00Z",
  "end_time": "2025-12-30T13:00:00Z",
  "is_electron_only": false,
  "is_proctored": false,
  "is_published": true,
  "num_of_ai_generated_questions": 6,
  "attachments": [],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Which design principle states that similar elements should be grouped together?",
      "options": ["Proximity", "Alignment", "Repetition", "Contrast"],
      "correct_option_index": 0,
      "positive_marks": 16,
      "negative_marks": -2,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "What is the recommended contrast ratio for normal text to meet WCAG AA standards?",
      "options": ["3:1", "4.5:1", "7:1", "2:1"],
      "correct_option_index": 1,
      "positive_marks": 16,
      "negative_marks": -2,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Which user research method is best for understanding user motivations and behaviors?",
      "options": ["Surveys", "A/B testing", "User interviews", "Analytics"],
      "correct_option_index": 2,
      "positive_marks": 16,
      "negative_marks": -2,
      "time_limit": 120
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "What is the primary goal of creating user personas?",
      "options": ["Demographic analysis", "Empathy building", "Market segmentation", "Feature prioritization"],
      "correct_option_index": 1,
      "positive_marks": 16,
      "negative_marks": -2,
      "time_limit": 120
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "Which prototyping fidelity is best for testing interaction flows?",
      "options": ["Low-fidelity wireframes", "Medium-fidelity mockups", "High-fidelity prototypes", "Paper prototypes"],
      "correct_option_index": 2,
      "positive_marks": 16,
      "negative_marks": -2,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "What is the main advantage of using design systems?",
      "options": ["Faster development", "Better aesthetics", "Consistency", "Cost reduction"],
      "correct_option_index": 2,
      "positive_marks": 16,
      "negative_marks": -2,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 2,
      "question_text": "Which color model is best for digital design?",
      "options": ["CMYK", "RGB", "HSB", "Pantone"],
      "correct_option_index": 1,
      "positive_marks": 16,
      "negative_marks": -2,
      "time_limit": 60
    },
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 2,
      "question_text": "What is the golden ratio commonly used for in design?",
      "options": ["Font sizing", "Proportional layouts", "Color harmony", "Animation timing"],
      "correct_option_index": 1,
      "positive_marks": 16,
      "negative_marks": -2,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 2,
      "question_text": "How many users are typically needed for effective usability testing?",
      "options": ["3-5 users", "10-15 users", "20-25 users", "50+ users"],
      "correct_option_index": 0,
      "positive_marks": 16,
      "negative_marks": -2,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 2,
      "question_text": "What is the primary purpose of card sorting in UX research?",
      "options": ["Content organization", "Visual hierarchy", "Navigation testing", "Preference analysis"],
      "correct_option_index": 0,
      "positive_marks": 16,
      "negative_marks": -2,
      "time_limit": 120
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 2,
      "question_text": "Which tool is best for collaborative design and real-time feedback?",
      "options": ["Photoshop", "Figma", "Illustrator", "InDesign"],
      "correct_option_index": 1,
      "positive_marks": 16,
      "negative_marks": -2,
      "time_limit": 60
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 2,
      "question_text": "What is the recommended approach for mobile-first design?",
      "options": ["Design for desktop first", "Design for mobile first", "Design for tablet first", "Design all simultaneously"],
      "correct_option_index": 1,
      "positive_marks": 16,
      "negative_marks": -2,
      "time_limit": 90
    }
  ]
}
```

---

## 6. Python Backend Development Assessment

```json
{
  "assessment_name": "Python Backend Developer Assessment",
  "assessment_type": "coding",
  "assessment_description": "Focused Python backend development assessment covering Django/Flask, databases, APIs, and testing.",
  "passing_marks": 90,
  "num_of_sets": 1,
  "section_names": ["Web Frameworks", "Database Design", "API Development"],
  "section_descriptions": [
    "Django and Flask framework development, ORM usage, and web security",
    "Database design, optimization, migrations, and data modeling",
    "RESTful API design, authentication, and API documentation"
  ],
  "start_time": "2026-01-05T09:00:00Z",
  "end_time": "2026-01-05T13:00:00Z",
  "is_electron_only": false,
  "is_proctored": true,
  "is_published": false,
  "num_of_ai_generated_questions": 0,
  "attachments": [],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Create a Django model with custom validation and methods.",
      "description": "Build a User model with custom validation, password hashing, and utility methods",
      "constraints": ["Inherit from AbstractUser", "Add custom validation", "Include manager methods"],
      "positive_marks": 30,
      "negative_marks": 0,
      "time_limit": 1800,
      "test_cases": {
        "examples": [
          {"input": "User creation data", "output": "Valid user instance with hashed password"},
          {"input": "Invalid email format", "output": "Validation error with appropriate message"}
        ]
      }
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Implement middleware for request logging and authentication.",
      "description": "Create Django middleware that logs requests and handles JWT authentication",
      "constraints": ["Log all requests", "Verify JWT tokens", "Handle authentication errors"],
      "positive_marks": 30,
      "negative_marks": 0,
      "time_limit": 2100,
      "test_cases": {
        "examples": [
          {"input": "Valid JWT request", "output": "Request processed and logged"},
          {"input": "Invalid token", "output": "401 authentication error"}
        ]
      }
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Design and implement a database schema for an e-commerce system.",
      "description": "Create models for products, orders, and users with proper relationships",
      "constraints": ["Use foreign keys correctly", "Include indexes for performance", "Add constraints for data integrity"],
      "positive_marks": 30,
      "negative_marks": 0,
      "time_limit": 2400,
      "test_cases": {
        "examples": [
          {"input": "Product and order data", "output": "Properly related database entries"},
          {"input": "Complex queries", "output": "Optimized database queries with joins"}
        ]
      }
    },
    {
      "question_type": "coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "Build a RESTful API with authentication and rate limiting.",
      "description": "Create a complete API with CRUD operations, JWT auth, and rate limiting",
      "constraints": ["Use Django REST Framework", "Implement JWT authentication", "Add rate limiting"],
      "positive_marks": 30,
      "negative_marks": 0,
      "time_limit": 2700,
      "test_cases": {
        "examples": [
          {"input": "API requests within limits", "output": "Successful responses with proper status codes"},
          {"input": "Rate limit exceeded", "output": "429 Too Many Requests error"}
        ]
      }
    }
  ]
}
```

---

## 7. Digital Marketing Assessment

```json
{
  "assessment_name": "Digital Marketing Specialist Assessment",
  "assessment_type": "non-coding",
  "assessment_description": "Comprehensive digital marketing assessment covering SEO, social media, content marketing, and analytics.",
  "passing_marks": 80,
  "num_of_sets": 1,
  "section_names": ["SEO & SEM", "Social Media Marketing", "Content Strategy", "Analytics & ROI"],
  "section_descriptions": [
    "Search engine optimization, keyword research, and paid advertising",
    "Social media strategy, community management, and platform optimization",
    "Content creation, editorial calendars, and content distribution",
    "Google Analytics, conversion tracking, and performance measurement"
  ],
  "start_time": "2026-01-08T10:00:00Z",
  "end_time": "2026-01-08T12:30:00Z",
  "is_electron_only": false,
  "is_proctored": false,
  "is_published": true,
  "num_of_ai_generated_questions": 8,
  "attachments": [],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "What is the primary factor that Google considers for search rankings?",
      "options": ["Keyword density", "Content relevance", "Page loading speed", "Social signals"],
      "correct_option_index": 1,
      "positive_marks": 10,
      "negative_marks": -2,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Which metric is most important for measuring PPC campaign success?",
      "options": ["Click-through rate", "Cost per click", "Return on ad spend", "Impressions"],
      "correct_option_index": 2,
      "positive_marks": 10,
      "negative_marks": -2,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "What is the best time to post on Instagram for maximum engagement?",
      "options": ["Early morning", "Lunch time", "Evening hours", "Depends on audience"],
      "correct_option_index": 3,
      "positive_marks": 10,
      "negative_marks": -2,
      "time_limit": 60
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Which social media platform is best for B2B marketing?",
      "options": ["Facebook", "LinkedIn", "Instagram", "TikTok"],
      "correct_option_index": 1,
      "positive_marks": 10,
      "negative_marks": -2,
      "time_limit": 60
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "What is the ideal length for a blog post for SEO purposes?",
      "options": ["300-500 words", "500-1000 words", "1000-2000 words", "2000+ words"],
      "correct_option_index": 2,
      "positive_marks": 10,
      "negative_marks": -2,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "Which content format typically generates the highest engagement?",
      "options": ["Text posts", "Images", "Videos", "Infographics"],
      "correct_option_index": 2,
      "positive_marks": 10,
      "negative_marks": -2,
      "time_limit": 60
    },
    {
      "question_type": "non-coding",
      "section_id": 4,
      "set_number": 1,
      "question_text": "What does a high bounce rate typically indicate?",
      "options": ["Good content", "Poor user experience", "High engagement", "Technical issues"],
      "correct_option_index": 1,
      "positive_marks": 10,
      "negative_marks": -2,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 4,
      "set_number": 1,
      "question_text": "Which attribution model gives credit to all touchpoints in the customer journey?",
      "options": ["First-click", "Last-click", "Linear", "Time-decay"],
      "correct_option_index": 2,
      "positive_marks": 10,
      "negative_marks": -2,
      "time_limit": 120
    }
  ]
}
```
