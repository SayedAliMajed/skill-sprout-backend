#!/usr/bin/env python3
"""
Database Migration Script
Adds categories table and category_id column to courses
"""

import sys
from sqlalchemy import text
from database import SessionLocal

def create_categories_table(db_session):
    """Create the categories table"""
    try:
        # Create categories table
        categories_sql = """
        CREATE TABLE IF NOT EXISTS categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            description TEXT,
            icon_url VARCHAR(500),
            color VARCHAR(7) DEFAULT '#3B82F6',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        db_session.execute(text(categories_sql))
        db_session.commit()
        print("✅ Categories table created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating categories table: {e}")
        db_session.rollback()
        return False

def add_category_id_to_courses(db_session):
    """Add category_id column to courses table"""
    try:
        # Add category_id column
        alter_sql = """
        ALTER TABLE courses 
        ADD COLUMN IF NOT EXISTS category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL;
        """
        db_session.execute(text(alter_sql))
        db_session.commit()
        print("✅ category_id column added to courses table")
        return True
    except Exception as e:
        print(f"❌ Error adding category_id column: {e}")
        db_session.rollback()
        return False

def verify_migration(db_session):
    """Verify the migration was successful"""
    try:
        # Check if categories table exists and has columns
        result = db_session.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'categories'
        """))
        
        print("\n🏷️ Categories table structure:")
        for row in result:
            print(f"  • {row[0]}: {row[1]}")
        
        # Check if category_id column exists in courses
        result = db_session.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'courses' AND column_name = 'category_id'
        """))
        
        category_col = result.fetchone()
        if category_col:
            print(f"✅ category_id column exists in courses: {category_col[1]}")
        else:
            print("❌ category_id column missing from courses")
            
        return True
    except Exception as e:
        print(f"❌ Error verifying migration: {e}")
        return False

def main():
    """Main migration function"""
    print("🔄 Starting Database Migration...")
    print("=" * 40)
    
    # Check database connection
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
        # Step 1: Create categories table
        print("\n📋 Step 1: Creating categories table...")
        if not create_categories_table(db_session):
            return False
        
        # Step 2: Add category_id to courses
        print("\n📊 Step 2: Adding category_id column to courses...")
        if not add_category_id_to_courses(db_session):
            return False
        
        # Step 3: Verify migration
        print("\n🔍 Step 3: Verifying migration...")
        verify_migration(db_session)
        
        print("\n🎉 Database migration completed successfully!")
        print("\nNext step: Run the seeding script again")
        print("python3 seed_database.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    finally:
        db_session.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
