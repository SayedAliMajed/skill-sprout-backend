# SkillSprout API - JSON Test Data for Manual Testing

This document provides ready-to-use JSON payloads for testing all API endpoints manually.

## 🔐 User Authentication Endpoints

### 1. User Registration - Student
```json
POST /api/users/register
{
    "username": "test_student_123",
    "email": "student@example.com",
    "password": "securePassword123",
    "first_name": "John",
    "last_name": "Student",
    "role": "student",
    "bio": "I am a passionate learner looking to improve my skills."
}
```

### 2. User Registration - Instructor
```json
POST /api/users/register
{
    "username": "expert_instructor",
    "email": "instructor@example.com",
    "password": "instructorPass456",
    "first_name": "Jane",
    "last_name": "Instructor",
    "role": "instructor",
    "bio": "Experienced instructor with 10+ years in the industry."
}
```

### 3. User Login (with email)
```json
POST /api/users/login
{
    "email": "student@example.com",
    "password": "securePassword123"
}
```

### 4. User Login (with username)
```json
POST /api/users/login
{
    "email": "test_student_123",
    "password": "securePassword123"
}
```

## 📚 Course Management Endpoints

### 5. Create Course (Authenticated)
```json
POST /api/courses/
{
    "title": "Complete Python Programming Masterclass",
    "description": "Learn Python from beginner to advanced level with hands-on projects and real-world applications.",
    "price": 199.99,
    "thumbnail_url": "https://example.com/python-course-thumbnail.jpg"
}
```

### 6. Create Course - Web Development
```json
POST /api/courses/
{
    "title": "Full-Stack Web Development with React and Node.js",
    "description": "Build modern web applications using React frontend and Node.js backend with Express and MongoDB.",
    "price": 249.99,
    "thumbnail_url": "https://example.com/webdev-course-thumbnail.jpg"
}
```

### 7. Create Course - Data Science
```json
POST /api/courses/
{
    "title": "Data Science and Machine Learning Fundamentals",
    "description": "Master data science concepts, statistics, and machine learning algorithms with Python.",
    "price": 299.99,
    "thumbnail_url": "https://example.com/datascience-course-thumbnail.jpg"
}
```

### 8. Update Course
```json
PUT /api/courses/1
{
    "title": "Updated Python Programming Course",
    "description": "Updated description with new content and projects",
    "price": 179.99,
    "thumbnail_url": "https://example.com/updated-python-course-thumbnail.jpg"
}
```

## 📖 Lesson Management Endpoints

### 9. Create Lesson for Course
```json
POST /api/lessons/courses/1
{
    "title": "Introduction to Python Variables and Data Types",
    "content": "In this lesson, we'll explore Python variables and basic data types including strings, integers, floats, and booleans.",
    "video_url": "https://example.com/videos/python-intro.mp4",
    "order_index": 1
}
```

### 10. Create Lesson - Advanced Topic
```json
POST /api/lessons/courses/1
{
    "title": "Object-Oriented Programming in Python",
    "content": "Learn about classes, objects, inheritance, and polymorphism in Python with practical examples.",
    "video_url": "https://example.com/videos/python-oop.mp4",
    "order_index": 10
}
```

### 11. Create Lesson - Web Development
```json
POST /api/lessons/courses/2
{
    "title": "React Components and JSX",
    "content": "Understanding React components, JSX syntax, and component composition.",
    "video_url": "https://example.com/videos/react-components.mp4",
    "order_index": 1
}
```

## 👥 Enrollment Endpoints

### 12. Enroll in Course
```json
POST /api/enrollments/enroll/1
```

### 13. Update Progress
```json
PATCH /api/enrollments/1/progress
{
    "progress_percent": 45.5
}
```

### 14. Update Progress - Completed
```json
PATCH /api/enrollments/1/progress
{
    "progress_percent": 100.0
}
```

### 15. Get My Enrollments
```json
GET /api/enrollments/my
```

## ⭐ Review Endpoints

### 16. Create Review - Positive
```json
POST /api/enrollments/1/reviews
{
    "rating": 5,
    "comment": "Excellent course! The instructor explains concepts clearly and the projects are very practical. Highly recommended!"
}
```

### 17. Create Review - Mixed
```json
POST /api/enrollments/2/reviews
{
    "rating": 4,
    "comment": "Good course content overall. Some sections could be more detailed, but the instructor is knowledgeable and responsive."
}
```

### 18. Create Review - Critical
```json
POST /api/enrollments/3/reviews
{
    "rating": 2,
    "comment": "The course has potential but needs more structure. Some videos are outdated and the pace is inconsistent."
}
```

