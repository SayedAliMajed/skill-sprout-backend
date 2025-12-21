from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base import BaseModel 

class LessonModel(BaseModel):
    __tablename__