from fastapi import APIRouter, Depends, HTTPException
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

@router.get("/{course_id}", response_model=List[LessonResponse])
def get_lessons(course_id: int, 
                db: Session = Depends(get_db),
                current_user: UserModel = Depends(get_current_user)
                ):
    
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

@router.patch("/{lesson_id}", response_model=LessonResponse)
def update_lesson(
    lesson_id: int,
    lesson_update: LessonUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    lesson = db.query(LessonModel).filter(LessonModel.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson no found")
    
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
    return {"message": "Lesson deleted succesfully"}
