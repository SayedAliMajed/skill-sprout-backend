# Manual Lessons API Testing - CURL Commands

## Prerequisites
- API server running on localhost:8000
- Database: skill_sprout_db
- Test users created (instructor and student)

## Authentication Setup

### 1. Create Test Users

```bash
# Create instructor user
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_instructor",
    "email": "instructor@test.com",
    "password": "instructor123",
    "first_name": "John",
    "last_name": "Instructor",
    "role": "instructor",
    "bio": "Test instructor user"
  }'

# Create student user
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_student",
    "email": "student@test.com",
    "password": "student123",
    "first_name": "Jane",
    "last_name": "Student",
    "role": "student",
    "bio": "Test student user"
  }'
```

### 2. Get Authentication Tokens

```bash
# Login as instructor
INSTRUCTOR_TOKEN=$(curl -s -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "instructor@test.com", "password": "instructor123"}' \
  | jq -r '.token')

# Login as student
STUDENT_TOKEN=$(curl -s -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "student@test.com", "password": "student123"}' \
  | jq -r '.token')

echo "Instructor Token: $INSTRUCTOR_TOKEN"
echo "Student Token: $STUDENT_TOKEN"
```

### 3. Create Test Course

```bash
# Create course (instructor only)
COURSE_ID=$(curl -s -X POST http://localhost:8000/api/courses/ \
  -H "Authorization: Bearer $INSTRUCTOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Course for Lessons",
    "description": "Course created for testing lessons API",
    "price": 99.99,
    "thumbnail_url": "https://example.com/course-thumb.jpg"
  }' | jq -r '.id')

echo "Course ID: $COURSE_ID"
```

## Lessons API Testing

### 📚 Lesson Creation Tests

#### ✅ Test 1: Create Lesson (Instructor) - SHOULD PASS
```bash
curl -X POST http://localhost:8000/api/lessons/courses/$COURSE_ID \
  -H "Authorization: Bearer $INSTRUCTOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction to the Course",
    "content_text": "Welcome to this course! In this lesson, you'\''ll learn the basics.",
    "video_url": "https://example.com/intro-video.mp4",
    "order_index": 1
  }'
```

#### ❌ Test 2: Create Lesson (No Auth) - SHOULD FAIL (403)
```bash
curl -X POST http://localhost:8000/api/lessons/courses/$COURSE_ID \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Unauthorized Lesson",
    "content_text": "This should fail",
    "order_index": 2
  }'
```

#### ❌ Test 3: Create Lesson (Student) - SHOULD FAIL (403)
```bash
curl -X POST http://localhost:8000/api/lessons/courses/$COURSE_ID \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Student Attempted Lesson",
    "content_text": "Students cannot create lessons",
    "order_index": 3
  }'
```

#### ❌ Test 4: Create Lesson (Invalid Course) - SHOULD FAIL (404)
```bash
curl -X POST http://localhost:8000/api/lessons/courses/99999 \
  -H "Authorization: Bearer $INSTRUCTOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Invalid Course Lesson",
    "content_text": "This should fail",
    "order_index": 1
  }'
```

### 📖 Lesson Retrieval Tests

#### ❌ Test 5: Get Lessons (No Enrollment) - SHOULD FAIL (403)
```bash
curl -X GET http://localhost:8000/api/lessons/$COURSE_ID \
  -H "Authorization: Bearer $STUDENT_TOKEN"
```

#### ✅ Test 6: Enroll Student in Course - SHOULD PASS
```bash
curl -X POST http://localhost:8000/api/enrollments/enroll/$COURSE_ID \
  -H "Authorization: Bearer $STUDENT_TOKEN"
```

#### ✅ Test 7: Get Lessons (With Enrollment) - SHOULD PASS
```bash
curl -X GET http://localhost:8000/api/lessons/$COURSE_ID \
  -H "Authorization: Bearer $STUDENT_TOKEN"
```

### ✏️ Lesson Update Tests

#### Get Lesson ID for Update Tests
```bash
# First, get the lesson ID
LESSON_ID=$(curl -s -X GET http://localhost:8000/api/lessons/$COURSE_ID \
  -H "Authorization: Bearer $STUDENT_TOKEN" | jq -r '.[0].id')

echo "Lesson ID: $LESSON_ID"
```

#### ✅ Test 8: Update Lesson (Instructor) - SHOULD PASS
```bash
curl -X PATCH http://localhost:8000/api/lessons/$LESSON_ID \
  -H "Authorization: Bearer $INSTRUCTOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Lesson Title",
    "content_text": "This lesson content has been updated with new information."
  }'
```

