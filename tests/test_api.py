from fastapi.testclient import TestClient
from main import app
from services.database import users_db, courses_db, enrollments_db

client = TestClient(app)


def setup_function():
    """Clear databases before each test"""
    users_db.clear()
    courses_db.clear()
    enrollments_db.clear()


# User Tests
def test_create_user():
    response = client.post(
        "/api/users/",
        json={"name": "John Doe", "email": "john@example.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["is_active"] is True


def test_create_duplicate_email():
    client.post("/api/users/", json={"name": "John", "email": "john@example.com"})
    response = client.post(
        "/api/users/",
        json={"name": "Jane", "email": "john@example.com"}
    )
    assert response.status_code == 400


def test_get_all_users():
    client.post("/api/users/", json={"name": "John", "email": "john@example.com"})
    client.post("/api/users/", json={"name": "Jane", "email": "jane@example.com"})
    
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_user():
    create_response = client.post(
        "/api/users/",
        json={"name": "John", "email": "john@example.com"}
    )
    user_id = create_response.json()["id"]
    
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "John"


def test_update_user():
    create_response = client.post(
        "/api/users/",
        json={"name": "John", "email": "john@example.com"}
    )
    user_id = create_response.json()["id"]
    
    response = client.put(
        f"/api/users/{user_id}",
        json={"name": "John Updated"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "John Updated"


def test_deactivate_user():
    create_response = client.post(
        "/api/users/",
        json={"name": "John", "email": "john@example.com"}
    )
    user_id = create_response.json()["id"]
    
    response = client.patch(f"/api/users/{user_id}/deactivate")
    assert response.status_code == 200
    assert response.json()["is_active"] is False


def test_delete_user():
    create_response = client.post(
        "/api/users/",
        json={"name": "John", "email": "john@example.com"}
    )
    user_id = create_response.json()["id"]
    
    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 204


# Course Tests
def test_create_course():
    response = client.post(
        "/api/courses/",
        json={"title": "Python 101", "description": "Intro to Python"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Python 101"
    assert data["is_open"] is True


def test_get_all_courses():
    client.post(
        "/api/courses/",
        json={"title": "Python 101", "description": "Intro to Python"}
    )
    client.post(
        "/api/courses/",
        json={"title": "JavaScript 101", "description": "Intro to JS"}
    )
    
    response = client.get("/api/courses/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_close_course_enrollment():
    create_response = client.post(
        "/api/courses/",
        json={"title": "Python 101", "description": "Intro to Python"}
    )
    course_id = create_response.json()["id"]
    
    response = client.patch(f"/api/courses/{course_id}/close")
    assert response.status_code == 200
    assert response.json()["is_open"] is False


# Enrollment Tests
def test_enroll_user():
    user_response = client.post(
        "/api/users/",
        json={"name": "John", "email": "john@example.com"}
    )
    user_id = user_response.json()["id"]
    
    course_response = client.post(
        "/api/courses/",
        json={"title": "Python 101", "description": "Intro to Python"}
    )
    course_id = course_response.json()["id"]
    
    response = client.post(
        "/api/enrollments/",
        json={"user_id": user_id, "course_id": course_id}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == user_id
    assert data["course_id"] == course_id
    assert data["completed"] is False


def test_enroll_inactive_user():
    user_response = client.post(
        "/api/users/",
        json={"name": "John", "email": "john@example.com"}
    )
    user_id = user_response.json()["id"]
    client.patch(f"/api/users/{user_id}/deactivate")
    
    course_response = client.post(
        "/api/courses/",
        json={"title": "Python 101", "description": "Intro to Python"}
    )
    course_id = course_response.json()["id"]
    
    response = client.post(
        "/api/enrollments/",
        json={"user_id": user_id, "course_id": course_id}
    )
    assert response.status_code == 400


def test_enroll_in_closed_course():
    user_response = client.post(
        "/api/users/",
        json={"name": "John", "email": "john@example.com"}
    )
    user_id = user_response.json()["id"]
    
    course_response = client.post(
        "/api/courses/",
        json={"title": "Python 101", "description": "Intro to Python"}
    )
    course_id = course_response.json()["id"]
    client.patch(f"/api/courses/{course_id}/close")
    
    response = client.post(
        "/api/enrollments/",
        json={"user_id": user_id, "course_id": course_id}
    )
    assert response.status_code == 400


def test_duplicate_enrollment():
    user_response = client.post(
        "/api/users/",
        json={"name": "John", "email": "john@example.com"}
    )
    user_id = user_response.json()["id"]
    
    course_response = client.post(
        "/api/courses/",
        json={"title": "Python 101", "description": "Intro to Python"}
    )
    course_id = course_response.json()["id"]
    
    client.post(
        "/api/enrollments/",
        json={"user_id": user_id, "course_id": course_id}
    )
    response = client.post(
        "/api/enrollments/",
        json={"user_id": user_id, "course_id": course_id}
    )
    assert response.status_code == 400


def test_mark_enrollment_complete():
    user_response = client.post(
        "/api/users/",
        json={"name": "John", "email": "john@example.com"}
    )
    user_id = user_response.json()["id"]
    
    course_response = client.post(
        "/api/courses/",
        json={"title": "Python 101", "description": "Intro to Python"}
    )
    course_id = course_response.json()["id"]
    
    enrollment_response = client.post(
        "/api/enrollments/",
        json={"user_id": user_id, "course_id": course_id}
    )
    enrollment_id = enrollment_response.json()["id"]
    
    response = client.patch(f"/api/enrollments/{enrollment_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_get_user_enrollments():
    user_response = client.post(
        "/api/users/",
        json={"name": "John", "email": "john@example.com"}
    )
    user_id = user_response.json()["id"]
    
    course1_response = client.post(
        "/api/courses/",
        json={"title": "Python 101", "description": "Intro to Python"}
    )
    course1_id = course1_response.json()["id"]
    
    course2_response = client.post(
        "/api/courses/",
        json={"title": "JavaScript 101", "description": "Intro to JS"}
    )
    course2_id = course2_response.json()["id"]
    
    client.post(
        "/api/enrollments/",
        json={"user_id": user_id, "course_id": course1_id}
    )
    client.post(
        "/api/enrollments/",
        json={"user_id": user_id, "course_id": course2_id}
    )
    
    response = client.get(f"/api/enrollments/user/{user_id}")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_course_enrollments():
    user1_response = client.post(
        "/api/users/",
        json={"name": "John", "email": "john@example.com"}
    )
    user1_id = user1_response.json()["id"]
    
    user2_response = client.post(
        "/api/users/",
        json={"name": "Jane", "email": "jane@example.com"}
    )
    user2_id = user2_response.json()["id"]
    
    course_response = client.post(
        "/api/courses/",
        json={"title": "Python 101", "description": "Intro to Python"}
    )
    course_id = course_response.json()["id"]
    
    client.post(
        "/api/enrollments/",
        json={"user_id": user1_id, "course_id": course_id}
    )
    client.post(
        "/api/enrollments/",
        json={"user_id": user2_id, "course_id": course_id}
    )
    
    response = client.get(f"/api/courses/{course_id}/enrollments")
    assert response.status_code == 200
    assert len(response.json()) == 2