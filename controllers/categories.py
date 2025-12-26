# controllers/categories.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.category import CategoryModel
from models.course import CourseModel
from serializers.category import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema,
    CategoryWithCoursesSchema
)

router = APIRouter()

# GET /categories - List all categories
@router.get("/", response_model=List[CategoryWithCoursesSchema])
def get_all_categories(
    include_counts: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(CategoryModel)
    
    if include_counts:
        # Join with courses to get course counts
        query = query.outerjoin(CourseModel).group_by(CategoryModel.id)
        categories = []
        for category in query.all():
            course_count = len(category.courses) if category.courses else 0
            category_dict = {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "icon_url": category.icon_url,
                "color": category.color,
                "created_at": category.created_at,
                "updated_at": category.updated_at,
                "courses_count": course_count
            }
            categories.append(category_dict)
        return categories
    else:
        return query.all()

# GET /categories/{category_id} - Get single category
@router.get("/{category_id}", response_model=CategoryResponseSchema)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return category

# POST /categories - Create new category
@router.post("/", response_model=CategoryResponseSchema, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreateSchema,
    db: Session = Depends(get_db)
):
    # Check if category name already exists
    existing = db.query(CategoryModel).filter(CategoryModel.name == category.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )
    
    # Create new category
    new_category = CategoryModel(
        name=category.name,
        description=category.description,
        icon_url=category.icon_url,
        color=category.color
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return new_category

# PUT /categories/{category_id} - Update category
@router.put("/{category_id}", response_model=CategoryResponseSchema)
def update_category(
    category_id: int,
    category_data: CategoryUpdateSchema,
    db: Session = Depends(get_db)
):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Check if name is being changed and already exists
    if category_data.name and category_data.name != category.name:
        existing = db.query(CategoryModel).filter(
            CategoryModel.name == category_data.name,
            CategoryModel.id != category_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )
    
    # Update fields if provided
    if category_data.name is not None:
        category.name = category_data.name
    if category_data.description is not None:
        category.description = category_data.description
    if category_data.icon_url is not None:
        category.icon_url = category_data.icon_url
    if category_data.color is not None:
        category.color = category_data.color
    
    db.commit()
    db.refresh(category)
    
    return category

# DELETE /categories/{category_id} - Delete category
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Check if category has courses
    courses_count = db.query(CourseModel).filter(CourseModel.category_id == category_id).count()
    if courses_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete category with {courses_count} courses. Please reassign or delete courses first."
        )
    
    db.delete(category)
    db.commit()
    
    return None

# GET /categories/{category_id}/courses - Get courses in category
@router.get("/{category_id}/courses")
def get_category_courses(category_id: int, db: Session = Depends(get_db)):
    # Verify category exists
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    courses = db.query(CourseModel).filter(CourseModel.category_id == category_id).all()
    
    return {
        "category": {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "icon_url": category.icon_url,
            "color": category.color
        },
        "courses": courses,
        "total_courses": len(courses)
    }
