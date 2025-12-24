# 🎯 Frontend API Documentation for AI Integration

**Generated:** 12/24/2025  
**Version:** 1.0.0  
**Base URL:** `http://localhost:8000`  
**Database:** PostgreSQL (`skill_sprout_db`)  
**Authentication:** JWT Bearer Token

---

## 📋 **API Overview**

The SkillSprout Backend provides a comprehensive Learning Management System (LMS) API with full CRUD operations for users, courses, lessons, enrollments, and reviews.

### **Core Features**
- ✅ User Management (Registration, Authentication, Authorization)
- ✅ Course Management (Create, Read, Update, Delete)
- ✅ Lesson Management (Content creation and delivery)
- ✅ Enrollment System (Student-course relationships)
- ✅ Review System (Course ratings and feedback)
- ✅ Role-Based Access Control (Student, Instructor)

---

## 🔐 **Authentication System**

### **Authentication Type:** JWT Bearer Token
```javascript
// Header Format
Authorization: Bearer <jwt_token>
```

### **Registration Endpoint**
```http
POST /api/users/register
Content-Type: application/json

{
  "username": "string (required, unique)",
  "email": "string (required, unique)",
  "password": "string (required, min 6 chars)",
  "first_name": "string (required)",
  "last_name": "string (required)",
  "role": "student|instructor",
  "bio": "string (optional)"
}
```

**Response (200):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "instructor",
  "bio": "Experienced educator"
}
```

### **Login Endpoint**
```http
POST /api/users/login
Content-Type: application/json

{
  "email": "string (required)",
  "password": "string (required)"
}
```

**Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Login successful"
}
```

---

## 👥 **User Management API**

### **Get Current User Profile**
```http
GET /api/users/me
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "instructor",
  "bio": "Experienced educator",
  "created_at": "2025-12-24T14:30:00Z"
}
```

---

## 📚 **Course Management API**

### **Create Course** (Instructor Only)
```http
POST /api/courses/
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "string (required)",
  "description": "string (required)",
  "price": "number (required, min 0)",
  "thumbnail_url": "string (optional, URL)"
}
```

**Response (201):**
```json
{
  "id": 15,
  "title": "Introduction to Python",
  "description": "Learn Python programming from scratch",
  "price": 99.99,
  "thumbnail_url": "https://example.com/python-course.jpg",
  "instructor_id": 1,
  "created_at": "2025-12-24T14:30:00Z",
  "updated_at": "2025-12-24T14:30:00Z"
}
```

### **Get All Courses** (Public)
```http
GET /api/courses/
```

**Response (200):**
```json
[
  {
    "id": 1,
    "title": "Python Fundamentals",
    "description": "Learn Python basics",
    "price": 49.99,
    "thumbnail_url": "https://example.com/thumb1.jpg",
    "instructor_id": 1,
    "created_at": "2025-12-24T14:30:00Z"
  }
]
```

### **Get Course by ID** (Public)
```http
GET /api/courses/{course_id}
```

**Response (200):**
```json
{
  "id": 15,
  "title": "Introduction to Python",
  "description": "Learn Python programming from scratch",
  "price": 99.99,
  "thumbnail_url": "https://example.com/python-course.jpg",
  "instructor_id": 1,
  "created_at": "2025-12-24T14:30:00Z",
  "updated_at": "2025-12-24T14:30:00Z"
}
```

### **Update Course** (Instructor - Course Owner)
```http
PUT /api/courses/{course_id}
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "string (optional)",
  "description": "string (optional)", 
  "price": "number (optional)",
  "thumbnail_url": "string (optional)"
}
```

### **Delete Course** (Instructor - Course Owner)
```http
DELETE /api/courses/{course_id}
Authorization: Bearer <jwt_token>
```

**Response (204):** No Content

---

## 📖 **Lesson Management API**

### **Create Lesson** (Instructor - Course Owner Only)
```http
POST /api/lessons/courses/{course_id}
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "string (required)",
  "content_text": "string (required)",
  "video_url": "string (optional, URL)",
  "order_index": "integer (required, min 1)"
}
```

**Response (200):**
```json
{
  "id": 15,
  "course_id": 15,
  "title": "Getting Started with Python",
  "content_text": "In this lesson, we'll cover the basics of Python programming...",
  "video_url": "https://example.com/python-intro.mp4",
  "order_index": 1,
  "created_at": "2025-12-24T14:30:00Z",
  "updated_at": "2025-12-24T14:30:00Z"
}
```

