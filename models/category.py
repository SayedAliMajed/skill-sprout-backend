# models/category.py

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from models.base import BaseModel
from datetime import datetime

class CategoryModel(BaseModel):

    __tablename__ = "categories"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    icon_url = Column(String(500), nullable=True)
    color = Column(String(7), nullable=True, default="#3B82F6")  # Hex color code
    
    # Relationship to CourseModel
    courses = relationship("CourseModel", back_populates="category")

    def __repr__(self):
        return f"<CategoryModel(id={self.id}, name='{self.name}')>"
