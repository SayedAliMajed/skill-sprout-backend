from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Schema for creating or updating a review
class ReviewCreateSchema(BaseModel):
    rating: float = Field(..., ge=1.0, le=5.0)
    comment: Optional[str] = None

    class Config:
        from_attributes = True  # Updated for Pydantic v2

# Schema for updating a review (same as create, since rating and comment can be updated)
class ReviewUpdateSchema(BaseModel):
    rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    comment: Optional[str] = None

    class Config:
        from_attributes = True  # Updated for Pydantic v2

# Schema for returning full review data
class ReviewResponseSchema(BaseModel):
    id: int
    user_id: int
    course_id: int
    rating: float
    comment: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Updated for Pydantic v2

# Schema for individual reviews in list responses
class ReviewListItemSchema(BaseModel):
    id: int
    user_id: int
    rating: float
    comment: Optional[str]

    class Config:
        from_attributes = True  # Updated for Pydantic v2
