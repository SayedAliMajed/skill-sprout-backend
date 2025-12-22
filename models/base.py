from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from database import Base  # Import Base from database.py

class BaseModel(Base):
    __abstract__ = True  # Prevents this class from being mapped to a database table

    id: Mapped[int] = mapped_column(primary_key=True, index=True)  # Unique identifier for each record
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())  # Timestamp for when the record is created
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())  # Auto-updates on changes
