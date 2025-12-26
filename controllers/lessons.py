from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models.lesson import LessonModel
from models.course import CourseModel
from models.user import UserModel
from models.enrollment import EnrollmentModel
from serializers.lesson import LessonCreate, LessonResponse, LessonUpdate
from database import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()

@router.post("/courses/{course_id}", response_model=LessonResponse)
def create_lesson(
    course_id: int,
    lesson_in: LessonCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Check if user is instructor
    if current_user.role != "instructor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors can create lessons"
        )
    
    # Verify course exists and user owns it
    course = db.query(CourseModel).filter(
        CourseModel.id == course_id,
        CourseModel.instructor_id == current_user.id
    ).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Create a new lesson in the database
    new_lesson = LessonModel(**lesson_in.dict(), course_id=course_id)
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson

@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db)
):
    """Get a single lesson by ID - Public endpoint (no authentication required)"""
    
    lesson = db.query(LessonModel).filter(LessonModel.id == lesson_id).first()
    
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    return lesson

@router.get("/course/{course_id}/public", response_model=List[LessonResponse])
def get_lessons_public(
    course_id: int, 
    db: Session = Depends(get_db)
):
    """Get lessons for a specific course - PUBLIC ENDPOINT (no authentication required)"""
    
    # First verify the course exists
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Get all lessons for this course
    lessons = db.query(LessonModel).filter(
        LessonModel.course_id == course_id
    ).order_by(LessonModel.order_index).all()

    # Return lesson previews (hide video URLs for non-enrolled users)
    preview_lessons = []
    for lesson in lessons:
        # Create a lesson preview without sensitive content
        lesson_dict = {
            "id": lesson.id,
            "title": lesson.title,
            "order_index": lesson.order_index,
            "content_text": f"Preview: {lesson.content_text[:100]}...",  # Truncated preview
            "video_url": None,  # Hide video URL from public users
            "course_id": lesson.course_id
        }
        preview_lessons.append(lesson_dict)
    
    return preview_lessons

@router.get("/course/{course_id}", response_model=List[LessonResponse])
def get_lessons(
    course_id: int, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Get lessons for a specific course - Requires authentication and enrollment"""
    
    # First verify the course exists
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check if user is enrolled in the course
    enrollment = db.query(EnrollmentModel).filter(
        EnrollmentModel.user_id == current_user.id,
        EnrollmentModel.course_id == course_id      
    ).first()

    if not enrollment:
        raise HTTPException(status_code=403, detail="Enroll in course first")
    
    lessons = db.query(LessonModel).filter(
        LessonModel.course_id == course_id
    ).order_by(LessonModel.order_index).all()

    return lessons

# New public route for course preview (no enrollment required)
@router.get("/course/{course_id}/public", response_model=List[LessonResponse])
def get_public_lessons(course_id: int, db: Session = Depends(get_db)):
    
    # Check if course exists
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    lessons = db.query(LessonModel).filter(
        LessonModel.course_id == course_id
    ).order_by(LessonModel.order_index).all()

    # For public view, return lessons but with limited content if needed
    # You can customize this based on your business logic
    return lessons

@router.patch("/{lesson_id}", response_model=LessonResponse)
def update_lesson(
    lesson_id: int,
    lesson_update: LessonUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Check if user is instructor
    if current_user.role != "instructor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors can update lessons"
        )
    
    lesson = db.query(LessonModel).filter(LessonModel.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    course = db.query(CourseModel).filter(
        CourseModel.id == lesson.course_id,
        CourseModel.instructor_id == current_user.id
    ).first()

    if not course:
        raise HTTPException(status_code=403, detail="Not authorized to edit this lesson")
    
    for field, value in lesson_update.dict(exclude_unset = True).items():
        setattr(lesson, field, value)

    db.commit()
    db.refresh(lesson)
    return lesson

@router.delete("/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Check if user is instructor
    if current_user.role != "instructor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors can delete lessons"
        )
    
    lesson = db.query(LessonModel).filter(LessonModel.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    course = db.query(CourseModel).filter(
        CourseModel.id == lesson.course_id,
        CourseModel.instructor_id == current_user.id
    ).first()

    if not course:
        raise HTTPException(status_code=403, detail="Not authorized to delete this lesson")
    
    db.delete(lesson)
    db.commit()
    return {"message": "Lesson deleted successfully"}
