#!/usr/bin/env python3

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def create_test_student():
    """Create a test student account"""
    timestamp = int(time.time())
    student_data = {
        "username": f"test_student_{timestamp}",
        "email": f"test_student_{timestamp}@example.com",
        "password": "student123",
        "first_name": "Test",
        "last_name": "Student",
        "role": "student",
        "bio": "Test student for course analysis"
    }
    
    # Register
    register_response = requests.post(
        f"{BASE_URL}/api/users/register",
        json=student_data,
        headers={"Content-Type": "application/json"}
    )
    
    if register_response.status_code == 200:
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
            return headers
    
    return None

def analyze_single_course(course_id, headers):
    """Analyze a single course for duplicates"""
    try:
        # Check enrollment status
        status_response = requests.get(
            f"{BASE_URL}/api/enrollments/course/{course_id}/status",
            headers=headers
        )
        
        if status_response.status_code != 200:
            return {'course_id': course_id, 'error': 'Cannot check enrollment'}
        
        # Try to enroll
        enroll_response = requests.post(
            f"{BASE_URL}/api/enrollments/enroll/{course_id}",
            headers=headers
        )
        
        # Get lessons
        lessons_response = requests.get(
            f"{BASE_URL}/api/lessons/{course_id}",
            headers=headers
        )
        
        if lessons_response.status_code == 200:
            lessons = lessons_response.json()
            
            # Analyze duplicates
            video_urls = [lesson.get('video_url', '') for lesson in lessons if lesson.get('video_url')]
            titles = [lesson.get('title', '') for lesson in lessons]
            
            unique_videos = len(set(video_urls))
            unique_titles = len(set(titles))
            
            has_duplicates = unique_videos < len(lessons) if lessons else False
            
            return {
                'course_id': course_id,
                'lesson_count': len(lessons),
                'unique_videos': unique_videos,
                'unique_titles': unique_titles,
                'has_duplicates': has_duplicates,
                'status': 'success'
            }
        else:
            return {'course_id': course_id, 'error': f'Cannot access lessons: {lessons_response.status_code}'}
            
    except Exception as e:
        return {'course_id': course_id, 'error': str(e)}

def main():
    print("🔍 Simple Course Analysis")
    print("=" * 40)
    
    # Get all courses
    response = requests.get(f"{BASE_URL}/api/courses/")
    if response.status_code != 200:
        print(f"❌ Cannot get courses: {response.status_code}")
        return
    
    courses = response.json()
    print(f"📚 Found {len(courses)} courses")
    
    # Create test student
    headers = create_test_student()
    if not headers:
        print("❌ Cannot create test student")
        return
    
    print("✅ Test student created")
    
    # Analyze each course
    print("\n🔍 Analyzing courses...")
    results = []
    
    for course in courses:
        print(f"\nChecking Course {course['id']}: {course['title']}")
        result = analyze_single_course(course['id'], headers)
        results.append(result)
        
        if result.get('status') == 'success':
            if result['has_duplicates']:
                print(f"  ❌ HAS DUPLICATES: {result['unique_videos']}/{result['lesson_count']} unique videos")
            else:
                print(f"  ✅ GOOD: {result['unique_videos']}/{result['lesson_count']} unique videos")
        else:
            print(f"  ⚠️ {result.get('error', 'Unknown error')}")
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print("=" * 30)
    
    courses_with_issues = [r for r in results if r.get('has_duplicates', False)]
    courses_good = [r for r in results if r.get('status') == 'success' and not r.get('has_duplicates', True)]
    courses_with_errors = [r for r in results if r.get('error')]
    
    print(f"Total courses: {len(results)}")
    print(f"Courses with duplicates: {len(courses_with_issues)}")
    print(f"Courses already good: {len(courses_good)}")
    print(f"Courses with errors: {len(courses_with_errors)}")
    
    if courses_with_issues:
        print(f"\n❌ COURSES NEEDING FIXES:")
        for result in courses_with_issues:
            course = next(c for c in courses if c['id'] == result['course_id'])
            print(f"  Course {result['course_id']}: {course['title']}")
            print(f"    - {result['unique_videos']}/{result['lesson_count']} unique videos")
    
    if courses_good:
        print(f"\n✅ COURSES ALREADY GOOD:")
        for result in courses_good:
            course = next(c for c in courses if c['id'] == result['course_id'])
            print(f"  Course {result['course_id']}: {course['title']}")
    
    if courses_with_errors:
        print(f"\n⚠️ COURSES WITH ERRORS:")
        for result in courses_with_errors:
            course = next((c for c in courses if c['id'] == result['course_id']), {'title': 'Unknown'})
            print(f"  Course {result['course_id']}: {course['title']} - {result['error']}")
    
    # Final recommendation
    print(f"\n🎯 RECOMMENDATION:")
    if courses_with_issues:
        print(f"Create fixed versions of {len(courses_with_issues)} courses")
        print(f"Course 27 is already fixed and working correctly")
        print(f"Update frontend to use Course 27 and any new fixed courses")
    else:
        print(f"✅ All analyzed courses are already good!")
        print(f"Only Course 27 needs to be used (it's the fixed version)")

if __name__ == "__main__":
    main()
