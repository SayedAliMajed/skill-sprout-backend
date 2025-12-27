from sqlalchemy import Column, Integer, Float, ForeignKey, Text, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from models.base import BaseModel


class ReviewModel(BaseModel):
    __tablename__ = "reviews"

    # ForeignKey (user/student)
    student_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # ForeignKey (course)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)

    # Rating: usually 1.0 – 5.0
    rating = Column(Integer, nullable=False)

    # text comment
    comment = Column(Text, nullable=True)

    # Prevent duplicate
    __table_args__ = (
        # One review per student per course
        UniqueConstraint( "course_id", "student_id", name="uq_student_course_review",),
        # Ensure rating is between 1 and 5
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_review_rating_range",),
    )

    # Relationships
    student = relationship("UserModel", back_populates="reviews")
    course = relationship("CourseModel", back_populates="reviews")
