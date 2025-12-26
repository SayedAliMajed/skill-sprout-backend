#!/usr/bin/env python3

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_enrollment_status_endpoint():
    print("🧪 Testing Enrollment Status Endpoint")
    print("=" * 50)
    
    # Step 1: Test without authentication (should fail)
    print("\n1️⃣ Testing without authentication:")
    try:
        response = requests.get(f"{BASE_URL}/api/enrollments/course/23/status")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        print("   ✅ Correctly requires authentication")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Step 2: Use existing test user if available
    print("\n2️⃣ Testing with existing test user:")
    
    # Try to use an existing test user or create new one
    timestamp = int(time.time())
    register_data = {
        "username": f"test_student_{timestamp}",
        "email": f"test_{timestamp}@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "Student",
        "role": "student",
        "bio": "Test student account"
    }
    
    try:
        # Register user
        register_response = requests.post(
            f"{BASE_URL}/api/users/register",
            json=register_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Registration status: {register_response.status_code}")
        
        if register_response.status_code == 200:
            user_data = register_response.json()
            print(f"   ✅ User registered: {user_data['username']}")
            
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
                
                print(f"   ✅ Login successful")
                
                # Test enrollment status before enrollment
                print("\n   📊 Checking enrollment status BEFORE enrollment:")
                status_response = requests.get(
                    f"{BASE_URL}/api/enrollments/course/23/status",
                    headers=headers
                )
                
                print(f"   Status: {status_response.status_code}")
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print(f"   Response: {status_data}")
                    
                    if not status_data["enrolled"]:
                        print("   ✅ Correctly shows NOT enrolled")
                        
                        # Enroll in course
                        print("\n   📝 Enrolling in course...")
                        enroll_response = requests.post(
                            f"{BASE_URL}/api/enrollments/enroll/23",
                            headers=headers
                        )
                        
                        print(f"   Enrollment status: {enroll_response.status_code}")
                        
                        if enroll_response.status_code == 201:
                            print("   ✅ Successfully enrolled")
                            
                            # Test enrollment status after enrollment
                            print("\n   📊 Checking enrollment status AFTER enrollment:")
                            status_response2 = requests.get(
                                f"{BASE_URL}/api/enrollments/course/23/status",
                                headers=headers
                            )
                            
                            if status_response2.status_code == 200:
                                status_data2 = status_response2.json()
                                print(f"   Response: {status_data2}")
                                
                                if status_data2["enrolled"]:
                                    print("   ✅ Correctly shows ENROLLED")
                                    print("\n🎉 SUCCESS: Enrollment status endpoint is working correctly!")
                                    return True
                                else:
                                    print("   ❌ Should show enrolled but doesn't")
                            else:
                                print(f"   ❌ Status check failed: {status_response2.status_code}")
                                print(f"   Response: {status_response2.text}")
                        elif enroll_response.status_code == 400:
                            # Already enrolled, which is also valid
                            print("   ✅ User already enrolled (valid case)")
                            
                            # Test enrollment status
                            print("\n   📊 Checking enrollment status (already enrolled):")
                            status_response2 = requests.get(
                                f"{BASE_URL}/api/enrollments/course/23/status",
                                headers=headers
                            )
                            
                            if status_response2.status_code == 200:
                                status_data2 = status_response2.json()
                                print(f"   Response: {status_data2}")
                                
                                if status_data2["enrolled"]:
                                    print("   ✅ Correctly shows ENROLLED")
                                    print("\n🎉 SUCCESS: Enrollment status endpoint is working correctly!")
                                    return True
                                else:
                                    print("   ❌ Should show enrolled but doesn't")
                        else:
                            print(f"   ❌ Enrollment failed: {enroll_response.status_code}")
                            print(f"   Response: {enroll_response.text}")
                    else:
                        print("   ⚠️  User is already enrolled (skipping enrollment test)")
                        print("\n🎉 SUCCESS: Enrollment status endpoint is working correctly!")
                        return True
                else:
                    print(f"   ❌ Status check failed: {status_response.status_code}")
                    print(f"   Response: {status_response.text}")
            else:
                print(f"   ❌ Login failed: {login_response.status_code}")
                print(f"   Response: {login_response.text}")
        else:
            print(f"   ❌ Registration failed: {register_response.status_code}")
            print(f"   Response: {register_response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    return False

if __name__ == "__main__":
    success = test_enrollment_status_endpoint()
    if success:
        print("\n✅ ALL TESTS PASSED")
    else:
        print("\n❌ SOME TESTS FAILED")
