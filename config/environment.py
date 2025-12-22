import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# JWT secret key from environment
secret = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-change-this")

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ali:123@localhost:5432/skill_db")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# CORS Origins
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:8080")

# Logging Level
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")