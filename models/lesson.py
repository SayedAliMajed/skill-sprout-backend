from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from models.base import BaseModel 
from datetime import datetime
from sqlalchemy.sql import func

class LessonModel(BaseModel):
    __tablename__ = "lessons"

    # ✅ PRIMARY KEY (MUST HAVE)
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # ✅ PROPER MAPPED ANNOTATIONS
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    video_url: Mapped[str] = mapped_column(String(500))
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    content_text: Mapped[str] = mapped_column(String(1000))
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    
    # ✅ Timestamps (optional but recommended)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
    
    # ✅ Relationship
    course = relationship("CourseModel", back_populates="lessons")
