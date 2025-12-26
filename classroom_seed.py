#!/usr/bin/env python3
"""
================================================================================
SKILLSPROUT CLASSROOM SEEDING SCRIPT
================================================================================

A comprehensive, classroom-friendly seeding script for SkillSprout Educational Platform.
This script populates the database with real educational content optimized for
Bahraini Dinar (BD) currency and YouTube thumbnail integration.

🎯 FEATURES:
- Real educational content from authentic instructors
- BD currency pricing with realistic course fees
- YouTube thumbnail integration for visual appeal
- Clear progress indicators and documentation
- Easy-to-use format for classmates

📋 PRICE STRATEGY (BD Currency):
- Programming Courses: 0.00 - 5.00 BD (affordable learning)
- Web Development: 0.00 - 7.50 BD (comprehensive coverage)
- Data Science: 5.00 - 12.00 BD (specialized skills)
- Mobile Development: 3.00 - 10.00 BD (growing market)
- DevOps: 8.00 - 15.00 BD (advanced topics)
- Business: 2.00 - 8.00 BD (practical skills)

🚀 QUICK START:
1. Ensure PostgreSQL is running
2. Run: python3 classroom_seed.py
3. Start backend: uvicorn main:app --reload
4. Test: curl http://127.0.0.1:8000/api/courses/

👥 FOR CLASSMATES:
- Copy this script to your project
- Run the same command
- All database content will be identical
- Easy collaboration and testing

================================================================================
"""

import sys
from sqlalchemy import text
from database import SessionLocal

def print_banner():
    """Display a nice banner for the seeding process"""
    print("🎓" + "="*78 + "🎓")
    print("    SKILLSPROUT CLASSROOM SEEDING - REAL EDUCATIONAL CONTENT")
    print("🎓" + "="*78 + "🎓")
    print()

def cleanup_test_data(db_session):
    """Clean up test data before seeding"""
    print("🧹 STEP 0: Cleaning up existing test data...")
    print("-" * 50)
    
    try:
        # Delete test courses
        db_session.execute(text("DELETE FROM courses WHERE title LIKE 'Test%' OR title LIKE 'Demo%'"))
        db_session.commit()
        print("✅ Deleted test courses")
        
        # Delete test lessons
        db_session.execute(text("DELETE FROM lessons WHERE title LIKE 'Test%' OR title LIKE 'Demo%'"))
        db_session.commit()
        print("✅ Deleted test lessons")
        
        # Delete test enrollments
        db_session.execute(text("DELETE FROM enrollments WHERE course_id IN (SELECT id FROM courses WHERE title LIKE 'Test%' OR title LIKE 'Demo%')"))
        db_session.commit()
        print("✅ Deleted test enrollments")
        
        # Delete test reviews
        db_session.execute(text("DELETE FROM reviews WHERE course_id IN (SELECT id FROM courses WHERE title LIKE 'Test%' OR title LIKE 'Demo%')"))
        db_session.commit()
        print("✅ Deleted test reviews")
        
        print("✅ Test data cleanup complete!\n")
        
    except Exception as e:
        print(f"❌ Error cleaning up test data: {e}")
        db_session.rollback()

def simple_seed_categories(db_session):
    """Seed course categories with descriptions and colors"""
    print("📂 STEP 1: Creating Course Categories...")
    print("-" * 50)
    
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
            print(f"✅ Added category: {name} ({description[:40]}...)")
        except Exception as e:
            print(f"❌ Failed to add {name}: {e}")
            db_session.rollback()
    
    print(f"✅ Categories setup complete!\n")

def simple_seed_instructors(db_session):
    """Seed real instructor profiles"""
    print("👨‍🏫 STEP 2: Adding Real Instructor Profiles...")
    print("-" * 50)
    
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
    
    print(f"✅ Instructor profiles setup complete!\n")

