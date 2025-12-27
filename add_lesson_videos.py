#!/usr/bin/env python3
"""
Add YouTube video URLs to existing lessons in the database
"""

from sqlalchemy.orm import Session
from database import SessionLocal
from models.lesson import LessonModel
from models.course import CourseModel
from models.user import UserModel
from models.category import CategoryModel
from models.enrollment import EnrollmentModel
from models.review import ReviewModel

# Sample YouTube video URLs for different lesson types
SAMPLE_VIDEOS = [
    "https://www.youtube.com/watch?v=rfscVS0vtbw",  # Python tutorial
    "https://www.youtube.com/watch?v=W6NZfCO5SIk",  # JavaScript tutorial
    "https://www.youtube.com/watch?v=sBws8MS3sJs",  # React tutorial
    "https://www.youtube.com/watch?v=8hly31xKli0",  # Algorithms
    "https://www.youtube.com/watch?v=GqQXzAPPD3g",  # C# tutorial
    "https://www.youtube.com/watch?v=QrR_gm6RqMc",  # Web development
    "https://www.youtube.com/watch?v=Air5N1kJ5iQ",  # Machine learning
    "https://www.youtube.com/watch?v=z9U3VmKa6eU",  # iOS development
    "https://www.youtube.com/watch?v=J99qYq9yNgg",  # Digital marketing
    "https://www.youtube.com/watch?v=UtFi7IHP7l4",  # Photoshop
]

def add_video_urls_to_lessons():
    """Add YouTube video URLs to lessons that don't have them"""
    db = SessionLocal()

    try:
        # Get all lessons - check all of them
        all_lessons = db.query(LessonModel).all()
        print(f"Total lessons in database: {len(all_lessons)}")

        # Get all lessons that don't have video URLs
        lessons_without_videos = db.query(LessonModel).filter(
            LessonModel.video_url.is_(None)
        ).all()

        print(f"Found {len(lessons_without_videos)} lessons without video URLs")

        # Also check for empty strings
        lessons_with_empty_videos = db.query(LessonModel).filter(
            LessonModel.video_url == ""
        ).all()

        print(f"Found {len(lessons_with_empty_videos)} lessons with empty video URLs")

        # Combine both lists
        lessons_to_update = lessons_without_videos + lessons_with_empty_videos

        for i, lesson in enumerate(lessons_to_update):
            # Cycle through the sample videos
            video_url = SAMPLE_VIDEOS[i % len(SAMPLE_VIDEOS)]
            lesson.video_url = video_url
            print(f"Updated lesson '{lesson.title}' (ID: {lesson.id}) with video: {video_url}")

        db.commit()
        print(f"Successfully updated {len(lessons_to_update)} lessons with video URLs")

    except Exception as e:
        print(f"Error updating lessons: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_video_urls_to_lessons()
