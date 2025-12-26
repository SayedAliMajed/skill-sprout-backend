-- =============================================================================
-- MANUAL DATABASE MIGRATION SCRIPT
-- Run these commands manually in your PostgreSQL database
-- =============================================================================

-- Step 1: Categories table was already created ✅

-- Step 2: Add category_id column to courses table (run this manually)
-- You need to run this command as a database owner/superuser:

ALTER TABLE courses 
ADD COLUMN category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL;

-- Step 3: Alternative approach if ALTER TABLE doesn't work:
-- Create a new courses table with category_id

CREATE TABLE courses_new AS 
SELECT 
    id,
    instructor_id,
    title,
    description,
    price,
    thumbnail_url,
    created_at,
    updated_at,
    NULL::INTEGER as category_id
FROM courses;

-- Drop old table and rename new one
DROP TABLE courses CASCADE;
ALTER TABLE courses_new RENAME TO courses;

-- Recreate indexes and constraints
ALTER TABLE courses ADD PRIMARY KEY (id);
ALTER TABLE courses ADD CONSTRAINT fk_courses_instructor 
    FOREIGN KEY (instructor_id) REFERENCES users(id) ON DELETE CASCADE;
ALTER TABLE courses ADD CONSTRAINT fk_courses_category 
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL;

-- Step 4: Recreate other tables if needed
-- This will recreate lessons, enrollments, reviews tables

CREATE TABLE lessons_new AS 
SELECT 
    id,
    course_id,
    title,
    content_text,
    video_url,
    order_index,
    created_at,
    updated_at
FROM lessons;

DROP TABLE lessons CASCADE;
ALTER TABLE lessons_new RENAME TO lessons;

CREATE TABLE enrollments_new AS 
SELECT 
    id,
    user_id,
    course_id,
    enrolled_at,
    completed_at
FROM enrollments;

DROP TABLE enrollments CASCADE;
ALTER TABLE lessons_new RENAME TO enrollments;

-- Verification queries
SELECT 'Courses structure' as check_type, COUNT(*) as count FROM courses;
SELECT 'Categories table' as check_type, COUNT(*) as count FROM categories;
SELECT 'Lessons table' as check_type, COUNT(*) as count FROM lessons;
