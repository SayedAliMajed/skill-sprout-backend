-- =============================================================================
-- CLEANUP TEST DATA SCRIPT
-- Removes all test data before seeding with real data
-- =============================================================================

-- =============================================================================
-- WARNING: This will permanently delete all test data!
-- =============================================================================

-- Delete test lessons first (due to foreign key constraints)
DELETE FROM lessons WHERE course_id IN (
    SELECT id FROM courses WHERE title LIKE 'Test%' OR title LIKE 'Demo%'
);

-- Delete test enrollments
DELETE FROM enrollments WHERE course_id IN (
    SELECT id FROM courses WHERE title LIKE 'Test%' OR title LIKE 'Demo%'
);

-- Delete test reviews
DELETE FROM reviews WHERE course_id IN (
    SELECT id FROM courses WHERE title LIKE 'Test%' OR title LIKE 'Demo%'
);

-- Delete test courses
DELETE FROM courses WHERE title LIKE 'Test%' OR title LIKE 'Demo%';

-- Delete test users (keep the main users: hussain, hassan, bro_code, etc.)
DELETE FROM users WHERE username NOT IN ('hussain', 'hassan', 'bro_code', 'dave_gray', 'free_code_camp', 'jovian_aakash', 'simplilearn_data');

-- Reset sequences to start from a clean state
-- Note: Adjust sequence names based on your actual database schema

-- Reset courses sequence (if using auto-increment)
-- ALTER SEQUENCE courses_id_seq RESTART WITH 1;

-- Reset users sequence (if using auto-increment)  
-- ALTER SEQUENCE users_id_seq RESTART WITH 1;

-- Reset lessons sequence (if using auto-increment)
-- ALTER SEQUENCE lessons_id_seq RESTART WITH 1;

-- Reset enrollments sequence (if using auto-increment)
-- ALTER SEQUENCE enrollments_id_seq RESTART WITH 1;

-- Reset reviews sequence (if using auto-increment)
-- ALTER SEQUENCE reviews_id_seq RESTART WITH 1;

-- Verification - Check remaining data
SELECT 
    '👥 USERS' as section, COUNT(*) as count
FROM users
UNION ALL
SELECT 
    '📚 COURSES', COUNT(*)
FROM courses
UNION ALL
SELECT 
    '📖 LESSONS', COUNT(*)
FROM lessons
UNION ALL
SELECT 
    '🎯 ENROLLMENTS', COUNT(*)
FROM enrollments
UNION ALL
SELECT 
    '⭐ REVIEWS', COUNT(*)
FROM reviews;

-- Show remaining users
SELECT 
    id,
    username,
    email,
    first_name,
    last_name,
    role
FROM users
ORDER BY id;
