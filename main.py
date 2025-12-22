from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
import logging
import uvicorn
from contextlib import asynccontextmanager

from controllers.users import router as UserRouter
from controllers.enrollments import router as EnrollmentRouter
from database import engine, Base
from config.environment import ENVIRONMENT, CORS_ORIGINS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up application...")
    try:
        # Create database tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Database connection failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Startup error: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")

app = FastAPI(
    title="Skill Sprout Backend API",
    description="A FastAPI backend for Skill Sprout application with user authentication",
    version="1.0.0",
    docs_url="/docs" if ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if ENVIRONMENT == "development" else None,
    lifespan=lifespan
)

# Add CORS middleware
origins = [origin.strip() for origin in CORS_ORIGINS.split(",")] if CORS_ORIGINS else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(UserRouter, prefix="/api")
app.include_router(EnrollmentRouter, prefix="/api")

@app.get('/')
def home():
    return {
        "message": "Welcome to Skill Sprout Backend API!",
        "version": "1.0.0",
        "docs": "/docs" if ENVIRONMENT == "development" else "Documentation disabled in production"
    }

@app.get('/health')
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "environment": ENVIRONMENT}

# Global exception handler
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    logger.error(f"Database error: {exc}")
    return {
        "error": "Database error occurred",
        "detail": str(exc) if ENVIRONMENT == "development" else "Internal server error"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True if ENVIRONMENT == "development" else False)
