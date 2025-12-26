#!/usr/bin/env python3
"""
Debug Seeding Script
Provides detailed logging to understand seeding issues
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
            content = f.read()
        print(f"📁 Read {len(content)} characters from {filename}")
        return content
    except FileNotFoundError:
        print(f"❌ Error: {filename} not found!")
        return None

def execute_sql_with_debug(db_session, sql_content, description):
    """Execute SQL statements with detailed logging"""
    print(f"\n🔍 Executing: {description}")
    print(f"SQL length: {len(sql_content)} characters")
    
    try:
        # Split by semicolon and execute each statement
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        print(f"Found {len(statements)} SQL statements")
        
        for i, statement in enumerate(statements[:5]):  # Show first 5 statements
            if statement and not statement.startswith('--'):
                print(f"  Statement {i+1}: {statement[:100]}...")
        
        if len(statements) > 5:
            print(f"  ... and {len(statements) - 5} more statements")
        
        success_count = 0
        error_count = 0
        
        for i, statement in enumerate(statements):
            if statement and not statement.startswith('--'):
                try:
                    print(f"\n⚡ Executing statement {i+1}...")
                    result = db_session.execute(text(statement))
                    db_session.commit()
                    print(f"✅ Statement {i+1} successful")
                    success_count += 1
                except Exception as e:
                    print(f"❌ Statement {i+1} failed: {e}")
                    error_count += 1
                    db_session.rollback()
                    
        print(f"\n📊 Results: {success_count} successful, {error_count} errors")
        return True
    except Exception as e:
        print(f"❌ Error executing SQL: {e}")
        return False

def debug_current_state(db_session):
    """Debug current database state"""
    try:
        print("\n🔍 CURRENT DATABASE STATE")
        print("=" * 40)
        
        # Check categories
        try:
            result = db_session.execute(text("SELECT COUNT(*) FROM categories"))
            count = result.scalar()
            print(f"🏷️  Categories: {count}")
            if count > 0:
                result = db_session.execute(text("SELECT name FROM categories LIMIT 5"))
                for row in result:
                    print(f"  • {row[0]}")
        except Exception as e:
            print(f"❌ Categories check failed: {e}")
        
        # Check users
        try:
            result = db_session.execute(text("SELECT COUNT(*) FROM users WHERE role = 'instructor'"))
            count = result.scalar()
            print(f"👥 Instructors: {count}")
            if count > 0:
                result = db_session.execute(text("SELECT username FROM users WHERE role = 'instructor' LIMIT 5"))
                for row in result:
                    print(f"  • {row[0]}")
        except Exception as e:
            print(f"❌ Instructors check failed: {e}")
        
        # Check courses
        try:
            result = db_session.execute(text("SELECT COUNT(*) FROM courses"))
            count = result.scalar()
            print(f"📚 Courses: {count}")
            if count > 0:
                result = db_session.execute(text("SELECT title FROM courses LIMIT 5"))
                for row in result:
                    print(f"  • {row[0]}")
        except Exception as e:
            print(f"❌ Courses check failed: {e}")
            
    except Exception as e:
        print(f"❌ Error checking database state: {e}")

def main():
    """Main debugging function"""
    print("🔧 Starting Database Seeding Debug...")
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
        # Step 1: Debug current state
        debug_current_state(db_session)
        
        # Step 2: Debug cleanup
        print("\n🧹 DEBUGGING CLEANUP...")
        cleanup_sql = read_sql_file("cleanup_test_data.sql")
        if cleanup_sql:
            execute_sql_with_debug(db_session, cleanup_sql, "Cleanup test data")
        else:
            print("⚠️  Skipping cleanup (cleanup file not found)")
        
        # Step 3: Debug seeding
        print("\n🌱 DEBUGGING SEEDING...")
        seed_sql = read_sql_file("seed_real_data.sql")
        if seed_sql:
            execute_sql_with_debug(db_session, seed_sql, "Seed real data")
        else:
            print("❌ Seeding failed (seed file not found)")
            return False
        
        # Step 4: Final state
        print("\n🔍 FINAL DATABASE STATE")
        debug_current_state(db_session)
        
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        return False
    finally:
        db_session.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
