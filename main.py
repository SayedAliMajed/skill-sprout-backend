# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.users import router as UserRouter
from controllers.courses import router as CourseRouter
from controllers.reviews import router as ReviewRouter

from database import engine
from models.base import BaseModel
# Import all models to ensure tables are created
from models.user import UserModel
from models.course import CourseModel
from models.review import ReviewModel

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
app.include_router(UserRouter, prefix="/api/users", tags=["Users"])
app.include_router(CourseRouter, prefix="/api/courses", tags=["Courses"])
app.include_router(ReviewRouter, prefix="/api/reviews", tags=["Reviews"])

@app.get('/')
def home():
    return {'message': 'Welcome to SkillSprout API!'}