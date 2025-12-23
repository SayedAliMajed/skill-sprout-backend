from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db

from models.review import ReviewModel
from models.enrollment import EnrollmentModel
from models.course import CourseModel
from models.user import UserModel
from dependencies.get_current_user import get_current_user

router = APIRouter()

@router.post("/{course_id}/reviews", status_code=status.HTTP_200_OK)
def create_or_update_review(course_id: int, rating: float, comment: str | None = None, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    
    # Validate rating early
    if rating < 1.0 or rating > 5.0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1.0 and 5.0",
        )

    # Check course exists
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    # Check enrollment
    enrollment = (db.query(EnrollmentModel).filter(
            EnrollmentModel.course_id == course_id,
            EnrollmentModel.user_id == current_user.id,
        ).first()
    )

    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be enrolled to review this course",
        )

    # Check existing review
    review = (db.query(ReviewModel).filter(
            ReviewModel.course_id == course_id,
            ReviewModel.user_id == current_user.id,
        ).first()
    )

    if review:
        review.rating = rating
        review.comment = comment
        message = "Review updated"
    else:
        review = ReviewModel(
            course_id=course_id,
            user_id=current_user.id,
            rating=rating,
            comment=comment,
        )
        db.add(review)
        message = "Review created"

    db.commit()
    db.refresh(review)

    return {
        "message": message,
        "review": {
            "id": review.id,
            "rating": review.rating,
            "comment": review.comment,
        },
    }

@router.get("/{course_id}/reviews")
def get_course_reviews(course_id: int, db: Session = Depends(get_db)):
    
    # Ensure course exists
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    reviews = (db.query(ReviewModel).filter(ReviewModel.course_id == course_id).all())

    average_rating = (db.query(func.avg(ReviewModel.rating)).filter(ReviewModel.course_id == course_id).scalar())

    return {
        "course_id": course_id,
        "average_rating": round(average_rating, 2) if average_rating else None,
        "total_reviews": len(reviews),
        "reviews": [
            {
                "id": review.id,
                "user_id": review.user_id,
                "rating": review.rating,
                "comment": review.comment,
            }
            for review in reviews
        ],
    }
