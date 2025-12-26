#!/usr/bin/env python3

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def check_lessons_data():
    print("🔍 Checking Lessons Data for Course 23")
    print("=" * 50)
    
    # Create a test user to get a valid token
    timestamp = int(time.time())
    register_data = {
        "username": f"test_check_{timestamp}",
        "email": f"test_check_{timestamp}@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "Check",
        "role": "student",
        "bio": "Test account for checking lessons"
    }
    
    try:
        # Register and login to get token
        register_response = requests.post(
            f"{BASE_URL}/api/users/register",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        
        if register_response.status_code == 200:
            # Login
            login_data = {
                "email": register_data["email"],
                "password": register_data["password"]
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
                
                # First, enroll in course 23
                enroll_response = requests.post(
                    f"{BASE_URL}/api/enrollments/enroll/23",
                    headers=headers
                )
                
                if enroll_response.status_code == 201 or enroll_response.status_code == 400:
                    # Now get lessons
                    lessons_response = requests.get(
                        f"{BASE_URL}/api/lessons/23",
                        headers=headers
                    )
                    
                    print(f"\n📚 Lessons API Response Status: {lessons_response.status_code}")
                    
                    if lessons_response.status_code == 200:
                        lessons_data = lessons_response.json()
                        print(f"\n📊 Found {len(lessons_data)} lessons:")
                        
                        # Check for unique video URLs
                        video_urls = []
                        content_texts = []
                        
                        for i, lesson in enumerate(lessons_data, 1):
                            print(f"\n--- Lesson {i} ---")
                            print(f"ID: {lesson.get('id')}")
                            print(f"Title: {lesson.get('title')}")
                            print(f"Content: {lesson.get('content_text', '')[:100]}...")
                            print(f"Video URL: {lesson.get('video_url', 'No video')}")
                            print(f"Order: {lesson.get('order_index')}")
                            
                            # Collect for analysis
                            video_urls.append(lesson.get('video_url', ''))
                            content_texts.append(lesson.get('content_text', ''))
                        
                        # Analyze uniqueness
                        print(f"\n🔍 Analysis:")
                        print(f"Total lessons: {len(lessons_data)}")
                        print(f"Unique video URLs: {len(set(video_urls))}")
                        print(f"Unique content texts: {len(set(content_texts))}")
                        
                        if len(set(video_urls)) == 1 and len(video_urls) > 1:
                            print(f"\n🚨 ISSUE FOUND: All lessons have the same video URL!")
                            print(f"Common video URL: {video_urls[0]}")
                            print("This explains why switching lessons doesn't change the video.")
                        elif len(set(video_urls)) == len(video_urls):
                            print(f"\n✅ GOOD: All lessons have unique video URLs")
                        else:
                            print(f"\n⚠️  PARTIAL: Some lessons share video URLs")
                        
                        if len(set(content_texts)) == 1 and len(content_texts) > 1:
                            print(f"\n🚨 ISSUE FOUND: All lessons have the same content text!")
                            print("This explains why lesson content doesn't change.")
                        elif len(set(content_texts)) == len(content_texts):
                            print(f"\n✅ GOOD: All lessons have unique content")
                        else:
                            print(f"\n⚠️  PARTIAL: Some lessons share content")
                        
                        return lessons_data
                    else:
                        print(f"❌ Failed to get lessons: {lessons_response.status_code}")
                        print(f"Response: {lessons_response.text}")
                else:
                    print(f"❌ Failed to enroll: {enroll_response.status_code}")
            else:
                print(f"❌ Login failed: {login_response.status_code}")
        else:
            print(f"❌ Registration failed: {register_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    lessons = check_lessons_data()
    if lessons:
        print(f"\n✅ Successfully retrieved {len(lessons)} lessons")
    else:
        print(f"\n❌ Failed to retrieve lessons")
