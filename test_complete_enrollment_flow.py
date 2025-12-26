#!/usr/bin/env python3

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_complete_enrollment_flow():
    print("🧪 Testing Complete Enrollment to Lesson Access Flow")
    print("=" * 60)
    
    # Step 1: Create test user
    timestamp = int(time.time())
    register_data = {
        "username": f"test_student_{timestamp}",
        "email": f"test_{timestamp}@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "Student",
        "role": "student",
        "bio": "Test student for enrollment flow"
    }
    
    try:
        # Register user
        register_response = requests.post(
            f"{BASE_URL}/api/users/register",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        
        if register_response.status_code != 200:
            print(f"❌ Registration failed: {register_response.status_code}")
            return False
        
        user_data = register_response.json()
        print(f"✅ User registered: {user_data['username']}")
        
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
        
        if login_response.status_code != 200:
            print(f"❌ Login failed: {login_response.status_code}")
            return False
        
        login_result = login_response.json()
        token = login_result["token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        print(f"✅ Login successful")
        
        # Step 2: Check enrollment status (should be false)
        print("\n📊 Step 1: Checking enrollment status BEFORE enrollment:")
        status_response = requests.get(
            f"{BASE_URL}/api/enrollments/course/23/status",
            headers=headers
        )
        
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"   Status: {status_data}")
            
            if not status_data["enrolled"]:
                print("   ✅ Correctly shows NOT enrolled")
                
                # Step 3: Try to access lessons (should fail)
                print("\n📚 Step 2: Attempting to access lessons BEFORE enrollment:")
                lessons_response = requests.get(
                    f"{BASE_URL}/api/lessons/23",
                    headers=headers
                )
                
                print(f"   Lessons response status: {lessons_response.status_code}")
                if lessons_response.status_code == 403:
                    print("   ✅ Correctly denied access (403 Forbidden)")
                    print("   Response: 'Enroll in course first'")
                else:
                    print(f"   ❌ Unexpected response: {lessons_response.status_code}")
                    print(f"   Response: {lessons_response.text}")
                
                # Step 4: Enroll in course
                print("\n📝 Step 3: Enrolling in course...")
                enroll_response = requests.post(
                    f"{BASE_URL}/api/enrollments/enroll/23",
                    headers=headers
                )
                
                if enroll_response.status_code == 201:
                    print("   ✅ Successfully enrolled")
                    
                    # Step 5: Verify enrollment status (should be true)
                    print("\n📊 Step 4: Checking enrollment status AFTER enrollment:")
                    status_response2 = requests.get(
                        f"{BASE_URL}/api/enrollments/course/23/status",
                        headers=headers
                    )
                    
                    if status_response2.status_code == 200:
                        status_data2 = status_response2.json()
                        print(f"   Status: {status_data2}")
                        
                        if status_data2["enrolled"]:
                            print("   ✅ Correctly shows ENROLLED")
                            
                            # Step 6: Access lessons (should succeed)
                            print("\n📚 Step 5: Accessing lessons AFTER enrollment:")
                            lessons_response2 = requests.get(
                                f"{BASE_URL}/api/lessons/23",
                                headers=headers
                            )
                            
                            print(f"   Lessons response status: {lessons_response2.status_code}")
                            if lessons_response2.status_code == 200:
                                lessons_data = lessons_response2.json()
                                print(f"   ✅ Successfully accessed {len(lessons_data)} lessons")
                                print("   🎉 COMPLETE SUCCESS: Enrollment-to-lesson flow working!")
                                return True
                            else:
                                print(f"   ❌ Still cannot access lessons: {lessons_response2.status_code}")
                                print(f"   Response: {lessons_response2.text}")
                        else:
                            print("   ❌ Should show enrolled but doesn't")
                    else:
                        print(f"   ❌ Status check failed: {status_response2.status_code}")
                else:
                    print(f"   ❌ Enrollment failed: {enroll_response.status_code}")
                    print(f"   Response: {enroll_response.text}")
            else:
                print("   ⚠️ User already enrolled, skipping to lesson access test")
                
                # Test lesson access directly
                print("\n📚 Testing lesson access with existing enrollment:")
                lessons_response = requests.get(
                    f"{BASE_URL}/api/lessons/23",
                    headers=headers
                )
                
                print(f"   Lessons response status: {lessons_response.status_code}")
                if lessons_response.status_code == 200:
                    lessons_data = lessons_response.json()
                    print(f"   ✅ Successfully accessed {len(lessons_data)} lessons")
                    print("   🎉 SUCCESS: User can access lessons when enrolled!")
                    return True
                else:
                    print(f"   ❌ Cannot access lessons: {lessons_response.status_code}")
                    print(f"   Response: {lessons_response.text}")
        else:
            print(f"   ❌ Status check failed: {status_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return False

if __name__ == "__main__":
    success = test_complete_enrollment_flow()
    if success:
        print("\n🎉 COMPLETE ENROLLMENT FLOW TEST PASSED!")
        print("✅ Users can successfully enroll and access lessons")
    else:
        print("\n❌ ENROLLMENT FLOW TEST FAILED!")
        print("❌ Issue with enrollment-to-lesson access")
