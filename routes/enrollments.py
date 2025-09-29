from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import date
from schemas import Enrollment, EnrollmentCreate, EnrollmentComplete
from services.database import (
    enrollments_db, users_db, courses_db, get_next_enrollment_id
)

router = APIRouter()


@router.post("/", response_model=Enrollment, status_code=status.HTTP_201_CREATED)
def enroll_user(enrollment: EnrollmentCreate):
    """Enroll a user in a course"""
    # Check if user exists
    if enrollment.user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user is active
    if not users_db[enrollment.user_id]["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only active users can enroll in courses"
        )
    
    # Check if course exists
    if enrollment.course_id not in courses_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # Check if course is open
    if not courses_db[enrollment.course_id]["is_open"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course enrollment is closed"
        )
    
    # Check if user is already enrolled
    for existing_enrollment in enrollments_db.values():
        if (existing_enrollment["user_id"] == enrollment.user_id and 
            existing_enrollment["course_id"] == enrollment.course_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already enrolled in this course"
            )
    
    # Create enrollment
    enrollment_id = get_next_enrollment_id()
    new_enrollment = {
        "id": enrollment_id,
        "user_id": enrollment.user_id,
        "course_id": enrollment.course_id,
        "enrolled_date": date.today(),
        "completed": False
    }
    enrollments_db[enrollment_id] = new_enrollment
    return new_enrollment


@router.get("/", response_model=List[Enrollment])
def get_all_enrollments():
    """Get all enrollments"""
    return list(enrollments_db.values())


@router.get("/{enrollment_id}", response_model=Enrollment)
def get_enrollment(enrollment_id: int):
    """Get a specific enrollment by ID"""
    if enrollment_id not in enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    return enrollments_db[enrollment_id]


@router.get("/user/{user_id}", response_model=List[Enrollment])
def get_user_enrollments(user_id: int):
    """Get all enrollments for a specific user"""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_enrollments = [
        enrollment 
        for enrollment in enrollments_db.values() 
        if enrollment["user_id"] == user_id
    ]
    return user_enrollments


@router.patch("/{enrollment_id}/complete", response_model=Enrollment)
def mark_course_complete(enrollment_id: int):
    """Mark a course enrollment as completed"""
    if enrollment_id not in enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    enrollments_db[enrollment_id]["completed"] = True
    return enrollments_db[enrollment_id]


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_enrollment(enrollment_id: int):
    """Delete an enrollment"""
    if enrollment_id not in enrollments_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    del enrollments_db[enrollment_id]