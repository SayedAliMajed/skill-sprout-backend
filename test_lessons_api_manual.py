#!/usr/bin/env python3
"""
Manual Lessons API Testing Script
Focused testing for SkillSprout lessons endpoints
"""

import requests
import json
import time
import sys
from typing import Dict, Any, Optional

class LessonsAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token = None
        self.user_id = None
        self.instructor_token = None
        self.instructor_id = None
        self.student_token = None
        self.student_id = None
        self.course_id = None
        self.lesson_id = None
        self.test_results = []
        
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
    
    def setup_test_data(self):
        """Setup test users and course for lessons testing"""
        print("🔧 Setting up test data...")
        
        # Create instructor user
        instructor_data = {
            "username": "test_instructor",
            "email": "instructor@test.com",
            "password": "instructor123",
            "first_name": "John",
            "last_name": "Instructor",
            "role": "instructor",
            "bio": "Test instructor user"
        }
        
        response = self.make_request("POST", "/api/users/register", instructor_data)
        if response and response.status_code == 200:
            try:
                data = response.json()
                self.instructor_id = data.get("id")
                print(f"✅ Instructor created: ID {self.instructor_id}")
            except:
                print("❌ Failed to parse instructor response")
        
        # Login instructor
        login_data = {
            "email": "instructor@test.com",
            "password": "instructor123"
        }
        
        response = self.make_request("POST", "/api/users/login", login_data)
        if response and response.status_code == 200:
            try:
                data = response.json()
                self.instructor_token = data.get("token")
                self.token = self.instructor_token  # Set as default token
                print(f"✅ Instructor logged in successfully")
            except:
                print("❌ Failed to login instructor")
        
        # Create student user
        student_data = {
            "username": "test_student",
            "email": "student@test.com",
            "password": "student123",
            "first_name": "Jane",
            "last_name": "Student",
            "role": "student",
            "bio": "Test student user"
        }
        
        response = self.make_request("POST", "/api/users/register", student_data)
        if response and response.status_code == 200:
            try:
                data = response.json()
                self.student_id = data.get("id")
                print(f"✅ Student created: ID {self.student_id}")
            except:
                print("❌ Failed to parse student response")
        
        # Login student
        login_data = {
            "email": "student@test.com",
            "password": "student123"
        }
        
        response = self.make_request("POST", "/api/users/login", login_data)
        if response and response.status_code == 200:
            try:
                data = response.json()
                self.student_token = data.get("token")
                print(f"✅ Student logged in successfully")
            except:
                print("❌ Failed to login student")
        
        # Create test course
        course_data = {
            "title": "Test Course for Lessons",
            "description": "Course created for testing lessons API",
            "price": 99.99,
            "thumbnail_url": "https://example.com/course-thumb.jpg"
        }
        
        response = self.make_request("POST", "/api/courses/", course_data, auth=True)
        if response and response.status_code == 201:
            try:
                data = response.json()
                self.course_id = data.get("id")
                print(f"✅ Test course created: ID {self.course_id}")
            except:
                print("❌ Failed to parse course response")
    
    def test_lesson_creation(self):
        """Test lesson creation (instructor only)"""
        if not self.token or not self.course_id:
            self.log_test("Lesson Creation", "SKIP", None)
            return
        
        # Test lesson creation (instructor)
        lesson_data = {
            "title": "Introduction to the Course",
            "content_text": "Welcome to this course! In this lesson, you'll learn the basics.",
            "video_url": "https://example.com/intro-video.mp4",
            "order_index": 1
        }
        
        response = self.make_request("POST", f"/api/lessons/courses/{self.course_id}", lesson_data, auth=True)
        if response and response.status_code == 200:
            try:
                data = response.json()
                self.lesson_id = data.get("id")
                self.log_test("Lesson Creation - Instructor", "PASS", response, 200)
                print(f"   Lesson created: ID {self.lesson_id}")
                return True
            except:
                self.log_test("Lesson Creation - Instructor", "FAIL", response, 200)
        else:
            self.log_test("Lesson Creation - Instructor", "FAIL", response, 200)
        
        # Test lesson creation without authentication
        response = self.make_request("POST", f"/api/lessons/courses/{self.course_id}", lesson_data)
        if response and response.status_code == 403:
            self.log_test("Lesson Creation - No Auth", "PASS", response, 403)
        else:
            self.log_test("Lesson Creation - No Auth", "FAIL", response, 403)
        
        # Test lesson creation as student (should fail)
        self.token = self.student_token
        response = self.make_request("POST", f"/api/lessons/courses/{self.course_id}", lesson_data, auth=True)
        if response and response.status_code == 403:
            self.log_test("Lesson Creation - Student Role", "PASS", response, 403)
        else:
            self.log_test("Lesson Creation - Student Role", "FAIL", response, 403)
        
        # Reset token to instructor
        self.token = self.instructor_token
    
    def test_lesson_retrieval(self):
        """Test lesson retrieval (requires enrollment)"""
        if not self.token or not self.course_id:
            self.log_test("Lesson Retrieval", "SKIP", None)
            return
        
        # Test getting lessons without enrollment (should fail)
        response = self.make_request("GET", f"/api/lessons/{self.course_id}", auth=True)
        if response and response.status_code == 403:
            self.log_test("Get Lessons - No Enrollment", "PASS", response, 403)
        else:
            self.log_test("Get Lessons - No Enrollment", "FAIL", response, 403)
        
        # Enroll student in course
        response = self.make_request("POST", f"/api/enrollments/enroll/{self.course_id}", auth=True)
        if response and response.status_code == 201:
            self.log_test("Course Enrollment", "PASS", response, 201)
        else:
            self.log_test("Course Enrollment", "FAIL", response, 201)
        
        # Test getting lessons as enrolled student
        self.token = self.student_token
        response = self.make_request("GET", f"/api/lessons/{self.course_id}", auth=True)
        if response and response.status_code == 200:
            try:
                lessons = response.json()
                if isinstance(lessons, list) and len(lessons) > 0:
                    self.log_test("Get Lessons - With Enrollment", "PASS", response, 200)
                    print(f"   Found {len(lessons)} lessons")
                else:
                    self.log_test("Get Lessons - With Enrollment", "FAIL", response, 200)
            except:
                self.log_test("Get Lessons - With Enrollment", "FAIL", response, 200)
        else:
            self.log_test("Get Lessons - With Enrollment", "FAIL", response, 200)
        
        # Reset token to instructor
        self.token = self.instructor_token
    
    def test_lesson_update(self):
        """Test lesson update (instructor only)"""
        if not self.token or not self.lesson_id:
            self.log_test("Lesson Update", "SKIP", None)
            return
        
        # Test lesson update as instructor
        update_data = {
            "title": "Updated Lesson Title",
            "content_text": "This lesson content has been updated with new information."
        }
        
        response = self.make_request("PATCH", f"/api/lessons/{self.lesson_id}", update_data, auth=True)
        if response and response.status_code == 200:
            self.log_test("Lesson Update - Instructor", "PASS", response, 200)
        else:
            self.log_test("Lesson Update - Instructor", "FAIL", response, 200)
        
        # Test lesson update as student (should fail)
        self.token = self.student_token
        response = self.make_request("PATCH", f"/api/lessons/{self.lesson_id}", update_data, auth=True)
        if response and response.status_code == 403:
            self.log_test("Lesson Update - Student Role", "PASS", response, 403)
        else:
            self.log_test("Lesson Update - Student Role", "FAIL", response, 403)
        
        # Test lesson update without authentication
        self.token = None
        response = self.make_request("PATCH", f"/api/lessons/{self.lesson_id}", update_data)
        if response and response.status_code == 403:
            self.log_test("Lesson Update - No Auth", "PASS", response, 403)
        else:
            self.log_test("Lesson Update - No Auth", "FAIL", response, 403)
        
        # Reset token to instructor
        self.token = self.instructor_token
    
    def test_lesson_deletion(self):
        """Test lesson deletion (instructor only)"""
        if not self.token or not self.lesson_id:
            self.log_test("Lesson Deletion", "SKIP", None)
            return
        
        # Test lesson deletion as instructor
        response = self.make_request("DELETE", f"/api/lessons/{self.lesson_id}", auth=True)
        if response and response.status_code == 200:
            self.log_test("Lesson Deletion - Instructor", "PASS", response, 200)
            self.lesson_id = None  # Clear lesson ID after deletion
        else:
            self.log_test("Lesson Deletion - Instructor", "FAIL", response, 200)
        
        # Test lesson deletion as student (should fail)
        self.token = self.student_token
        response = self.make_request("DELETE", f"/api/lessons/99999", auth=True)
        if response and response.status_code == 403:
            self.log_test("Lesson Deletion - Student Role", "PASS", response, 403)
        else:
            self.log_test("Lesson Deletion - Student Role", "FAIL", response, 403)
        
        # Test lesson deletion without authentication
        self.token = None
        response = self.make_request("DELETE", f"/api/lessons/99999")
        if response and response.status_code == 403:
            self.log_test("Lesson Deletion - No Auth", "PASS", response, 403)
        else:
            self.log_test("Lesson Deletion - No Auth", "FAIL", response, 403)
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        if not self.token:
            self.log_test("Edge Cases", "SKIP", None)
            return
        
        # Test invalid course ID for lesson creation
        lesson_data = {
            "title": "Test Lesson",
            "content_text": "Test content",
            "order_index": 1
        }
        
        response = self.make_request("POST", "/api/lessons/courses/99999", lesson_data, auth=True)
        if response and response.status_code == 404:
            self.log_test("Create Lesson - Invalid Course ID", "PASS", response, 404)
        else:
            self.log_test("Create Lesson - Invalid Course ID", "FAIL", response, 404)
        
        # Test invalid lesson ID for update
        update_data = {"title": "Updated Title"}
        response = self.make_request("PATCH", "/api/lessons/99999", update_data, auth=True)
        if response and response.status_code == 404:
            self.log_test("Update Lesson - Invalid Lesson ID", "PASS", response, 404)
        else:
            self.log_test("Update Lesson - Invalid Lesson ID", "FAIL", response, 404)
        
        # Test invalid lesson ID for deletion
        response = self.make_request("DELETE", "/api/lessons/99999", auth=True)
        if response and response.status_code == 404:
            self.log_test("Delete Lesson - Invalid Lesson ID", "PASS", response, 404)
        else:
            self.log_test("Delete Lesson - Invalid Lesson ID", "FAIL", response, 404)
        
        # Test invalid JSON payload
        invalid_data = {"invalid_field": "value"}
        response = self.make_request("POST", f"/api/lessons/courses/{self.course_id}", invalid_data, auth=True)
        if response and response.status_code in [400, 422]:
            self.log_test("Create Lesson - Invalid JSON", "PASS", response, 400)
        else:
            self.log_test("Create Lesson - Invalid JSON", "FAIL", response, 400)
    
    def generate_report(self):
        """Generate test report"""
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["status"] == "PASS"])
        failed_tests = len([t for t in self.test_results if t["status"] == "FAIL"])
        skipped_tests = len([t for t in self.test_results if t["status"] == "SKIP"])
        
        print("\n" + "="*60)
        print("LESSONS API TESTING REPORT")
        print("="*60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⏭️  Skipped: {skipped_tests}")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "N/A")
        print("="*60)
        
        # Save detailed report
        with open("lessons_api_test_report.json", "w") as f:
            json.dump({
                "summary": {
                    "total": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "skipped": skipped_tests,
                    "success_rate": f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "N/A"
                },
                "test_data": {
                    "instructor_id": self.instructor_id,
                    "student_id": self.student_id,
                    "course_id": self.course_id,
                    "lesson_id": self.lesson_id
                },
                "tests": self.test_results
            }, indent=2)
        
        print(f"\nDetailed report saved to: lessons_api_test_report.json")
    
    def run_lessons_tests(self):
        """Run all lessons API tests"""
        print("🚀 Starting Manual Lessons API Testing")
        print("="*60)
        
        # Setup test data
        self.setup_test_data()
        
        # Test lesson operations
        print("\n📚 PHASE 1: Lesson Creation Tests")
        print("-" * 40)
        self.test_lesson_creation()
        
        print("\n📖 PHASE 2: Lesson Retrieval Tests")
        print("-" * 40)
        self.test_lesson_retrieval()
        
        print("\n✏️  PHASE 3: Lesson Update Tests")
        print("-" * 40)
        self.test_lesson_update()
        
        print("\n🗑️  PHASE 4: Lesson Deletion Tests")
        print("-" * 40)
        self.test_lesson_deletion()
        
        print("\n🔍 PHASE 5: Edge Cases and Error Handling")
        print("-" * 40)
        self.test_edge_cases()
        
        # Generate final report
        self.generate_report()

if __name__ == "__main__":
    tester = LessonsAPITester()
    tester.run_lessons_tests()
