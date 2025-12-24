# serializers/user.py


from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserSchema(BaseModel):
    username: str  # User's unique name
    email: str  # User's email address
    password: str  # Plain text password for user registration (will be hashed before saving)
    first_name: str 
    last_name: str
    role: str = "student"
    bio: str

    class Config:
        from_attributes = True  # Updated for Pydantic v2

# Schema for returning user data (without exposing the password)
class UserResponseSchema(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True  # Updated for Pydantic v2

class UserLogin(BaseModel):
    email: str  # Email provided by the user during login (supports both email and username)
    password: str  # Plain text password provided by the user during login

    class Config:
        from_attributes = True  # Updated for Pydantic v2

# New schema for the response (containing the JWT token and a success message)
class UserToken(BaseModel):
    token: str  # JWT token generated upon successful login
    message: str  # Success message

    class Config:
        from_attributes = True  # Updated for Pydantic v2
