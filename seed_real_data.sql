-- =============================================================================
-- SKILLSPROUT REAL DATA SEED - CATEGORIES + 5 INSTRUCTORS + 5 COURSES + 25 LESSONS
-- =============================================================================

-- =============================================================================
-- 1. CREATE 6 COURSE CATEGORIES
-- =============================================================================

INSERT INTO categories (name, description, icon_url, color) VALUES 
    ('Programming', 'Learn programming languages and software development', 'https://cdn-icons-png.flaticon.com/512/2721/2721282.png', '#FF6B6B'),
    ('Web Development', 'Frontend and backend web development technologies', 'https://cdn-icons-png.flaticon.com/512/888/888859.png', '#4ECDC4'),
    ('Data Science', 'Data analysis, machine learning, and artificial intelligence', 'https://cdn-icons-png.flaticon.com/512/2806/2806141.png', '#45B7D1'),
    ('Mobile Development', 'iOS, Android, and cross-platform mobile app development', 'https://cdn-icons-png.flaticon.com/512/888/888847.png', '#96CEB4'),
    ('DevOps', 'Infrastructure, deployment, and system administration', 'https://cdn-icons-png.flaticon.com/512/2335/2335719.png', '#FFEAA7'),
    ('Business', 'Business skills, management, and entrepreneurship', 'https://cdn-icons-png.flaticon.com/512/3209/3209028.png', '#DDA0DD')
ON CONFLICT (name) DO NOTHING;

-- =============================================================================
-- 2. CREATE 5 REAL INSTRUCTORS
-- =============================================================================

INSERT INTO users (username, email, first_name, last_name, password_hash, role, bio, created_at) 
VALUES 
    ('bro_code', 'brocode@skillsprout.com', 'Bro', 'Code', '$2b$12$fakehash1234567890abcdef', 'instructor', 
     'Java & Python instructor with 1M+ YouTube subscribers. Teaching programming since 2018.', NOW()),
     
    ('dave_gray', 'davegray@skillsprout.com', 'Dave', 'Gray', '$2b$12$fakehash1234567890abcdef', 'instructor', 
     'Full-stack developer teaching Python, JavaScript, React. 500K+ students worldwide.', NOW()),
     
    ('free_code_camp', 'beaucarnes@skillsprout.com', 'Beau', 'Carnes', '$2b$12$fakehash1234567890abcdef', 'instructor', 
     'freeCodeCamp.org curriculum lead. Python & web development expert.', NOW()),
     
    ('jovian_aakash', 'aakash@skillsprout.com', 'Aakash', 'N S', '$2b$12$fakehash1234567890abcdef', 'instructor', 
     'Founder of Jovian.ai. Teaching web development & data science to 100K+ learners.', NOW()),
     
    ('simplilearn_data', 'simplilearn@skillsprout.com', 'Simplilearn', 'Team', '$2b$12$fakehash1234567890abcdef', 'instructor', 
     'Data analytics & business intelligence training experts. 2M+ professionals trained.', NOW())
ON CONFLICT (email) DO NOTHING;

-- =============================================================================
-- 3. COURSE 1: Java Tutorial (Bro Code) - Programming Category
-- =============================================================================
INSERT INTO courses (title, description, instructor_id, category_id, price, thumbnail_url, created_at, updated_at) 
SELECT 'Java Tutorial for Beginners', 
       'Complete Java programming course for absolute beginners by Bro Code. Learn Java from scratch with hands-on examples, covering variables, loops, methods, and object-oriented programming concepts.',
       u.id, c.id, 0.00, 'https://i.ytimg.com/vi/YZkyL-f-YXY/maxresdefault.jpg', NOW(), NOW()
FROM users u, categories c 
WHERE u.username = 'bro_code' AND c.name = 'Programming'
AND NOT EXISTS (SELECT 1 FROM courses WHERE title = 'Java Tutorial for Beginners');

-- Lessons for Java course
INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
SELECT c.id, 'Introduction to Java', 
       'Welcome to Java programming! In this lesson, you will learn about Java''s history, its key features, and why it''s one of the most popular programming languages worldwide. We''ll also set up your development environment.',
       'https://www.youtube.com/watch?v=YZkyL-f-YXY', 1, NOW(), NOW()
FROM courses c 
WHERE c.title = 'Java Tutorial for Beginners'
AND NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id AND l.title = 'Introduction to Java');

INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
SELECT c.id, 'Variables and Data Types', 
       'Learn about Java variables, primitive data types (int, double, boolean, char), and how to declare and initialize variables.',
       'https://www.youtube.com/watch?v=YZkyL-f-YXY&t=300s', 2, NOW(), NOW()
FROM courses c 
WHERE c.title = 'Java Tutorial for Beginners'
AND NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id AND l.title = 'Variables and Data Types');

INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
SELECT c.id, 'Operators and Expressions', 
       'Master arithmetic, logical, and comparison operators in Java. Learn how to combine variables and values to create expressions.',
       'https://www.youtube.com/watch?v=YZkyL-f-YXY&t=600s', 3, NOW(), NOW()
