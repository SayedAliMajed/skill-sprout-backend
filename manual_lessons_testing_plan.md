# Manual Lessons API Testing Plan

## Objective
Create comprehensive manual testing tools for the SkillSprout lessons API endpoints.

## Current Status
- Database: `skill_sprout_db`
- Server: Running on localhost:8000
- Lessons API: Basic functionality working (50% success rate overall)

## Lessons API Endpoints
1. `POST /api/lessons/courses/{course_id}` - Create lesson (instructor only)
2. `GET /api/lessons/{course_id}` - Get lessons (requires enrollment)
3. `PATCH /api/lessons/{lesson_id}` - Update lesson (instructor only)
4. `DELETE /api/lessons/{lesson_id}` - Delete lesson (instructor only)

## Task Checklist

### Phase 1: Database Investigation
- [ ] Check current database schema for `skill_sprout_db`
- [ ] Verify table structure for users, courses, lessons, enrollments
- [ ] Identify any remaining schema issues

### Phase 2: Create Testing Tools
- [ ] Create focused lessons API test script
- [ ] Generate ready-to-use curl commands
- [ ] Create test data setup scripts

### Phase 3: Manual Testing Implementation
- [ ] Test lesson creation (instructor workflow)
- [ ] Test lesson retrieval (student workflow)
- [ ] Test lesson updates (authorization testing)
- [ ] Test lesson deletion (authorization testing)
- [ ] Test edge cases and error handling

### Phase 4: Documentation
- [ ] Create comprehensive testing guide
- [ ] Document all curl commands
- [ ] Provide troubleshooting steps

## Success Criteria
- All lessons CRUD operations working
- Authorization properly tested
- Clear manual testing procedures documented
- Ready-to-use testing tools provided
