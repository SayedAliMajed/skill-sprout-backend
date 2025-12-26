# models/course.py

from sqlalchemy import ForeignKey, Text, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import BaseModel
from typing import Optional

class CourseModel(BaseModel):

    __tablename__ = "courses"

    instructor_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="")
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, default="")

    # Relationship to User (instructor)
    instructor = relationship("UserModel", back_populates="courses")
    
    # Relationship to CategoryModel
    category = relationship("CategoryModel", back_populates="courses")
    
    # Relationship to EnrollmentModel
    enrollments = relationship("EnrollmentModel", back_populates="course")
    
    # Relationship to LessonModel
    lessons = relationship("LessonModel", back_populates="course")
    
    # Relationship to ReviewModel
    reviews = relationship("ReviewModel", back_populates="course")