#### ❌ Test 9: Update Lesson (Student) - SHOULD FAIL (403)
```bash
curl -X PATCH http://localhost:8000/api/lessons/$LESSON_ID \
  -H "Authorization: Bearer $STUDENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Unauthorized Update"
  }'
```

#### ❌ Test 10: Update Lesson (No Auth) - SHOULD FAIL (403)
```bash
curl -X PATCH http://localhost:8000/api/lessons/$LESSON_ID \
  -H "Content-Type: application/json" \
  -d '{
    "title": "No Auth Update"
  }'
```

#### ❌ Test 11: Update Invalid Lesson - SHOULD FAIL (404)
```bash
curl -X PATCH http://localhost:8000/api/lessons/99999 \
  -H "Authorization: Bearer $INSTRUCTOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Invalid Lesson Update"
  }'
```

### 🗑️ Lesson Deletion Tests

#### ✅ Test 12: Delete Lesson (Instructor) - SHOULD PASS
```bash
curl -X DELETE http://localhost:8000/api/lessons/$LESSON_ID \
  -H "Authorization: Bearer $INSTRUCTOR_TOKEN"
```

#### ❌ Test 13: Delete Lesson (Student) - SHOULD FAIL (403)
```bash
curl -X DELETE http://localhost:8000/api/lessons/99999 \
  -H "Authorization: Bearer $STUDENT_TOKEN"
```

#### ❌ Test 14: Delete Lesson (No Auth) - SHOULD FAIL (403)
```bash
curl -X DELETE http://localhost:8000/api/lessons/99999
```

#### ❌ Test 15: Delete Invalid Lesson - SHOULD FAIL (404)
```bash
curl -X DELETE http://localhost:8000/api/lessons/99999 \
  -H "Authorization: Bearer $INSTRUCTOR_TOKEN"
```

### 🔍 Edge Cases

#### Test 16: Invalid JSON Payload - SHOULD FAIL (400/422)
```bash
curl -X POST http://localhost:8000/api/lessons/courses/$COURSE_ID \
  -H "Authorization: Bearer $INSTRUCTOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "invalid_field": "value"
  }'
```

#### Test 17: Missing Required Fields - SHOULD FAIL (422)
```bash
curl -X POST http://localhost:8000/api/lessons/courses/$COURSE_ID \
  -H "Authorization: Bearer $INSTRUCTOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Lesson without content_text"
  }'
```

## Expected Results Summary

| Test | Endpoint | Auth | Expected Status | Description |
|------|----------|------|-----------------|-------------|
| 1 | POST /api/lessons/courses/{id} | Instructor | 200 | Create lesson successfully |
| 2 | POST /api/lessons/courses/{id} | None | 403 | Unauthorized creation |
| 3 | POST /api/lessons/courses/{id} | Student | 403 | Student cannot create |
| 4 | POST /api/lessons/courses/99999 | Instructor | 404 | Invalid course ID |
| 5 | GET /api/lessons/{id} | Student (no enroll) | 403 | No enrollment |
| 6 | POST /api/enrollments/enroll/{id} | Student | 201 | Enroll in course |
| 7 | GET /api/lessons/{id} | Student (enrolled) | 200 | Get lessons with enrollment |
| 8 | PATCH /api/lessons/{id} | Instructor | 200 | Update lesson successfully |
| 9 | PATCH /api/lessons/{id} | Student | 403 | Student cannot update |
| 10 | PATCH /api/lessons/{id} | None | 403 | No auth for update |
| 11 | PATCH /api/lessons/99999 | Instructor | 404 | Invalid lesson ID |
| 12 | DELETE /api/lessons/{id} | Instructor | 200 | Delete lesson successfully |
| 13 | DELETE /api/lessons/99999 | Student | 403 | Student cannot delete |
| 14 | DELETE /api/lessons/99999 | None | 403 | No auth for delete |
| 15 | DELETE /api/lessons/99999 | Instructor | 404 | Invalid lesson ID |
| 16 | POST /api/lessons/courses/{id} | Instructor | 400/422 | Invalid JSON |
| 17 | POST /api/lessons/courses/{id} | Instructor | 422 | Missing required fields |

## Running All Tests

You can run all tests in sequence by copying the commands above. For automated testing, use the Python script:

```bash
python3 test_lessons_api_manual.py
