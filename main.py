import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from controllers.users import router as UserRouter
from controllers.courses import router as CourseRouter
from controllers.lessons import router as LessonsRouter
from controllers.enrollments import router as EnrollmentRouter
from controllers.reviews import router as ReviewsRouter
from controllers.categories import router as CategoryRouter
from database import engine, Base
from config.environment import ENVIRONMENT, CORS_ORIGINS

# Import all models to ensure tables are created
from models.user import UserModel
from models.course import CourseModel
from models.lesson import LessonModel
from models.category import CategoryModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
app.include_router(ReviewsRouter, prefix="/api/reviews", tags=["Reviews"])
app.include_router(CategoryRouter, prefix="/api/categories", tags=["Categories"])

@app.get('/')
def home():
    return {'message': 'Welcome to SkillSprout API!'}

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
