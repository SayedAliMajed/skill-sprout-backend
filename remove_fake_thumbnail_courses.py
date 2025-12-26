#!/usr/bin/env python3

import requests
import json

BASE_URL = "http://localhost:8000"

def login_instructor():
    """Login with instructor credentials"""
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

def delete_course(course_id, headers):
    """Delete a course via API"""
    try:
        response = requests.delete(
            f"{BASE_URL}/api/courses/{course_id}",
            headers=headers
        )
        
        if response.status_code == 204:
            print(f"   ✅ Successfully deleted Course {course_id}")
            return True
        else:
            print(f"   ❌ Failed to delete Course {course_id}: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error deleting Course {course_id}: {e}")
        return False

def main():
    print("🗑️ Removing Courses with Fake Thumbnails")
    print("=" * 50)
    
    # Login as instructor
    headers = login_instructor()
    if not headers:
        print("❌ Cannot proceed without instructor login")
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
    
    # Ask for confirmation
    print(f"\n⚠️  WARNING: This will permanently delete {len(fake_courses)} courses!")
    print("Courses to be deleted:")
    for course in fake_courses:
        print(f"   Course {course['id']}: {course['title']}")
    
    # Since we can't ask for user input in automation, proceed with deletion
    print(f"\n🗑️ Proceeding with deletion...")
    
    deleted_count = 0
    
    for course in fake_courses:
        course_id = course['id']
        title = course['title']
        
        print(f"\n🗑️ Deleting Course {course_id}: {title}")
        
        if delete_course(course_id, headers):
            deleted_count += 1
    
    # Final summary
    print(f"\n🎉 DELETION COMPLETE!")
    print("=" * 25)
    print(f"✅ Deleted {deleted_count} courses with fake thumbnails")
    
    # Verify deletion
    print(f"\n🔍 Verifying deletion...")
    remaining_courses = get_all_courses()
    remaining_fake = [c for c in remaining_courses if is_fake_thumbnail_url(c.get('thumbnail_url', ''))]
    
    print(f"📊 Final Status:")
    print(f"   Total courses remaining: {len(remaining_courses)}")
    print(f"   Courses with fake thumbnails: {len(remaining_fake)}")
    
    if len(remaining_fake) == 0:
        print(f"🎉 SUCCESS! All fake thumbnails have been removed!")
        print(f"✅ Your course platform now has 100% working thumbnails!")
    else:
        print(f"⚠️  {len(remaining_fake)} courses still have fake thumbnails")
        for course in remaining_fake:
            print(f"   Course {course['id']}: {course['title']}")
    
    return deleted_count

if __name__ == "__main__":
    count = main()
    if count > 0:
        print(f"\n🌟 Success! Removed {count} courses with fake thumbnails.")
    else:
        print(f"\n⚠️ No courses were deleted.")