def simple_seed_courses(db_session):
    """Seed courses with YouTube thumbnails and BD currency pricing"""
    print("📚 STEP 3: Creating Courses with BD Currency Pricing...")
    print("-" * 50)
    
    try:
        # Get category IDs
        result = db_session.execute(text("SELECT id, name FROM categories"))
        categories = {row[1]: row[0] for row in result}
        
        # Get instructor IDs
        result = db_session.execute(text("SELECT id, username FROM users WHERE role = 'instructor'"))
        instructors = {row[1]: row[0] for row in result}
        
        # Courses with YouTube URLs and BD currency pricing
        courses = [
            ('Java Tutorial for Beginners', 
             'Complete Java programming course for absolute beginners by Bro Code. Learn Java from scratch with hands-on examples.',
             instructors.get('bro_code'), categories.get('Programming'), 3.50, 'https://www.youtube.com/watch?v=YZkyL-f-YXY'),
            ('Python Full Course for Beginners', 
             'Complete Python programming tutorial by Dave Gray. This 9-hour all-in-one course covers everything beginners need.',
             instructors.get('dave_gray'), categories.get('Programming'), 2.75, 'https://www.youtube.com/watch?v=H2EJuAcrZYU'),
            ('Full Stack Web Development for Beginners', 
             'Complete full-stack course covering HTML, CSS, JavaScript, Node.js, MongoDB, and React by the freeCodeCamp team.',
             instructors.get('free_code_camp'), categories.get('Web Development'), 6.25, 'https://www.youtube.com/watch?v=nu_pCVPKzTk'),
            ('Web Development with HTML & CSS', 
             'Complete HTML & CSS course for beginners by Aakash N S from Jovian. Learn to create beautiful, responsive websites.',
             instructors.get('jovian_aakash'), categories.get('Web Development'), 4.50, 'https://www.youtube.com/watch?v=dX8396ZmSPk'),
            ('Data Analytics Full Course 2025', 
             'Complete data analytics course for beginners covering Excel, SQL, Python, Power BI, and Tableau by Simplilearn.',
             instructors.get('simplilearn_data'), categories.get('Data Science'), 11.75, 'https://www.youtube.com/watch?v=ZUdlc5LsmHA'),
        ]
        
        print("💰 BD Currency Pricing Strategy:")
        print("   • Programming Courses: 2.75 - 3.50 BD (affordable entry-level)")
        print("   • Web Development: 4.50 - 6.25 BD (comprehensive coverage)")
        print("   • Data Science: 11.75 BD (specialized, high-value skills)")
        print()
        
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
                        "thumbnail_url": thumbnail_url
                    })
                    db_session.commit()
                    print(f"✅ Added course: {title} ({price:.2f} BD)")
                except Exception as e:
                    print(f"❌ Failed to add {title}: {e}")
                    db_session.rollback()
            else:
                print(f"⚠️  Skipping {title} (missing instructor_id or category_id)")
                
    except Exception as e:
        print(f"❌ Error seeding courses: {e}")
    
    print(f"✅ Courses setup complete with BD currency!\n")

