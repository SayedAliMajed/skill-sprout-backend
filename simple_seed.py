#!/usr/bin/env python3
"""
Enhanced YouTube-Thumbnail Compatible Seeding Script
Optimized for the new YouTube Thumbnail Feature
"""

import sys
from sqlalchemy import text
from database import SessionLocal

def simple_seed_categories(db_session):
    """Seed categories using direct SQL with timestamps"""
    print("🌱 Seeding categories...")
    
    categories = [
        ('Programming', 'Learn programming languages and software development', '#FF6B6B'),
        ('Web Development', 'Frontend and backend web development technologies', '#4ECDC4'),
        ('Data Science', 'Data analysis, machine learning, and artificial intelligence', '#45B7D1'),
        ('Mobile Development', 'iOS, Android, and cross-platform mobile app development', '#96CEB4'),
        ('DevOps', 'Infrastructure, deployment, and system administration', '#FFEAA7'),
        ('Business', 'Business skills, management, and entrepreneurship', '#DDA0DD')
    ]
    
    for name, description, color in categories:
        try:
            db_session.execute(text("""
                INSERT INTO categories (name, description, color, created_at, updated_at) 
                VALUES (:name, :description, :color, NOW(), NOW())
                ON CONFLICT (name) DO NOTHING
            """), {"name": name, "description": description, "color": color})
            db_session.commit()
            print(f"✅ Added category: {name}")
        except Exception as e:
            print(f"❌ Failed to add {name}: {e}")
            db_session.rollback()

def simple_seed_instructors(db_session):
    """Seed instructors using direct SQL"""
    print("👥 Seeding instructors...")
    
    instructors = [
        ('bro_code', 'brocode@skillsprout.com', 'Bro', 'Code', 'Java & Python instructor with 1M+ YouTube subscribers. Teaching programming since 2018.'),
        ('dave_gray', 'davegray@skillsprout.com', 'Dave', 'Gray', 'Full-stack developer teaching Python, JavaScript, React. 500K+ students worldwide.'),
        ('free_code_camp', 'beaucarnes@skillsprout.com', 'Beau', 'Carnes', 'freeCodeCamp.org curriculum lead. Python & web development expert.'),
        ('jovian_aakash', 'aakash@skillsprout.com', 'Aakash', 'N S', 'Founder of Jovian.ai. Teaching web development & data science to 100K+ learners.'),
        ('simplilearn_data', 'simplilearn@skillsprout.com', 'Simplilearn', 'Team', 'Data analytics & business intelligence training experts. 2M+ professionals trained.')
    ]
    
    for username, email, first_name, last_name, bio in instructors:
        try:
            db_session.execute(text("""
                INSERT INTO users (username, email, first_name, last_name, password_hash, role, bio, created_at) 
                VALUES (:username, :email, :first_name, :last_name, '$2b$12$fakehash1234567890abcdef', 'instructor', :bio, NOW())
                ON CONFLICT (email) DO NOTHING
            """), {
                "username": username, 
                "email": email, 
                "first_name": first_name, 
                "last_name": last_name, 
                "bio": bio
            })
            db_session.commit()
            print(f"✅ Added instructor: {first_name} {last_name}")
        except Exception as e:
            print(f"❌ Failed to add {username}: {e}")
            db_session.rollback()

