#!/usr/bin/env python3
"""
Comprehensive Role Access Investigation
Tests all API endpoints systematically for both users
"""

import requests
import json
import base64
import sys

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

def test_endpoint(method, endpoint, token=None, data=None, description=""):
    """Test a single API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == "PUT":
            response = requests.put(url, headers=headers, json=data)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        elif method.upper() == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        else:
            return {"success": False, "error": f"Unsupported method: {method}"}
        
        response_data = response.json() if response.content else {}
        
        return {
            "success": response.status_code < 400,
            "status_code": response.status_code,
            "response": response_data
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    """Main investigation function"""
    print("🔍 COMPREHENSIVE ROLE ACCESS INVESTIGATION")
    print("=" * 60)
    
    # Users to test
    users = [
        {"username": "hussain", "password": "123", "expected_role": "instructor"},
        {"username": "hassan", "password": "123", "expected_role": "student"}
    ]
    
    # Login all users
    user_sessions = {}
    for user in users:
        print(f"\n🔐 Logging in {user['username']}...")
        login_result = login_user(user["username"], user["password"])
        
        if login_result["success"]:
            print(f"✅ Login successful for {user['username']}")
            user_sessions[user["username"]] = {
                **login_result,
                "expected_role": user["expected_role"]
            }
        else:
            print(f"❌ Login failed for {user['username']}: {login_result['error']}")
            continue
    
    if not user_sessions:
        print("❌ No users could login. Investigation stopped.")
        return
    
    # Define test endpoints
    endpoints = [
        # Public endpoints
        {"method": "GET", "endpoint": "/courses", "description": "Browse all courses"},
        {"method": "GET", "endpoint": "/courses/1", "description": "View course details"},
        
        # Protected endpoints
        {"method": "GET", "endpoint": "/courses/my/courses", "description": "Get my courses"},
        {"method": "GET", "endpoint": "/enrollments/me", "description": "Get my enrollments"},
        
        # Course management (instructor-only)
        {"method": "POST", "endpoint": "/courses", "data": {
            "title": "Test Course",
            "description": "Test Description", 
            "price": 0
        }, "description": "Create course"},
        
        # Enrollment (student-only)
        {"method": "POST", "endpoint": "/enrollments/enroll/1", "data": {}, "description": "Enroll in course"},
    ]
    
    # Test all endpoints for all users
    results = {}
    for username, session in user_sessions.items():
        print(f"\n🧪 Testing endpoints for {username}...")
        results[username] = {}
        
        for endpoint_info in endpoints:
            method = endpoint_info["method"]
            endpoint = endpoint_info["endpoint"]
            data = endpoint_info.get("data")
            description = endpoint_info["description"]
            
            print(f"  Testing: {method} {endpoint} - {description}")
            
            result = test_endpoint(
                method, 
                endpoint, 
                session["token"], 
                data, 
                description
            )
            
            results[username][f"{method}_{endpoint}"] = result
            
            if result["success"]:
                print(f"    ✅ SUCCESS ({result['status_code']})")
            else:
                if "error" in result:
                    print(f"    ❌ ERROR: {result['error']}")
                else:
                    print(f"    ❌ FAILED ({result['status_code']}) - {result.get('response', {}).get('detail', 'Unknown error')}")
    
    # Generate comparison report
    print(f"\n{'='*80}")
    print("📊 FINAL INVESTIGATION REPORT")
    print(f"{'='*80}")
    
    # Compare permissions
    print("\n🔍 PERMISSION COMPARISON:")
    all_endpoints = set()
    for username_results in results.values():
        all_endpoints.update(username_results.keys())
    
    security_issues = []
    
    for endpoint in sorted(all_endpoints):
        print(f"\n  📋 {endpoint}:")
        
        user_results = {}
        for username, username_results in results.items():
            user_results[username] = username_results.get(endpoint, {})
        
        hussain_success = user_results.get("hussain", {}).get("success", False)
        hassan_success = user_results.get("hassan", {}).get("success", False)
        
        hussain_status = "✅" if hussain_success else "❌"
        hassan_status = "✅" if hassan_success else "❌"
        
        print(f"    hussain: {hussain_status}")
        print(f"    hassan:  {hassan_status}")
        
        # Check for security issues
        if "POST_courses" in endpoint:
            if hussain_success and hassan_success:
                security_issues.append(f"❌ CRITICAL: Both users can create courses! (endpoint: {endpoint})")
            elif hassan_success and not hussain_success:
                security_issues.append(f"❌ CRITICAL: Student can create courses but instructor cannot! (endpoint: {endpoint})")
            elif hussain_success and not hassan_success:
                print(f"    ✅ SECURE: Only instructor can create courses")
            else:
                print(f"    ⚠️  Neither user can create courses")
        
        if "POST_enrollments" in endpoint:
            if hassan_success and not hussain_success:
                print(f"    ✅ SECURE: Only student can enroll in courses")
            elif hussain_success and not hassan_success:
                security_issues.append(f"❌ CRITICAL: Instructor can enroll but student cannot! (endpoint: {endpoint})")
            elif hussain_success and hassan_success:
                security_issues.append(f"⚠️  WARNING: Both users can enroll in courses (endpoint: {endpoint})")
    
    # Summary
    print(f"\n{'='*80}")
    print("🎯 INVESTIGATION SUMMARY")
    print(f"{'='*80}")
    
    print(f"\n📝 USER INFORMATION:")
    for username, session in user_sessions.items():
        print(f"  {username}:")
        print(f"    User ID: {session.get('user_id', 'Unknown')}")
        print(f"    Expected Role: {session['expected_role']}")
        print(f"    Token: {session.get('token', 'No token')[:50]}...")
    
    if security_issues:
        print(f"\n🚨 SECURITY ISSUES FOUND:")
        for issue in security_issues:
            print(f"  {issue}")
    else:
        print(f"\n✅ NO CRITICAL SECURITY ISSUES FOUND")
    
    # Course creation specifically
    print(f"\n🎯 COURSE CREATION TEST:")
    course_creation_results = [
        (username, results.get(username, {}).get("POST_courses", {}))
        for username in ["hussain", "hassan"]
    ]
    
    for username, result in course_creation_results:
        expected_role = user_sessions[username]["expected_role"]
        can_create = result.get("success", False)
        
        if expected_role == "instructor" and can_create:
            print(f"  ✅ {username} (instructor): CAN create courses")
        elif expected_role == "instructor" and not can_create:
            print(f"  ❌ {username} (instructor): CANNOT create courses")
        elif expected_role == "student" and can_create:
            print(f"  🚨 {username} (student): CAN create courses - SECURITY ISSUE!")
        elif expected_role == "student" and not can_create:
            print(f"  ✅ {username} (student): CANNOT create courses")
    
    print(f"\n{'='*80}")
    print("Investigation completed!")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
