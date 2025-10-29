EduTrack Lite API
A lightweight RESTful API for educational data management built with FastAPI. Designed for efficient course tracking, user management, and enrollment workflows with robust validation and clean architecture.
Overview
EduTrack Lite demonstrates production-ready API design patterns including CRUD operations, business logic validation, and relational data management using an in-memory data store optimized for rapid prototyping and testing.
Core Features
User Management

Complete CRUD operations with data validation
User activation/deactivation for access control
Active status enforcement for enrollment eligibility

Course Management

Full course lifecycle management (create, read, update, delete)
Enrollment status controls (open/closed)
Course enrollment tracking and reporting

Enrollment System

Smart enrollment validation (prevents duplicates, enforces business rules)
Course completion tracking
User-specific and course-specific enrollment queries
Automatic constraint enforcement (active users, open courses)

Architecture
edutrack-lite/
├── main.py                 # Application entry point
├── schemas/                # Pydantic models for validation
├── routes/                 # API endpoint definitions
│   ├── users.py
│   ├── courses.py
│   └── enrollments.py
└── services/
    └── database.py         # In-memory data persistence layer
Design Principles:

Separation of concerns (routes, schemas, services)
Pydantic-based validation for data integrity
RESTful conventions with proper HTTP status codes
Automatic API documentation generation

Tech Stack

Framework: FastAPI
Validation: Pydantic v2
Testing: Pytest
Data Storage: In-memory (ideal for development/testing)
Documentation: Auto-generated OpenAPI (Swagger/ReDoc)

Getting Started
Prerequisites

Python 3.8+
pip

Installation

Clone the repository

bash   git clone https://github.com/your-username/edutrack-lite-api.git
   cd edutrack-lite-api

Set up virtual environment

bash   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows

Install dependencies

bash   pip install -r requirements.txt

Run the application

bash   uvicorn main:app --reload
Access Points

API Base: http://127.0.0.1:8000
Interactive Docs: http://127.0.0.1:8000/docs (Swagger UI)
Alternative Docs: http://127.0.0.1:8000/redoc (ReDoc)

API Endpoints
Users

POST /users - Create new user
GET /users - List all users
GET /users/{id} - Get user details
PUT /users/{id} - Update user
DELETE /users/{id} - Remove user
PATCH /users/{id}/deactivate - Deactivate user account

Courses

POST /courses - Create new course
GET /courses - List all courses
GET /courses/{id} - Get course details
PUT /courses/{id} - Update course
DELETE /courses/{id} - Remove course
PATCH /courses/{id}/close - Close enrollment
GET /courses/{id}/enrollments - View enrolled users

Enrollments

POST /enrollments - Enroll user in course
GET /enrollments - List all enrollments
GET /enrollments/user/{user_id} - User's enrollments
PATCH /enrollments/{id}/complete - Mark course completed

Testing
Run the test suite:
bashpytest
Run with coverage report:
bashpytest --cov=. --cov-report=html
Data Models
User
json{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice.johnson@example.com",
  "is_active": true
}
Course
json{
  "id": 1,
  "title": "Python for Backend Development",
  "description": "Learn FastAPI and database integration",
  "is_open": true
}
Enrollment
json{
  "id": 1,
  "user_id": 1,
  "course_id": 1,
  "enrolled_date": "2025-10-29",
  "completed": false
}
Business Logic

Enrollment Validation: Only active users can enroll in open courses
Duplicate Prevention: Users cannot enroll in the same course twice
Cascading Updates: Deactivated users lose enrollment privileges
Status Tracking: Course completion status persists independently

Future Enhancements

 Database integration (PostgreSQL/MySQL)
 JWT authentication and authorization
 Course capacity limits and waitlist management
 Email notifications for enrollments
 Advanced filtering and pagination
 Docker containerization

Contributing
This project is open for feedback and contributions. Feel free to fork, submit issues, or create pull requests.
License
MIT License - See LICENSE file for details
