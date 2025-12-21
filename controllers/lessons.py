from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from models.Lesson import LessonModel
from models.course import CourseModel
from serializers.lesson import LessonCreate, LessonResponse
from database import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()

@router.post("/", response_model=LessonResponse)
def create_lesson(
    lesson_in: LessonCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    
     # Verify course exists and user owns it
    course = db.query(CourseModel).filter(
        CourseModel.id == lesson_in.course_id,
        CourseModel.instructor_id == current_user.id
    ).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Create a new lesson in the database
    new_lesson = LessonModel(**lesson_in.dict())
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson
