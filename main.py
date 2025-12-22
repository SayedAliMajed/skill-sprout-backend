# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.users import router as UserRouter
<<<<<<< HEAD
from controllers.enrollments import router as EnrollmentRouter
from database import engine, Base
from config.environment import ENVIRONMENT, CORS_ORIGINS
=======
from controllers.courses import router as CourseRouter
from database import engine
from models.base import BaseModel
# Import all models to ensure tables are created
from models.user import UserModel
from models.course import CourseModel
>>>>>>> eb0ee7f7ccc3be10c1e7df6b636dff69b08a3444

# Create all database tables
BaseModel.metadata.create_all(bind=engine)

app = FastAPI(title="SkillSprout API", version="1.0.0")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
<<<<<<< HEAD
app.include_router(UserRouter, prefix="/api")
app.include_router(EnrollmentRouter, prefix="/api")
=======
app.include_router(UserRouter, prefix="/api/users", tags=["Users"])
app.include_router(CourseRouter, prefix="/api/courses", tags=["Courses"])
>>>>>>> eb0ee7f7ccc3be10c1e7df6b636dff69b08a3444

@app.get('/')
def home():
    return {'message': 'Welcome to SkillSprout API!'}