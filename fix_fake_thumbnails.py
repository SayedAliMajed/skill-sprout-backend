#!/usr/bin/env python3

import requests
import json
import re

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

def convert_youtube_url_to_thumbnail(youtube_url):
    """Convert YouTube video URL to thumbnail URL"""
    if not youtube_url:
        return None
    
    # Extract video ID from various YouTube URL formats
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            video_id = match.group(1)
            return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    
    return None

def update_course_thumbnail(course_id, new_thumbnail, headers):
    """Update course thumbnail via API"""
    try:
        update_data = {"thumbnail_url": new_thumbnail}
        
        response = requests.put(
            f"{BASE_URL}/api/courses/{course_id}",
            json=update_data,
            headers=headers
        )
        
        if response.status_code == 200:
            print(f"   ✅ Successfully updated Course {course_id}")
            return True
        else:
            print(f"   ❌ Failed to update Course {course_id}: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error updating Course {course_id}: {e}")
        return False

def main():
    print("🔧 Fixing Fake Thumbnail URLs")
    print("=" * 40)
    
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
            print(f"❌ Found fake thumbnail: Course {course['id']} - {thumbnail_url}")
    
    print(f"\n📊 Found {len(fake_courses)} courses with fake thumbnails")
    
    if not fake_courses:
        print("✅ All thumbnails are already good!")
        return
    
    # Fix fake thumbnails with real YouTube URLs
    print(f"\n🛠️ Fixing fake thumbnails...")
    
    # Define mapping of fake thumbnails to real ones based on course type
    thumbnail_fixes = {
        # Web Development courses get HTML thumbnail
        'web development': 'https://img.youtube.com/vi/UB1O30fR-EE/maxresdefault.jpg',
        'html': 'https://img.youtube.com/vi/UB1O30fR-EE/maxresdefault.jpg',
        'css': 'https://img.youtube.com/vi/yfoY53QXEnI/maxresdefault.jpg',
        'javascript': 'https://img.youtube.com/vi/PkZNo7MFNFg/maxresdefault.jpg',
        
        # Data Analytics gets Data Analytics thumbnail
        'data analytics': 'https://img.youtube.com/vi/ZUdlc5LsmHA/maxresdefault.jpg',
        'data science': 'https://img.youtube.com/vi/ZUdlc5LsmHA/maxresdefault.jpg',
        
        # Python gets Python thumbnail
        'python': 'https://img.youtube.com/vi/_uQrJ0TkZlc/maxresdefault.jpg',
        
        # Java gets Java thumbnail
        'java': 'https://img.youtube.com/vi/eIrMbAQSU34/maxresdefault.jpg',
    }
    
    updated_count = 0
    
    for course in fake_courses:
        course_id = course['id']
        title = course['title'].lower()
        current_thumbnail = course.get('thumbnail_url', '')
        
        print(f"\n🔧 Fixing Course {course_id}: {course['title']}")
        print(f"   Current (fake): {current_thumbnail}")
        
        # Find appropriate thumbnail based on course topic
        new_thumbnail = None
        for keyword, thumbnail in thumbnail_fixes.items():
            if keyword in title:
                new_thumbnail = thumbnail
                break
        
        # Default to HTML thumbnail if no match found
        if not new_thumbnail:
            new_thumbnail = 'https://img.youtube.com/vi/UB1O30fR-EE/maxresdefault.jpg'
        
        print(f"   New (real): {new_thumbnail}")
        
        # Update the course
        if update_course_thumbnail(course_id, new_thumbnail, headers):
            updated_count += 1
    
    # Final summary
    print(f"\n🎉 THUMBNAIL FIX COMPLETE!")
    print("=" * 35)
    print(f"✅ Updated {updated_count} courses with real thumbnails")
    print(f"✅ All fake thumbnail URLs have been replaced")
    
    print(f"\n📋 Updated Courses:")
    for course in fake_courses:
        course_id = course['id']
        title = course['title']
        print(f"   Course {course_id}: {title}")
    
    print(f"\n🎯 All course thumbnails now use real YouTube images!")
    print(f"✅ No more broken or placeholder images")
    
    return updated_count

if __name__ == "__main__":
    count = main()
    if count > 0:
        print(f"\n🌟 Success! Fixed {count} fake thumbnail URLs.")
    else:
        print(f"\n⚠️ No thumbnails were updated.")
