#!/usr/bin/env python3
"""
Debug script to investigate JSON parsing errors in the SkillSprout API
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_environment():
    """Test if environment variables are loaded correctly"""
    print("=== ENVIRONMENT TEST ===")
    try:
        from config.environment import DATABASE_URL, secret, ENVIRONMENT
        print(f"✅ DATABASE_URL: {DATABASE_URL}")
        print(f"✅ JWT_SECRET: {secret[:10]}...")
        print(f"✅ ENVIRONMENT: {ENVIRONMENT}")
    except Exception as e:
        print(f"❌ Environment loading failed: {e}")
        return False
    return True

def test_database_connection():
    """Test database connectivity"""
    print("\n=== DATABASE CONNECTION TEST ===")
    try:
        from database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text('SELECT 1'))
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_models_import():
    """Test if all models can be imported"""
    print("\n=== MODELS IMPORT TEST ===")
    try:
        from models.user import UserModel
        from models.course import CourseModel
        from models.review import ReviewModel
        from models.enrollment import EnrollmentModel
        print("✅ All models imported successfully")
        return True
    except Exception as e:
        print(f"❌ Models import failed: {e}")
        return False

def test_serializer_import():
    """Test if all serializers can be imported"""
    print("\n=== SERIALIZERS IMPORT TEST ===")
    try:
        from serializers.review import ReviewCreateSchema, ReviewResponseSchema
        print("✅ Serializers imported successfully")
        return True
    except Exception as e:
        print(f"❌ Serializers import failed: {e}")
        return False

def test_fastapi_app():
    """Test if FastAPI app can be created"""
    print("\n=== FASTAPI APP TEST ===")
    try:
        from main import app
        print("✅ FastAPI app created successfully")
        return True
    except Exception as e:
        print(f"❌ FastAPI app creation failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 SkillSprout API Debug Script")
    print("=" * 50)
    
    tests = [
        test_environment,
        test_database_connection,
        test_models_import,
        test_serializer_import,
        test_fastapi_app
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print(f"Passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("✅ All basic tests passed. API should work correctly.")
    else:
        print("❌ Some tests failed. Please fix these issues before proceeding.")
    
    sys.exit(0 if all(results) else 1)
