# Database Setup Guide - Real Data Seeding

## Overview

This guide will help you set up your SkillSprout database with real educational content, including categories, instructors, courses, and lessons. The process involves cleaning up test data and seeding with authentic content.

## Prerequisites

- PostgreSQL database configured
- SkillSprout backend API running
- Database connection details available

## Step-by-Step Setup

### Step 1: Cleanup Test Data ⚠️

**IMPORTANT**: This will permanently delete all test data from your database.

```bash
# Connect to your PostgreSQL database
psql -d your_database_name

# Run the cleanup script
\i cleanup_test_data.sql
```

**What this does:**
- Removes all test courses (titles starting with "Test" or "Demo")
- Removes associated lessons, enrollments, and reviews
- Keeps important users: hussain, hassan, and the new instructor accounts
- Provides verification of remaining data

### Step 2: Create Categories Table (First Time Only)

If this is the first time setting up categories, the table will be created automatically when you start the FastAPI server:

```bash
# Start the backend server
uvicorn main:app --reload
```

The server will automatically create the `categories` table when it starts.

### Step 3: Seed Real Data

```bash
# Run the real data seeding script
\i seed_real_data.sql
```

**What this creates:**
- **6 Course Categories**: Programming, Web Development, Data Science, Mobile Development, DevOps, Business
- **5 Real Instructors**: Bro Code, Dave Gray, Beau Carnes, Aakash N S, Simplilearn Team
- **5 Comprehensive Courses**: With proper category assignments and BD currency pricing
- **25+ Lessons**: Real YouTube video URLs and detailed content

### Step 4: Verify Setup

The seeding script includes automatic verification. You should see output like:

```
 section | count 
---------+-------
 🏆 INSTRUCTORS |     5
 📚 COURSES     |     5
 📖 LESSONS     |    25+
 🏷️ CATEGORIES  |     6
```

## Data Structure

### Categories (BD Currency)
| Name | Price Range | Description |
|------|-------------|-------------|
| Programming | 0.00 BD | Java, Python, C++ courses |
| Web Development | 0.00 BD | HTML, CSS, JavaScript, React |
| Data Science | 7.50 BD | Excel, SQL, Python, Power BI |
| Mobile Development | 0.00 BD | iOS, Android development |
| DevOps | 0.00 BD | Infrastructure, deployment |
| Business | 0.00 BD | Management, entrepreneurship |

### Instructors
- **Bro Code**: Java & Python instructor (1M+ subscribers)
- **Dave Gray**: Full-stack developer (500K+ students)
- **Beau Carnes**: freeCodeCamp.org curriculum lead
- **Aakash N S**: Jovian.ai founder (100K+ learners)
- **Simplilearn Team**: 2M+ professionals trained

### Courses Overview
1. **Java Tutorial for Beginners** (Bro Code) - 0.00 BD
2. **Python Full Course for Beginners** (Dave Gray) - 0.00 BD
3. **Full Stack Web Development** (freeCodeCamp) - 0.00 BD
4. **Web Development with HTML & CSS** (Aakash N S) - 0.00 BD
5. **Data Analytics Full Course 2025** (Simplilearn) - 7.50 BD

## API Testing

### Categories API
```bash
# Get all categories
curl http://127.0.0.1:8000/api/categories/

# Get category with course counts
curl http://127.0.0.1:8000/api/categories/?include_counts=true

# Get courses in a specific category
curl http://127.0.0.1:8000/api/categories/1/courses
```

### Courses API (Updated)
```bash
# Get all courses (now includes category information)
curl http://127.0.0.1:8000/api/courses/

# Get course details (includes category)
curl http://127.0.0.1:8000/api/courses/1
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check database credentials in your environment
- Verify database exists

### Foreign Key Errors
- Run cleanup script first to remove conflicting data
- Ensure categories table is created before seeding

### Permission Errors
- Ensure database user has CREATE, INSERT, DELETE permissions
- Check PostgreSQL user privileges

### API Not Working
- Restart FastAPI server after database changes
- Check server logs for errors
- Verify all model imports are correct

## Rollback

If something goes wrong, you can:

1. **Clean and reseed**:
   ```bash
   \i cleanup_test_data.sql
   \i seed_real_data.sql
   ```

2. **Reset database** (⚠️ destructive):
   ```sql
   DROP SCHEMA public CASCADE;
   CREATE SCHEMA public;
   GRANT ALL ON SCHEMA public TO postgres;
   GRANT ALL ON SCHEMA public TO public;
   ```
   Then restart your FastAPI server to recreate tables.

## Files Reference

- `cleanup_test_data.sql` - Removes test data
- `seed_real_data.sql` - Seeds real educational content
- `models/category.py` - Category database model
- `controllers/categories.py` - Category API endpoints
- `serializers/category.py` - Category validation schemas

## Support

If you encounter issues:

1. Check the verification output from the scripts
2. Review server logs for API errors
3. Verify database schema matches the models
4. Ensure all dependencies are installed

---

*Setup guide created on December 26, 2025*
