📘 EduTrack Lite API

EduTrack Lite API is a simple course tracking system that allows users to register for courses, track course completion, and manage course information. It demonstrates CRUD operations, data validation, and entity relationships using FastAPI.

🚀 Features
👤 User Endpoints

Create, Read, Update, Delete (CRUD) users

Deactivate a user

🗓️ Course Endpoints

Create, Read, Update, Delete (CRUD) courses

Close enrollment for a course

View all users enrolled in a course

📝 Enrollment Endpoints

Enroll a user in a course

Only active users can enroll

Course must be open

A user cannot enroll twice in the same course

Mark a course as completed

View enrollments for a specific user

View all enrollments

📂 Project Structure
edutrack-lite/
├── main.py
├── schemas/__init__.py
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

Validation: Pydantic models

Database: In-memory lists/dictionaries (no external DB required)

Testing: Pytest

Status Codes: Follows standard REST API codes (200, 201, 400, 404, 409, etc.)

▶️ Getting Started
1. Clone the repository
git clone https://github.com/your-username/edutrack-lite-api.git
cd edutrack-lite-api

2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On macOS/Linux

3. Install dependencies
pip install -r requirements.txt

4. Run the application
uvicorn main:app --reload


API will be available at 👉 http://127.0.0.1:8000

Swagger Docs 👉 http://127.0.0.1:8000/docs

🧪 Running Tests
pytest

📊 Example Data
{
  "course": { "id": 1, "title": "Python Basics", "description": "Learn Python", "is_open": true },
  "user": { "id": 1, "name": "Alice", "email": "alice@example.com", "is_active": true },
  "enrollment": { "id": 1, "user_id": 1, "course_id": 1, "enrolled_date": "2025-09-16", "completed": false }
}

📝 Notes

No authentication required

Simple validation with Pydantic
