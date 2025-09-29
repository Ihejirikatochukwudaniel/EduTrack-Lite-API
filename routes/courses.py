from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas import Course, CourseCreate, CourseUpdate, User
from services.database import courses_db, users_db, enrollments_db, get_next_course_id

router = APIRouter()


@router.post("/", response_model=Course, status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate):
    """Create a new course"""
    course_id = get_next_course_id()
    new_course = {
        "id": course_id,
        "title": course.title,
        "description": course.description,
        "is_open": True
    }
    courses_db[course_id] = new_course
    return new_course


@router.get("/", response_model=List[Course])
def get_all_courses():
    """Get all courses"""
    return list(courses_db.values())


@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int):
    """Get a specific course by ID"""
    if course_id not in courses_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    return courses_db[course_id]


@router.put("/{course_id}", response_model=Course)
def update_course(course_id: int, course_update: CourseUpdate):
    """Update a course"""
    if course_id not in courses_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    course = courses_db[course_id]
    update_data = course_update.model_dump(exclude_unset=True)
    course.update(update_data)
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int):
    """Delete a course"""
    if course_id not in courses_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    del courses_db[course_id]


@router.patch("/{course_id}/close", response_model=Course)
def close_course_enrollment(course_id: int):
    """Close enrollment for a course"""
    if course_id not in courses_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    courses_db[course_id]["is_open"] = False
    return courses_db[course_id]


@router.get("/{course_id}/enrollments", response_model=List[User])
def get_course_enrollments(course_id: int):
    """Get all users enrolled in a specific course"""
    if course_id not in courses_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Find all enrollments for this course
    enrolled_user_ids = [
        enrollment["user_id"] 
        for enrollment in enrollments_db.values() 
        if enrollment["course_id"] == course_id
    ]
    
    # Get user details
    enrolled_users = [
        users_db[user_id] 
        for user_id in enrolled_user_ids 
        if user_id in users_db
    ]
    
    return enrolled_users