### **Get Lessons for Course** (Student - Enrolled Only)
```http
GET /api/lessons/{course_id}
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
[
  {
    "id": 15,
    "course_id": 15,
    "title": "Getting Started with Python",
    "content_text": "In this lesson, we'll cover the basics of Python programming...",
    "video_url": "https://example.com/python-intro.mp4",
    "order_index": 1,
    "created_at": "2025-12-24T14:30:00Z",
    "updated_at": "2025-12-24T14:30:00Z"
  }
]
```

### **Update Lesson** (Instructor - Course Owner Only)
```http
PATCH /api/lessons/{lesson_id}
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "string (optional)",
  "content_text": "string (optional)",
  "video_url": "string (optional)",
  "order_index": "integer (optional)"
}
```

**Response (200):**
```json
{
  "id": 15,
  "course_id": 15,
  "title": "Updated Lesson Title",
  "content_text": "Updated lesson content...",
  "video_url": "https://example.com/updated-video.mp4",
  "order_index": 1,
  "created_at": "2025-12-24T14:30:00Z",
  "updated_at": "2025-12-24T14:30:00Z"
}
```

### **Delete Lesson** (Instructor - Course Owner Only)
```http
DELETE /api/lessons/{lesson_id}
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
{
  "message": "Lesson deleted successfully"
}
```

---

## 🎓 **Enrollment System API**

### **Enroll in Course** (Student Only)
```http
POST /api/enrollments/enroll/{course_id}
Authorization: Bearer <jwt_token>
```

**Response (201):**
```json
{
  "id": 2,
  "user_id": 4,
  "course_id": 15,
  "enrolled_at": "2025-12-24T14:30:00Z",
  "progress_percent": 0.0,
  "created_at": "2025-12-24T14:30:00Z",
  "updated_at": "2025-12-24T14:30:00Z"
}
```

### **Get My Enrollments** (Student)
```http
GET /api/enrollments/me
Authorization: Bearer <jwt_token>
```

**Response (200):**
```json
[
  {
    "course_id": 15,
    "progress_percent": 25.5
  }
]
```

### **Update Progress** (Student - Own Enrollment Only)
```http
PATCH /api/enrollments/{enrollment_id}/progress
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "progress_percent": 0.75
}
```

**Response (200):**
```json
{
  "id": 2,
  "user_id": 4,
  "course_id": 15,
  "enrolled_at": "2025-12-24T14:30:00Z",
  "progress_percent": 0.75,
  "created_at": "2025-12-24T14:30:00Z",
  "updated_at": "2025-12-24T14:30:00Z"
}
```

---

## ⭐ **Review System API**

### **Create Review** (Student - Enrolled Only)
```http
POST /api/enrollments/{course_id}/reviews
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "rating": "integer (required, 1-5)",
  "comment": "string (optional)"
}
```

**Response (200):**
```json
{
  "id": 1,
  "user_id": 4,
  "course_id": 15,
  "rating": 5,
  "comment": "Excellent course! Very informative.",
  "created_at": "2025-12-24T14:30:00Z"
}
```

### **Get Course Reviews** (Public)
```http
GET /api/enrollments/{course_id}/reviews
```

**Response (200):**
```json
[
  {
    "id": 1,
    "user_id": 4,
    "course_id": 15,
    "rating": 5,
    "comment": "Excellent course! Very informative.",
    "created_at": "2025-12-24T14:30:00Z",
    "user": {
      "first_name": "John",
      "last_name": "Student"
    }
  }
]
```

---

## 🔍 **Data Models**

### **User Model**
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "role": "string (student|instructor)",
  "bio": "string",
  "created_at": "timestamp"
}
```

### **Course Model**
```json
{
  "id": "integer",
  "title": "string",
  "description": "string",
  "price": "number",
  "thumbnail_url": "string",
  "instructor_id": "integer",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### **Lesson Model**
```json
{
  "id": "integer",
  "course_id": "integer",
  "title": "string",
  "content_text": "string",
  "video_url": "string",
  "order_index": "integer",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### **Enrollment Model**
```json
{
  "id": "integer",
  "user_id": "integer",
  "course_id": "integer",
  "enrolled_at": "timestamp",
  "progress_percent": "number (0.0-1.0)",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### **Review Model{
  "id**
```json
": "integer",
  "user_id": "integer",
  "course_id": "integer",
  "rating": "integer (1-5)",
  "comment": "string",
  "created_at": "timestamp"
}
```

---

## 🛡️ **Authorization Rules**

### **Role-Based Access Control**

| Action | Student | Instructor | Public |
|--------|---------|------------|--------|
| Register/Login | ✅ | ✅ | ✅ |
| View Courses | ✅ | ✅ | ✅ |
| Create Course | ❌ | ✅ | ❌ |
| Edit Own Course | ❌ | ✅ | ❌ |
| Delete Own Course | ❌ | ✅ | ❌ |
| Create Lesson | ❌ | ✅ (Own Courses) | ❌ |
| Edit Own Lesson | ❌ | ✅ (Own Courses) | ❌ |
| Delete Own Lesson | ❌ | ✅ (Own Courses) | ❌ |
| View Lessons | ✅ (Enrolled Only) | ✅ (Own Courses) | ❌ |
| Enroll in Course | ✅ | ❌ | ❌ |
| Update Progress | ✅ (Own Enrollment) | ❌ | ❌ |
| Create Review | ✅ (Enrolled Only) | ❌ | ❌ |
| View Reviews | ✅ | ✅ | ✅ |

---

## ⚠️ **Error Handling**

### **Standard Error Response Format**
```json
{
  "detail": "Error message describing what went wrong"
}
```

### **Common HTTP Status Codes**

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Invalid or missing authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |

### **Common Error Scenarios**
- **401 Unauthorized**: Invalid JWT token or missing Authorization header
- **403 Forbidden**: User doesn't have permission for the requested action
- **404 Not Found**: Course, lesson, or user doesn't exist
- **422 Unprocessable Entity**: Missing required fields or invalid data format

---

## 🚀 **Quick Start for Frontend Integration**

### **1. Authentication Flow**
```javascript
// 1. Register User
const registerResponse = await fetch('/api/users/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(userData)
});

// 2. Login User  
const loginResponse = await fetch('/api/users/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(loginData)
});

const { token } = await loginResponse.json();

// 3. Use Token for Authenticated Requests
const authenticatedHeaders = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
};
```

### **2. Course and Lesson Flow**
```javascript
// Get courses (public)
const courses = await fetch('/api/courses/').then(r => r.json());

// Create course (instructor only)
const newCourse = await fetch('/api/courses/', {
  method: 'POST',
  headers: authenticatedHeaders,
  body: JSON.stringify(courseData)
});

// Get lessons (student - enrolled only)
const lessons = await fetch(`/api/lessons/${courseId}`, {
  headers: authenticatedHeaders
});
```

### **3. Enrollment Flow**
```javascript
// Enroll in course (student only)
const enrollment = await fetch(`/api/enrollments/enroll/${courseId}`, {
  method: 'POST',
  headers: authenticatedHeaders
});

// Update progress
const progressUpdate = await fetch(`/api/enrollments/${enrollmentId}/progress`, {
  method: 'PATCH',
  headers: authenticatedHeaders,
  body: JSON.stringify({ progress_percent: 0.75 })
});
```

---

## 📝 **Configuration Requirements**

### **Environment Variables**
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/skill_sprout_db
JWT_SECRET=your-super-secret-jwt-key
CORS_ORIGINS=http://localhost:5173,http://localhost:8080
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### **Database Schema Requirements**
- **Users Table**: Contains user accounts with roles
- **Courses Table**: Course information and metadata
- **Lessons Table**: Lesson content and ordering
- **Enrollments Table**: Student-course relationships with progress
- **Reviews Table**: Course ratings and feedback

---

## 🧪 **Testing Endpoints**

### **Quick Test Commands**
```bash
# Test basic connectivity
curl http://localhost:8000/

# Test user registration
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"test123","first_name":"Test","last_name":"User","role":"student"}'

# Test course creation (requires auth)
curl -X POST http://localhost:8000/api/courses/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Course","description":"Test","price":99.99}'
```

---

## 📞 **Support & Documentation**

- **API Testing Tools**: Available in repository
- **Manual Testing Guide**: Comprehensive step-by-step procedures
