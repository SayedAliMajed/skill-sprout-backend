# Manual Lessons API Testing Guide

## Overview
This comprehensive guide provides everything you need to manually test the SkillSprout lessons API endpoints. The lessons API supports CRUD operations with proper authorization based on user roles and course enrollments.

## Database Status ✅
- **Database**: `skill_sprout_db`
- **Tables Verified**: users, courses, lessons, enrollments, reviews
- **Schema**: Properly aligned with application models
- **Key Fields Confirmed**: 
  - `lessons.content_text` (JSON field fix applied)
  - `users.first_name`, `users.last_name`, `users.password_hash`, `users.role`

## Lessons API Endpoints

| Method | Endpoint | Description | Auth Required | Expected Role |
|--------|----------|-------------|---------------|---------------|
| POST | `/api/lessons/courses/{course_id}` | Create lesson | ✅ Yes | instructor |
| GET | `/api/lessons/{course_id}` | Get lessons | ✅ Yes | student (enrolled) |
| PATCH | `/api/lessons/{lesson_id}` | Update lesson | ✅ Yes | instructor |
| DELETE | `/api/lessons/{lesson_id}` | Delete lesson | ✅ Yes | instructor |

## Authorization Rules

### Lesson Creation (Instructor Only)
- ✅ **Allow**: Course instructor can create lessons for their own courses
- ❌ **Deny**: Students cannot create lessons
- ❌ **Deny**: Unauthenticated requests
- ❌ **Deny**: Invalid course IDs

### Lesson Retrieval (Enrollment Required)
- ✅ **Allow**: Enrolled students can view lessons
- ❌ **Deny**: Unenrolled students (even with valid auth token)
- ❌ **Deny**: Unauthenticated requests

### Lesson Update/Delete (Instructor Only)
- ✅ **Allow**: Course instructor can update/delete their own lessons
- ❌ **Deny**: Students cannot modify lessons
- ❌ **Deny**: Unauthenticated requests
- ❌ **Deny**: Invalid lesson IDs

## Quick Start Testing

### Option 1: Automated Testing Script
```bash
cd /home/sayed/code/skill-sprout-backend
python3 test_lessons_api_manual.py
```

### Option 2: Manual CURL Commands
```bash
# See curl_commands_lessons.md for complete command set
cd /home/sayed/code/skill-sprout-backend
cat curl_commands_lessons.md
```

## Testing Workflow

### Phase 1: Setup (5 minutes)
1. **Start API Server** (if not running)
   ```bash
   cd /home/sayed/code/skill-sprout-backend
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Verify Database Connection**
   ```bash
   PGPASSWORD=skill_password psql -h localhost -U skill_user -d skill_sprout_db -c "\dt"
   ```

### Phase 2: Authentication (10 minutes)
1. **Create Test Users**
   - Register instructor user
   - Register student user
   - Login both users to get tokens

2. **Verify Tokens Work**
   - Test token validation
   - Confirm role-based access

### Phase 3: Course Setup (5 minutes)
1. **Create Test Course**
   - Use instructor token
   - Save course ID for testing

### Phase 4: Lessons CRUD Testing (15 minutes)
1. **Create Lessons**
   - Test instructor creation ✅
   - Test unauthorized access ❌
   - Test student attempt ❌

2. **Retrieve Lessons**
   - Test enrollment requirement ❌ (without enrollment)
   - Enroll student ✅
   - Test lesson retrieval ✅ (with enrollment)

3. **Update Lessons**
   - Test instructor update ✅
   - Test unauthorized update ❌

4. **Delete Lessons**
   - Test instructor deletion ✅
   - Test unauthorized deletion ❌

## Expected Test Results

### ✅ Should Pass (Successful Operations)
1. User registration and login
2. Course creation by instructor
3. Lesson creation by instructor
4. Student enrollment in course
5. Lesson retrieval by enrolled student
6. Lesson update by instructor
7. Lesson deletion by instructor

### ❌ Should Fail (Authorization/Database Errors)
1. Lesson creation without authentication (403)
2. Lesson creation by student (403)
3. Lesson retrieval without enrollment (403)
4. Lesson update by student (403)
5. Lesson deletion by student (403)
6. Invalid course ID (404)
7. Invalid lesson ID (404)
8. Invalid JSON payload (400/422)

## Troubleshooting Guide

### Issue: "Server not responding"
```bash
# Check if server is running
curl http://localhost:8000/

# If not running, start it
cd /home/sayed/code/skill-sprout-backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Issue: "Database connection failed"
```bash
# Check database connectivity
PGPASSWORD=skill_password psql -h localhost -U skill_user -d skill_sprout_db -c "SELECT 1;"

# Check database status
sudo systemctl status postgresql
```

### Issue: "Authentication failed"
```bash
# Test with simple login
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'
```

### Issue: "JWT token invalid"
- Check token expiration
- Verify token format (should start with proper JWT structure)
- Ensure correct Authorization header format: `Bearer {token}`

### Issue: "Permission denied"
- Verify user role in database
- Check course ownership for instructor operations
- Confirm enrollment exists for student operations

## Test Data Cleanup

### Automated Cleanup
The test script automatically cleans up test data after completion.

### Manual Cleanup
```bash
# Delete test users
curl -X DELETE http://localhost:8000/api/users/{user_id} \
  -H "Authorization: Bearer {token}"

# Or use database directly
PGPASSWORD=skill_password psql -h localhost -U skill_user -d skill_sprout_db -c \
  "DELETE FROM users WHERE email IN ('instructor@test.com', 'student@test.com');"
```

## Success Criteria

### Functional Requirements
- [ ] All CRUD operations work correctly
- [ ] Authorization rules enforced properly
- [ ] Error handling returns appropriate status codes
- [ ] Database operations are consistent
- [ ] JSON field mappings work correctly (`content_text`)

### Performance Requirements
- [ ] API responses under 2 seconds
- [ ] Database queries optimized
- [ ] No memory leaks during testing

### Security Requirements
- [ ] Authentication required for all endpoints
- [ ] Role-based access control working
- [ ] No privilege escalation possible
- [ ] Input validation prevents injection

## Files Created

| File | Purpose |
|------|---------|
| `test_lessons_api_manual.py` | Automated Python test script |
| `curl_commands_lessons.md` | Ready-to-use CURL commands |
| `manual_lessons_testing_plan.md` | Project planning document |
| `manual_lessons_testing_guide.md` | This comprehensive guide |

## Next Steps

After completing manual testing:

1. **Review Test Results**
   - Check `lessons_api_test_report.json`
   - Verify all expected behaviors
   - Document any issues found

2. **Performance Testing**
   - Load test with multiple concurrent requests
   - Monitor database performance
   - Check API response times

3. **Security Testing**
   - Test input validation thoroughly
   - Verify all authorization boundaries
   - Check for potential injection vulnerabilities

4. **Integration Testing**
   - Test lessons API with frontend
   - Verify complete user workflows
   - Test with real course data

## Support

If you encounter issues during testing:

1. Check the troubleshooting section above
2. Review the API server logs
3. Verify database schema matches application models
4. Ensure all prerequisites are met

The lessons API should now be fully tested and ready for production use!
