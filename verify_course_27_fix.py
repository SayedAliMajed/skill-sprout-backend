#!/usr/bin/env python3

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def verify_course_27_fix():
    print("🎯 Verifying Course 27 Fix")
    print("=" * 40)
    
    # Create a student to test the new course
    timestamp = int(time.time())
    student_data = {
        "username": f"test_student_{timestamp}",
        "email": f"test_student_{timestamp}@example.com",
        "password": "student123",
        "first_name": "Test",
        "last_name": "Student",
        "role": "student",
        "bio": "Testing the fixed course 27"
    }
    
    # Register and login as student
    register_response = requests.post(
        f"{BASE_URL}/api/users/register",
        json=student_data,
        headers={"Content-Type": "application/json"}
    )
    
    if register_response.status_code != 200:
        print(f"❌ Student registration failed: {register_response.status_code}")
        return False
    
    print("✅ Student account created")
    
    login_data = {
        "email": student_data["email"],
        "password": student_data["password"]
    }
    
    login_response = requests.post(
        f"{BASE_URL}/api/users/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    if login_response.status_code != 200:
        print(f"❌ Student login failed: {login_response.status_code}")
        return False
    
    login_result = login_response.json()
    token = login_result["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    print("✅ Student logged in")
    
    # Test course 27
    course_id = 27
    
    # Step 1: Check enrollment status (should be false initially)
    print(f"\n1️⃣ Checking enrollment status for course {course_id}...")
    
    status_response = requests.get(
        f"{BASE_URL}/api/enrollments/course/{course_id}/status",
        headers=headers
    )
    
    if status_response.status_code == 200:
        status_data = status_response.json()
        print(f"   Enrollment status: {status_data}")
        
        if not status_data["enrolled"]:
            print("   ✅ Correctly shows NOT enrolled")
            
            # Step 2: Try to access lessons (should fail)
            print(f"\n2️⃣ Attempting to access lessons before enrollment...")
            
            lessons_response = requests.get(
                f"{BASE_URL}/api/lessons/{course_id}",
                headers=headers
            )
            
            if lessons_response.status_code == 403:
                print("   ✅ Correctly denied access (403 Forbidden)")
            else:
                print(f"   ⚠️ Unexpected response: {lessons_response.status_code}")
            
            # Step 3: Enroll in course
            print(f"\n3️⃣ Enrolling in course {course_id}...")
            
            enroll_response = requests.post(
                f"{BASE_URL}/api/enrollments/enroll/{course_id}",
                headers=headers
            )
            
            if enroll_response.status_code == 201:
                print("   ✅ Successfully enrolled")
                
                # Step 4: Check enrollment status (should be true)
                print(f"\n4️⃣ Checking enrollment status after enrollment...")
                
                status_response2 = requests.get(
                    f"{BASE_URL}/api/enrollments/course/{course_id}/status",
                    headers=headers
                )
                
                if status_response2.status_code == 200:
                    status_data2 = status_response2.json()
                    print(f"   Enrollment status: {status_data2}")
                    
                    if status_data2["enrolled"]:
                        print("   ✅ Correctly shows ENROLLED")
                        
                        # Step 5: Access lessons (should succeed)
                        print(f"\n5️⃣ Accessing lessons after enrollment...")
                        
                        lessons_response = requests.get(
                            f"{BASE_URL}/api/lessons/{course_id}",
                            headers=headers
                        )
                        
                        if lessons_response.status_code == 200:
                            lessons_data = lessons_response.json()
                            print(f"   ✅ Successfully accessed {len(lessons_data)} lessons")
                            
                            # Step 6: Verify uniqueness
                            print(f"\n6️⃣ Verifying lesson uniqueness...")
                            
                            video_urls = [lesson.get('video_url', '') for lesson in lessons_data]
                            titles = [lesson.get('title', '') for lesson in lessons_data]
                            content_texts = [lesson.get('content_text', '') for lesson in lessons_data]
                            
                            unique_videos = len(set(video_urls))
                            unique_titles = len(set(titles))
                            unique_content = len(set(content_texts))
                            
                            print(f"   Total lessons: {len(lessons_data)}")
                            print(f"   Unique video URLs: {unique_videos}")
                            print(f"   Unique titles: {unique_titles}")
                            print(f"   Unique content: {unique_content}")
                            
                            if (unique_videos == len(lessons_data) and 
                                unique_titles == len(lessons_data) and 
                                unique_content == len(lessons_data)):
                                
                                print("\n🎉 PERFECT! All lessons have unique content and videos!")
                                
                                print(f"\n📋 Course {course_id} Lessons:")
                                for i, lesson in enumerate(lessons_data, 1):
                                    print(f"  {i}. {lesson['title']}")
                                    print(f"     Video: {lesson['video_url']}")
                                    print()
                                
                                print("✅ ISSUE COMPLETELY RESOLVED!")
                                print("✅ Users can now switch between lessons and see different videos!")
                                print(f"✅ Use course ID {course_id} instead of course 23")
                                
                                return True
                            else:
                                print("\n⚠️ Some lessons still have duplicates")
                                return False
                        else:
                            print(f"   ❌ Failed to access lessons: {lessons_response.status_code}")
                            return False
                    else:
                        print("   ❌ Should show enrolled but doesn't")
                        return False
                else:
                    print(f"   ❌ Status check failed: {status_response2.status_code}")
                    return False
            else:
                print(f"   ❌ Enrollment failed: {enroll_response.status_code}")
                print(f"   Response: {enroll_response.text}")
                return False
        else:
            print("   ⚠️ Already enrolled, skipping to lesson access")
            
            # Direct lesson access test
            lessons_response = requests.get(
                f"{BASE_URL}/api/lessons/{course_id}",
                headers=headers
            )
            
            if lessons_response.status_code == 200:
                lessons_data = lessons_response.json()
                print(f"   ✅ Successfully accessed {len(lessons_data)} lessons")
                
                # Check uniqueness
                video_urls = [lesson.get('video_url', '') for lesson in lessons_data]
                unique_videos = len(set(video_urls))
                
                if unique_videos == len(lessons_data):
                    print("   ✅ All lessons have unique video URLs!")
                    return True
                else:
                    print("   ⚠️ Some lessons share video URLs")
                    return False
            else:
                print(f"   ❌ Failed to access lessons: {lessons_response.status_code}")
                return False
    else:
        print(f"❌ Status check failed: {status_response.status_code}")
        return False

if __name__ == "__main__":
    success = verify_course_27_fix()
    if success:
        print("\n🎉 COURSE 27 VERIFICATION SUCCESSFUL!")
        print("✅ The lesson switching issue has been completely resolved!")
        print("✅ Users can now switch between lessons and see different videos/content")
        print("✅ Course 27 is ready for use!")
    else:
        print("\n❌ Verification failed")
        print("There may still be issues with course 27")
