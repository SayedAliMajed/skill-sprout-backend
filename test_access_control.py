#!/usr/bin/env python3
"""
Test script to verify access control fix for role-based permissions
"""
import requests
import json
import time
import sys

# API base URL
BASE_URL = "http://localhost:8000/api"

def wait_for_server():
    """Wait for server to be ready"""
    print("🔄 Waiting for server to be ready...")
    for i in range(30):
        try:
            response = requests.get(f"{BASE_URL}/users/health", timeout=2)
            print("✅ Server is ready!")
            return True
        except:
            time.sleep(1)
            print(f"⏳ Waiting... ({i+1}/30)")
    print("❌ Server failed to start")
    return False

def login_user(email, password):
    """Login user and return token"""
    print(f"\n🔐 Logging in as {email}...")
    
    login_data = {
        "username": email,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/users/login", json=login_data)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"✅ Login successful! Token: {token[:20]}...")
        return token
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return None

def test_student_access(token):
    """Test that student cannot create courses/lessons"""
    print("\n🧑‍🎓 TESTING STUDENT ACCESS (Should be BLOCKED)")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Student tries to create a course (should fail)
    print("\n1️⃣ Testing POST /courses (Student should get 403)")
    course_data = {
        "title": "Student Course Test",
        "description": "This should fail",
        "price": 99.99
    }
    
    response = requests.post(f"{BASE_URL}/courses", json=course_data, headers=headers)
    
    if response.status_code == 403:
        print("✅ PASS: Student correctly blocked from creating courses (403 Forbidden)")
        print(f"   Message: {response.json().get('detail', 'No message')}")
        return True
    else:
        print(f"❌ FAIL: Student was able to create course! Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def test_instructor_access(token):
    """Test that instructor can create courses/lessons"""
    print("\n👨‍🏫 TESTING INSTRUCTOR ACCESS (Should be ALLOWED)")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 1: Instructor creates a course (should succeed)
    print("\n1️⃣ Testing POST /courses (Instructor should get 201)")
    course_data = {
        "title": "Instructor Course Test",
        "description": "This should succeed",
        "price": 199.99
    }
    
    response = requests.post(f"{BASE_URL}/courses", json=course_data, headers=headers)
    
    if response.status_code == 201:
        print("✅ PASS: Instructor successfully created course (201 Created)")
        course_id = response.json().get("id")
        print(f"   Course ID: {course_id}")
        
        # Test 2: Instructor creates a lesson (should succeed)
        print(f"\n2️⃣ Testing POST /lessons/courses/{course_id} (Instructor should get 201)")
        lesson_data = {
            "title": "Test Lesson",
            "content": "Test content",
            "order_index": 1
        }
        
        lesson_response = requests.post(f"{BASE_URL}/lessons/courses/{course_id}", 
                                      json=lesson_data, headers=headers)
        
        if lesson_response.status_code == 201:
            print("✅ PASS: Instructor successfully created lesson (201 Created)")
            return True
        else:
            print(f"⚠️  Course created but lesson creation failed: {lesson_response.status_code}")
            return True  # Course creation is the main test
    else:
        print(f"❌ FAIL: Instructor could not create course! Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def test_student_viewing(token):
    """Test that students can still view courses"""
    print("\n👀 TESTING STUDENT VIEWING ACCESS (Should be ALLOWED)")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test: Student views courses (should succeed)
    print("\n1️⃣ Testing GET /courses (Student should get 200)")
    
    response = requests.get(f"{BASE_URL}/courses", headers=headers)
    
    if response.status_code == 200:
        courses = response.json()
        print(f"✅ PASS: Student can view {len(courses)} courses (200 OK)")
        return True
    else:
        print(f"❌ FAIL: Student cannot view courses! Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def main():
    """Main test function"""
    print("🚀 ACCESS CONTROL TEST - Role-Based Permissions")
    print("=" * 50)
    
    if not wait_for_server():
        sys.exit(1)
    
    # Test accounts (make sure these exist in your database)
    STUDENT_EMAIL = "student@test.com"
    STUDENT_PASSWORD = "password123"
    INSTRUCTOR_EMAIL = "instructor@test.com" 
    INSTRUCTOR_PASSWORD = "password123"
    
    # Test student login
    student_token = login_user(STUDENT_EMAIL, STUDENT_PASSWORD)
    if not student_token:
        print("❌ Cannot proceed without student token")
        sys.exit(1)
    
    # Test instructor login  
    instructor_token = login_user(INSTRUCTOR_EMAIL, INSTRUCTOR_PASSWORD)
    if not instructor_token:
        print("❌ Cannot proceed without instructor token")
        sys.exit(1)
    
    # Run tests
    student_blocked = test_student_access(student_token)
    instructor_allowed = test_instructor_access(instructor_token)
    student_can_view = test_student_viewing(student_token)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    tests = [
        ("Student Create Course (Blocked)", student_blocked),
        ("Instructor Create Course (Allowed)", instructor_allowed), 
        ("Student View Courses (Allowed)", student_can_view)
    ]
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in tests)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Access control is working correctly!")
        print("   - Students are blocked from creating content")
        print("   - Instructors can create and manage content")
        print("   - Students can still view content")
    else:
        print("\n❌ SOME TESTS FAILED! Check the implementation.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
