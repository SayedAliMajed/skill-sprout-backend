from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db

from models.review import ReviewModel
from models.enrollment import EnrollmentModel
from models.course import CourseModel
from models.user import UserModel
from dependencies.get_current_user import get_current_user
from serializers.review import ReviewCreateSchema, ReviewResponseSchema

router = APIRouter()

@router.post("/{course_id}/reviews", response_model=ReviewResponseSchema, status_code=status.HTTP_200_OK)
def create_or_update_review(course_id: int, review_data: ReviewCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):

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
        review.rating = review_data.rating
        review.comment = review_data.comment
    else:
        review = ReviewModel(
            course_id=course_id,
            user_id=current_user.id,
            rating=review_data.rating,
            comment=review_data.comment,
        )
        db.add(review)

    db.commit()
    db.refresh(review)

    return review

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
