from sqlalchemy import Column, DateTime, Integer, func
from database import Base  # Import Base from database.py

class BaseModel(Base):
    __abstract__ = True  # Prevents this class from being mapped to a database table

    id = Column(Integer, primary_key=True, index=True)  # Unique identifier for each record
    created_at = Column(DateTime, default=func.now())  # Timestamp for when the record is created
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Auto-updates on changes
