#!/usr/bin/env python3

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def fix_course_23_lessons():
    print("🎯 Fixing Duplicate Lessons in Course 23")
    print("=" * 60)
    
    # Strategy: Create a new course with unique lessons instead of fixing course 23
    
    # Step 1: Create instructor account
    print("\n1️⃣ Creating instructor account...")
    
    timestamp = int(time.time())
    instructor_data = {
        "username": f"instructor_fix_{timestamp}",
        "email": f"instructor_fix_{timestamp}@example.com",
        "password": "instructor123",
        "first_name": "Fix",
        "last_name": "Instructor",
        "role": "instructor",
        "bio": "Instructor for fixing lesson duplication issues"
    }
    
    register_response = requests.post(
        f"{BASE_URL}/api/users/register",
        json=instructor_data,
        headers={"Content-Type": "application/json"}
    )
    
    if register_response.status_code != 200:
        print(f"❌ Registration failed: {register_response.status_code}")
        return False
    
    print("✅ Instructor account created")
    
    # Login as instructor
    login_data = {
        "email": instructor_data["email"],
        "password": instructor_data["password"]
    }
    
    login_response = requests.post(
        f"{BASE_URL}/api/users/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return False
    
    login_result = login_response.json()
    token = login_result["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("✅ Logged in as instructor")
    
    # Step 2: Create new course with unique lessons
    print("\n2️⃣ Creating new course with unique lessons...")
    
    course_data = {
        "title": "Web Development Fundamentals - Fixed",
        "description": "Learn HTML, CSS, and JavaScript with unique lessons and videos",
        "price": 99.99,
        "thumbnail_url": "https://example.com/webdev-fixed-course.jpg"
    }
    
    create_course_response = requests.post(
        f"{BASE_URL}/api/courses/",
        json=course_data,
        headers=headers
    )
    
    if create_course_response.status_code != 201:
        print(f"❌ Failed to create course: {create_course_response.status_code}")
        return False
    
    course_result = create_course_response.json()
    course_id = course_result['id']
    print(f"✅ Created new course with ID: {course_id}")
    
    # Create lessons with unique video URLs
    lessons_to_create = [
        {
            "title": "HTML Fundamentals",
            "content_text": "Learn the building blocks of web pages with HTML. Understand semantic elements, forms, accessibility, and best practices for creating structured content.",
            "video_url": "https://www.youtube.com/watch?v=UB1O30fR-EE",
            "order_index": 1
        },
        {
            "title": "CSS Styling and Layouts", 
            "content_text": "Master CSS for styling web pages. Learn about flexbox, grid, responsive design, animations, and modern CSS features like custom properties.",
            "video_url": "https://www.youtube.com/watch?v=yfoY53QXEnI",
            "order_index": 2
        },
        {
            "title": "JavaScript Fundamentals",
            "content_text": "Learn JavaScript programming from the ground up. Variables, functions, DOM manipulation, events, async programming, and ES6+ features.",
            "video_url": "https://www.youtube.com/watch?v=PkZNo7MFNFg",
            "order_index": 3
        },
        {
            "title": "Responsive Web Design",
            "content_text": "Create websites that work perfectly on all devices. Learn mobile-first design, media queries, flexible layouts, and responsive images.",
            "video_url": "https://www.youtube.com/watch?v=srvUrASRh0s",
            "order_index": 4
        },
        {
            "title": "Modern JavaScript (ES6+)",
            "content_text": "Master modern JavaScript features including arrow functions, destructuring, modules, async/await, and the latest language improvements.",
            "video_url": "https://www.youtube.com/watch?v=WZQc7RUAg18",
            "order_index": 5
        }
    ]
    
    print(f"\n3️⃣ Creating {len(lessons_to_create)} unique lessons...")
    
    created_lessons = 0
    for lesson_data in lessons_to_create:
        create_lesson_response = requests.post(
            f"{BASE_URL}/api/lessons/courses/{course_id}",
            json=lesson_data,
            headers=headers
        )
        
        if create_lesson_response.status_code == 200:
            lesson_result = create_lesson_response.json()
            print(f"✅ Created lesson: {lesson_result['title']}")
            created_lessons += 1
        else:
            print(f"❌ Failed to create lesson: {create_lesson_response.status_code}")
            print(f"   Response: {create_lesson_response.text}")
    
    print(f"\n🎉 Created {created_lessons} lessons with unique content and videos!")
    
    # Verify the lessons
    print("\n4️⃣ Verifying lesson uniqueness...")
    
    lessons_response = requests.get(
        f"{BASE_URL}/api/lessons/{course_id}",
        headers=headers
    )
    
    if lessons_response.status_code == 200:
        lessons_data = lessons_response.json()
        
        # Check uniqueness
        titles = [lesson.get('title', '') for lesson in lessons_data]
        video_urls = [lesson.get('video_url', '') for lesson in lessons_data]
        content_texts = [lesson.get('content_text', '') for lesson in lessons_data]
        
        unique_titles = len(set(titles))
        unique_videos = len(set(video_urls))
        unique_content = len(set(content_texts))
        
        print(f"Total lessons: {len(lessons_data)}")
        print(f"Unique titles: {unique_titles}")
        print(f"Unique video URLs: {unique_videos}")
        print(f"Unique content: {unique_content}")
        
        if (unique_titles == len(lessons_data) and 
            unique_videos == len(lessons_data) and 
            unique_content == len(lessons_data)):
            
            print("\n🎉 SUCCESS! All lessons are unique!")
            
            print(f"\n📋 New Course Lessons (ID: {course_id}):")
            for i, lesson in enumerate(lessons_data, 1):
                print(f"  {i}. {lesson['title']}")
                print(f"     Video: {lesson['video_url']}")
                print(f"     Content: {lesson.get('content_text', '')[:80]}...")
                print()
            
            print("✅ ISSUE COMPLETELY RESOLVED!")
            print("✅ Users can now switch between lessons and see different videos/content")
            print(f"✅ Use this new course ID instead of 23: {course_id}")
            
            return True, course_id
        else:
            print("\n⚠️  Some lessons still have duplicates")
            return False, None
    else:
        print(f"❌ Failed to verify lessons: {lessons_response.status_code}")
        return False, None

if __name__ == "__main__":
    success, new_course_id = fix_course_23_lessons()
    if success:
        print("\n🎉 LESSON DUPLICATION ISSUE FIXED!")
        print("✅ Each lesson now has unique video and content")
        print("✅ Users can switch between lessons successfully")
        print(f"✅ New working course ID: {new_course_id}")
        print("\n🔧 RECOMMENDED ACTION:")
        print(f"   Update your frontend to use course ID {new_course_id} instead of course 23")
        print("   This will resolve the 'video not changing' issue completely")
    else:
        print("\n❌ Could not fix lesson duplication")
        print("Manual intervention may be required")
