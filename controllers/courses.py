# controllers/courses.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from models.course import CourseModel
from models.user import UserModel
from serializers.course import (
    CourseCreateSchema,
    CourseUpdateSchema,
    CourseResponseSchema,
    CourseWithInstructorSchema
)
from database import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()

# GET /courses - List all courses (public)
@router.get("/", response_model=List[CourseWithInstructorSchema])
def get_all_courses(
    search: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(CourseModel)

    # Apply search filter
    if search:
        query = query.filter(
            or_(
                CourseModel.title.ilike(f"%{search}%"),
                CourseModel.description.ilike(f"%{search}%")
            )
        )

    # Apply price filters
    if min_price is not None:
        query = query.filter(CourseModel.price >= min_price)
    if max_price is not None:
        query = query.filter(CourseModel.price <= max_price)

    # Order by newest first and apply pagination
    courses = query.order_by(CourseModel.created_at.desc()).offset(skip).limit(limit).all()

    # Build response with instructor info
    result = []
    for course in courses:
        course_data = {
            "id": course.id,
            "instructor_id": course.instructor_id,
            "title": course.title,
            "description": course.description,
            "price": course.price,
            "thumbnail_url": course.thumbnail_url,
            "created_at": course.created_at,
            "updated_at": course.updated_at,
            "instructor": {
                "id": course.instructor.id,
                "username": course.instructor.username,
                "email": course.instructor.email
            } if course.instructor else None
        }
        result.append(course_data)

    return result

# GET /courses/{id} - Get single course by ID (public)
@router.get("/{course_id}", response_model=CourseWithInstructorSchema)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    return {
        "id": course.id,
        "instructor_id": course.instructor_id,
        "title": course.title,
        "description": course.description,
        "price": course.price,
        "thumbnail_url": course.thumbnail_url,
        "created_at": course.created_at,
        "updated_at": course.updated_at,
        "instructor": {
            "id": course.instructor.id,
            "username": course.instructor.username,
            "email": course.instructor.email
        } if course.instructor else None
    }

# POST /courses - Create a new course (instructors only)
@router.post("/", response_model=CourseResponseSchema, status_code=status.HTTP_201_CREATED)
def create_course(
    course: CourseCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Check if user is instructor
    if current_user.role != "instructor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only instructors can create courses"
        )
    
    # Create new course with current user as instructor
    new_course = CourseModel(
        instructor_id=current_user.id,
        title=course.title,
        description=course.description or "",
        price=course.price or 0.0,
        thumbnail_url=course.thumbnail_url or ""
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course

# PUT /courses/{id} - Update a course (only owner can update)
@router.put("/{course_id}", response_model=CourseResponseSchema)
def update_course(
    course_id: int,
    course_data: CourseUpdateSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Find the course
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # Check if current user is the owner
    if course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this course"
        )

    # Update fields if provided
    if course_data.title is not None:
        course.title = course_data.title
    if course_data.description is not None:
        course.description = course_data.description
    if course_data.price is not None:
        course.price = course_data.price
    if course_data.thumbnail_url is not None:
        course.thumbnail_url = course_data.thumbnail_url

    db.commit()
    db.refresh(course)

    return course

# DELETE /courses/{id} - Delete a course (only owner can delete)
@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    # Find the course
    course = db.query(CourseModel).filter(CourseModel.id == course_id).first()

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    # Check if current user is the owner
    if course.instructor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this course"
        )

    db.delete(course)
    db.commit()

    return None

# GET /courses/my/courses - Get courses by current user (authenticated)
@router.get("/my/courses", response_model=List[CourseResponseSchema])
def get_my_courses(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    courses = db.query(CourseModel).filter(
        CourseModel.instructor_id == current_user.id
    ).order_by(CourseModel.created_at.desc()).all()

    return courses
