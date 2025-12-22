from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment
<<<<<<< HEAD
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://ali:123@localhost:5432/skill_db")
=======
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")
>>>>>>> eb0ee7f7ccc3be10c1e7df6b636dff69b08a3444

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models using modern SQLAlchemy 2.0 pattern
class Base(DeclarativeBase):
    pass

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
