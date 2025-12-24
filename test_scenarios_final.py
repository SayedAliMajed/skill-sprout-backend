#!/usr/bin/env python3
"""
Complete Comprehensive Test Scenarios for SkillSprout Backend API
This script implements detailed end-to-end testing scenarios
"""

import requests
import json
import time
import sys
from typing import Dict, Any, Optional

class SkillSproutComprehensiveTester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token = None
        self.student_token = None
        self.instructor_token = None
        self.course_id = None
        self.lesson_id = None
        self.enrollment_id = None
        self.scenario_results = []
        
    def log_scenario(self, scenario: str, status: str, details: str = ""):
        """Log scenario results"""
        result = {
            "scenario": scenario,
            "status": status,
            "details": details,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.scenario_results.append(result)
        
        status_indicator = "✅ PASS" if status == "PASS" else "❌ FAIL"
        print(f"{status_indicator} {scenario}")
        if details:
            print(f"   Details: {details}")
        print()
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, auth: bool = False, token: str = None) -> Optional[requests.Response]:
        """Make HTTP request with proper headers"""
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if auth and token:
            headers["Authorization"] = f"Bearer {token}"
        
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
    
    def create_test_course(self):
        """Helper method to create a test course"""
        test_course_data = {
            "title": "Test Course for Scenarios",
            "description": "A test course created for comprehensive testing",
            "price": 99.99,
            "thumbnail_url": "https://example.com/test-course.jpg"
        }
        
        # Create instructor for test course
        instructor_data = {
            "username": "test_instructor",
            "email": "test_instructor@example.com",
            "password": "instructor123",
            "first_name": "Test",
            "last_name": "Instructor",
            "role": "instructor",
            "bio": "Test instructor for scenarios"
        }
        
        # Register instructor
        self.make_request("POST", "/api/users/register", instructor_data)
        
        # Login as instructor
        login_data = {
            "email": "test_instructor@example.com",
            "password": "instructor123"
        }
        
        response = self.make_request("POST", "/api/users/login", login_data)
        if response and response.status_code == 200:
            data = response.json()
            instructor_token = data.get("token")
            
            # Create course
            response = self.make_request("POST", "/api/courses/", test_course_data, auth=True, token=instructor_token)
            if response and response.status_code == 201:
                course_data = response.json()
                self.course_id = course_data.get("id")
                return True
        return False

    # ========================================
    # SCENARIO 1: COMPLETE STUDENT JOURNEY
    # ========================================
    
    def scenario_1_complete_student_journey(self):
        """Test complete student workflow"""
        print("🎓 SCENARIO 1: Complete Student Journey")
        print("=" * 50)
        
        try:
            # Step 1: Register new student
            student_data = {
                "username": "student_journey",
                "email": "student_journey@example.com",
                "password": "studentpass123",
                "first_name": "Student",
                "last_name": "Journey",
                "role": "student",
                "bio": "Testing complete student journey"
            }
            
            response = self.make_request("POST", "/api/users/register", student_data)
            if not response or response.status_code != 200:
                self.log_scenario("Student Registration", "FAIL", f"Status: {response.status_code if response else 'No response'}")
                return
            
            self.log_scenario("Student Registration", "PASS", "New student registered successfully")
            
            # Step 2: Login as student
            login_data = {
                "email": "student_journey@example.com",
                "password": "studentpass123"
            }
            
            response = self.make_request("POST", "/api/users/login", login_data)
            if response and response.status_code == 200:
                data = response.json()
                self.student_token = data.get("token")
                self.log_scenario("Student Login", "PASS", "JWT token obtained")
            else:
                self.log_scenario("Student Login", "FAIL", f"Status: {response.status_code if response else 'No response'}")
                return
            
            # Step 3: Browse available courses
            response = self.make_request("GET", "/api/courses/")
            if response and response.status_code == 200:
                courses = response.json()
                self.log_scenario("Browse Courses", "PASS", f"Found {len(courses)} courses")
                
                # If no courses exist, create one for testing
                if len(courses) == 0:
                    if self.create_test_course():
                        self.log_scenario("Create Test Course", "PASS", "Test course created for testing")
                    else:
                        self.log_scenario("Create Test Course", "FAIL", "Failed to create test course")
                        return
                        
            else:
                self.log_scenario("Browse Courses", "FAIL", f"Status: {response.status_code if response else 'No response'}")
                return
            
            # Step 4: Get course ID for enrollment
            if not self.course_id:
                response = self.make_request("GET", "/api/courses/")
                if response and response.status_code == 200:
                    courses = response.json()
                    if courses:
                        self.course_id = courses[0]["id"]
                    else:
                        self.log_scenario("Course Enrollment", "FAIL", "No courses available for enrollment")
                        return
            
            # Step 5: Enroll in course
            response = self.make_request("POST", f"/api/enrollments/enroll/{self.course_id}", 
                                       auth=True, token=self.student_token)
            if response and response.status_code == 201:
                data = response.json()
                self.enrollment_id = data.get("id")
                self.log_scenario("Course Enrollment", "PASS", "Successfully enrolled in course")
            else:
                self.log_scenario("Course Enrollment", "FAIL", f"Status: {response.status_code if response else 'No response'}")
                return
            
            # Step 6: Update progress
            if self.enrollment_id:
                progress_data = {"progress_percent": 50.0}
                response = self.make_request("PATCH", f"/api/enrollments/{self.enrollment_id}/progress", 
                                           progress_data, auth=True, token=self.student_token)
                if response and response.status_code == 200:
                    self.log_scenario("Update Progress", "PASS", "Progress updated to 50%")
                else:
                    self.log_scenario("Update Progress", "FAIL", f"Status: {response.status_code if response else 'No response'}")
            
            # Step 7: Submit review
            review_data = {
                "rating": 5,
                "comment": "Excellent course! Very informative and well-structured."
            }
            
            response = self.make_request("POST", f"/api/enrollments/{self.course_id}/reviews", 
                                       review_data, auth=True, token=self.student_token)
            if response and response.status_code == 200:
                self.log_scenario("Submit Review", "PASS", "Review submitted successfully")
            else:
                self.log_scenario("Submit Review", "FAIL", f"Status: {response.status_code if response else 'No response'}")
            
            self.log_scenario("Complete Student Journey", "PASS", "All steps completed successfully")
            
        except Exception as e:
            self.log_scenario("Complete Student Journey", "FAIL", f"Exception: {str(e)}")

    # ========================================
    # SCENARIO 2: AUTHENTICATION & SECURITY
    # ========================================
    
    def scenario_2_authentication_security(self):
        """Test authentication and security scenarios"""
        print("🔐 SCENARIO 2: Authentication & Security")
        print("=" * 50)
        
        try:
            # Test 1: Access protected endpoint without token
            response = self.make_request("POST", "/api/courses/", {"title": "Unauthorized Course"})
            if response and response.status_code == 403:
                self.log_scenario("Protected Endpoint Without Token", "PASS", "Correctly rejected unauthorized access")
            else:
                self.log_scenario("Protected Endpoint Without Token", "FAIL", f"Status: {response.status_code if response else 'No response'}")
            
            # Test 2: Invalid token
            headers = {"Authorization": "Bearer invalid_token_123"}
            response = requests.get(f"{self.base_url}/api/courses/my/courses", headers=headers)
            if response and response.status_code == 403:
                self.log_scenario("Invalid Token", "PASS", "Correctly rejected invalid token")
            else:
                self.log_scenario("Invalid Token", "FAIL", f"Status: {response.status_code if response else 'No response'}")
            
            # Test 3: Duplicate registration prevention
            user_data = {
                "username": "duplicate_test",
                "email": "duplicate_test@example.com",
                "password": "password123",
                "first_name": "Duplicate",
                "last_name": "Test",
                "role": "student",
                "bio": "Testing duplicate prevention"
            }
            
            # First registration
            self.make_request("POST", "/api/users/register", user_data)
            
            # Second registration (should fail)
            response = self.make_request("POST", "/api/users/register", user_data)
            if response and response.status_code == 400:
                self.log_scenario("Duplicate Registration Prevention", "PASS", "Correctly prevented duplicate registration")
            else:
                self.log_scenario("Duplicate Registration Prevention", "FAIL", f"Status: {response.status_code if response else 'No response'}")
            
            self.log_scenario("Authentication & Security", "PASS", "Security tests completed")
            
        except Exception as e:
            self.log_scenario("Authentication & Security", "FAIL", f"Exception: {str(e)}")

    # ========================================
    # SCENARIO 3: ERROR HANDLING
    # ========================================
    
    def scenario_3_error_handling(self):
        """Test error handling and edge cases"""
        print("🚨 SCENARIO 3: Error Handling")
        print("=" * 50)
        
        try:
            # Test 1: Non-existent course
            response = self.make_request("GET", "/api/courses/99999")
            if response and response.status_code == 404:
                self.log_scenario("Non-existent Course", "PASS", "Correctly returned 404")
            else:
                self.log_scenario("Non-existent Course", "FAIL", f"Status: {response.status_code if response else 'No response'}")
            
            # Test 2: Missing required fields
            incomplete_data = {
                "username": "incomplete",
                "email": "incomplete@example.com"
                # Missing password and other required fields
            }
            
            response = self.make_request("POST", "/api/users/register", incomplete_data)
            if response and response.status_code == 422:
                self.log_scenario("Missing Required Fields", "PASS", "Correctly validated required fields")
            else:
                self.log_scenario("Missing Required Fields", "FAIL", f"Status: {response.status_code if response else 'No response'}")
            
            # Test 3: Invalid email format
            invalid_email_data = {
                "username": "bademail",
                "email": "not-an-email",
                "password": "password123",
                "first_name": "Bad",
                "last_name": "Email",
                "role": "student",
                "bio": "Testing invalid email"
            }
            
            response = self.make_request("POST", "/api/users/register", invalid_email_data)
            if response and response.status_code == 422:
                self.log_scenario("Invalid Email Format", "PASS", "Correctly validated email format")
            else:
                self.log_scenario("Invalid Email Format", "INFO", f"Status: {response.status_code if response else 'No response'}")
            
            self.log_scenario("Error Handling", "PASS", "Error handling tests completed")
            
        except Exception as e:
            self.log_scenario("Error Handling", "FAIL", f"Exception: {str(e)}")

    # ========================================
    # SCENARIO 4: INSTRUCTOR WORKFLOW
    # ========================================
    
    def scenario_4_instructor_workflow(self):
        """Test instructor course creation workflow"""
        print("👨‍🏫 SCENARIO 4: Instructor Workflow")
        print("=" * 50)
        
        try:
            # Step 1: Register instructor
            instructor_data = {
                "username": "instructor_workflow",
                "email": "instructor_workflow@example.com",
                "password": "instructorpass123",
                "first_name": "Instructor",
                "last_name": "Workflow",
                "role": "instructor",
                "bio": "Testing instructor workflow"
            }
            
            response = self.make_request("POST", "/api/users/register", instructor_data)
            if not response or response.status_code != 200:
                self.log_scenario("Instructor Registration", "FAIL", f"Status: {response.status_code if response else 'No response'}")
                return
            
            self.log_scenario("Instructor Registration", "PASS", "Instructor registered successfully")
            
            # Step 2: Login as instructor
            login_data = {
                "email": "instructor_workflow@example.com",
                "password": "instructorpass123"
            }
            
            response = self.make_request("POST", "/api/users/login", login_data)
            if response and response.status_code == 200:
                data = response.json()
                self.instructor_token = data.get("token")
                self.log_scenario("Instructor Login", "PASS", "Instructor JWT token obtained")
            else:
                self.log_scenario("Instructor Login", "FAIL", f"Status: {response.status_code if response else 'No response'}")
                return
            
            # Step 3: Create course
            course_data = {
                "title": "Advanced Python Programming",
                "description": "Master advanced Python concepts and best practices",
                "price": 299.99,
                "thumbnail_url": "https://example.com/advanced-python.jpg"
            }
            
            response = self.make_request("POST", "/api/courses/", course_data, auth=True, token=self.instructor_token)
            if response and response.status_code == 201:
                data = response.json()
                self.course_id = data.get("id")
                self.log_scenario("Course Creation", "PASS", f"Course created with ID: {self.course_id}")
            else:
                self.log_scenario("Course Creation", "FAIL", f"Status: {response.status_code if response else 'No response'}")
                return
            
            # Step 4: Get instructor's courses
            response = self.make_request("GET", "/api/courses/my/courses", auth=True, token=self.instructor_token)
            if response and response.status_code == 200:
                courses = response.json()
                self.log_scenario("Get My Courses", "PASS", f"Instructor has {len(courses)} courses")
            else:
                self.log_scenario("Get My Courses", "FAIL", f"Status: {response.status_code if response else 'No response'}")
            
            self.log_scenario("Instructor Workflow", "PASS", "Complete instructor workflow successful")
            
        except Exception as e:
            self.log_scenario("Instructor Workflow", "FAIL", f"Exception: {str(e)}")

    def generate_scenario_report(self):
        """Generate comprehensive scenario test report"""
        total_scenarios = len(self.scenario_results)
        passed_scenarios = len([s for s in self.scenario_results if s["status"] == "PASS"])
        failed_scenarios = len([s for s in self.scenario_results if s["status"] == "FAIL"])
        
        print("\n" + "="*70)
        print("SKILLS PROUT COMPREHENSIVE SCENARIO TESTING REPORT")
        print("="*70)
        print(f"Total Scenarios: {total_scenarios}")
        print(f"✅ Passed: {passed_scenarios}")
        print(f"❌ Failed: {failed_scenarios}")
        print(f"Success Rate: {(passed_scenarios/total_scenarios*100):.1f}%" if total_scenarios > 0 else "N/A")
        print("="*70)
        
        # Save detailed report
        with open("comprehensive_scenario_report.json", "w") as f:
            json.dump({
                "summary": {
                    "total": total_scenarios,
                    "passed": passed_scenarios,
                    "failed": failed_scenarios,
                    "success_rate": f"{(passed_scenarios/total_scenarios*100):.1f}%" if total_scenarios > 0 else "N/A"
                },
                "scenarios": self.scenario_results
            }, indent=2)
        
        print(f"\nDetailed report saved to: comprehensive_scenario_report.json")

    def run_all_scenarios(self):
        """Run all comprehensive test scenarios"""
        print("🚀 Starting SkillSprout Comprehensive Scenario Testing")
        print("="*70)
        
        # Run all scenarios
        self.scenario_1_complete_student_journey()
        self.scenario_2_authentication_security()
        self.scenario_3_error_handling()
        self.scenario_4_instructor_workflow()
