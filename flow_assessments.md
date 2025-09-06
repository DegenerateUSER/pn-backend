# Flow Assessment API Requests - Real-World Multi-Set Examples

## Overview
This document demonstrates real-world assessment scenarios with proper multi-set implementation. Each assessment contains multiple sets, and each set contains multiple questions, showing how assessments would actually be used in production environments.

## Multi-Set Assessment Concept

### Real-World Usage Patterns:
- **Student Randomization**: Each student gets assigned a random set (anti-cheating)
- **Difficulty Progression**: Sets represent increasing difficulty levels
- **Subject Variations**: Different sets cover different aspects of the same topic
- **Time-based Rotation**: Different sets used in different exam sessions

---

## Assessment Examples

### 1. Software Development Internship Assessment (3 Sets, Multiple Questions Each)
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Software Development Internship Technical Assessment 2025",
  "assessment_type": "mix",
  "assessment_description": "Comprehensive assessment for software development internship candidates. Contains 3 different sets with varying question combinations to ensure fair evaluation while preventing cheating. Each set covers the same competencies but with different problems.",
  "passing_marks": 120,
  "total_marks": 200,
  "num_of_sets": 3,
  "section_names": [
    "Programming Fundamentals",
    "Data Structures & Algorithms", 
    "Web Development Concepts",
    "Database Fundamentals"
  ],
  "section_descriptions": [
    "Basic programming concepts, syntax, and problem-solving skills",
    "Understanding of common data structures and basic algorithms",
    "HTML, CSS, JavaScript, and basic web technologies",
    "SQL queries, database design, and basic database concepts"
  ],
  "start_time": "2025-10-01T09:00:00Z",
  "end_time": "2025-10-01T12:00:00Z",
  "is_electron_only": true,
  "num_of_ai_generated_questions": 10,
  "is_proctored": true,
  "is_published": false,
  "attachments": [
    "https://s3.amazonaws.com/assessments/web-dev-reference.pdf",
    "https://s3.amazonaws.com/assessments/database-schema.png"
  ],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Write a function that finds the second largest number in an array. Handle edge cases where the array has fewer than 2 elements.",
      "description": "Implement a function that returns the second largest element from an integer array.",
      "constraints": [
        "Array length: 0 ≤ n ≤ 1000",
        "Array elements: -10^6 ≤ element ≤ 10^6",
        "Return null/None if second largest doesn't exist"
      ],
      "positive_marks": 15,
      "negative_marks": 0,
      "time_limit": 900,
      "test_cases": {
        "examples": [
          {"input": "[5, 2, 8, 1, 9]", "output": "8"},
          {"input": "[3, 3, 3]", "output": "null"}
        ],
        "hidden": [
          {"input": "[1]", "output": "null"},
          {"input": "[-5, -2, -8, -1]", "output": "-2"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Which of the following best describes the purpose of a constructor in object-oriented programming?",
      "options": [
        "To destroy objects when they are no longer needed",
        "To initialize object properties when the object is created",
        "To define static methods for the class",
        "To inherit properties from parent classes",
        "To handle exceptions during object creation"
      ],
      "correct_option_index": 1,
      "positive_marks": 8,
      "negative_marks": -2,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Implement a function to check if a given string is a valid palindrome. Ignore spaces, punctuation, and case.",
      "description": "Create a function that determines if a string reads the same forwards and backwards, ignoring non-alphanumeric characters and case.",
      "constraints": [
        "String length: 0 ≤ n ≤ 1000",
        "Contains letters, numbers, spaces, and punctuation",
        "Case insensitive comparison"
      ],
      "positive_marks": 12,
      "negative_marks": 0,
      "time_limit": 1200,
      "test_cases": {
        "examples": [
          {"input": "A man, a plan, a canal: Panama", "output": "true"},
          {"input": "race a car", "output": "false"}
        ],
        "hidden": [
          {"input": "Was it a car or a cat I saw?", "output": "true"},
          {"input": "Madam", "output": "true"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "In the web development reference document $1, which HTTP status code should be returned when a user tries to access a resource they don't have permission to view?",
      "options": [
        "401 Unauthorized",
        "403 Forbidden", 
        "404 Not Found",
        "500 Internal Server Error",
        "400 Bad Request"
      ],
      "correct_option_index": 1,
      "positive_marks": 6,
      "negative_marks": -1,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 4,
      "set_number": 1,
      "question_text": "Looking at the database schema in $2, what type of relationship exists between the 'users' and 'orders' tables?",
      "options": [
        "One-to-One",
        "One-to-Many",
        "Many-to-Many", 
        "Self-referencing",
        "No relationship"
      ],
      "correct_option_index": 1,
      "positive_marks": 7,
      "negative_marks": -1,
      "time_limit": 180
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 2,
      "question_text": "Write a function that removes duplicate elements from an array while maintaining the original order of first occurrences.",
      "description": "Implement a function that removes all duplicate elements from an array, keeping only the first occurrence of each element.",
      "constraints": [
        "Array length: 0 ≤ n ≤ 1000",
        "Array elements can be integers or strings",
        "Maintain relative order of elements"
      ],
      "positive_marks": 15,
      "negative_marks": 0,
      "time_limit": 900,
      "test_cases": {
        "examples": [
          {"input": "[1, 2, 2, 3, 4, 4, 5]", "output": "[1, 2, 3, 4, 5]"},
          {"input": "['a', 'b', 'a', 'c', 'b']", "output": "['a', 'b', 'c']"}
        ],
        "hidden": [
          {"input": "[5, 5, 5, 5]", "output": "[5]"},
          {"input": "[]", "output": "[]"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 2,
      "question_text": "What is the main difference between '==' and '===' operators in JavaScript?",
      "options": [
        "There is no difference, they work the same way",
        "'==' checks value only, '===' checks both value and type",
        "'==' is for numbers, '===' is for strings",
        "'==' is deprecated, only '===' should be used",
        "'==' is case-sensitive, '===' is case-insensitive"
      ],
      "correct_option_index": 1,
      "positive_marks": 8,
      "negative_marks": -2,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 2,
      "question_text": "Implement a function to find the intersection of two arrays (elements that appear in both arrays).",
      "description": "Create a function that returns an array containing elements that exist in both input arrays, without duplicates.",
      "constraints": [
        "Array lengths: 0 ≤ n, m ≤ 1000",
        "Array elements are integers",
        "Result should not contain duplicates"
      ],
      "positive_marks": 12,
      "negative_marks": 0,
      "time_limit": 1200,
      "test_cases": {
        "examples": [
          {"input": "[1, 2, 3, 4] and [3, 4, 5, 6]", "output": "[3, 4]"},
          {"input": "[1, 1, 2, 2] and [2, 2, 3, 3]", "output": "[2]"}
        ],
        "hidden": [
          {"input": "[1, 2, 3] and [4, 5, 6]", "output": "[]"},
          {"input": "[] and [1, 2, 3]", "output": "[]"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 2,
      "question_text": "Which CSS property is used to control the spacing between letters in a text?",
      "options": [
        "line-height",
        "letter-spacing",
        "word-spacing", 
        "text-indent",
        "white-space"
      ],
      "correct_option_index": 1,
      "positive_marks": 6,
      "negative_marks": -1,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 4,
      "set_number": 2,
      "question_text": "Which SQL command is used to retrieve data from a database?",
      "options": [
        "GET",
        "RETRIEVE",
        "SELECT",
        "FETCH",
        "EXTRACT"
      ],
      "correct_option_index": 2,
      "positive_marks": 7,
      "negative_marks": -1,
      "time_limit": 180
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 3,
      "question_text": "Write a function that counts the frequency of each character in a string and returns the result as a dictionary/object.",
      "description": "Implement a function that takes a string and returns a dictionary with characters as keys and their frequencies as values.",
      "constraints": [
        "String length: 0 ≤ n ≤ 1000",
        "Case sensitive counting",
        "Include spaces and special characters"
      ],
      "positive_marks": 15,
      "negative_marks": 0,
      "time_limit": 900,
      "test_cases": {
        "examples": [
          {"input": "hello", "output": "{'h': 1, 'e': 1, 'l': 2, 'o': 1}"},
          {"input": "aabcc", "output": "{'a': 2, 'b': 1, 'c': 2}"}
        ],
        "hidden": [
          {"input": "Hello World!", "output": "{'H': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'W': 1, 'r': 1, 'd': 1, '!': 1}"},
          {"input": "", "output": "{}"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 3,
      "question_text": "Which of the following is NOT a valid variable naming convention in most programming languages?",
      "options": [
        "camelCase",
        "snake_case",
        "PascalCase",
        "kebab-case",
        "UPPER_CASE"
      ],
      "correct_option_index": 3,
      "positive_marks": 8,
      "negative_marks": -2,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 3,
      "question_text": "Implement a function that rotates an array to the right by k positions.",
      "description": "Create a function that shifts all elements in an array k positions to the right, with elements wrapping around.",
      "constraints": [
        "Array length: 0 ≤ n ≤ 1000",
        "Rotation steps: 0 ≤ k ≤ 10^9",
        "Handle cases where k > array length"
      ],
      "positive_marks": 12,
      "negative_marks": 0,
      "time_limit": 1200,
      "test_cases": {
        "examples": [
          {"input": "[1, 2, 3, 4, 5] rotated by 2", "output": "[4, 5, 1, 2, 3]"},
          {"input": "[1, 2] rotated by 3", "output": "[2, 1]"}
        ],
        "hidden": [
          {"input": "[1, 2, 3, 4, 5, 6, 7] rotated by 3", "output": "[5, 6, 7, 1, 2, 3, 4]"},
          {"input": "[] rotated by 5", "output": "[]"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 3,
      "question_text": "What does the 'box-sizing: border-box' CSS property do?",
      "options": [
        "Makes the border invisible",
        "Includes padding and border in the element's total width and height",
        "Creates a shadow around the element",
        "Changes the border style to a box shape",
        "Removes the default margin from the element"
      ],
      "correct_option_index": 1,
      "positive_marks": 6,
      "negative_marks": -1,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 4,
      "set_number": 3,
      "question_text": "What is a primary key in a database table?",
      "options": [
        "The first column in a table",
        "A column that can contain duplicate values",
        "A column or combination of columns that uniquely identifies each row",
        "A column that stores the creation date of each row",
        "A column that is automatically generated by the database"
      ],
      "correct_option_index": 2,
      "positive_marks": 7,
      "negative_marks": -1,
      "time_limit": 180
    }
  ]
}
```

### 2. Data Science Junior Role Assessment (4 Sets with Progressive Difficulty)
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Data Science Junior Position Assessment - Multi-Level Evaluation",
  "assessment_type": "mix",
  "assessment_description": "Progressive assessment for data science positions with 4 difficulty levels. Set 1: Entry level, Set 2: Junior level, Set 3: Mid-level, Set 4: Senior level. Each candidate is assigned to a set based on their experience level and initial screening results.",
  "passing_marks": 180,
  "total_marks": 300,
  "num_of_sets": 4,
  "section_names": [
    "Statistics & Probability",
    "Python Programming for Data Science",
    "Machine Learning Fundamentals",
    "Data Analysis & Visualization"
  ],
  "section_descriptions": [
    "Statistical concepts, probability distributions, hypothesis testing, and statistical inference",
    "Python programming with focus on data manipulation libraries like pandas, numpy, and data processing",
    "Machine learning algorithms, model evaluation, feature engineering, and ML pipeline concepts",
    "Data cleaning, exploratory data analysis, visualization tools, and interpretation of results"
  ],
  "start_time": "2025-10-15T10:00:00Z",
  "end_time": "2025-10-15T14:00:00Z",
  "is_electron_only": true,
  "num_of_ai_generated_questions": 20,
  "is_proctored": true,
  "is_published": false,
  "attachments": [
    "https://s3.amazonaws.com/assessments/dataset-sample.csv",
    "https://s3.amazonaws.com/assessments/ml-algorithm-cheatsheet.pdf",
    "https://s3.amazonaws.com/assessments/statistical-tables.pdf"
  ],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "What is the mean of the dataset: [2, 4, 6, 8, 10]?",
      "options": [
        "5",
        "6",
        "7",
        "8",
        "10"
      ],
      "correct_option_index": 1,
      "positive_marks": 10,
      "negative_marks": -2,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Write a Python function that calculates the mean, median, and mode of a list of numbers. Return the results as a dictionary.",
      "description": "Implement a function that computes basic statistical measures for a given list of numbers.",
      "constraints": [
        "List length: 1 ≤ n ≤ 1000",
        "Numbers can be integers or floats",
        "Handle edge cases (empty list, no mode)"
      ],
      "positive_marks": 20,
      "negative_marks": 0,
      "time_limit": 1800,
      "test_cases": {
        "examples": [
          {"input": "[1, 2, 2, 3, 4]", "output": "{'mean': 2.4, 'median': 2, 'mode': 2}"},
          {"input": "[1, 2, 3, 4, 5]", "output": "{'mean': 3, 'median': 3, 'mode': None}"}
        ],
        "hidden": [
          {"input": "[10, 20, 30]", "output": "{'mean': 20, 'median': 20, 'mode': None}"},
          {"input": "[5, 5, 5, 5]", "output": "{'mean': 5, 'median': 5, 'mode': 5}"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "Which of the following is a supervised learning algorithm?",
      "options": [
        "K-means clustering",
        "Linear Regression",
        "DBSCAN",
        "Principal Component Analysis (PCA)",
        "Hierarchical clustering"
      ],
      "correct_option_index": 1,
      "positive_marks": 12,
      "negative_marks": -3,
      "time_limit": 90
    },
    {
      "question_type": "coding",
      "section_id": 4,
      "set_number": 1,
      "question_text": "Using the sample dataset in $1, write a Python function to identify and count missing values in each column.",
      "description": "Analyze the provided dataset and create a function that reports missing data statistics.",
      "constraints": [
        "Use pandas library for data manipulation",
        "Return a dictionary with column names as keys and missing counts as values",
        "Handle different data types (numeric, string, boolean)"
      ],
      "positive_marks": 15,
      "negative_marks": 0,
      "time_limit": 1200,
      "test_cases": {
        "examples": [
          {"input": "DataFrame with some null values", "output": "{'col1': 2, 'col2': 0, 'col3': 5}"},
          {"input": "DataFrame with no missing values", "output": "{'col1': 0, 'col2': 0, 'col3': 0}"}
        ],
        "hidden": [
          {"input": "Large dataset with mixed missing patterns", "output": "Accurate missing value counts"},
          {"input": "Dataset with all missing values in one column", "output": "Correct identification of completely missing column"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 2,
      "question_text": "If a normal distribution has a mean of 100 and standard deviation of 15, approximately what percentage of values fall within one standard deviation of the mean?",
      "options": [
        "50%",
        "68%",
        "95%",
        "99.7%",
        "90%"
      ],
      "correct_option_index": 1,
      "positive_marks": 12,
      "negative_marks": -3,
      "time_limit": 180
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 2,
      "question_text": "Implement a function that performs one-hot encoding on categorical data using pandas. The function should handle missing values appropriately.",
      "description": "Create a robust one-hot encoding function that can handle various edge cases in categorical data.",
      "constraints": [
        "Use pandas get_dummies or similar functionality",
        "Handle NaN values in categorical columns",
        "Return a cleaned DataFrame with encoded features"
      ],
      "positive_marks": 25,
      "negative_marks": 0,
      "time_limit": 2400,
      "test_cases": {
        "examples": [
          {"input": "DataFrame with ['A', 'B', 'A', 'C']", "output": "One-hot encoded columns for A, B, C"},
          {"input": "DataFrame with missing values", "output": "Proper handling of NaN values"}
        ],
        "hidden": [
          {"input": "Large dataset with many categories", "output": "Efficient encoding without memory issues"},
          {"input": "Edge case with single category", "output": "Correct handling of single-value categorical"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 2,
      "question_text": "What is the purpose of cross-validation in machine learning?",
      "options": [
        "To increase the size of the training dataset",
        "To evaluate model performance and reduce overfitting",
        "To clean the data before training",
        "To select the best features for the model",
        "To speed up the training process"
      ],
      "correct_option_index": 1,
      "positive_marks": 15,
      "negative_marks": -3,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 4,
      "set_number": 2,
      "question_text": "Create a function that generates a correlation matrix for numerical columns in a dataset and identifies highly correlated pairs (correlation > 0.8).",
      "description": "Implement a comprehensive correlation analysis tool for feature selection and multicollinearity detection.",
      "constraints": [
        "Use pandas and numpy for calculations",
        "Return both the correlation matrix and highly correlated pairs",
        "Handle edge cases like constant columns"
      ],
      "positive_marks": 20,
      "negative_marks": 0,
      "time_limit": 1800,
      "test_cases": {
        "examples": [
          {"input": "DataFrame with numerical columns", "output": "Correlation matrix and list of highly correlated pairs"},
          {"input": "DataFrame with constant column", "output": "Proper handling of zero variance columns"}
        ],
        "hidden": [
          {"input": "Large dataset with mixed correlations", "output": "Accurate correlation calculations and pair identification"},
          {"input": "Dataset with perfect correlations", "output": "Correct identification of perfect correlation (1.0)"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 3,
      "question_text": "In hypothesis testing, what does a p-value of 0.03 indicate when the significance level (α) is set to 0.05?",
      "options": [
        "Accept the null hypothesis",
        "Reject the null hypothesis",
        "The test is inconclusive",
        "Need more data to decide",
        "The alternative hypothesis is false"
      ],
      "correct_option_index": 1,
      "positive_marks": 15,
      "negative_marks": -4,
      "time_limit": 240
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 3,
      "question_text": "Implement a custom train-test split function that ensures stratified sampling for classification problems while handling imbalanced datasets.",
      "description": "Create a robust data splitting function that maintains class proportions and handles edge cases in imbalanced datasets.",
      "constraints": [
        "Maintain class distribution in both train and test sets",
        "Handle minimum class size constraints",
        "Support custom test size ratios",
        "Return indices for reproducible splits"
      ],
      "positive_marks": 30,
      "negative_marks": 0,
      "time_limit": 3000,
      "test_cases": {
        "examples": [
          {"input": "Balanced dataset with 1000 samples, 2 classes", "output": "Stratified split maintaining proportions"},
          {"input": "Imbalanced dataset (90-10 split)", "output": "Proper handling of minority class"}
        ],
        "hidden": [
          {"input": "Extremely imbalanced dataset (99-1 split)", "output": "Robust handling of severe class imbalance"},
          {"input": "Multi-class problem with varying class sizes", "output": "Accurate stratification across all classes"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 3,
      "question_text": "Which evaluation metric would be most appropriate for a highly imbalanced binary classification problem where detecting the minority class is critical?",
      "options": [
        "Accuracy",
        "Precision",
        "F1-Score",
        "Recall",
        "ROC-AUC"
      ],
      "correct_option_index": 3,
      "positive_marks": 18,
      "negative_marks": -4,
      "time_limit": 180
    },
    {
      "question_type": "coding",
      "section_id": 4,
      "set_number": 3,
      "question_text": "Build a comprehensive data profiling function that generates a statistical summary report for any dataset, including data types, missing values, outliers, and distribution characteristics.",
      "description": "Create an advanced data profiling tool that provides insights into dataset quality and characteristics.",
      "constraints": [
        "Handle mixed data types (numerical, categorical, datetime)",
        "Identify outliers using multiple methods (IQR, Z-score)",
        "Generate distribution statistics and skewness measures",
        "Output formatted report with recommendations"
      ],
      "positive_marks": 35,
      "negative_marks": 0,
      "time_limit": 3600,
      "test_cases": {
        "examples": [
          {"input": "Mixed dataset with various data types", "output": "Comprehensive profiling report"},
          {"input": "Dataset with outliers and missing values", "output": "Accurate outlier detection and missing data analysis"}
        ],
        "hidden": [
          {"input": "Large dataset with complex patterns", "output": "Efficient profiling without performance issues"},
          {"input": "Dataset with temporal patterns", "output": "Proper handling of datetime features"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 4,
      "question_text": "Referring to the statistical tables in $3, what is the critical value for a two-tailed t-test with 15 degrees of freedom at α = 0.01 significance level?",
      "options": [
        "2.131",
        "2.602",
        "2.947",
        "3.252",
        "2.977"
      ],
      "correct_option_index": 2,
      "positive_marks": 20,
      "negative_marks": -5,
      "time_limit": 300
    },
    {
      "question_type": "coding",
      "section_id": 2,
      "set_number": 4,
      "question_text": "Implement a complete feature engineering pipeline that includes automatic feature selection, polynomial feature generation, and feature scaling with proper handling of categorical variables and missing data.",
      "description": "Build an end-to-end feature engineering system that can automatically prepare data for machine learning models.",
      "constraints": [
        "Support multiple feature selection methods (univariate, recursive)",
        "Generate polynomial and interaction features selectively",
        "Handle mixed data types with appropriate preprocessing",
        "Implement proper train/validation separation for preprocessing steps",
        "Include feature importance ranking"
      ],
      "positive_marks": 45,
      "negative_marks": 0,
      "time_limit": 4800,
      "test_cases": {
        "examples": [
          {"input": "Raw dataset with mixed features", "output": "Processed feature matrix with selected features"},
          {"input": "Dataset with high cardinality categoricals", "output": "Efficient encoding and feature selection"}
        ],
        "hidden": [
          {"input": "Large dataset requiring memory-efficient processing", "output": "Scalable pipeline with optimized memory usage"},
          {"input": "Dataset with complex missing patterns", "output": "Intelligent imputation and feature engineering"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 4,
      "question_text": "Based on the ML algorithm cheatsheet in $2, which ensemble method would be most effective for reducing both bias and variance in a machine learning model?",
      "options": [
        "Bagging with Random Forest",
        "Boosting with AdaBoost", 
        "Gradient Boosting with early stopping",
        "Voting classifier with diverse base models",
        "Stacking with meta-learner"
      ],
      "correct_option_index": 4,
      "positive_marks": 22,
      "negative_marks": -5,
      "time_limit": 240
    },
    {
      "question_type": "coding",
      "section_id": 4,
      "set_number": 4,
      "question_text": "Design and implement an advanced anomaly detection system that combines multiple algorithms (Isolation Forest, Local Outlier Factor, and One-Class SVM) with ensemble voting and confidence scoring.",
      "description": "Create a sophisticated anomaly detection framework that leverages multiple algorithms for robust outlier identification.",
      "constraints": [
        "Implement ensemble of at least 3 different anomaly detection algorithms",
        "Provide confidence scores for each prediction",
        "Handle high-dimensional data efficiently",
        "Include hyperparameter optimization for each algorithm",
        "Support both univariate and multivariate anomaly detection"
      ],
      "positive_marks": 50,
      "negative_marks": 0,
      "time_limit": 5400,
      "test_cases": {
        "examples": [
          {"input": "Dataset with known anomalies", "output": "High accuracy anomaly detection with confidence scores"},
          {"input": "High-dimensional dataset", "output": "Efficient processing with maintained accuracy"}
        ],
        "hidden": [
          {"input": "Real-world dataset with subtle anomalies", "output": "Robust detection of complex anomaly patterns"},
          {"input": "Streaming data simulation", "output": "Adaptable anomaly detection for evolving patterns"}
        ]
      }
    }
  ]
}
```

### 3. Digital Marketing Specialist Assessment (2 Sets for A/B Testing)
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "Digital Marketing Specialist Certification - A/B Testing Variants",
  "assessment_type": "non-coding",
  "assessment_description": "Digital marketing assessment with 2 equivalent sets for A/B testing question effectiveness. Both sets cover the same competencies but with different scenarios and case studies to measure question quality and candidate response patterns.",
  "passing_marks": 160,
  "total_marks": 240,
  "num_of_sets": 2,
  "section_names": [
    "Digital Marketing Strategy",
    "Social Media Marketing",
    "Search Engine Optimization",
    "Paid Advertising & Analytics",
    "Content Marketing & Email Campaigns"
  ],
  "section_descriptions": [
    "Marketing strategy development, target audience analysis, competitive analysis, and campaign planning",
    "Platform-specific strategies, community management, influencer marketing, and social media analytics",
    "On-page and off-page SEO, keyword research, technical SEO, and search engine marketing",
    "PPC campaigns, Google Ads, Facebook Ads, conversion tracking, and performance analytics",
    "Content strategy, email marketing automation, lead nurturing, and campaign optimization"
  ],
  "start_time": "2025-11-01T09:00:00Z",
  "end_time": "2025-11-01T12:00:00Z",
  "is_electron_only": false,
  "num_of_ai_generated_questions": 30,
  "is_proctored": false,
  "is_published": false,
  "attachments": [
    "https://s3.amazonaws.com/assessments/marketing-case-study-ecommerce.pdf",
    "https://s3.amazonaws.com/assessments/google-analytics-dashboard.png",
    "https://s3.amazonaws.com/assessments/social-media-campaign-data.xlsx"
  ],
  "questions": [
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Based on the e-commerce case study in $1, what should be the primary KPI for measuring the success of a customer acquisition campaign for a luxury fashion brand?",
      "options": [
        "Click-through rate (CTR)",
        "Cost per click (CPC)",
        "Customer lifetime value (CLV)",
        "Social media followers",
        "Email open rates"
      ],
      "correct_option_index": 2,
      "positive_marks": 15,
      "negative_marks": -3,
      "time_limit": 180
    },
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "For a B2B SaaS company targeting enterprise clients, which marketing channel typically provides the highest quality leads?",
      "options": [
        "Social media advertising",
        "Content marketing and SEO",
        "Display advertising",
        "Influencer partnerships",
        "Print advertising"
      ],
      "correct_option_index": 1,
      "positive_marks": 12,
      "negative_marks": -2,
      "time_limit": 120
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "According to the social media campaign data in $3, what is the optimal posting frequency for maximum engagement on Instagram for a food and beverage brand?",
      "options": [
        "Once per day",
        "2-3 times per day",
        "Every other day",
        "3-5 times per week",
        "Once per week"
      ],
      "correct_option_index": 3,
      "positive_marks": 10,
      "negative_marks": -2,
      "time_limit": 150
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "Which of the following is the most important factor for local SEO ranking?",
      "options": [
        "Number of backlinks",
        "Google My Business optimization",
        "Social media presence",
        "Website loading speed",
        "Keyword density"
      ],
      "correct_option_index": 1,
      "positive_marks": 13,
      "negative_marks": -3,
      "time_limit": 120
    },
    {
      "question_type": "non-coding",
      "section_id": 4,
      "set_number": 1,
      "question_text": "Looking at the Google Analytics dashboard in $2, what would be the most effective way to reduce the bounce rate for the product pages?",
      "options": [
        "Increase page loading speed and improve mobile responsiveness",
        "Add more product images",
        "Increase the price of products",
        "Remove the navigation menu",
        "Add more text content"
      ],
      "correct_option_index": 0,
      "positive_marks": 14,
      "negative_marks": -3,
      "time_limit": 200
    },
    {
      "question_type": "non-coding",
      "section_id": 5,
      "set_number": 1,
      "question_text": "What is the optimal email sending frequency for a weekly newsletter to maintain high engagement rates?",
      "options": [
        "Daily",
        "Every 3 days",
        "Weekly",
        "Bi-weekly",
        "Monthly"
      ],
      "correct_option_index": 2,
      "positive_marks": 11,
      "negative_marks": -2,
      "time_limit": 90
    },
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 2,
      "question_text": "For a technology startup launching a new mobile app, which marketing strategy would be most effective for initial user acquisition?",
      "options": [
        "Traditional TV advertising",
        "App Store Optimization (ASO) and influencer partnerships",
        "Print media campaigns",
        "Radio advertising",
        "Billboard advertising"
      ],
      "correct_option_index": 1,
      "positive_marks": 15,
      "negative_marks": -3,
      "time_limit": 180
    },
    {
      "question_type": "non-coding",
      "section_id": 1,
      "set_number": 2,
      "question_text": "What is the most effective way to measure the ROI of a brand awareness campaign?",
      "options": [
        "Direct sales attribution only",
        "Combination of brand lift studies, search volume increases, and assisted conversions",
        "Social media likes and shares",
        "Website traffic increase",
        "Email subscription growth"
      ],
      "correct_option_index": 1,
      "positive_marks": 12,
      "negative_marks": -2,
      "time_limit": 120
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 2,
      "question_text": "For a B2B software company, which LinkedIn content strategy typically generates the highest engagement rates?",
      "options": [
        "Daily product promotional posts",
        "Industry insights and thought leadership content",
        "Company culture and behind-the-scenes content",
        "Competitor comparison posts",
        "Sales-focused call-to-action posts"
      ],
      "correct_option_index": 1,
      "positive_marks": 10,
      "negative_marks": -2,
      "time_limit": 150
    },
    {
      "question_type": "non-coding",
      "section_id": 3,
      "set_number": 2,
      "question_text": "Which technical SEO factor has the most significant impact on search engine rankings in 2025?",
      "options": [
        "Meta keyword tags",
        "Core Web Vitals and page experience",
        "Exact match domains",
        "Keyword stuffing",
        "Hidden text optimization"
      ],
      "correct_option_index": 1,
      "positive_marks": 13,
      "negative_marks": -3,
      "time_limit": 120
    },
    {
      "question_type": "non-coding",
      "section_id": 4,
      "set_number": 2,
      "question_text": "For a Google Ads campaign with a limited budget, which bidding strategy would maximize conversions while maintaining cost efficiency?",
      "options": [
        "Manual CPC bidding",
        "Target CPA (Cost Per Acquisition)",
        "Maximize clicks",
        "Target ROAS (Return on Ad Spend)",
        "Enhanced CPC"
      ],
      "correct_option_index": 1,
      "positive_marks": 14,
      "negative_marks": -3,
      "time_limit": 200
    },
    {
      "question_type": "non-coding",
      "section_id": 5,
      "set_number": 2,
      "question_text": "What is the most effective email segmentation strategy for an e-commerce fashion retailer?",
      "options": [
        "Geographic location only",
        "Purchase history, browsing behavior, and demographic data",
        "Email open rates only",
        "Subscription date",
        "Random segmentation"
      ],
      "correct_option_index": 1,
      "positive_marks": 11,
      "negative_marks": -2,
      "time_limit": 90
    }
  ]
}
```

---

## Real-World Assessment Management Scenarios

### 4. University Computer Science Midterm (3 Sets for Different Class Sections)
```http
POST /api/v1/assessments/
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "assessment_name": "CS102 Data Structures Midterm Examination - Fall 2025",
  "assessment_type": "mix",
  "assessment_description": "Midterm examination for CS102 Data Structures course with 3 different sets for different class sections (Section A, B, and C). Each set maintains equivalent difficulty while using different problems to prevent academic dishonesty during simultaneous testing sessions.",
  "passing_marks": 140,
  "total_marks": 200,
  "num_of_sets": 3,
  "section_names": [
    "Arrays and Linked Lists",
    "Stacks and Queues", 
    "Trees and Binary Search Trees",
    "Algorithmic Analysis"
  ],
  "section_descriptions": [
    "Array operations, dynamic arrays, singly and doubly linked lists, and list manipulation algorithms",
    "Stack and queue implementations, applications, and related algorithms including expression evaluation",
    "Binary trees, BST operations, tree traversals, and tree-based algorithms",
    "Time and space complexity analysis, Big O notation, and algorithm comparison"
  ],
  "start_time": "2025-10-20T14:00:00Z",
  "end_time": "2025-10-20T16:30:00Z",
  "is_electron_only": true,
  "num_of_ai_generated_questions": 0,
  "is_proctored": true,
  "is_published": true,
  "attachments": [],
  "questions": [
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 1,
      "question_text": "Implement a function to reverse a linked list iteratively. Your function should take the head of a singly linked list and return the new head after reversing.",
      "description": "Write an iterative solution to reverse a singly linked list without using extra space for another list.",
      "constraints": [
        "Number of nodes: 0 ≤ n ≤ 1000",
        "Node values: -1000 ≤ val ≤ 1000",
        "Must be iterative (no recursion)",
        "Space complexity: O(1)"
      ],
      "positive_marks": 25,
      "negative_marks": 0,
      "time_limit": 1800,
      "test_cases": {
        "examples": [
          {"input": "1 -> 2 -> 3 -> 4 -> NULL", "output": "4 -> 3 -> 2 -> 1 -> NULL"},
          {"input": "NULL", "output": "NULL"}
        ],
        "hidden": [
          {"input": "Single node: 5 -> NULL", "output": "5 -> NULL"},
          {"input": "Two nodes: 1 -> 2 -> NULL", "output": "2 -> 1 -> NULL"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 1,
      "question_text": "Which of the following applications is most suitable for a stack data structure?",
      "options": [
        "Implementing a queue",
        "Function call management and recursion",
        "Breadth-first search in graphs",
        "Round-robin scheduling",
        "Finding the shortest path"
      ],
      "correct_option_index": 1,
      "positive_marks": 15,
      "negative_marks": -3,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 3,
      "set_number": 1,
      "question_text": "Write a function to find the maximum depth (height) of a binary tree. The depth is the number of nodes along the longest path from the root to a leaf.",
      "description": "Implement a recursive solution to calculate the maximum depth of a binary tree.",
      "constraints": [
        "Number of nodes: 0 ≤ n ≤ 1000",
        "Node values: -1000 ≤ val ≤ 1000",
        "Return 0 for empty tree"
      ],
      "positive_marks": 20,
      "negative_marks": 0,
      "time_limit": 1200,
      "test_cases": {
        "examples": [
          {"input": "Tree: [3,9,20,null,null,15,7]", "output": "3"},
          {"input": "Empty tree", "output": "0"}
        ],
        "hidden": [
          {"input": "Single node tree", "output": "1"},
          {"input": "Skewed tree with 10 nodes", "output": "10"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 4,
      "set_number": 1,
      "question_text": "What is the time complexity of searching for an element in a balanced binary search tree?",
      "options": [
        "O(1)",
        "O(log n)",
        "O(n)",
        "O(n log n)",
        "O(n²)"
      ],
      "correct_option_index": 1,
      "positive_marks": 10,
      "negative_marks": -2,
      "time_limit": 90
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 2,
      "question_text": "Implement a function to find the middle element of a linked list in a single pass. If the list has even number of elements, return the second middle element.",
      "description": "Use the two-pointer technique to find the middle element efficiently.",
      "constraints": [
        "Number of nodes: 1 ≤ n ≤ 1000",
        "Node values: -1000 ≤ val ≤ 1000",
        "Must solve in single pass",
        "Space complexity: O(1)"
      ],
      "positive_marks": 25,
      "negative_marks": 0,
      "time_limit": 1800,
      "test_cases": {
        "examples": [
          {"input": "1 -> 2 -> 3 -> 4 -> 5 -> NULL", "output": "3"},
          {"input": "1 -> 2 -> 3 -> 4 -> NULL", "output": "3"}
        ],
        "hidden": [
          {"input": "Single node: 1 -> NULL", "output": "1"},
          {"input": "Two nodes: 1 -> 2 -> NULL", "output": "2"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 2,
      "question_text": "In which scenario would you prefer a queue over a stack?",
      "options": [
        "Undo operations in a text editor",
        "Function call management",
        "Breadth-first search traversal",
        "Expression evaluation with parentheses",
        "Backtracking algorithms"
      ],
      "correct_option_index": 2,
      "positive_marks": 15,
      "negative_marks": -3,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 3,
      "set_number": 2,
      "question_text": "Write a function to check if a binary tree is symmetric (mirror image of itself around its center).",
      "description": "Implement a solution that checks if a binary tree is a mirror of itself.",
      "constraints": [
        "Number of nodes: 0 ≤ n ≤ 1000",
        "Node values: -1000 ≤ val ≤ 1000",
        "Consider both structure and values"
      ],
      "positive_marks": 20,
      "negative_marks": 0,
      "time_limit": 1200,
      "test_cases": {
        "examples": [
          {"input": "Tree: [1,2,2,3,4,4,3]", "output": "true"},
          {"input": "Tree: [1,2,2,null,3,null,3]", "output": "false"}
        ],
        "hidden": [
          {"input": "Single node tree", "output": "true"},
          {"input": "Empty tree", "output": "true"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 4,
      "set_number": 2,
      "question_text": "What is the worst-case time complexity of inserting an element into an unbalanced binary search tree?",
      "options": [
        "O(1)",
        "O(log n)",
        "O(n)",
        "O(n log n)",
        "O(n²)"
      ],
      "correct_option_index": 2,
      "positive_marks": 10,
      "negative_marks": -2,
      "time_limit": 90
    },
    {
      "question_type": "coding",
      "section_id": 1,
      "set_number": 3,
      "question_text": "Implement a function to detect if a linked list has a cycle. Return true if there is a cycle, false otherwise.",
      "description": "Use Floyd's Cycle Detection Algorithm (tortoise and hare) to solve this efficiently.",
      "constraints": [
        "Number of nodes: 0 ≤ n ≤ 1000",
        "Node values: -1000 ≤ val ≤ 1000",
        "Space complexity: O(1)",
        "No modification of list structure allowed"
      ],
      "positive_marks": 25,
      "negative_marks": 0,
      "time_limit": 1800,
      "test_cases": {
        "examples": [
          {"input": "3 -> 2 -> 0 -> -4 -> (back to 2)", "output": "true"},
          {"input": "1 -> 2 -> NULL", "output": "false"}
        ],
        "hidden": [
          {"input": "Single node with self-cycle", "output": "true"},
          {"input": "Empty list", "output": "false"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 2,
      "set_number": 3,
      "question_text": "Which operation is NOT efficiently supported by a standard queue implementation?",
      "options": [
        "Enqueue (add to rear)",
        "Dequeue (remove from front)",
        "Access middle element",
        "Check if queue is empty",
        "Get front element without removing"
      ],
      "correct_option_index": 2,
      "positive_marks": 15,
      "negative_marks": -3,
      "time_limit": 120
    },
    {
      "question_type": "coding",
      "section_id": 3,
      "set_number": 3,
      "question_text": "Write a function to perform level-order traversal (breadth-first traversal) of a binary tree and return the values as a list of lists, where each list contains the values of nodes at the same level.",
      "description": "Implement BFS traversal that groups nodes by their level in the tree.",
      "constraints": [
        "Number of nodes: 0 ≤ n ≤ 1000",
        "Node values: -1000 ≤ val ≤ 1000",
        "Return empty list for empty tree"
      ],
      "positive_marks": 20,
      "negative_marks": 0,
      "time_limit": 1200,
      "test_cases": {
        "examples": [
          {"input": "Tree: [3,9,20,null,null,15,7]", "output": "[[3],[9,20],[15,7]]"},
          {"input": "Empty tree", "output": "[]"}
        ],
        "hidden": [
          {"input": "Single node tree", "output": "[[1]]"},
          {"input": "Complete binary tree with 7 nodes", "output": "Proper level grouping"}
        ]
      }
    },
    {
      "question_type": "non-coding",
      "section_id": 4,
      "set_number": 3,
      "question_text": "What is the space complexity of the recursive implementation of binary tree traversal?",
      "options": [
        "O(1)",
        "O(log n) for balanced trees, O(n) for skewed trees",
        "O(n)",
        "O(n log n)",
        "O(n²)"
      ],
      "correct_option_index": 1,
      "positive_marks": 10,
      "negative_marks": -2,
      "time_limit": 90
    }
  ]
}
```

---

*This document demonstrates real-world assessment scenarios with proper multi-set implementation, showing how assessments are actually structured in production environments with multiple questions per set and practical use cases.*