FROM courses c 
WHERE c.title = 'Java Tutorial for Beginners'
AND NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id AND l.title = 'Operators and Expressions');

INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
SELECT c.id, 'Control Flow - If Statements', 
       'Understand how to make decisions in your code using if, if-else, and if-else-if statements with practical examples.',
       'https://www.youtube.com/watch?v=YZkyL-f-YXY&t=900s', 4, NOW(), NOW()
FROM courses c 
WHERE c.title = 'Java Tutorial for Beginners'
AND NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id AND l.title = 'Control Flow - If Statements');

INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
SELECT c.id, 'Loops - For and While', 
       'Learn how to repeat code blocks using for loops, while loops, and do-while loops with real-world examples.',
       'https://www.youtube.com/watch?v=YZkyL-f-YXY&t=1200s', 5, NOW(), NOW()
FROM courses c 
WHERE c.title = 'Java Tutorial for Beginners'
AND NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id AND l.title = 'Loops - For and While');

-- =============================================================================
-- 4. COURSE 2: Python Full Course (Dave Gray) - Programming Category
-- =============================================================================
INSERT INTO courses (title, description, instructor_id, category_id, price, thumbnail_url, created_at, updated_at) 
SELECT 'Python Full Course for Beginners', 
       'Complete Python programming tutorial by Dave Gray. This 9-hour all-in-one course covers everything beginners need to know to start programming with Python, including installation, syntax, data structures, and web development basics.',
       u.id, c.id, 0.00, 'https://i.ytimg.com/vi/H2EJuAcrZYU/maxresdefault.jpg', NOW(), NOW()
FROM users u, categories c 
WHERE u.username = 'dave_gray' AND c.name = 'Programming'
AND NOT EXISTS (SELECT 1 FROM courses WHERE title = 'Python Full Course for Beginners');

INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
SELECT c.id, 'Python Installation & Setup', 
       'Learn how to install Python on different operating systems and set up your development environment with VS Code or your preferred editor.',
       'https://www.youtube.com/watch?v=H2EJuAcrZYU&t=120s', 1, NOW(), NOW()
FROM courses c 
WHERE c.title = 'Python Full Course for Beginners'
AND NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id AND l.title = 'Python Installation & Setup');

INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
SELECT c.id, 'Python Syntax and Variables', 
       'Understand Python''s simple syntax, variable naming conventions, and basic data types including strings, integers, and floats.',
       'https://www.youtube.com/watch?v=H2EJuAcrZYU&t=600s', 2, NOW(), NOW()
FROM courses c 
WHERE c.title = 'Python Full Course for Beginners'
AND NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id AND l.title = 'Python Syntax and Variables');

INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
SELECT c.id, 'Lists and Dictionaries', 
       'Master Python''s most important data structures - lists and dictionaries - and learn how to manipulate collections of data.',
       'https://www.youtube.com/watch?v=H2EJuAcrZYU&t=1200s', 3, NOW(), NOW()
FROM courses c 
WHERE c.title = 'Python Full Course for Beginners'
AND NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id AND l.title = 'Lists and Dictionaries');

INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
SELECT c.id, 'Functions and Modules', 
       'Learn how to write reusable code with functions, import modules, and organize your Python projects effectively.',
       'https://www.youtube.com/watch?v=H2EJuAcrZYU&t=1800s', 4, NOW(), NOW()
FROM courses c 
WHERE c.title = 'Python Full Course for Beginners'
AND NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id AND l.title = 'Functions and Modules');

-- =============================================================================
-- 5. COURSE 3: Full Stack Web Development (freeCodeCamp) - Web Development Category
-- =============================================================================
INSERT INTO courses (title, description, instructor_id, category_id, price, thumbnail_url, created_at, updated_at) 
SELECT 'Full Stack Web Development for Beginners', 
       'Complete full-stack course covering HTML, CSS, JavaScript, Node.js, MongoDB, and React by the freeCodeCamp team. Build real-world projects and learn modern web development practices.',
       u.id, c.id, 0.00, 'https://i.ytimg.com/vi/nu_pCVPKzTk/maxresdefault.jpg', NOW(), NOW()
FROM users u, categories c 
WHERE u.username = 'free_code_camp' AND c.name = 'Web Development'
AND NOT EXISTS (SELECT 1 FROM courses WHERE title = 'Full Stack Web Development for Beginners');

INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
SELECT c.id, 'HTML Fundamentals', 
       'Learn the building blocks of web pages with HTML. Understand semantic elements, forms, and accessibility best practices.',
       'https://www.youtube.com/watch?v=nu_pCVPKzTk&t=300s', 1, NOW(), NOW()
FROM courses c 
WHERE c.title = 'Full Stack Web Development for Beginners'
AND NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id AND l.title = 'HTML Fundamentals');

INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
SELECT c.id, 'CSS Styling and Layouts', 
       'Master CSS for styling web pages. Learn about flexbox, grid, responsive design, and modern CSS features.',
       'https://www.youtube.com/watch?v=nu_pCVPKzTk&t=900s', 2, NOW(), NOW()
FROM courses c 
WHERE c.title = 'Full Stack Web Development for Beginners'
AND NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id AND l.title = 'CSS Styling and Layouts');

INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
SELECT c.id, 'JavaScript Fundamentals', 
       'Learn JavaScript programming from the ground up. Variables, functions, DOM manipulation, and asynchronous programming.',
       'https://www.youtube.com/watch?v=nu_pCVPKzTk&t=1800s', 3, NOW(), NOW()
FROM courses c 
WHERE c.title = 'Full Stack Web Development for Beginners'
AND NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id AND l.title = 'JavaScript Fundamentals');

-- =============================================================================
-- 6. COURSE 4: HTML & CSS Course (Aakash N S) - Web Development Category
-- =============================================================================
INSERT INTO courses (title, description, instructor_id, category_id, price, thumbnail_url, created_at, updated_at) 
SELECT 'Web Development with HTML & CSS', 
       'Complete HTML & CSS course for beginners by Aakash N S from Jovian. Learn to create beautiful, responsive websites from scratch with hands-on projects and real-world examples.',
       u.id, c.id, 0.00, 'https://i.ytimg.com/vi/dX8396ZmSPk/maxresdefault.jpg', NOW(), NOW()
FROM users u, categories c 
WHERE u.username = 'jovian_aakash' AND c.name = 'Web Development'
AND NOT EXISTS (SELECT 1 FROM courses WHERE title = 'Web Development with HTML & CSS');

INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
SELECT c.id, 'Introduction to HTML', 
       'Get started with HTML basics. Learn about elements, tags, attributes, and how to structure web page content.',
       'https://www.youtube.com/watch?v=dX8396ZmSPk&t=180s', 1, NOW(), NOW()
FROM courses c 
WHERE c.title = 'Web Development with HTML & CSS'
AND NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id AND l.title = 'Introduction to HTML');

INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
SELECT c.id, 'CSS Selectors and Properties', 
       'Master CSS selectors, properties, and how to style HTML elements. Learn about colors, fonts, and basic layout properties.',
       'https://www.youtube.com/watch?v=dX8396ZmSPk&t=600s', 2, NOW(), NOW()
FROM courses c 
WHERE c.title = 'Web Development with HTML & CSS'
AND NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id AND l.title = 'CSS Selectors and Properties');

-- =============================================================================
-- 7. COURSE 5: Data Analytics Course (Simplilearn) - Data Science Category
-- =============================================================================
INSERT INTO courses (title, description, instructor_id, category_id, price, thumbnail_url, created_at, updated_at) 
SELECT 'Data Analytics Full Course 2025', 
       'Complete data analytics course for beginners covering Excel, SQL, Python, Power BI, and Tableau by Simplilearn. Learn to analyze data and make data-driven decisions.',
       u.id, c.id, 19.99, 'https://i.ytimg.com/vi/ZUdlc5LsmHA/maxresdefault.jpg', NOW(), NOW()
FROM users u, categories c 
WHERE u.username = 'simplilearn_data' AND c.name = 'Data Science'
AND NOT EXISTS (SELECT 1 FROM courses WHERE title = 'Data Analytics Full Course 2025');

INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
SELECT c.id, 'Introduction to Data Analytics', 
       'Understand what data analytics is, its importance in business, different types of analytics, and career opportunities in this field.',
       'https://www.youtube.com/watch?v=ZUdlc5LsmHA&t=120s', 1, NOW(), NOW()
FROM courses c 
WHERE c.title = 'Data Analytics Full Course 2025'
AND NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id AND l.title = 'Introduction to Data Analytics');

INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
SELECT c.id, 'Excel for Data Analysis', 
       'Learn Excel from scratch for data analysis. Master formulas, pivot tables, charts, and data visualization techniques.',
       'https://www.youtube.com/watch?v=ZUdlc5LsmHA&t=600s', 2, NOW(), NOW()
FROM courses c 
WHERE c.title = 'Data Analytics Full Course 2025'
AND NOT EXISTS (SELECT 1 FROM lessons l WHERE l.course_id = c.id AND l.title = 'Excel for Data Analysis');

-- =============================================================================
-- VERIFICATION - SEE YOUR REAL DATA!
-- =============================================================================
SELECT 
    '🏆 INSTRUCTORS' as section, COUNT(*) as count, '' as details
FROM users WHERE role = 'instructor'
UNION ALL
SELECT 
    '📚 COURSES', COUNT(*), ''
FROM courses 
UNION ALL
SELECT 
    '📖 LESSONS', COUNT(*), ''
FROM lessons
UNION ALL
SELECT 
    '🏷️ CATEGORIES', COUNT(*), ''
FROM categories;

-- Show seeded courses with lesson counts and categories
SELECT 
    c.title,
    cat.name as category,
    u.first_name || ' ' || u.last_name as instructor,
    c.price,
    COUNT(l.id) as lessons_count
FROM courses c
JOIN users u ON c.instructor_id = u.id
JOIN categories cat ON c.category_id = cat.id
LEFT JOIN lessons l ON c.id = l.course_id
GROUP BY c.id, c.title, cat.name, u.first_name, u.last_name, c.price
ORDER BY c.id;

--
