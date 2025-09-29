import requests

BASE_URL = "http://127.0.0.1:8000"

def test_full_workflow():
    print("🚀 Starting API Tests...\n")
    
    # 1. Create a user
    print("1️⃣ Creating a user...")
    user_response = requests.post(
        f"{BASE_URL}/api/users/",
        json={"name": "Test User", "email": "test@example.com"}
    )
    print(f"   Status: {user_response.status_code}")
    user = user_response.json()
    print(f"   Created user with ID: {user['id']}\n")
    
    # 2. Create a course
    print("2️⃣ Creating a course...")
    course_response = requests.post(
        f"{BASE_URL}/api/courses/",
        json={"title": "Test Course", "description": "A test course"}
    )
    print(f"   Status: {course_response.status_code}")
    course = course_response.json()
    print(f"   Created course with ID: {course['id']}\n")
    
    # 3. Enroll user in course
    print("3️⃣ Enrolling user in course...")
    enrollment_response = requests.post(
        f"{BASE_URL}/api/enrollments/",
        json={"user_id": user['id'], "course_id": course['id']}
    )
    print(f"   Status: {enrollment_response.status_code}")
    enrollment = enrollment_response.json()
    print(f"   Created enrollment with ID: {enrollment['id']}\n")
    
    # 4. Mark as complete
    print("4️⃣ Marking course as complete...")
    complete_response = requests.patch(
        f"{BASE_URL}/api/enrollments/{enrollment['id']}/complete"
    )
    print(f"   Status: {complete_response.status_code}")
    completed_enrollment = complete_response.json()
    print(f"   Completed: {completed_enrollment['completed']}\n")
    
    # 5. Get user's enrollments
    print("5️⃣ Getting user's enrollments...")
    user_enrollments = requests.get(
        f"{BASE_URL}/api/enrollments/user/{user['id']}"
    )
    print(f"   Status: {user_enrollments.status_code}")
    print(f"   User has {len(user_enrollments.json())} enrollment(s)\n")
    
    print("✅ All tests completed successfully!")

if __name__ == "__main__":
    test_full_workflow()