def simple_seed_lessons(db_session):
    """Seed comprehensive lessons with YouTube video content"""
    print("📖 STEP 4: Adding YouTube Video Lessons...")
    print("-" * 50)
    
    try:
        # Get course IDs and titles
        result = db_session.execute(text("SELECT id, title FROM courses"))
        courses = {row[1]: row[0] for row in result}
        
        lessons_data = [
            # Java Tutorial lessons (Bro Code)
            (courses.get('Java Tutorial for Beginners'), 'Introduction to Java', 'Welcome to Java programming! Learn about Java history, key features, and setup.', 'https://www.youtube.com/watch?v=YZkyL-f-YXY', 1),
            (courses.get('Java Tutorial for Beginners'), 'Variables and Data Types', 'Learn about Java variables, primitive data types, and practical examples.', 'https://www.youtube.com/watch?v=YZkyL-f-YXY&t=300s', 2),
            (courses.get('Java Tutorial for Beginners'), 'Operators and Expressions', 'Master arithmetic, logical, and comparison operators in Java.', 'https://www.youtube.com/watch?v=YZkyL-f-YXY&t=600s', 3),
            (courses.get('Java Tutorial for Beginners'), 'Control Flow - If Statements', 'Understand decision-making in code using if, if-else statements.', 'https://www.youtube.com/watch?v=YZkyL-f-YXY&t=900s', 4),
            (courses.get('Java Tutorial for Beginners'), 'Loops - For and While', 'Learn to repeat code blocks using various loop types.', 'https://www.youtube.com/watch?v=YZkyL-f-YXY&t=1200s', 5),
            
            # Python Course lessons (Dave Gray)
            (courses.get('Python Full Course for Beginners'), 'Python Installation & Setup', 'Learn how to install Python and set up development environment.', 'https://www.youtube.com/watch?v=H2EJuAcrZYU&t=120s', 1),
            (courses.get('Python Full Course for Beginners'), 'Python Syntax and Variables', 'Understand Python syntax, naming conventions, and data types.', 'https://www.youtube.com/watch?v=H2EJuAcrZYU&t=600s', 2),
            (courses.get('Python Full Course for Beginners'), 'Lists and Dictionaries', 'Master Python most important data structures.', 'https://www.youtube.com/watch?v=H2EJuAcrZYU&t=1200s', 3),
            (courses.get('Python Full Course for Beginners'), 'Functions and Modules', 'Learn to write reusable code with functions and modules.', 'https://www.youtube.com/watch?v=H2EJuAcrZYU&t=1800s', 4),
            
            # Web Development lessons (freeCodeCamp)
            (courses.get('Full Stack Web Development for Beginners'), 'HTML Fundamentals', 'Learn the building blocks of web pages with HTML.', 'https://www.youtube.com/watch?v=nu_pCVPKzTk&t=300s', 1),
            (courses.get('Full Stack Web Development for Beginners'), 'CSS Styling and Layouts', 'Master CSS for styling web pages and layouts.', 'https://www.youtube.com/watch?v=nu_pCVPKzTk&t=900s', 2),
            (courses.get('Full Stack Web Development for Beginners'), 'JavaScript Fundamentals', 'Learn JavaScript programming from the ground up.', 'https://www.youtube.com/watch?v=nu_pCVPKzTk&t=1800s', 3),
            
            # HTML & CSS lessons (Aakash N S)
            (courses.get('Web Development with HTML & CSS'), 'Introduction to HTML', 'Get started with HTML basics and structure.', 'https://www.youtube.com/watch?v=dX8396ZmSPk&t=180s', 1),
            (courses.get('Web Development with HTML & CSS'), 'CSS Selectors and Properties', 'Master CSS selectors and styling properties.', 'https://www.youtube.com/watch?v=dX8396ZmSPk&t=600s', 2),
            (courses.get('Web Development with HTML & CSS'), 'Flexbox and Grid Layout', 'Learn modern CSS layout techniques.', 'https://www.youtube.com/watch?v=dX8396ZmSPk&t=1800s', 3),
            
            # Data Analytics lessons (Simplilearn)
            (courses.get('Data Analytics Full Course 2025'), 'Introduction to Data Analytics', 'Understand data analytics importance and career opportunities.', 'https://www.youtube.com/watch?v=ZUdlc5LsmHA&t=120s', 1),
            (courses.get('Data Analytics Full Course 2025'), 'Excel for Data Analysis', 'Learn Excel for data analysis and visualization.', 'https://www.youtube.com/watch?v=ZUdlc5LsmHA&t=600s', 2),
            (courses.get('Data Analytics Full Course 2025'), 'SQL for Data Analysis', 'Master SQL queries for data extraction and analysis.', 'https://www.youtube.com/watch?v=ZUdlc5LsmHA&t=1800s', 3),
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
    
    print(f"✅ Lessons setup complete with YouTube videos!\n")

def verify_seeding(db_session):
    """Verify the seeding was successful"""
    print("🔍 STEP 5: Verifying Seeding Results...")
    print("-" * 50)
    
    try:
        # Check categories
        categories_count = db_session.execute(text("SELECT COUNT(*) FROM categories")).scalar()
        print(f"📂 Categories: {categories_count}")
        
        # Check instructors
        instructors_count = db_session.execute(text("SELECT COUNT(*) FROM users WHERE role = 'instructor'")).scalar()
        print(f"👨‍🏫 Instructors: {instructors_count}")
        
        # Check courses
        courses_count = db_session.execute(text("SELECT COUNT(*) FROM courses")).scalar()
        print(f"📚 Courses: {courses_count}")
        
        # Check lessons
        lessons_count = db_session.execute(text("SELECT COUNT(*) FROM lessons")).scalar()
        print(f"📖 Lessons: {lessons_count}")
        
        # Check YouTube URLs
        youtube_courses = db_session.execute(text("""
            SELECT COUNT(*) FROM courses 
            WHERE thumbnail_url LIKE '%youtube%' OR thumbnail_url LIKE '%youtu.be%'
        """)).scalar()
        print(f"🎥 Courses with YouTube URLs: {youtube_courses}")
        
        print(f"\n✅ Seeding verification complete!")
        print(f"🎯 System ready with {courses_count} courses, {lessons_count} lessons!")
        
    except Exception as e:
        print(f"❌ Error verifying seeding: {e}")

def main():
    """Main function to run the complete seeding process"""
    print_banner()
    
    # Initialize database connection
    db = SessionLocal()
    
    try:
        # Run all seeding steps in order
        cleanup_test_data(db)
        simple_seed_categories(db)
        simple_seed_instructors(db)
        simple_seed_courses(db)
        simple_seed_lessons(db)
        verify_seeding(db)
        
        print("\n🎉 CLASSROOM SEEDING COMPLETED SUCCESSFULLY!")
        print("📚 Your SkillSprout database is now populated with real educational content")
        print("💰 All courses use BD currency formatting")
        print("🎥 YouTube thumbnails are ready for automatic display")
        print("👥 Perfect for classroom collaboration and testing!")
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        print("Please check your database connection and try again.")
        
    finally:
        db.close()
        print("\n👋 Database connection closed. Happy coding!")

if __name__ == "__main__":
    main()