## 🔍 Error Testing JSON Payloads

### 19. Registration with Duplicate Email
```json
POST /api/users/register
{
    "username": "different_username",
    "email": "student@example.com",
    "password": "anotherPassword",
    "first_name": "Another",
    "last_name": "User",
    "role": "student",
    "bio": "This should fail due to duplicate email"
}
```

### 20. Registration with Invalid Email
```json
POST /api/users/register
{
    "username": "invalid_email_user",
    "email": "not-a-valid-email",
    "password": "password123",
    "first_name": "Invalid",
    "last_name": "Email",
    "role": "student",
    "bio": "Testing invalid email format"
}
```

### 21. Registration with Missing Fields
```json
POST /api/users/register
{
    "username": "incomplete_user"
}
```

### 22. Login with Wrong Password
```json
POST /api/users/login
{
    "email": "student@example.com",
    "password": "wrongPassword"
}
```

### 23. Create Course with Invalid Price
```json
POST /api/courses/
{
    "title": "Invalid Price Course",
    "description": "Testing invalid price",
    "price": -50.00,
    "thumbnail_url": "https://example.com/thumb.jpg"
}
```

### 24. Create Review with Invalid Rating
```json
POST /api/enrollments/1/reviews
{
    "rating": 10,
    "comment": "Rating should be between 1-5"
}
```

## 📊 Complete Student Journey Test Data

### Step 1: Register Student
```json
POST /api/users/register
{
    "username": "learning_journey_student",
    "email": "journey.student@example.com",
    "password": "studentJourney123",
    "first_name": "Sarah",
    "last_name": "Learner",
    "role": "student",
    "bio": "I love learning new skills and completing courses."
}
```

### Step 2: Login Student
```json
POST /api/users/login
{
    "email": "journey.student@example.com",
    "password": "studentJourney123"
}
```

### Step 3: Browse Courses
```json
GET /api/courses/
```

### Step 4: Enroll in Course (use course ID from step 3)
```json
POST /api/enrollments/enroll/[COURSE_ID]
```

### Step 5: Update Progress
```json
PATCH /api/enrollments/[ENROLLMENT_ID]/progress
{
    "progress_percent": 75.0
}
```

### Step 6: Submit Review
```json
POST /api/enrollments/[COURSE_ID]/reviews
{
    "rating": 5,
    "comment": "Amazing course! I learned so much and the instructor was fantastic."
}
```

## 🎯 Instructor Course Creation Journey

### Step 1: Register Instructor
```json
POST /api/users/register
{
    "username": "course_creator_instructor",
    "email": "course.creator@example.com",
    "password": "instructorCreate123",
    "first_name": "Mike",
    "last_name": "Creator",
    "role": "instructor",
    "bio": "I create high-quality educational content for aspiring developers."
}
```

### Step 2: Login Instructor
```json
POST /api/users/login
{
    "email": "course.creator@example.com",
    "password": "instructorCreate123"
}
```

### Step 3: Create Course
```json
POST /api/courses/
{
    "title": "JavaScript ES6+ Modern Features",
    "description": "Master modern JavaScript features including arrow functions, destructuring, modules, and async/await.",
    "price": 149.99,
    "thumbnail_url": "https://example.com/javascript-es6-thumbnail.jpg"
}
```

### Step 4: Create Lessons
```json
POST /api/lessons/courses/[COURSE_ID]
{
    "title": "Arrow Functions and Template Literals",
    "content": "Learn how to write cleaner, more concise code using arrow functions and template literals.",
    "video_url": "https://example.com/videos/es6-arrow-functions.mp4",
    "order_index": 1
}
```

## 🔄 Authentication Headers

After successful login, use the JWT token in the Authorization header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 📝 Testing Tips

1. **Start Simple**: Begin with user registration and login
2. **Check Authentication**: Test protected endpoints without tokens
3. **Test Error Cases**: Use invalid data to test error handling
4. **Verify Persistence**: Check that created data persists between requests
5. **Test Relationships**: Ensure foreign key constraints work properly

## 🚀 Base URL

All requests should be made to:
```
http://localhost:8000
```

## ✅ Expected Success Responses

- User Registration: `200 OK` with user data
- User Login: `200 OK` with JWT token
- Course Creation: `201 Created` with course details
- Lesson Creation: `200 OK` with lesson details
- Enrollment: `201 Created` with enrollment details
- Review: `200 OK` with review details

## ⚠️ Expected Error Responses

- Invalid Data: `422 Unprocessable Entity`
- Authentication Failed: `403 Forbidden`
- Resource Not Found: `404 Not Found`
- Duplicate Resource: `400 Bad Request`
