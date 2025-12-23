from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel 
from models.course import CourseModel

class LessonModel(BaseModel):
    __tablename__ = "lessons"

    title = Column(String(255),nullable=False)
    video_url = Column(String(500))
    order_index = Column(Integer, nullable=False, default=0)
    content_text = Column(String)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)

    course = relationship("CourseModel", back_populates="lessons")
    
