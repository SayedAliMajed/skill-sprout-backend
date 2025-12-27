 # serializers/course.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Schema for creating a new course
class CourseCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = ""
    price: Optional[float] = 0.0
    thumbnail_url: Optional[str] = ""

    class Config:
        from_attributes = True

# Schema for updating a course
class CourseUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    thumbnail_url: Optional[str] = None

    class Config:
        from_attributes = True

# Schema for returning course data
class CourseResponseSchema(BaseModel):
    id: int
    instructor_id: int
    title: str
    description: Optional[str]
    price: float
    thumbnail_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schema for returning course with instructor info
class InstructorInfoSchema(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class CourseWithInstructorSchema(BaseModel):
    id: int
    instructor_id: int
    title: str
    description: Optional[str]
    price: float
    thumbnail_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    instructor: Optional[InstructorInfoSchema] = None

    class Config:
        from_attributes = True