from sqlalchemy import Column, Integer, ForeignKey, Float, UniqueConstraint, func, DateTime
from sqlalchemy.orm import relationship
from models.base import BaseModel


class EnrollmentModel(BaseModel):
    __tablename__ = "enrollments"

    # ForeignKey (user)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # ForeignKey (course)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)

    # set the enrolled_at to the current database timestamp when a new record is inserted
    # DateTime and func.now() is better then datetime and day.now
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # % is Float (0.0 to 1.0)
    progress_percent = Column(Float, default=0.0, nullable=False)

    # Prevent duplicate enrollment
    __table_args__ = (UniqueConstraint("user_id", "course_id", name="uq_user_course_enrollment"),)

    # Relationships
    user = relationship("UserModel", back_populates="enrollments")
    course = relationship("CourseModel", back_populates="enrollments")
    # course relationship is not added yet to course model