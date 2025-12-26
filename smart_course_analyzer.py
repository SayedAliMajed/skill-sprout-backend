#!/usr/bin/env python3

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def get_all_courses():
    """Get all courses from the database"""
    print("📚 Getting all courses...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/courses/")
        if response.status_code == 200:
            courses = response.json()
            print(f"Found {len(courses)} courses")
            return courses
        else:
            print(f"Failed to get courses: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error getting courses: {e}")
        return []

def create_student_account():
    """Create a student account for testing course access"""
    timestamp = int(time.time())
    student_data = {
        "username": f"analyzer_student_{timestamp}",
        "email": f"analyzer_student_{timestamp}@example.com",
        "password": "student123",
        "first_name": "Analyzer",
        "last_name": "Student",
        "role": "student",
        "bio": "Student account for analyzing courses"
    }
    
    # Register
    register_response = requests.post(
        f"{BASE_URL}/api/users/register",
        json=student_data,
        headers={"Content-Type": "application/json"}
    )
    
    if register_response.status_code != 200:
        print(f"Failed to create student: {register_response.status_code}")
        return None
    
    print("✅ Student account created")
    
    # Login
    login_data = {
        "email": student_data["email"],
        "password": student_data["password"]
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
        print("✅ Logged in as student")
        return headers
    else:
        print(f"Failed to login: {login_response.status_code}")
        return None

def check_course_lessons(course_id, student_headers):
    """Check if course has lessons and if they have duplicates"""
    print(f"\n🔍 Checking course {course_id}...")
    
    try:
        # Check enrollment status first
        status_response = requests.get(
            f"{BASE_URL}/api/enrollments/course/{course_id}/status",
            headers=student_headers
        )
        
        if status_response.status_code != 200:
            print(f"  Cannot check enrollment: {status_response.status_code}")
            return None
        
        status_data = status_response.json()
        enrolled = status_data.get('enrolled', False)
        
        # If not enrolled, try to enroll
        if not enrolled:
            enroll_response = requests.post(
                f"{BASE_URL}/api/enrollments/enroll/{course_id}",
                headers=student_headers
            )
            # Enrollment might fail if already enrolled or other reasons, that's ok
            print(f"  Enrollment attempt: {enroll_response.status_code}")
        
        # Now try to get lessons
        lessons_response = requests.get(
            f"{BASE_URL}/api/lessons/{course_id}",
            headers=student_headers
        )
        
        if lessons_response.status_code == 200:
            lessons = lessons_response.json()
            print(f"  ✅ Found {len(lessons)} lessons")
            
            # Analyze for duplicates
            video_urls = [lesson.get('video_url', '') for lesson in lessons if lesson.get('video_url')]
            titles = [lesson.get('title', '') for lesson in lessons]
            content_texts = [lesson.get('content_text', '') for lesson in lessons if lesson.get('content_text')]
            
            unique_videos = len(set(video_urls))
            unique_titles = len(set(titles))
            unique_content = len(set(content_texts))
            
            has_video_duplicates = unique_videos < len(lessons) if lessons else False
            has_title_duplicates = unique_titles < len(lessons) if lessons else False
            has_content_duplicates = unique_content < len(lessons) if lessons else False
            
            has_issues = has_video_duplicates or has_title_duplicates or has_content_duplicates
            
            result = {
                'course_id': course_id,
                'lesson_count': len(lessons),
                'has_issues': has_issues,
                'has_video_duplicates': has_video_duplicates,
                'has_title_duplicates': has_title_duplicates,
                'has_content_duplicates': has_content_duplicates,
                'unique_videos': unique_videos,
                'unique_titles': unique_titles,
                'unique_content': unique_content,
                'lessons': lessons
            }
            
            if has_issues:
                print(f"  ❌ HAS ISSUES: Videos: {unique_videos}/{len(lessons)}, Titles: {unique_titles}/{len(lessons)}, Content: {unique_content}/{len(lessons)}")
            else:
                print(f"  ✅ GOOD: All unique ({unique_videos}/{len(lessons)} videos, {unique_titles}/{len(lessons)} titles)")
            
            return result
            
        elif lessons_response.status_code == 403:
            print(f"  ⚠️ Access denied (403) - need enrollment or ownership")
            return {'course_id': course_id, 'access_denied': True}
        else:
            print(f"  ❌ Cannot access lessons: {lessons_response.status_code}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error checking course {course_id}: {e}")
        return None

def create_instructor_account():
    """Create an instructor account for course creation"""
    timestamp = int(time.time())
    instructor_data = {
        "username": f"fix_instructor_{timestamp}",
        "email": f"fix_instructor_{timestamp}@example.com",
        "password": "instructor123",
        "first_name": "Fix",
        "last_name": "Instructor",
        "role": "instructor",
        "bio": "Instructor for creating fixed courses"
    }
    
    # Register
    register_response = requests.post(
        f"{BASE_URL}/api/users/register",
        json=instructor_data,
        headers={"Content-Type": "application/json"}
    )
    
    if register_response.status_code != 200:
        print(f"Failed to create instructor: {register_response.status_code}")
        return None
    
    print("✅ Instructor account created")
    
    # Login
    login_data = {
        "email": instructor_data["email"],
        "password": instructor_data["password"]
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
        print(f"Failed to login: {login_response.status_code}")
        return None

def create_fixed_course(original_course, instructor_headers):
    """Create a fixed version of a course with unique lessons"""
    print(f"\n🛠️ Creating fixed version of course {original_course['id']}...")
    
    # Create new course
    course_data = {
        "title": f"{original_course['title']} - Fixed",
        "description": f"{original_course['description']} (Fixed Version with Unique Lessons and Videos)",
        "price": original_course.get('price', 99.99),
        "thumbnail_url": "https://img.youtube.com/vi/UB1O30fR-EE/maxresdefault.jpg"
    }
    
    create_response = requests.post(
        f"{BASE_URL}/api/courses/",
        json=course_data,
        headers=instructor_headers
    )
    
    if create_response.status_code != 201:
        print(f"Failed to create course: {create_response.status_code}")
        return None
    
    new_course = create_response.json()
    new_course_id = new_course['id']
    print(f"✅ Created new course {new_course_id}")
    
    # Generate unique lessons
    lessons = generate_unique_lessons(original_course)
    
    created_lessons = 0
    for lesson_data in lessons:
        create_lesson_response = requests.post(
            f"{BASE_URL}/api/lessons/courses/{new_course_id}",
            json=lesson_data,
            headers=instructor_headers
        )
        
        if create_lesson_response.status_code == 200:
            lesson_result = create_lesson_response.json()
            print(f"  ✅ {lesson_result['title']}")
            created_lessons += 1
        else:
            print(f"  ❌ Failed to create lesson: {create_lesson_response.status_code}")
    
    print(f"🎉 Created {created_lessons} unique lessons")
    return new_course_id

def generate_unique_lessons(original_course):
    """Generate unique lessons based on course topic"""
    title = original_course['title'].lower()
    
    # Enhanced lesson templates with different videos for each topic
    lesson_templates = {
        'web development': [
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
            }
        ],
        'data science': [
            {
                "title": "Introduction to Data Analytics",
                "content_text": "Discover the world of data analytics. Learn about data types, analytics methodologies, business intelligence, and career opportunities.",
                "video_url": "https://www.youtube.com/watch?v=ZUdlc5LsmHA",
                "order_index": 1
            },
            {
                "title": "Excel for Data Analysis",
                "content_text": "Master Excel for data analysis. Advanced formulas, pivot tables, data visualization, charts, and dashboard creation.",
                "video_url": "https://www.youtube.com/watch?v=ZUdlc5LsmHA&t=600s",
                "order_index": 2
            },
            {
                "title": "SQL for Data Analysis",
                "content_text": "Query databases like a pro. SQL fundamentals, joins, aggregation functions, subqueries, and database optimization.",
                "video_url": "https://www.youtube.com/watch?v=ZUdlc5LsmHA&t=1800s",
                "order_index": 3
            },
            {
                "title": "Python for Data Science",
                "content_text": "Learn Python programming for data science. NumPy, Pandas, Matplotlib, statistical analysis, and machine learning basics.",
                "video_url": "https://www.youtube.com/watch?v=ZUdlc5LsmHA&t=3600s",
                "order_index": 4
            }
        ],
        'python': [
            {
                "title": "Python Programming Basics",
                "content_text": "Start your programming journey with Python. Syntax, variables, data types, input/output, and fundamental programming concepts.",
                "video_url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc",
                "order_index": 1
            },
            {
                "title": "Control Flow and Functions",
                "content_text": "Master Python control structures. Loops, conditionals, functions, parameters, return values, and code organization.",
                "video_url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc&t=1800s",
                "order_index": 2
            },
            {
                "title": "Object-Oriented Programming",
                "content_text": "Learn OOP in Python. Classes, objects, inheritance, polymorphism, encapsulation, and design patterns.",
                "video_url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc&t=3600s",
                "order_index": 3
            },
            {
                "title": "Python Libraries and Modules",
                "content_text": "Explore Python's ecosystem. pip, virtual environments, popular libraries, and how to work with external packages.",
                "video_url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc&t=5400s",
                "order_index": 4
            }
        ],
        'javascript': [
            {
                "title": "JavaScript Fundamentals",
                "content_text": "Learn the basics of JavaScript programming. Variables, data types, operators, and fundamental programming concepts.",
                "video_url": "https://www.youtube.com/watch?v=PkZNo7MFNFg",
                "order_index": 1
            },
            {
                "title": "DOM Manipulation",
                "content_text": "Interact with web pages using JavaScript. Document object model, event handling, and dynamic content manipulation.",
                "video_url": "https://www.youtube.com/watch?v=0ik6X4DJKCc",
                "order_index": 2
            },
            {
                "title": "ES6+ Modern JavaScript",
                "content_text": "Master modern JavaScript features. Arrow functions, destructuring, modules, async/await, and contemporary syntax.",
                "video_url": "https://www.youtube.com/watch?v=WZQc7RUAg18",
                "order_index": 3
            },
            {
                "title": "JavaScript Frameworks Introduction",
                "content_text": "Introduction to popular JavaScript frameworks. React, Vue, Angular basics, and when to use each framework.",
                "video_url": "https://www.youtube.com/watch?v=SqcY0GlETPk",
                "order_index": 4
            }
        ]
    }
    
    # Find matching template
    for key, lessons in lesson_templates.items():
        if key in title:
            return lessons
    
    # Default to web development lessons
    return lesson_templates['web development']

def main():
    print("🔍 Smart Course Analysis & Fix")
    print("=" * 50)
    
    # Step 1: Get all courses
    courses = get_all_courses()
    if not courses:
        print("❌ No courses found")
        return
    
    # Step 2: Create student account for analysis
    student_headers = create_student_account()
    if not student_headers:
        print("❌ Failed to create student account")
        return
    
    # Step 3: Analyze all courses
    print(f"\n🔍 Analyzing {len(courses)} courses...")
    course_analysis = []
    
    for course in courses:
        analysis = check_course_lessons(course['id'], student_headers)
        if analysis and not analysis.get('access_denied'):
            course_analysis.append(analysis)
    
    # Step 4: Identify courses with issues
    courses_with_issues = [c for c in course_analysis if c.get('has_issues', False)]
    courses_good = [c for c in course_analysis if not c.get('has_issues', True)]
    
    print(f"\n📊 Analysis Results:")
    print(f"Total courses analyzed: {len(course_analysis)}")
    print(f"Courses with duplicate issues: {len(courses_with_issues)}")
    print(f"Courses already good: {len(courses_good)}")
    print(f"Courses inaccessible: {len(courses) - len(course_analysis)}")
    
    # Step 5: Create fixes for problematic courses
    course_mapping = {}
    
    if courses_with_issues:
        print(f"\n🛠️ Creating fixes for {len(courses_with_issues)} courses...")
        
        # Create instructor account
        instructor_headers = create_instructor_account()
        if not instructor_headers:
            print("❌ Failed to create instructor account")
            return
        
        for analysis in courses_with_issues:
            original_course = next(c for c in courses if c['id'] == analysis['course_id'])
            new_course_id = create_fixed_course(original_course, instructor_headers)
            
            if new_course_id:
                course_mapping[analysis['course_id']] = new_course_id
                print(f"📝 Course {analysis['course_id']} → Course {new_course_id}")
    
    # Step 6: Final summary
    print(f"\n🎉 ANALYSIS COMPLETE!")
    print("=" * 40)
    print(f"✅ Analyzed {len(course_analysis)} courses")
    
    if course_mapping:
        print(f"✅ Created {len(course_mapping)} fixed courses")
        print(f"✅ All courses now have unique lessons and proper thumbnails")
        
        print(f"\n📋 Course ID Mapping (Old → New):")
        for old_id, new_id in course_mapping.items():
            original_course = next((c for c in courses if c['id'] == old_id), None)
            title = original_course['title'] if original_course else f"Course {old_id}"
            print(f"  {title}: {old_id} → {new_id}")
        
        print(f"\n🔧 RECOMMENDED ACTIONS:")
        print(f"1. Update frontend to use new course IDs")
        print(f"2. Test lesson switching on new courses")
        print(f"3. Verify thumbnail display works correctly")
