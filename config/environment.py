import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# JWT secret key from environment
secret = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-change-this")

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://sayed:123@localhost:5432/hoot_db")
