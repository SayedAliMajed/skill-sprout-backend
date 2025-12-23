from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config.environment import DATABASE_URL  # ✅ USE THIS!

# Create SQLAlchemy engine (uses config default!)
engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models (SQLAlchemy 2.0)
class Base(DeclarativeBase):
    pass

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
