#!/usr/bin/env python3
"""
Clean API Testing Suite for SkillSprout Backend
This script tests all endpoints systematically with proper authentication flow
"""

import requests
import json
import time
import sys
from typing import Dict, Any, Optional

class SkillSproutAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.test_results = []
        self.course_id = None
        self.lesson_id = None
        self.enrollment_id = None
        
    def log_test(self, test_name: str, status: str, response: Any, expected_status: int = None):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "status_code": getattr(response, 'status_code', 'N/A') if response else 'N/A',
            "response": response.text if response else 'No response',
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        
        status_indicator = "✅ PASS" if status == "PASS" else "❌ FAIL"
        print(f"{status_indicator} {test_name}")
        if expected_status:
            actual_status = getattr(response, 'status_code', 'N/A')
            if actual_status == expected_status:
                print(f"   Status: {actual_status} (Expected: {expected_status})")
            else:
                print(f"   Status: {actual_status} (Expected: {expected_status}) ❌")
        print()
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, auth: bool = False, expected_status: int = None) -> Optional[requests.Response]:
        """Make HTTP request with proper headers"""
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if auth and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=headers)
            elif method.upper() == "PATCH":
                response = requests.patch(url, json=data, headers=headers)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
    
    def test_home_endpoint(self):
        """Test home endpoint"""
        response = self.make_request("GET", "/")
        if response and response.status_code == 200:
            try:
                data = response.json()
                if "message" in data and "SkillSprout API" in data["message"]:
                    self.log_test("Home Endpoint", "PASS", response, 200)
                    return True
            except:
                pass
        self.log_test("Home Endpoint", "FAIL", response, 200)
        return False
    
    def test_user_registration(self):
        """Test user registration"""
        user_data = {
            "username": "testuser123",
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User",
            "role": "student",
            "bio": "Test user bio"
        }
        
        response = self.make_request("POST", "/api/users/register", user_data)
        if response and response.status_code == 200:
            try:
                data = response.json()
                if "id" in data and data["username"] == "testuser123":
                    self.user_id = data["id"]
                    self.log_test("User Registration - Valid", "PASS", response, 200)
                    return True
            except:
                pass
        self.log_test("User Registration - Valid", "FAIL", response, 200)
        return False
    
    def test_user_login(self):
        """Test user login"""
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        response = self.make_request("POST", "/api/users/login", login_data)
        if response and response.status_code == 200:
            try:
                data = response.json()
                if "token" in data:
                    self.token = data["token"]
                    self.log_test("User Login - Valid", "PASS", response, 200)
                    return True
            except:
                pass
        self.log_test("User Login - Valid", "FAIL", response, 200)
        return False
    
    def test_public_course_endpoints(self):
        """Test public course endpoints"""
        response = self.make_request("GET", "/api/courses/")
        if response and response.status_code == 200:
            self.log_test("Course Listing - Public", "PASS", response, 200)
        else:
            self.log_test("Course Listing - Public", "FAIL", response, 200)
    
    def test_authenticated_course_endpoints(self):
        """Test authenticated course endpoints"""
        if not self.token:
            self.log_test("Authenticated Course Endpoints", "SKIP", None)
            return
        
        course_data = {
            "title": "Test Course API",
            "description": "Test course created via API",
            "price": 149.99,
            "thumbnail_url": "https://example.com/thumb.jpg"
        }
        
        response = self.make_request("POST", "/api/courses/", course_data, auth=True)
        if response and response.status_code == 201:
            try:
                data = response.json()
                self.course_id = data.get("id")
                self.log_test("Course Creation - Authenticated", "PASS", response, 201)
            except:
                self.log_test("Course Creation - Authenticated", "FAIL", response, 201)
        else:
            self.log_test("Course Creation - Authenticated", "FAIL", response, 201)
    
    def test_lesson_endpoints(self):
        """Test lesson endpoints"""
        if not self.token or not self.course_id:
            self.log_test("Lesson Endpoints", "SKIP", None)
            return
        
        lesson_data = {
            "title": "Introduction Lesson",
            "content": "This is the first lesson content",
            "order_index": 1,
            "video_url": "https://example.com/video1.mp4"
        }
        
        response = self.make_request("POST", f"/api/lessons/courses/{self.course_id}", lesson_data, auth=True)
        if response and response.status_code == 200:
            try:
                data = response.json()
                self.lesson_id = data.get("id")
                self.log_test("Lesson Creation", "PASS", response, 200)
            except:
                self.log_test("Lesson Creation", "FAIL", response, 200)
        else:
            self.log_test("Lesson Creation", "FAIL", response, 200)
    
    def test_enrollment_endpoints(self):
        """Test enrollment endpoints"""
        if not self.token or not self.course_id:
            self.log_test("Enrollment Endpoints", "SKIP", None)
            return
        
        response = self.make_request("POST", f"/api/enrollments/enroll/{self.course_id}", auth=True)
        if response and response.status_code == 201:
            try:
                data = response.json()
                self.enrollment_id = data.get("id")
                self.log_test("Course Enrollment", "PASS", response, 201)
            except:
                self.log_test("Course Enrollment", "FAIL", response, 201)
        else:
            self.log_test("Course Enrollment", "FAIL", response, 201)
    
    def test_review_endpoints(self):
        """Test review endpoints"""
        if not self.token or not self.course_id:
            self.log_test("Review Endpoints", "SKIP", None)
            return
        
        review_data = {
            "rating": 5,
            "comment": "Great course! Very informative."
        }
        
        response = self.make_request("POST", f"/api/enrollments/{self.course_id}/reviews", review_data, auth=True)
        if response and response.status_code == 200:
            self.log_test("Create Review", "PASS", response, 200)
        else:
            self.log_test("Create Review", "FAIL", response, 200)
    
    def test_error_handling(self):
        """Test error handling"""
        response = self.make_request("GET", "/api/courses/99999")
        if response and response.status_code == 404:
            self.log_test("Invalid Course ID", "PASS", response, 404)
        else:
            self.log_test("Invalid Course ID", "FAIL", response, 404)
    
    def cleanup(self):
        """Clean up test data"""
        if self.token and self.course_id:
            response = self.make_request("DELETE", f"/api/courses/{self.course_id}", auth=True)
            if response and response.status_code == 204:
                self.log_test("Course Deletion - Cleanup", "PASS", response, 204)
            else:
                self.log_test("Course Deletion - Cleanup", "FAIL", response, 204)
    
    def generate_report(self):
        """Generate test report"""
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["status"] == "PASS"])
        failed_tests = len([t for t in self.test_results if t["status"] == "FAIL"])
        skipped_tests = len([t for t in self.test_results if t["status"] == "SKIP"])
        
        print("\n" + "="*60)
        print("SKILLS PROUT API TESTING REPORT")
        print("="*60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⏭️  Skipped: {skipped_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
        print("="*60)
        
        with open("api_test_report.json", "w") as f:
            json.dump({
                "summary": {
                    "total": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "skipped": skipped_tests,
                    "success_rate": f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "N/A"
                },
                "tests": self.test_results
            }, indent=2)
        
        print(f"\nDetailed report saved to: api_test_report.json")
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting SkillSprout API Testing Suite")
        print("="*60)
        
        self.test_home_endpoint()
        self.test_user_registration()
        self.test_user_login()
        self.test_public_course_endpoints()
        self.test_authenticated_course_endpoints()
        self.test_lesson_endpoints()
        self.test_enrollment_endpoints()
        self.test_review_endpoints()
        self.test_error_handling()
        self.cleanup()
        
        print("\n📊 Generating Test Report...")
        self.generate_report()

def main():
    """Main execution function"""
    tester = SkillSproutAPITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
