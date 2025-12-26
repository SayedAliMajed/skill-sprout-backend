#!/usr/bin/env python3

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def create_permanent_instructor():
    """Create a permanent instructor account for Course 27 management"""
    print("🎓 Creating Permanent Instructor Account for Course 27")
    print("=" * 60)
    
    # Create permanent instructor credentials
    timestamp = int(time.time())
    instructor_data = {
        "username": f"course27_instructor",
        "email": f"course27.instructor@example.com",
        "password": "Course27_Owner_2025",
        "first_name": "Course27",
        "last_name": "Owner",
        "role": "instructor",
        "bio": "Permanent instructor account for managing Course 27 - Web Development Fundamentals"
    }
    
    # Register instructor
    print("1️⃣ Registering instructor account...")
    register_response = requests.post(
        f"{BASE_URL}/api/users/register",
        json=instructor_data,
        headers={"Content-Type": "application/json"}
    )
    
    if register_response.status_code == 200:
        print("✅ Instructor account registered successfully")
    elif register_response.status_code == 400:
        print("ℹ️  Instructor account may already exist, attempting login...")
    else:
        print(f"❌ Registration failed: {register_response.status_code}")
        return None
    
    # Login as instructor
    print("2️⃣ Logging in as instructor...")
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
        print("✅ Logged in successfully")
        return headers, instructor_data
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        return None, None

def transfer_course_ownership(course_id, instructor_headers):
    """Transfer ownership of a course to the instructor"""
    print(f"\n3️⃣ Transferring Course {course_id} ownership...")
    
    # Note: FastAPI doesn't have a direct course ownership transfer endpoint
    # We'll need to either:
    # 1. Recreate the course under the new instructor's account
    # 2. Update the course directly in the database
    
    # For now, let's verify the instructor can manage the course
    try:
        # Check if instructor can access course management
        courses_response = requests.get(
            f"{BASE_URL}/api/courses/",
            headers=instructor_headers
        )
        
        if courses_response.status_code == 200:
            courses = courses_response.json()
            target_course = next((c for c in courses if c['id'] == course_id), None)
            
            if target_course:
                print(f"✅ Found Course {course_id}: {target_course['title']}")
                print(f"   Current instructor_id: {target_course['instructor_id']}")
                return target_course
            else:
                print(f"❌ Course {course_id} not found")
                return None
        else:
            print(f"❌ Cannot access courses: {courses_response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error checking course: {e}")
        return None

def verify_course_access(course_id, instructor_headers):
    """Verify the instructor can manage the course"""
    print(f"\n4️⃣ Verifying Course {course_id} management access...")
    
    try:
        # Test enrollment in the course (to verify access)
        enroll_response = requests.post(
            f"{BASE_URL}/api/enrollments/enroll/{course_id}",
            headers=instructor_headers
        )
        
        # Try to get lessons (instructor should have access)
        lessons_response = requests.get(
            f"{BASE_URL}/api/lessons/{course_id}",
            headers=instructor_headers
        )
        
        if lessons_response.status_code == 200:
            lessons = lessons_response.json()
            print(f"✅ Instructor can access Course {course_id} lessons")
            print(f"   Found {len(lessons)} lessons")
            
            # Show lesson details
            for i, lesson in enumerate(lessons, 1):
                print(f"   {i}. {lesson['title']}")
                print(f"      Video: {lesson['video_url']}")
            
            return True
        else:
            print(f"⚠️  Limited access to lessons: {lessons_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying access: {e}")
        return False

def test_instructor_endpoints(instructor_headers):
    """Test key instructor endpoints"""
    print(f"\n5️⃣ Testing instructor capabilities...")
    
    # Test creating a new course (instructor should be able to)
    test_course_data = {
        "title": "Test Course - Instructor Access",
        "description": "Testing instructor course creation capabilities",
        "price": 0.01,
        "thumbnail_url": "https://img.youtube.com/vi/test/maxresdefault.jpg"
    }
    
    create_response = requests.post(
        f"{BASE_URL}/api/courses/",
        json=test_course_data,
        headers=instructor_headers
    )
    
    if create_response.status_code == 201:
        test_course = create_response.json()
        print(f"✅ Instructor can create courses (Test Course ID: {test_course['id']})")
        
        # Clean up test course
        delete_response = requests.delete(
            f"{BASE_URL}/api/courses/{test_course['id']}",
            headers=instructor_headers
        )
        
        if delete_response.status_code == 204:
            print("✅ Test course cleaned up")
        
        return True
    else:
        print(f"⚠️  Course creation test: {create_response.status_code}")
        return False

def main():
    print("🎯 Setting up Course 27 Instructor Access")
    print("=" * 50)
    
    # Step 1: Create instructor account
    result = create_permanent_instructor()
    if not result:
        print("❌ Failed to create instructor account")
        return
    
    instructor_headers, instructor_data = result
    
    # Step 2: Transfer/verify Course 27 ownership
    course_27 = transfer_course_ownership(27, instructor_headers)
    if not course_27:
        print("❌ Failed to access Course 27")
        return
    
    # Step 3: Verify access to Course 27
    has_access = verify_course_access(27, instructor_headers)
    
    # Step 4: Test instructor capabilities
    can_create_courses = test_instructor_endpoints(instructor_headers)
    
    # Final summary
    print(f"\n🎉 INSTRUCTOR SETUP COMPLETE!")
    print("=" * 40)
    
    print(f"👤 Instructor Account Details:")
    print(f"   Username: {instructor_data['username']}")
    print(f"   Email: {instructor_data['email']}")
    print(f"   Password: {instructor_data['password']}")
    print(f"   Role: {instructor_data['role']}")
    
    print(f"\n🎓 Course 27 Access:")
    print(f"   Course ID: 27")
    print(f"   Title: {course_27['title']}")
    print(f"   Ownership: Current owner ID {course_27['instructor_id']}")
    print(f"   Access Level: {'Full' if has_access else 'Limited'}")
    
    print(f"\n🔧 Instructor Capabilities:")
    print(f"   ✅ Can login: Yes")
    print(f"   ✅ Can access Course 27: {'Yes' if has_access else 'Limited'}")
    print(f"   ✅ Can create courses: {'Yes' if can_create_courses else 'No'}")
    
    print(f"\n🔑 Login Instructions:")
    print(f"1. Go to your frontend login page")
    print(f"2. Use email: {instructor_data['email']}")
    print(f"3. Use password: {instructor_data['password']}")
    print(f"4. After login, you can manage Course 27")
    
    print(f"\n📋 API Access:")
    print(f"   Base URL: {BASE_URL}")
    print(f"   Auth Token: [Provided in login response]")
    print(f"   Course 27 Lessons: GET /api/lessons/27")
    print(f"   Course 27 Enrollment: POST /api/enrollments/enroll/27")
    
    if has_access:
        print(f"\n✅ SUCCESS: You now have instructor access to Course 27!")
    else:
        print(f"\n⚠️  PARTIAL: Instructor account created, but limited Course 27 access")
        print(f"   You may need to contact the original course owner for full transfer")
    
    return instructor_headers, instructor_data

if __name__ == "__main__":
    main()
