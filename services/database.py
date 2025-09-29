from datetime import date
from typing import Dict, List

# In-memory storage
users_db: Dict[int, dict] = {}
courses_db: Dict[int, dict] = {}
enrollments_db: Dict[int, dict] = {}

# Counters for IDs
user_id_counter = {"current": 0}
course_id_counter = {"current": 0}
enrollment_id_counter = {"current": 0}


def get_next_user_id() -> int:
    user_id_counter["current"] += 1
    return user_id_counter["current"]

def get_next_course_id() -> int:
    course_id_counter["current"] += 1
    return course_id_counter["current"]

def get_next_enrollment_id() -> int:
    enrollment_id_counter["current"] += 1
    return enrollment_id_counter["current"]


# Initialize with sample data
def init_sample_data():
    """Initialize database with sample data"""
    # Sample user
    user_id = get_next_user_id()
    users_db[user_id] = {
        "id": user_id,
        "name": "Alice",
        "email": "alice@example.com",
        "is_active": True
    }
    
    # Sample course
    course_id = get_next_course_id()
    courses_db[course_id] = {
        "id": course_id,
        "title": "Python Basics",
        "description": "Learn Python",
        "is_open": True
    }
    
    # Sample enrollment
    enrollment_id = get_next_enrollment_id()
    enrollments_db[enrollment_id] = {
        "id": enrollment_id,
        "user_id": user_id,
        "course_id": course_id,
        "enrolled_date": date(2025, 9, 16),
        "completed": False
    }

# Initialize sample data on module load
init_sample_data()