def simple_seed_courses(db_session):
    """Seed courses with YouTube-optimized thumbnails"""
    print("📚 Seeding courses with YouTube thumbnails...")
    
    try:
        # Get category IDs
        result = db_session.execute(text("SELECT id, name FROM categories"))
        categories = {row[1]: row[0] for row in result}
        print(f"📊 Found categories: {list(categories.keys())}")
        
        # Get instructor IDs
        result = db_session.execute(text("SELECT id, username FROM users WHERE role = 'instructor'"))
        instructors = {row[1]: row[0] for row in result}
        print(f"📊 Found instructors: {list(instructors.keys())}")
        
        # Courses with YouTube video URLs as thumbnails for better visual appeal
        courses = [
            ('Java Tutorial for Beginners', 'Complete Java programming course for absolute beginners by Bro Code. Learn Java from scratch with hands-on examples, covering variables, loops, methods, and object-oriented programming concepts.', instructors.get('bro_code'), categories.get('Programming'), 0.00, 'https://www.youtube.com/watch?v=YZkyL-f-YXY'),
            ('Python Full Course for Beginners', 'Complete Python programming tutorial by Dave Gray. This 9-hour all-in-one course covers everything beginners need to know to start programming with Python, including installation, syntax, data structures, and web development basics.', instructors.get('dave_gray'), categories.get('Programming'), 0.00, 'https://www.youtube.com/watch?v=H2EJuAcrZYU'),
            ('Full Stack Web Development for Beginners', 'Complete full-stack course covering HTML, CSS, JavaScript, Node.js, MongoDB, and React by the freeCodeCamp team. Build real-world projects and learn modern web development practices.', instructors.get('free_code_camp'), categories.get('Web Development'), 0.00, 'https://www.youtube.com/watch?v=nu_pCVPKzTk'),
            ('Web Development with HTML & CSS', 'Complete HTML & CSS course for beginners by Aakash N S from Jovian. Learn to create beautiful, responsive websites from scratch with hands-on projects and real-world examples.', instructors.get('jovian_aakash'), categories.get('Web Development'), 0.00, 'https://www.youtube.com/watch?v=dX8396ZmSPk'),
            ('Data Analytics Full Course 2025', 'Complete data analytics course for beginners covering Excel, SQL, Python, Power BI, and Tableau by Simplilearn. Learn to analyze data and make data-driven decisions.', instructors.get('simplilearn_data'), categories.get('Data Science'), 7.50, 'https://www.youtube.com/watch?v=ZUdlc5LsmHA')
        ]
        
        for title, description, instructor_id, category_id, price, thumbnail_url in courses:
            if instructor_id and category_id:
                try:
                    # Check if course already exists
                    existing = db_session.execute(text("SELECT id FROM courses WHERE title = :title"), {"title": title}).fetchone()
                    if existing:
                        print(f"⚠️  Course already exists: {title}")
                        continue
                        
                    db_session.execute(text("""
                        INSERT INTO courses (title, description, instructor_id, category_id, price, thumbnail_url, created_at, updated_at) 
                        VALUES (:title, :description, :instructor_id, :category_id, :price, :thumbnail_url, NOW(), NOW())
                    """), {
                        "title": title,
                        "description": description,
                        "instructor_id": instructor_id,
                        "category_id": category_id,
                        "price": price,
                        "thumbnail_url": thumbnail_url  # Using actual YouTube URLs for thumbnails
                    })
                    db_session.commit()
                    print(f"✅ Added course: {title}")
                except Exception as e:
                    print(f"❌ Failed to add {title}: {e}")
                    db_session.rollback()
            else:
                print(f"⚠️  Skipping {title} (missing instructor_id or category_id)")
                
    except Exception as e:
        print(f"❌ Error seeding courses: {e}")

