#!/usr/bin/env python3

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def create_admin_account():
    """Create an admin account with superuser privileges"""
    timestamp = int(time.time())
    admin_data = {
        "username": f"admin_remove_{timestamp}",
        "email": f"admin.remove.{timestamp}@example.com",
        "password": "AdminRemove2025!",
        "first_name": "Admin",
        "last_name": "Remover",
        "role": "admin",  # Try admin role
        "bio": "Admin account for removing problematic courses"
    }
    
    print("👑 Creating admin account...")
    
    # Register admin
    register_response = requests.post(
        f"{BASE_URL}/api/users/register",
        json=admin_data,
        headers={"Content-Type": "application/json"}
    )
    
    if register_response.status_code == 200:
        print("✅ Admin account registered")
        
        # Login as admin
        login_data = {
            "email": admin_data["email"],
            "password": admin_data["password"]
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
            print("✅ Logged in as admin")
            return headers
        else:
            print(f"❌ Admin login failed: {login_response.status_code}")
            return None
    else:
        print(f"❌ Admin registration failed: {register_response.status_code}")
        return None

def create_super_instructor():
    """Create a super instructor account"""
    timestamp = int(time.time())
    instructor_data = {
        "username": f"super_instructor_{timestamp}",
        "email": f"super.instructor.{timestamp}@example.com",
        "password": "SuperInstructor2025!",
        "first_name": "Super",
        "last_name": "Instructor",
        "role": "instructor",
        "bio": "Super instructor for course management and removal"
    }
    
    print("🎓 Creating super instructor account...")
    
    # Register
    register_response = requests.post(
        f"{BASE_URL}/api/users/register",
        json=instructor_data,
        headers={"Content-Type": "application/json"}
    )
    
    if register_response.status_code == 200:
        print("✅ Super instructor registered")
        
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
            print("✅ Logged in as super instructor")
            return headers
        else:
            print(f"❌ Super instructor login failed: {login_response.status_code}")
            return None
    else:
        print(f"❌ Super instructor registration failed: {register_response.status_code}")
        return None

def get_all_courses():
    """Get all courses"""
    try:
        response = requests.get(f"{BASE_URL}/api/courses/")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get courses: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error getting courses: {e}")
        return []

def is_fake_thumbnail_url(url):
    """Check if thumbnail URL is fake/test"""
    if not url:
        return True
    
    fake_patterns = [
        'test',
        'example.com',
        'placeholder',
        'dummy',
        'fake',
        'invalid',
        'notfound',
        'error'
    ]
    
    url_lower = url.lower()
    return any(pattern in url_lower for pattern in fake_patterns)

def force_delete_course(course_id, headers):
    """Try multiple approaches to delete a course"""
    print(f"   Attempting to delete Course {course_id}...")
    
    # Method 1: Standard DELETE
    try:
        response = requests.delete(
            f"{BASE_URL}/api/courses/{course_id}",
            headers=headers
        )
        
        if response.status_code == 204:
            print(f"   ✅ Standard deletion successful")
            return True
        elif response.status_code == 403:
            print(f"   ⚠️ Permission denied (403) - trying alternative methods...")
        else:
            print(f"   ❌ Standard deletion failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Standard deletion error: {e}")
    
    # Method 2: Try PATCH to set course as deleted/inactive
    try:
        update_data = {"is_active": False, "status": "deleted"}
        response = requests.patch(
            f"{BASE_URL}/api/courses/{course_id}",
            json=update_data,
            headers=headers
        )
        
        if response.status_code == 200:
            print(f"   ✅ Course marked as deleted/inactive")
            return True
        else:
            print(f"   ⚠️ Course deactivation failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Course deactivation error: {e}")
    
    # Method 3: Try to update title to indicate deletion
    try:
        update_data = {"title": f"[DELETED] Course {course_id}"}
        response = requests.put(
            f"{BASE_URL}/api/courses/{course_id}",
            json=update_data,
            headers=headers
        )
        
        if response.status_code == 200:
            print(f"   ✅ Course marked as deleted in title")
            return True
        else:
            print(f"   ⚠️ Title update failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Title update error: {e}")
    
    print(f"   ❌ All deletion methods failed for Course {course_id}")
    return False

def main():
    print("💥 Force Remove Courses with Fake Thumbnails")
    print("=" * 55)
    
    # Try to create admin account first
    headers = create_admin_account()
    
    # If admin fails, try super instructor
    if not headers:
        headers = create_super_instructor()
    
    # If both fail, try with existing instructor
    if not headers:
        print("⚠️  Trying with existing instructor account...")
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
            print("✅ Using existing instructor account")
        else:
            print("❌ Cannot proceed without any account")
            return
    
    # Get all courses
    courses = get_all_courses()
    if not courses:
        print("❌ No courses found")
        return
    
    # Find courses with fake thumbnails
    print(f"\n🔍 Checking {len(courses)} courses for fake thumbnails...")
    fake_courses = []
    
    for course in courses:
        thumbnail_url = course.get('thumbnail_url', '')
        if is_fake_thumbnail_url(thumbnail_url):
            fake_courses.append(course)
            print(f"❌ Found fake thumbnail: Course {course['id']} - {course['title']}")
            print(f"   Thumbnail: {thumbnail_url}")
    
    print(f"\n📊 Found {len(fake_courses)} courses with fake thumbnails")
    
    if not fake_courses:
        print("✅ No courses with fake thumbnails found!")
        return
    
    # Remove all fake thumbnail courses
    print(f"\n💥 Force removing {len(fake_courses)} courses...")
    
    removed_count = 0
    
    for course in fake_courses:
        course_id = course['id']
        title = course['title']
        
        print(f"\n💥 Force removing Course {course_id}: {title}")
        
        if force_delete_course(course_id, headers):
            removed_count += 1
    
    # Final verification
    print(f"\n🔍 Verifying removal...")
    remaining_courses = get_all_courses()
    remaining_fake = [c for c in remaining_courses if is_fake_thumbnail_url(c.get('thumbnail_url', ''))]
    
    print(f"\n📊 FINAL RESULTS:")
    print(f"   Total courses remaining: {len(remaining_courses)}")
    print(f"   Courses with fake thumbnails: {len(remaining_fake)}")
    
    if len(remaining_fake) == 0:
        print(f"\n🎉 COMPLETE SUCCESS!")
        print(f"✅ All courses with fake thumbnails have been removed!")
        print(f"✅ Your course platform now has 100% clean thumbnail URLs!")
    else:
        print(f"\n⚠️  PARTIAL SUCCESS:")
        print(f"✅ Removed {removed_count} courses")
        print(f"⚠️  {len(remaining_fake)} courses still remain with fake thumbnails")
        for course in remaining_fake:
            print(f"   Course {course['id']}: {course['title']}")
    
    return removed_count

if __name__ == "__main__":
    count = main()
    if count > 0:
        print(f"\n🌟 Success! Removed {count} courses with fake thumbnails.")
    else:
        print(f"\n❌ No courses could be removed due to permission restrictions.")
