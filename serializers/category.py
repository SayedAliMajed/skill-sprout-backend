# serializers/category.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CategoryBaseSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    icon_url: Optional[str] = None
    color: Optional[str] = Field(default="#3B82F6", description="Hex color code")

class CategoryCreateSchema(CategoryBaseSchema):
    pass

class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    icon_url: Optional[str] = None
    color: Optional[str] = None

class CategoryResponseSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    icon_url: Optional[str]
    color: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CategoryWithCoursesSchema(CategoryResponseSchema):
    courses_count: Optional[int] = 0

    class Config:
        from_attributes = True
