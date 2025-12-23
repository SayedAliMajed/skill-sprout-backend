from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.enrollment import EnrollmentModel
from models.course import Course
from models.user import UserModel
from dependencies.get_current_user import get_current_user

router = APIRouter()

# Enroll user to a course
@router.post("/enroll/{course_id}", status_code=status.HTTP_201_CREATED)
def enroll_in_course(course_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):

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

    return {
        "message": "Successfully enrolled",
        "enrollment_id": enrollment.id
    }


# get all the enrollments for a User
@router.get("/me")
def get_my_enrollments(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):

    # get all enrollments
    enrollments = (db.query(EnrollmentModel).filter(EnrollmentModel.user_id == current_user.id).all())

    # return enrolled courses with progress
    return [{"course_id": e.course_id, "progress_percent": e.progress_percent} for e in enrollments]

# Update progress percent for an enrollment
@router.patch("/{enrollment_id}/progress")
def update_progress(enrollment_id: int, progress_percent: float, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):

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

    # check the enrollment progress % is valid to update
    if progress_percent < 0.0 or progress_percent > 1.0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Progress must be between 0.0 and 1.0"
        )

    # update the progress
    enrollment.progress_percent = progress_percent
    db.commit()
    db.refresh(enrollment)

    return {
        "message": "Progress updated",
        "progress_percent": enrollment.progress_percent
    }