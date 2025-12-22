from sqlalchemy.orm import Mapped, mapped_column
from models.base import BaseModel  # Import BaseModel instead of Base
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta  # New import for timestamps
from jose import jwt

# Creating a password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from config.environment import secret

class UserModel(BaseModel):

    __tablename__ = "users"

    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=True)  # Add new field for storing the hashed password
    role = Column(String, nullable=False)
    bio = Column(String)
    

    courses = relationship("CourseModel", back_populates="instructor")
    enrollments = relationship("EnrollmentModel", back_populates="user")

    # Method to hash and store the password
    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    def generate_token(self):
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
            "iat": datetime.now(timezone.utc),
            "sub": self.id
        }

        token = jwt.encode(payload, secret, algorithm="HS256")

        return token
