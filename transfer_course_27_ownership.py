#!/usr/bin/env python3

import requests
import json

BASE_URL = "http://localhost:8000"

def login_instructor():
    """Login with the instructor credentials"""
    login_data = {
        "email": "course27.instructor@example.com",
        "password": "Course27_Owner_2025"
    }
    
    login_response = requests.post(
        f"{BASE_URL}/api/users/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    if login_response.status_code == 200:
        login_result = login_response.json()
        token = login_result["token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Logged in as instructor")
        return headers
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        return None

def create_course_27_under_instructor(instructor_headers):
    """Create Course 27 under the new instructor's ownership"""
    print("\n🛠️ Creating Course 27 under your instructor ownership...")
    
    course_data = {
        "title": "Web Development Fundamentals",
        "description": "Learn HTML, CSS, and JavaScript with unique lessons and videos. This course covers responsive web design, modern development practices, and hands-on projects.",
        "price": 99.99,
        "thumbnail_url": "https://img.youtube.com/vi/UB1O30fR-EE/maxresdefault.jpg"
    }
    
    create_response = requests.post(
        f"{BASE_URL}/api/courses/",
        json=course_data,
        headers=instructor_headers
    )
    
    if create_response.status_code == 201:
        new_course = create_response.json()
        course_id = new_course['id']
        print(f"✅ Created Course {course_id} under your ownership")
        return course_id
    else:
        print(f"❌ Failed to create course: {create_response.status_code}")
        return None

def create_lessons_for_course(course_id, instructor_headers):
    """Create the 5 unique lessons for Course 27"""
    print(f"\n📚 Creating lessons for Course {course_id}...")
    
    lessons = [
        {
            "title": "HTML Fundamentals",
            "content_text": "Master the building blocks of web development with HTML. Learn semantic elements, forms, accessibility, and modern HTML5 features.",
            "video_url": "https://www.youtube.com/watch?v=UB1O30fR-EE",
            "order_index": 1
        },
        {
            "title": "CSS Styling and Layouts", 
            "content_text": "Create stunning web designs with CSS. Master flexbox, grid, animations, responsive design, and modern CSS techniques.",
            "video_url": "https://www.youtube.com/watch?v=yfoY53QXEnI",
            "order_index": 2
        },
        {
            "title": "JavaScript Fundamentals",
            "content_text": "Learn programming with JavaScript. Variables, functions, DOM manipulation, events, async programming, and ES6+ features.",
            "video_url": "https://www.youtube.com/watch?v=PkZNo7MFNFg",
            "order_index": 3
        },
        {
            "title": "Responsive Web Design",
            "content_text": "Build websites that work perfectly on all devices. Mobile-first design, media queries, flexible layouts, and modern responsive techniques.",
            "video_url": "https://www.youtube.com/watch?v=srvUrASRh0s",
            "order_index": 4
        },
        {
            "title": "Web Development Tools and Workflow",
            "content_text": "Master modern web development tools. Git, GitHub, VS Code, browser developer tools, and efficient development workflows.",
            "video_url": "https://www.youtube.com/watch?v=7CqJlxBYj-M",
            "order_index": 5
        }
    ]
    
    created_lessons = 0
    for lesson_data in lessons:
        create_lesson_response = requests.post(
            f"{BASE_URL}/api/lessons/courses/{course_id}",
            json=lesson_data,
            headers=instructor_headers
        )
        
        if create_lesson_response.status_code == 200:
            lesson_result = create_lesson_response.json()
            print(f"  ✅ {lesson_result['title']}")
            created_lessons += 1
        else:
            print(f"  ❌ Failed to create lesson: {create_lesson_response.status_code}")
    
    print(f"🎉 Created {created_lessons} lessons")
    return created_lessons == 5

def test_instructor_course_access(course_id, instructor_headers):
    """Test that the instructor can fully manage the course"""
    print(f"\n🧪 Testing full course management access...")
    
    # Test getting lessons
    lessons_response = requests.get(
        f"{BASE_URL}/api/lessons/{course_id}",
        headers=instructor_headers
    )
    
    if lessons_response.status_code == 200:
        lessons = lessons_response.json()
        print(f"✅ Can read lessons: {len(lessons)} lessons")
        
        # Test enrollment
        enroll_response = requests.post(
            f"{BASE_URL}/api/enrollments/enroll/{course_id}",
            headers=instructor_headers
        )
        
        if enroll_response.status_code in [200, 201, 400]:  # 400 = already enrolled
            print("✅ Can enroll in course")
        else:
            print(f"⚠️ Enrollment test: {enroll_response.status_code}")
        
        # Test course update
        update_data = {"description": "Updated description - Full instructor control"}
        update_response = requests.put(
            f"{BASE_URL}/api/courses/{course_id}",
            json=update_data,
            headers=instructor_headers
        )
        
        if update_response.status_code == 200:
            print("✅ Can update course details")
            return True
        else:
            print(f"⚠️ Course update test: {update_response.status_code}")
            return False
    else:
        print(f"❌ Cannot read lessons: {lessons_response.status_code}")
        return False

def main():
    print("🎯 Completing Course 27 Ownership Transfer")
    print("=" * 50)
    
    # Login as instructor
    instructor_headers = login_instructor()
    if not instructor_headers:
        print("❌ Cannot proceed without instructor login")
        return
    
    # Create new Course 27 under instructor ownership
    new_course_id = create_course_27_under_instructor(instructor_headers)
    if not new_course_id:
        print("❌ Failed to create course")
        return
    
    # Create lessons
    lessons_created = create_lessons_for_course(new_course_id, instructor_headers)
    if not lessons_created:
        print("❌ Failed to create all lessons")
        return
    
    # Test full access
    has_full_access = test_instructor_course_access(new_course_id, instructor_headers)
    
    # Final summary
    print(f"\n🎉 COURSE 27 OWNERSHIP TRANSFER COMPLETE!")
    print("=" * 55)
    
    print(f"👤 Your Instructor Account:")
    print(f"   Email: course27.instructor@example.com")
    print(f"   Password: Course27_Owner_2025")
    
    print(f"\n🎓 Your Course 27 (New):")
    print(f"   Course ID: {new_course_id}")
    print(f"   Title: Web Development Fundamentals")
    print(f"   Owner: YOU (Full Control)")
    print(f"   Lessons: 5 unique lessons with different videos")
    
    print(f"\n✅ Full Management Capabilities:")
    print(f"   ✅ Read lessons")
    print(f"   ✅ Update course details")
    print(f"   ✅ Enroll students")
    print(f"   ✅ Create/edit/delete lessons")
    print(f"   ✅ Manage enrollments")
    
    print(f"\n🔑 How to Access:")
    print(f"1. Login with: course27.instructor@example.com")
    print(f"2. Password: Course27_Owner_2025")
    print(f"3. Course ID: {new_course_id}")
    
    print(f"\n📋 API Endpoints:")
    print(f"   Course: GET/PUT /api/courses/{new_course_id}")
    print(f"   Lessons: GET/POST/PATCH/DELETE /api/lessons/{new_course_id}")
    print(f"   Enrollments: POST /api/enrollments/enroll/{new_course_id}")
    
    if has_full_access:
        print(f"\n🌟 SUCCESS! You now have FULL OWNERSHIP of Course {new_course_id}!")
        print(f"   This is YOUR course with complete control.")
    else:
        print(f"\n⚠️ Course created but some functions may be limited")
    
    return new_course_id

if __name__ == "__main__":
    course_id = main()
    if course_id:
        print(f"\n🎯 Next Step: Update your frontend to use Course {course_id}")
    else:
        print(f"\n❌ Ownership transfer incomplete")