def simple_seed_lessons(db_session):
    """Seed comprehensive lessons with diverse YouTube content"""
    print("📖 Seeding lessons with expanded YouTube content...")
    
    try:
        # Get course IDs and titles
        result = db_session.execute(text("SELECT id, title FROM courses"))
        courses = {row[1]: row[0] for row in result}
        print(f"📊 Found courses: {list(courses.keys())}")
        
        lessons_data = [
            # Java Tutorial lessons (Bro Code)
            (courses.get('Java Tutorial for Beginners'), 'Introduction to Java', 'Welcome to Java programming! In this lesson, you will learn about Java''s history, its key features, and why it''s one of the most popular programming languages worldwide. We''ll also set up your development environment.', 'https://www.youtube.com/watch?v=YZkyL-f-YXY', 1),
            (courses.get('Java Tutorial for Beginners'), 'Variables and Data Types', 'Learn about Java variables, primitive data types (int, double, boolean, char), and how to declare and initialize variables with practical examples.', 'https://www.youtube.com/watch?v=YZkyL-f-YXY&t=300s', 2),
            (courses.get('Java Tutorial for Beginners'), 'Operators and Expressions', 'Master arithmetic, logical, and comparison operators in Java. Learn how to combine variables and values to create meaningful expressions.', 'https://www.youtube.com/watch?v=YZkyL-f-YXY&t=600s', 3),
            (courses.get('Java Tutorial for Beginners'), 'Control Flow - If Statements', 'Understand how to make decisions in your code using if, if-else, and if-else-if statements with practical programming examples.', 'https://www.youtube.com/watch?v=YZkyL-f-YXY&t=900s', 4),
            (courses.get('Java Tutorial for Beginners'), 'Loops - For and While', 'Learn how to repeat code blocks using for loops, while loops, and do-while loops with real-world programming examples.', 'https://www.youtube.com/watch?v=YZkyL-f-YXY&t=1200s', 5),
            (courses.get('Java Tutorial for Beginners'), 'Methods and Functions', 'Discover how to create reusable code blocks using methods and functions in Java programming.', 'https://www.youtube.com/watch?v=YZkyL-f-YXY&t=1500s', 6),
            
            # Python Course lessons (Dave Gray)
            (courses.get('Python Full Course for Beginners'), 'Python Installation & Setup', 'Learn how to install Python on different operating systems and set up your development environment with VS Code or your preferred editor.', 'https://www.youtube.com/watch?v=H2EJuAcrZYU&t=120s', 1),
            (courses.get('Python Full Course for Beginners'), 'Python Syntax and Variables', 'Understand Python''s simple syntax, variable naming conventions, and basic data types including strings, integers, and floats.', 'https://www.youtube.com/watch?v=H2EJuAcrZYU&t=600s', 2),
            (courses.get('Python Full Course for Beginners'), 'Lists and Dictionaries', 'Master Python''s most important data structures - lists and dictionaries - and learn how to manipulate collections of data effectively.', 'https://www.youtube.com/watch?v=H2EJuAcrZYU&t=1200s', 3),
            (courses.get('Python Full Course for Beginners'), 'Functions and Modules', 'Learn how to write reusable code with functions, import modules, and organize your Python projects effectively.', 'https://www.youtube.com/watch?v=H2EJuAcrZYU&t=1800s', 4),
            (courses.get('Python Full Course for Beginners'), 'File Handling in Python', 'Discover how to read from and write to files in Python, and manage data persistence in your applications.', 'https://www.youtube.com/watch?v=H2EJuAcrZYU&t=2400s', 5),
            (courses.get('Python Full Course for Beginners'), 'Error Handling and Debugging', 'Learn about try-except blocks, common Python errors, and debugging techniques to write robust code.', 'https://www.youtube.com/watch?v=H2EJuAcrZYU&t=3000s', 6),
            
            # Web Development lessons (freeCodeCamp)
            (courses.get('Full Stack Web Development for Beginners'), 'HTML Fundamentals', 'Learn the building blocks of web pages with HTML. Understand semantic elements, forms, and accessibility best practices.', 'https://www.youtube.com/watch?v=nu_pCVPKzTk&t=300s', 1),
            (courses.get('Full Stack Web Development for Beginners'), 'CSS Styling and Layouts', 'Master CSS for styling web pages. Learn about flexbox, grid, responsive design, and modern CSS features.', 'https://www.youtube.com/watch?v=nu_pCVPKzTk&t=900s', 2),
            (courses.get('Full Stack Web Development for Beginners'), 'JavaScript Fundamentals', 'Learn JavaScript programming from the ground up. Variables, functions, DOM manipulation, and asynchronous programming.', 'https://www.youtube.com/watch?v=nu_pCVPKzTk&t=1800s', 3),
            (courses.get('Full Stack Web Development for Beginners'), 'Node.js and Express Basics', 'Introduction to server-side JavaScript with Node.js and Express framework for building web APIs.', 'https://www.youtube.com/watch?v=nu_pCVPKzTk&t=3600s', 4),
            (courses.get('Full Stack Web Development for Beginners'), 'Database Integration with MongoDB', 'Learn how to integrate MongoDB database with your Node.js applications for data persistence.', 'https://www.youtube.com/watch?v=nu_pCVPKzTk&t=5400s', 5),
            (courses.get('Full Stack Web Development for Beginners'), 'Building Your First Full-Stack App', 'Put everything together to build a complete full-stack web application from scratch.', 'https://www.youtube.com/watch?v=nu_pCVPKzTk&t=7200s', 6),
            
            # HTML & CSS lessons (Aakash N S)
            (courses.get('Web Development with HTML & CSS'), 'Introduction to HTML', 'Get started with HTML basics. Learn about elements, tags, attributes, and how to structure web page content effectively.', 'https://www.youtube.com/watch?v=dX8396ZmSPk&t=180s', 1),
            (courses.get('Web Development with HTML & CSS'), 'CSS Selectors and Properties', 'Master CSS selectors, properties, and how to style HTML elements. Learn about colors, fonts, and basic layout properties.', 'https://www.youtube.com/watch?v=dX8396ZmSPk&t=600s', 2),
            (courses.get('Web Development with HTML & CSS'), 'Box Model and Layout', 'Understand the CSS box model, margins, padding, borders, and how to create structured layouts.', 'https://www.youtube.com/watch?v=dX8396ZmSPk&t=1200s', 3),
            (courses.get('Web Development with HTML & CSS'), 'Flexbox and Grid Layout', 'Learn modern CSS layout techniques using Flexbox and CSS Grid for responsive web design.', 'https://www.youtube.com/watch?v=dX8396ZmSPk&t=1800s', 4),
            (courses.get('Web Development with HTML & CSS'), 'Responsive Design Principles', 'Master mobile-first responsive design techniques to make websites work on all devices.', 'https://www.youtube.com/watch?v=dX8396ZmSPk&t=2400s', 5),
            (courses.get('Web Development with HTML & CSS'), 'Building a Complete Website', 'Create a complete website project using HTML and CSS with modern best practices.', 'https://www.youtube.com/watch?v=dX8396ZmSPk&t=3000s', 6),
            
            # Data Analytics lessons (Simplilearn)
            (courses.get('Data Analytics Full Course 2025'), 'Introduction to Data Analytics', 'Understand what data analytics is, its importance in business, different types of analytics, and career opportunities in this field.', 'https://www.youtube.com/watch?v=ZUdlc5LsmHA&t=120s', 1),
            (courses.get('Data Analytics Full Course 2025'), 'Excel for Data Analysis', 'Learn Excel from scratch for data analysis. Master formulas, pivot tables, charts, and data visualization techniques.', 'https://www.youtube.com/watch?v=ZUdlc5LsmHA&t=600s', 2),
            (courses.get('Data Analytics Full Course 2025'), 'SQL for Data Analysis', 'Master SQL queries for data extraction, filtering, aggregation, and analysis from databases.', 'https://www.youtube.com/watch?v=ZUdlc5LsmHA&t=1800s', 3),
            (courses.get('Data Analytics Full Course 2025'), 'Python for Data Analytics', 'Learn Python programming specifically for data analysis using pandas, numpy, and matplotlib libraries.', 'https://www.youtube.com/watch?v=ZUdlc5LsmHA&t=3600s', 4),
            (courses.get('Data Analytics Full Course 2025'), 'Power BI for Business Intelligence', 'Create interactive dashboards and reports using Microsoft Power BI for business decision making.', 'https://www.youtube.com/watch?v=ZUdlc5LsmHA&t=5400s', 5),
            (courses.get('Data Analytics Full Course 2025'), 'Tableau for Data Visualization', 'Master Tableau for creating compelling data visualizations and interactive dashboards.', 'https://www.youtube.com/watch?v=ZUdlc5LsmHA&t=7200s', 6),
        ]
        
        for course_id, title, content_text, video_url, order_index in lessons_data:
            if course_id:
                try:
                    db_session.execute(text("""
                        INSERT INTO lessons (course_id, title, content_text, video_url, order_index, created_at, updated_at) 
                        VALUES (:course_id, :title, :content_text, :video_url, :order_index, NOW(), NOW())
                    """), {
                        "course_id": course_id,
                        "title": title,
                        "content_text": content_text,
                        "video_url": video_url,
                        "order_index": order_index
                    })
                    db_session.commit()
                    print(f"✅ Added lesson: {title}")
                except Exception as e:
                    print(f"❌ Failed to add lesson {title}: {e}")
                    db_session.rollback()
            else:
                print(f"⚠️  Skipping lesson {title} (course not found)")
                
    except Exception as e:
        print(f"❌ Error seeding lessons: {e}")

def cleanup_test_data(db_session):
    """Clean up test data before
