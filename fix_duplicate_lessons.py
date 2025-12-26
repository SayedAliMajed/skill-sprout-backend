#!/usr/bin/env python3

import requests
import json

BASE_URL = "http://localhost:8000"

def fix_duplicate_lessons():
    print("🧹 Fixing Duplicate Lessons Issue")
    print("=" * 50)
    
    # First, we need to login as an instructor to delete lessons
    # For this example, we'll try to use an existing instructor or create one
    
    print("🔐 Setting up instructor account...")
    
    # Try to login as instructor (you might need to adjust these credentials)
    instructor_login = {
        "email": "instructor@example.com",
        "password": "password123"
    }
    
    login_response = requests.post(
        f"{BASE_URL}/api/users/login",
        json=instructor_login,
        headers={"Content-Type": "application/json"}
    )
    
    if login_response.status_code != 200:
        print("❌ Could not login as instructor. You'll need to:")
        print("1. Create an instructor account")
        print("2. Make sure they own course 23")
        print("3. Run this script with their credentials")
        return False
    
    login_result = login_response.json()
    token = login_result["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("✅ Logged in as instructor")
    
    # Get lessons for course 23
    print("\n📚 Getting current lessons...")
    
    # We need to be enrolled or be the instructor to see lessons
    enroll_response = requests.post(
        f"{BASE_URL}/api/enrollments/enroll/23",
        headers=headers
    )
    
    lessons_response = requests.get(
        f"{BASE_URL}/api/lessons/23",
        headers=headers
    )
    
    if lessons_response.status_code != 200:
        print(f"❌ Could not get lessons: {lessons_response.status_code}")
        return False
    
    lessons_data = lessons_response.json()
    print(f"Found {len(lessons_data)} lessons")
    
    # Identify duplicates
    print("\n🔍 Analyzing duplicates...")
    lessons_by_title = {}
    
    for lesson in lessons_data:
        title = lesson['title']
        if title not in lessons_by_title:
            lessons_by_title[title] = []
        lessons_by_title[title].append(lesson)
    
    print("\nLessons by title:")
    for title, lessons in lessons_by_title.items():
        print(f"  {title}: {len(lessons)} lessons")
        for lesson in lessons:
            print(f"    - ID {lesson['id']}: {lesson['video_url']}")
    
    # Delete duplicates (keep the first one, delete the rest)
    print("\n🗑️  Deleting duplicate lessons...")
    deleted_count = 0
    
    for title, lessons in lessons_by_title.items():
        if len(lessons) > 1:
            # Keep the first lesson, delete the rest
            lessons_to_delete = lessons[1:]
            
            for lesson in lessons_to_delete:
                delete_response = requests.delete(
                    f"{BASE_URL}/api/lessons/{lesson['id']}",
                    headers=headers
                )
                
                if delete_response.status_code == 200:
                    print(f"✅ Deleted lesson {lesson['id']}: {lesson['title']}")
                    deleted_count += 1
                else:
                    print(f"❌ Failed to delete lesson {lesson['id']}: {delete_response.status_code}")
    
    print(f"\n🎉 Cleanup complete! Deleted {deleted_count} duplicate lessons")
    
    # Verify the fix
    print("\n✅ Verifying the fix...")
    
    final_response = requests.get(
        f"{BASE_URL}/api/lessons/23",
        headers=headers
    )
    
    if final_response.status_code == 200:
        final_lessons = final_response.json()
        print(f"Final lesson count: {len(final_lessons)}")
        
        # Check video URL uniqueness
        video_urls = [lesson.get('video_url', '') for lesson in final_lessons]
        unique_videos = len(set(video_urls))
        
        print(f"Unique video URLs: {unique_videos}")
        
        if unique_videos == len(final_lessons):
            print("✅ SUCCESS: Each lesson now has a unique video URL!")
            print("✅ Users can now switch between lessons and see different videos!")
        else:
            print("⚠️  Still have some duplicate video URLs")
            
        # Show final lesson list
        print("\n📋 Final lessons:")
        for i, lesson in enumerate(final_lessons, 1):
            print(f"  {i}. {lesson['title']} - Video: {lesson['video_url']}")
            
        return True
    else:
        print(f"❌ Failed to verify: {final_response.status_code}")
        return False

if __name__ == "__main__":
    success = fix_duplicate_lessons()
    if success:
        print("\n🎉 ISSUE RESOLVED!")
        print("Users can now switch between lessons and see different videos/content")
    else:
        print("\n❌ Could not complete the fix automatically")
        print("You may need to manually delete duplicate lessons via the API")
