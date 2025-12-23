from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.users import router as UserRouter
from controllers.courses import router as CourseRouter
from controllers.lessons import router as LessonsRouter
from controllers.enrollments import router as EnrollmentRouter
from database import engine, Base
from config.environment import ENVIRONMENT, CORS_ORIGINS

# Import all models to ensure tables are created
from models.user import UserModel
from models.course import CourseModel
from models.lesson import LessonModel

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SkillSprout API", version="1.0.0")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include ALL routers with proper prefixes + tags
app.include_router(UserRouter, prefix="/api/users", tags=["Users"])
app.include_router(CourseRouter, prefix="/api/courses", tags=["Courses"])
app.include_router(LessonsRouter, prefix="/api/lessons", tags=["Lessons"])
app.include_router(EnrollmentRouter, prefix="/api/enrollments", tags=["Enrollments"])

@app.get('/')
def home():
    return {'message': 'Welcome to SkillSprout API!'}
