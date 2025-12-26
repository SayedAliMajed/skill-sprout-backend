#!/usr/bin/env python3
"""
Role Access Investigation Script
Investigates role-based access control for users hussain and hassan
"""

import requests
import json
import sys
from typing import Dict, Any

# API base URL
BASE_URL = "http://127.0.0.1:8000/api"

def make_request(method: str, endpoint: str, token: str = None, data: Dict = None) -> Dict[str, Any]:
    """Make API request with proper headers"""
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
            raise ValueError(f"Unsupported method: {method}")
        
        return {
            "status_code": response.status_code,
            "response": response.json() if response.content else {},
            "success": response.status_code < 400
        }
    except Exception as e:
        return {
            "status_code": 0,
            "response": {"error": str(e)},
            "success": False
        }

def login_user(username: str, password: str) -> Dict[str, Any]:
    """Login user and return token and user info"""
    login_data = {
        "email": username,  # API accepts username in email field
        "password": password
    }
    
    result = make_request("POST", "/users/login", data=login_data)
    
    if result["success"]:
        # Extract token and user info from token payload
        token = result["response"].get("token", "")
        
        # For now, let's try to decode the token to get role info
        # This is a simplified approach - in real app, you'd decode JWT
        return {
            "success": True,
            "token": token,
            "username": username
        }
    else:
        return {
            "success": False,
            "error": result["response"]
        }

def test_user_permissions(username: str, password: str) -> Dict[str, Any]:
    """Test all API endpoints for a user"""
    print(f"\n{'='*60}")
    print(f"TESTING USER: {username}")
    print(f"{'='*60}")
    
    # Login user
    login_result = login_user(username, password)
    
    if not login_result["success"]:
        print(f"❌ LOGIN FAILED for {username}: {login_result['error']}")
        return {"login_success": False}
    
    print(f"✅ LOGIN SUCCESS for {username}")
    token = login_result["token"]
    
    # Test endpoints
    endpoints_to_test = [
        # Public endpoints
        ("GET", "/courses", "Browse all courses"),
        ("GET", "/courses/1", "View course details"),
        
        # Protected endpoints that should work for any authenticated user
        ("GET", "/courses/my/courses", "Get my courses"),
        ("GET", "/enrollments/me", "Get my enrollments"),
        
        # Instructor-specific endpoints
        ("POST", "/courses", "Create course", {"title": "Test Course", "description": "Test", "price": 0}),
        ("POST", "/lessons/courses/1", "Create lesson", {"title": "Test Lesson", "content": "Test content", "order_index": 1}),
    ]
    
    results = {}
    
    for endpoint_info in endpoints_to_test:
        if len(endpoint_info) == 3:
            method, path, description = endpoint_info
            data = None
        else:
            method, path, description, data = endpoint_info
        
        print(f"\n🧪 Testing: {method} {path}")
        print(f"   Description: {description}")
        
        result = make_request(method, path, token, data)
        
        results[f"{method}_{path}"] = {
            "status_code": result["status_code"],
            "success": result["success"],
            "response": result["response"]
        }
        
        if result["success"]:
            print(f"   ✅ SUCCESS ({result['status_code']})")
        else:
            print(f"   ❌ FAILED ({result['status_code']})")
            if "detail" in result["response"]:
                print(f"   Error: {result['response']['detail']}")
            elif "error" in result["response"]:
                print(f"   Error: {result['response']['error']}")
    
    return {
        "login_success": True,
        "token": token,
        "results": results
    }

def main():
    """Main investigation function"""
    print("🔍 ROLE ACCESS INVESTIGATION")
    print("Investigating API access for users hussain and hassan")
    
    # Test both users
    users_to_test = [
        ("hussain", "123"),
        ("hassan", "123")
    ]
    
    investigation_results = {}
    
    for username, password in users_to_test:
        results = test_user_permissions(username, password)
        investigation_results[username] = results
    
    # Compare results
    print(f"\n{'='*80}")
    print("📊 COMPARISON ANALYSIS")
    print(f"{'='*80}")
    
    hussain_results = investigation_results.get("hussain", {})
    hassan_results = investigation_results.get("hassan", {})
    
    # Check if both users have same permissions
    hussain_success = {k: v["success"] for k, v in hussain_results.get("results", {}).items()}
    hassan_success = {k: v["success"] for k, v in hassan_results.get("results", {}).items()}
    
    print("\n🔍 PERMISSION COMPARISON:")
    all_endpoints = set(hussain_success.keys()) | set(hassan_success.keys())
    
    for endpoint in sorted(all_endpoints):
        hussain_access = hussain_success.get(endpoint, False)
        hassan_access = hassan_success.get(endpoint, False)
        
        status = "✅ SAME" if hussain_access == hassan_access else "❌ DIFFERENT"
        hussain_status = "✅" if hussain_access else "❌"
        hassan_status = "✅" if hassan_access else "❌"
        
        print(f"  {endpoint}:")
        print(f"    hussain: {hussain_status} | hassan: {hassan_status} | {status}")
    
    # Check course creation specifically
    print(f"\n🎯 COURSE CREATION TEST:")
    course_creation_endpoints = [k for k in all_endpoints if "POST_courses" in k]
    
    for endpoint in course_creation_endpoints:
        hussain_access = hussain_success.get(endpoint, False)
        hassan_access = hassan_success.get(endpoint, False)
        
        print(f"  {endpoint}:")
        print(f"    hussain (instructor): {'✅ ALLOWED' if hussain_access else '❌ DENIED'}")
        print(f"    hassan (student): {'✅ ALLOWED' if hassan_access else '❌ DENIED'}")
        
        if hassan_access:
            print(f"    ⚠️  SECURITY ISSUE: Student user can create courses!")
        else:
            print(f"    ✅ SECURE: Student user cannot create courses")

if __name__ == "__main__":
    main()
