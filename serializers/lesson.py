from pydantic import BaseModel
from typing import Optional, List

class LessonCreate(BaseModel):
    title: str
    video_url: Optional[str] = None
    order_index: int = 0
    content_text: Optional[str] = None

class LessonResponse(BaseModel):
    id: int
    course_id: int
    title: str
    video_url: Optional[str] = None
    order_index: int
    content_text: Optional[str] = None

class LessonUpdate(BaseModel):  
    title: Optional[str] = None
    video_url: Optional[str] = None
    order_index: Optional[int] = None
    content_text: Optional[str] = None


    class Config:
        from_attributes = True
