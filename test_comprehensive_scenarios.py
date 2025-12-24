#!/usr/bin/env python3
"""
Comprehensive Test Scenarios for SkillSprout Backend API
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

    # ========================================
    # SCENARIO 1: COMPLETE STUDENT JOURNEY
    # ========================================
    
    def scenario_1_complete_student_journey(self):
        """Test complete student workflow: Registration → Login → Browse → Enroll → Take Lessons → Review"""
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
                    self.create_test_course()
                    
            else:
                self.log_scenario("Browse Courses", "FAIL", f"Status: {response.status_code if response else 'No response'}")
                return
            
            # Step 4: Enroll in a course (need course_id)
            if not self.course_id:
                # Get first available course
                response = self.make_request("GET", "/api/courses/")
                if response and response.status_code == 200:
                    courses = response.json()
                    if courses:
                        self.course_id = courses[0]["id"]
                    else:
                        self.log_scenario("Course Enrollment", "FAIL", "No courses available for enrollment")
                        return
            
            response = self.make_request("POST", f"/api/enrollments/enroll/{self.course_id}", auth=True, token=self.student_token)
            if response and response.status_code == 201:
                data = response.json()
                self.enrollment_id = data.get("id")
                self.log_scenario("Course Enrollment", "PASS", "Successfully enrolled in course")
            else:
                self.log_scenario("Course Enrollment", "FAIL", f"Status: {response.status_code if response else 'No response'}")
                return
            
            # Step 5: Update progress
            if self.enrollment_id:
                progress_data = {"progress_percent": 50.0}
                response = self.make_request("PATCH", f"/api/enrollments/{self.enrollment_id}/progress", 
                                           progress_data, auth=True, token=self.student_token)
                if response and response.status_code == 200:
                    self.log_scenario("Update Progress", "PASS", "Progress updated to 50%")
                else:
                    self.log_scenario("Update Progress", "FAIL", f"Status: {response.status_code if response else 'No response'}")
            
            # Step 6: Submit review
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
    # SCENARIO 2: INSTRUCTOR COURSE CREATION
    # ========================================
    
    def scenario_2_instructor_course_creation(self):
        """Test instructor workflow: Registration → Login → Create Course → Add Lessons"""
        print("👨‍🏫 SCENARIO 2: Instructor Course Creation")
        print("=" * 50)
        
        try:
            # Step 1: Register new instructor
            instructor_data = {
                "username": "instructor_creator",
                "email": "instructor_creator@example.com",
                "password": "instructorpass123",
                "first_name": "Instructor",
                "last_name": "Creator",
                "role": "instructor",
                "bio": "Expert instructor creating courses"
            }
            
            response = self.make_request("POST", "/api/users/register", instructor_data)
            if not response or response.status_code != 200:
                self.log_scenario("Instructor Registration", "FAIL", f"Status: {response.status_code if response else 'No response'}")
                return
            
            self.log_scenario("Instructor Registration", "PASS", "New instructor registered successfully")
            
            # Step 2: Login as instructor
            login_data = {
                "email": "instructor_creator@example.com",
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
            
            # Step 3: Create new course
            course_data = {
                "title": "Complete Python Programming Course",
                "description": "Learn Python from basics to advanced concepts with hands-on projects",
                "price": 199.99,
                "thumbnail_url": "https://example.com/python-course-thumb.jpg"
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
            
            self.log_scenario("Instructor Course Creation", "PASS", "Complete instructor workflow successful")
            
        except Exception as e:
            self.log_scenario("Instructor Course Creation", "FAIL", f"Exception: {str(e)}")
    
    # ========================================
    # SCENARIO 3: AUTHENTICATION & SECURITY
    # ========================================
    
    def scenario_3_authentication_security(self):
        """Test authentication and security scenarios"""
        print("🔐 SCENARIO 3: Authentication & Security")
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
            
            # Test 3: Register with weak password (if validation exists)
            weak_password_data = {
                "username": "weakuser",
                "email": "weak@example.com",
                "password": "123",  # Weak password
                "first_name": "Weak",
                "last_name": "User",
                "role": "student",
                "bio": "Testing weak password"
            }
            
            response = self.make_request("POST", "/api/users/register", weak_password_data)
            if response:
                if response.status_code == 400:
                    self.log_scenario("Weak Password Validation", "PASS", "Password validation working")
                else:
                    self.log_scenario("Weak Password Validation", "INFO", f"No password validation (Status: {response.status_code})")
            
            # Test 4: Duplicate registration
            duplicate_data = {
                "username": "duplicate_user",
                "email": "duplicate@example.com",
                "password": "password123",
                "first_name": "Duplicate",
                "last_name": "User",
                "role": "student",
                "bio": "First registration"
            }
            
            # First registration
            self.make_request("POST", "/api/users/register", duplicate_data)
            
            # Second registration (should fail)
            response = self.make_request("POST", "/api/users/register", duplicate_data)
            if response and response.status_code == 400:
                self.log_scenario("Duplicate Registration Prevention", "PASS", "Correctly prevented duplicate registration")
            else:
                self.log_scenario("Duplicate Registration Prevention", "FAIL", f"Status: {response.status_code if response else 'No response'}")
            
            self.log_scenario("Authentication & Security", "PASS", "Security tests completed")
            
        except Exception as e:
            self.log_scenario("Authentication & Security", "FAIL", f"Exception: {str(e)}")
    
    # ========================================
    # SCENARIO 4: ERROR HANDLING
    # ========================================
    
    def scenario_4_error_handling(self):
        """Test error handling and edge cases"""
        print("🚨 SCENARIO 4: Error Handling")
        print("=" * 50)
        
        try:
            # Test 1: Non-existent course
            response = self.make_request("GET", "/api/courses/99999")
            if response and response.status_code == 404:
                self.log_scenario("Non-existent Course", "PASS", "Correctly returned 404")
            else:
                self.log_scenario("Non-existent Course", "FAIL", f"Status: {response.status_code if response else 'No response'}")
            
            # Test 2: Invalid JSON
            response = requests.post(f"{self.base_url}/api/users/register", 
                                   data="invalid json", 
                                   headers={"Content-Type": "application/json"})
            if response and response.status_code == 422:
                self.log_scenario("Invalid JSON", "PASS", "Correctly handled invalid JSON")
            else:
                self.log_scenario("Invalid JSON", "INFO", f"Status: {response.status_code if response else 'No response'}")
            
            # Test 3: Missing required fields
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
            
            # Test 4: Invalid email format
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
    # SCENARIO 5: DATA INTEGRITY
    # ========================================
    
    def scenario_5_data_integrity(self):
        """Test data integrity and constraints"""
        print("🔒 SCENARIO 5: Data Integrity")
        print("=" * 50)
        
        try:
            # Test 1: Same username and email
            user_data = {
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "password123",
                "first_name": "Test",
                "last_name": "User",
                "role": "student",
                "bio": "Testing data integrity"
            }
            
            # First registration
            response1 = self.make_request("POST", "/api/users/register", user_data)
            
            # Try same username
            user_data["email"] = "different@example.com"
            response2 = self.make_request("POST", "/api/users/register", user_data)
            
            if response2 and response2.status_code == 400:
                self.log_scenario("Unique Username Constraint", "PASS", "Username uniqueness enforced")
            else:
                self.log_scenario("Unique Username Constraint", "FAIL", f"Status: {response2.status_code if response2 else 'No response'}")
            
            # Test 2: Same email
            user_data["username"] = "differentuser"
            user_data["email"] = "testuser@example.com"  # Same email
            response3 = self.make_request("POST", "/api/users/register", user_data)
            
            if response3 and response3.status_code == 400:
                self.log_scenario("Unique Email Constraint", "PASS", "Email uniqueness enforced")
            else:
                self.log_scenario("Unique
