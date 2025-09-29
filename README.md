📘 EduTrack Lite API
A lightweight course tracking system built with FastAPI, designed to manage users, courses, and enrollments with ease. It showcases CRUD operations, data validation, and entity relationships in a simple, in-memory setup.

🚀 Features
👤 User Endpoints

Create, Read, Update, Delete (CRUD) operations for users
Deactivate a user to prevent further enrollments

🗓️ Course Endpoints

Create, Read, Update, Delete (CRUD) operations for courses
Close enrollment for a course
View all users enrolled in a specific course

📝 Enrollment Endpoints

Enroll a user in an open course
Only active users can enroll
Courses must be open for enrollment
Prevent duplicate enrollments for the same course
Mark a course as completed
View enrollments for a specific user
View all enrollments


📂 Project Structure
edutrack-lite/
├── main.py
├── schemas/
│   ├── __init__.py
├── routes/
│   ├── __init__.py
│   ├── users.py
│   ├── courses.py
│   └── enrollments.py
└── services/
    ├── __init__.py
    └── database.py


⚙️ Technical Details

Framework: FastAPI
Validation: Pydantic models for robust data validation
Database: In-memory lists/dictionaries (no external database required)
Testing: Pytest for unit and integration tests
Status Codes: Standard REST API codes (200, 201, 400, 404, 409, etc.)


▶️ Getting Started

Clone the repository:
git clone https://github.com/your-username/edutrack-lite-api.git
cd edutrack-lite-api


Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On macOS/Linux


Install dependencies:
pip install -r requirements.txt


Run the application:
uvicorn main:app --reload

The API will be available at: 👉 http://127.0.0.1:8000
Explore the interactive API documentation at: 👉 http://127.0.0.1:8000/docs



🧪 Running Tests
Run the test suite with:
pytest


📊 Example Data
Below is a sample of the data structure used in the API:
{
  "course": {
    "id": 1,
    "title": "Python Basics",
    "description": "Learn Python",
    "is_open": true
  },
  "user": {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "is_active": true
  },
  "enrollment": {
    "id": 1,
    "user_id": 1,
    "course_id": 1,
    "enrolled_date": "2025-09-16",
    "completed": false
  }
}


📝 Notes

No authentication is required, keeping the system lightweight and accessible
Pydantic ensures simple yet effective data validation
Ideal for learning and prototyping FastAPI applications


Thanks
