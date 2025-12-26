#!/usr/bin/env python3
"""
Post-Fix Verification Test
Verify that the frontend fix resolved the instructor course creation issue
"""

import requests
import json
import base64

# API base URL
BASE_URL = "http://127.0.0.1:8000/api"

def decode_jwt_payload(token):
    """Decode JWT token payload to extract user info"""
    try:
        parts = token.split('.')
        payload = parts[1]
        payload += '=' * (4 - len(payload) % 4)
        decoded = base64.b64decode(payload)
        return json.loads(decoded)
    except Exception as e:
        return {"error": str(e)}

def login_user(username, password):
    """Login user and return token and user info"""
    login_data = {"email": username, "password": password}
    
    try:
        response = requests.post(f"{BASE_URL}/users/login", json=login_data)
        result = response.json()
        
        if response.status_code == 200:
            token = result.get("token")
            payload = decode_jwt_payload(token)
            return {
                "success": True,
                "token": token,
                "user_id": payload.get("sub"),
                "username": username
            }
        else:
            return {"success": False, "error": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

def test_course_creation(username, token):
    """Test course creation for a specific user"""
    print(f"\n🧪 Testing course creation for {username}...")
    
    course_data = {
        "title": f"Test Course by {username.title()}",
        "description": f"Testing course creation after frontend fix - {username}",
        "price": 0
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/courses", json=course_data, headers=headers)
        
        if response.status_code == 201:
            course = response.json()
            print(f"  ✅ SUCCESS: Course created with ID {course.get('id')}")
            print(f"     Title: {course.get('title')}")
            print(f"     Instructor ID: {course.get('instructor_id')}")
            return {"success": True, "course_id": course.get('id')}
        else:
            error_data = response.json() if response.content else {}
            print(f"  ❌ FAILED ({response.status_code}): {error_data.get('detail', 'Unknown error')}")
            return {"success": False, "status_code": response.status_code, "error": error_data.get('detail')}
            
    except Exception as e:
        print(f"  ❌ ERROR: {str(e)}")
        return {"success": False, "error": str(e)}

def main():
    """Main verification function"""
    print("🔍 POST-FIX VERIFICATION TEST")
    print("=" * 60)
    print("Testing if frontend fix resolved instructor course creation issue")
    
    # Test both users
    users = [
        {"username": "hussain", "password": "123", "expected_role": "instructor"},
        {"username": "hassan", "password": "123", "expected_role": "student"}
    ]
    
    results = {}
    
    for user in users:
        print(f"\n{'='*50}")
        print(f"Testing user: {user['username']} ({user['expected_role']})")
        print(f"{'='*50}")
        
        # Login
        print(f"🔐 Logging in {user['username']}...")
        login_result = login_user(user["username"], user["password"])
        
        if not login_result["success"]:
            print(f"❌ Login failed: {login_result['error']}")
            continue
        
        print(f"✅ Login successful")
        print(f"   User ID: {login_result['user_id']}")
        
        # Test course creation
        course_result = test_course_creation(user["username"], login_result["token"])
        results[user["username"]] = {
            "login": login_result,
            "course_creation": course_result
        }
    
    # Final analysis
    print(f"\n{'='*80}")
    print("📊 POST-FIX VERIFICATION RESULTS")
    print(f"{'='*80}")
    
    hussain_result = results.get("hussain", {})
    hassan_result = results.get("hassan", {})
    
    print(f"\n🎯 COURSE CREATION TEST RESULTS:")
    
    # Check hussain (instructor)
    hussain_course_success = hussain_result.get("course_creation", {}).get("success", False)
    if hussain_course_success:
        print(f"  ✅ hussain (instructor): CAN create courses - FIXED!")
    else:
        print(f"  ❌ hussain (instructor): CANNOT create courses - STILL BROKEN")
    
    # Check hassan (student) 
    hassan_course_success = hassan_result.get("course_creation", {}).get("success", False)
    if hassan_course_success:
        print(f"  🚨 hassan (student): CAN create courses - SECURITY ISSUE!")
    else:
        print(f"  ✅ hassan (student): CANNOT create courses - SECURE")
    
    print(f"\n🔍 DETAILED ANALYSIS:")
    
    # Check if the fix worked
    if hussain_course_success and not hassan_course_success:
        print(f"  ✅ SUCCESS: Frontend fix worked correctly!")
        print(f"     - Instructor can create courses")
        print(f"     - Student is properly restricted")
        print(f"     - Role-based access control is working")
    elif not hussain_course_success:
        print(f"  ❌ ISSUE: Instructor still cannot create courses")
        print(f"     - Frontend fix may not be complete")
        print(f"     - Backend role validation may still be broken")
    elif hassan_course_success:
        print(f"  🚨 SECURITY ISSUE: Student can create courses")
        print(f"     - This should never be allowed")
    else:
        print(f"  ⚠️  NEITHER user can create courses")
        print(f"     - This might indicate a broader system issue")
    
    print(f"\n{'='*80}")
    print("Verification completed!")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
