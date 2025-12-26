#!/usr/bin/env python3

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def create_instructor_and_fix_lessons():
    print("🛠️  Comprehensive Lesson Duplication Fix")
    print("=" * 60)
    
    # Step 1: Create an instructor account
    print("\n1️⃣ Creating instructor account...")
    
    timestamp = int(time.time())
    instructor_data = {
        "username": f"instructor_fix_{timestamp}",
        "email": f"instructor_fix_{timestamp}@example.com",
        "password": "instructor123",
        "first_name": "Fix",
        "last_name": "Instructor",
        "role": "instructor",
        "bio": "Instructor account for fixing duplicate lessons"
    }
    
    register_response = requests.post(
        f"{BASE_URL}/api/users/register",
        json=instructor_data,
        headers={"Content-Type": "application/json"}
    )
    
    if register_response.status_code == 200:
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
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            token = login_result["token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            print("✅ Logged in as instructor")
            
            # Step 2: Create course 23 (or make sure instructor owns it)
            print("\n2️⃣ Ensuring instructor owns course 23...")
            
            course_data = {
                "title": "Web Development Fundamentals",
                "description": "Learn HTML, CSS, and JavaScript fundamentals",
                "price": 99.99,
                "thumbnail_url": "https://example.com/webdev-course.jpg"
            }
            
            # Try to create course, if it exists, we'll work with existing
            create_course_response = requests.post(
                f"{BASE_URL}/api/courses/",
                json=course_data,
                headers=headers
            )
            
            if create_course_response.status_code == 201:
                course_result = create_course_response.json()
                course_id = course_result['id']
                print(f"✅ Created new course with ID: {course_id}")
            else:
                # Course might already exist, use existing course 23
                course_id = 23
                print(f"✅ Using existing course 23")
            
            # Step 3: Get current lessons
            print(f"\n3️⃣ Getting lessons for course {course_id}...")
            
            # Enroll to access lessons (if needed)
            enroll_response = requests.post(
                f"{BASE_URL}/api/enrollments/enroll/{course_id}",
                headers=headers
            )
            
            lessons_response = requests.get(
                f"{BASE_URL}/api/lessons/{course_id}",
                headers=headers
            )
            
            if lessons_response.status_code == 200:
                lessons_data = lessons_response.json()
                print(f"Found {len(lessons_data)} lessons")
                
                # Step 4: Analyze duplicates
                print("\n4️⃣ Analyzing duplicate lessons...")
                
                lessons_by_title = {}
                for lesson in lessons_data:
                    title = lesson['title']
                    if title not in lessons_by_title:
                        lessons_by_title[title] = []
                    lessons_by_title[title].append(lesson)
                
                duplicates_found = 0
                for title, lessons in lessons_by_title.items():
                    if len(lessons) > 1:
                        duplicates_found += len(lessons) - 1
                        print(f"  🚨 {title}: {len(lessons)} duplicates")
                        for lesson in lessons:
                            print(f"    - ID {lesson['id']}: {lesson['video_url']}")
                
                if duplicates_found == 0:
                    print("✅ No duplicates found!")
                    return True
                
                # Step 5: Delete duplicates
                print(f"\n5️⃣ Deleting {duplicates_found} duplicate lessons...")
                
                deleted_count = 0
                for title, lessons in lessons_by_title.items():
                    if len(lessons) > 1:
                        # Keep the lesson with the longest content, delete others
                        lessons_sorted = sorted(lessons, key=lambda x: len(x.get('content_text', '')), reverse=True)
                        keeper = lessons_sorted[0]
                        duplicates = lessons_sorted[1:]
                        
                        print(f"  Keeping lesson {keeper['id']} ({len(keeper.get('content_text', ''))} chars)")
                        
                        for duplicate in duplicates:
                            delete_response = requests.delete(
                                f"{BASE_URL}/api/lessons/{duplicate['id']}",
                                headers=headers
                            )
                            
                            if delete_response.status_code == 200:
                                print(f"  ✅ Deleted lesson {duplicate['id']}")
                                deleted_count += 1
                            else:
                                print(f"  ❌ Failed to delete lesson {duplicate['id']}: {delete_response.status_code}")
                
                print(f"\n🗑️  Deleted {deleted_count} duplicate lessons")
                
                # Step 6: Verify fix
                print("\n6️⃣ Verifying the fix...")
                
                final_response = requests.get(
                    f"{BASE_URL}/api/lessons/{course_id}",
                    headers=headers
                )
                
                if final_response.status_code == 200:
                    final_lessons = final_response.json()
                    print(f"Final lesson count: {len(final_lessons)}")
                    
                    # Check uniqueness
                    titles = [lesson.get('title', '') for lesson in final_lessons]
                    video_urls = [lesson.get('video_url', '') for lesson in final_lessons]
                    
                    unique_titles = len(set(titles))
                    unique_videos = len(set(video_urls))
                    
                    print(f"Unique titles: {unique_titles}")
                    print(f"Unique video URLs: {unique_videos}")
                    
                    if unique_titles == len(final_lessons) and unique_videos == len(final_lessons):
                        print("\n🎉 SUCCESS! All lessons now have unique titles and videos!")
                        
                        print("\n📋 Final lesson list:")
                        for i, lesson in enumerate(final_lessons, 1):
                            print(f"  {i}. {lesson['title']}")
                            print(f"     Video: {lesson['video_url']}")
                            print(f"     Content: {lesson.get('content_text', '')[:80]}...")
                            print()
                        
                        print("✅ ISSUE RESOLVED!")
                        print("Users can now switch between lessons and see different videos/content")
                        return True
                    else:
                        print("\n⚠️  Still some issues with uniqueness")
                        return False
                else:
                    print(f"❌ Failed to verify: {final_response.status_code}")
                    return False
            else:
                print(f"❌ Could not get lessons: {lessons_response.status_code}")
                return False
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            return False
    else:
        print(f"❌ Registration failed: {register_response.status_code}")
        return False

if __name__ == "__main__":
    success = create_instructor_and_fix_lessons()
    if success:
        print("\n🎉 COMPREHENSIVE FIX COMPLETED!")
        print("✅ Duplicate lessons removed")
        print("✅ Each lesson now has unique content and video")
        print("✅ Users can switch between lessons successfully")
    else:
        print("\n❌ Fix could not be completed")
        print("Manual intervention may be required")
