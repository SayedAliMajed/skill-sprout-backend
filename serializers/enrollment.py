from pydantic import BaseModel, Field
from datetime import datetime

# Schema for updating enrollment progress
class ProgressUpdateSchema(BaseModel):
    progress_percent: float = Field(..., ge=0.0, le=1.0)

    class Config:
        from_attributes = True  # Updated for Pydantic v2

# Schema for returning full enrollment data
class EnrollmentResponseSchema(BaseModel):
    id: int
    user_id: int
    course_id: int
    enrolled_at: datetime
    progress_percent: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Updated for Pydantic v2

# Schema for enrollment items in list responses (user's enrollments)
class EnrollmentListItemSchema(BaseModel):
    course_id: int
    progress_percent: float

    class Config:
        from_attributes = True  # Updated for Pydantic v2
