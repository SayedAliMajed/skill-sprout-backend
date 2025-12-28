# models/user.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import BaseModel  # Import BaseModel from base.py
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta  # New import for timestamps
from jose import jwt

# Creating a password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel(BaseModel):

    __tablename__ = "users"

    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False) 
    password_hash = Column(String, nullable=True)  # Add new field for storing the hashed password
    role = Column(String, nullable=False)
    bio = Column(String)
    

    courses = relationship("CourseModel", back_populates="instructor")
    enrollments = relationship("EnrollmentModel", back_populates="user")
    reviews = relationship("ReviewModel", back_populates="student")

    # Method to hash and store the password
    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    def generate_token(self):
        from config.environment import secret
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
            "iat": datetime.now(timezone.utc),
            "sub": str(self.id),
            "role": self.role  # Include role in JWT token for enhanced authorization
        }

        token = jwt.encode(payload, secret, algorithm="HS256")

        return token
