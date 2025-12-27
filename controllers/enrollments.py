from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.enrollment import EnrollmentModel
from models.course import CourseModel
from models.user import UserModel
from dependencies.get_current_user import get_current_user
from serializers.enrollment import ProgressUpdateSchema, EnrollmentResponseSchema, EnrollmentListItemSchema

router = APIRouter()

# Enroll user to a course (existing route)
@router.post("/enroll/{course_id}", response_model=EnrollmentResponseSchema, status_code=status.HTTP_201_CREATED)
def enroll_in_course(course_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):

    # Validate course_id is a positive integer
    if course_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course ID. Must be a positive integer.",
        )

    # User role check
    if current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can enroll in courses"
        )

    # check if already enrolled
    existing_enrollment = ( db.query(EnrollmentModel).filter(
            EnrollmentModel.user_id == current_user.id,
            EnrollmentModel.course_id == course_id
        )
        .first()
    )

    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already enrolled in this course"
        )

    # create enrollment
    enrollment = EnrollmentModel(
        user_id=current_user.id,
        course_id=course_id
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment

# New route: Enroll user to a course (POST /api/enrollments with course_id in body)
@router.post("/", response_model=EnrollmentResponseSchema, status_code=status.HTTP_201_CREATED)
def enroll_in_course_body(course_data: dict, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):

    # User role check
    if current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can enroll in courses"
        )

    # Extract course_id from request body
    course_id = course_data.get("course_id")
    if not course_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="course_id is required in request body"
        )

    # Validate course_id is a positive integer
    if not isinstance(course_id, int) or course_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course ID. Must be a positive integer.",
        )

    # check if already enrolled
    existing_enrollment = ( db.query(EnrollmentModel).filter(
            EnrollmentModel.user_id == current_user.id,
            EnrollmentModel.course_id == course_id
        )
        .first()
    )

    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already enrolled in this course"
        )

    # Check if course exists
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # create enrollment
    enrollment = EnrollmentModel(
        user_id=current_user.id,
        course_id=course_id
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment

# Check enrollment status for a specific course
@router.get("/course/{course_id}/status")
def check_enrollment_status(course_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):

    # Validate course_id is a positive integer
    if course_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid course ID. Must be a positive integer.",
        )

    # Check if user is enrolled in the course
    enrollment = ( db.query(EnrollmentModel).filter(
            EnrollmentModel.user_id == current_user.id,
            EnrollmentModel.course_id == course_id
        )
        .first()
    )

    return {
        "enrolled": enrollment is not None,
        "course_id": course_id
    }

# get all the enrollments for a User
@router.get("/me", response_model=List[EnrollmentListItemSchema])
def get_my_enrollments(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):

    # get all enrollments
    enrollments = (db.query(EnrollmentModel).filter(EnrollmentModel.user_id == current_user.id).all())

    # return enrolled courses with progress
    return [{"course_id": e.course_id, "progress_percent": e.progress_percent} for e in enrollments]

# Update progress percent for an enrollment
@router.patch("/{enrollment_id}/progress", response_model=EnrollmentResponseSchema)
def update_progress(enrollment_id: int, progress_data: ProgressUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):

    # Validate enrollment_id is a positive integer
    if enrollment_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid enrollment ID. Must be a positive integer.",
        )

    # get the enrolled course
    enrollment = (db.query(EnrollmentModel).filter(EnrollmentModel.id == enrollment_id).first())

    # check if enrollment exsist
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )

    # in here only user can update its course atus
    if enrollment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this enrollment"
        )

    # update the progress
    enrollment.progress_percent = progress_data.progress_percent
    db.commit()
    db.refresh(enrollment)

    return enrollment
