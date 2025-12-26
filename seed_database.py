#!/usr/bin/env python3
"""
Database Seeding Script
Automatically seeds the database with real educational content
"""

import os
import sys
from pathlib import Path
from sqlalchemy import text
from database import SessionLocal

def read_sql_file(filename):
    """Read and return SQL file content"""
    filepath = Path(__file__).parent / filename
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: {filename} not found!")
        return None

def execute_sql_statements(db_session, sql_content):
    """Execute SQL statements with proper error handling"""
    try:
        # Split by semicolon and execute each statement
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
        
        for statement in statements:
            if statement:
                try:
                    db_session.execute(text(statement))
                    db_session.commit()
                except Exception as e:
                    print(f"⚠️  Warning executing statement: {e}")
                    db_session.rollback()
                    
        return True
    except Exception as e:
        print(f"❌ Error executing SQL: {e}")
        return False

def verify_seeding(db_session):
    """Verify that seeding was successful"""
    try:
        # Check categories
        categories_count = db_session.execute(text("SELECT COUNT(*) FROM categories")).scalar()
        print(f"🏷️  Categories: {categories_count}")
        
        # Check users (instructors)
        instructors_count = db_session.execute(text("SELECT COUNT(*) FROM users WHERE role = 'instructor'")).scalar()
        print(f"👥 Instructors: {instructors_count}")
        
        # Check courses
        courses_count = db_session.execute(text("SELECT COUNT(*) FROM courses")).scalar()
        print(f"📚 Courses: {courses_count}")
        
        # Check lessons
        lessons_count = db_session.execute(text("SELECT COUNT(*) FROM lessons")).scalar()
        print(f"📖 Lessons: {lessons_count}")
        
        # Show sample data
        print("\n📋 Sample Courses:")
        result = db_session.execute(text("""
            SELECT c.title, u.first_name || ' ' || u.last_name as instructor, c.price, cat.name as category
            FROM courses c
            JOIN users u ON c.instructor_id = u.id
            JOIN categories cat ON c.category_id = cat.id
            ORDER BY c.id
            LIMIT 5
        """))
        
        for row in result:
            print(f"  • {row[0]} - {row[1]} ({row[2]} BD) - {row[3]}")
            
        return True
    except Exception as e:
        print(f"❌ Error verifying seeding: {e}")
        return False

def main():
    """Main seeding function"""
    print("🚀 Starting Database Seeding Process...")
    print("=" * 50)
    
    # Check if database is accessible
    try:
        db_session = SessionLocal()
        # Test connection
        db_session.execute(text("SELECT 1"))
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check your DATABASE_URL in config/environment.py")
        return False
    
    try:
        # Step 1: Cleanup test data
        print("\n🧹 Step 1: Cleaning up test data...")
        cleanup_sql = read_sql_file("cleanup_test_data.sql")
        if cleanup_sql:
            execute_sql_statements(db_session, cleanup_sql)
            print("✅ Test data cleanup completed")
        else:
            print("⚠️  Skipping cleanup (cleanup file not found)")
        
        # Step 2: Seed real data
        print("\n🌱 Step 2: Seeding real educational content...")
        seed_sql = read_sql_file("seed_real_data.sql")
        if seed_sql:
            execute_sql_statements(db_session, seed_sql)
            print("✅ Real data seeding completed")
        else:
            print("❌ Seeding failed (seed file not found)")
            return False
        
        # Step 3: Verify results
        print("\n🔍 Step 3: Verifying seeding results...")
        verify_seeding(db_session)
        
        print("\n🎉 Database seeding completed successfully!")
        print("\nNext steps:")
        print("1. Start your FastAPI server: uvicorn main:app --reload")
        print("2. Test the API: curl http://127.0.0.1:8000/api/categories/")
        print("3. Check courses: curl http://127.0.0.1:8000/api/courses/")
        
        return True
        
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        return False
    finally:
        db_session.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
