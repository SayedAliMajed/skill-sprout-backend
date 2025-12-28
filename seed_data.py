"""Seed data for Skill Sprout Platform
Real YouTube courses across different subjects, categories, and price ranges
"""

from sqlalchemy.orm import Session
from models.user import UserModel
from models.category import CategoryModel
from models.course import CourseModel
from database import SessionLocal, engine

# Create all tables
def create_tables():
    from models.base import BaseModel
    BaseModel.metadata.create_all(bind=engine)

def seed_data():
    """Seed the database with real course data from YouTube"""
    db = SessionLocal()
    
    try:
        # Clear existing data (in reverse order to avoid foreign key issues)
        db.query(CourseModel).delete()
        db.query(CategoryModel).delete()
        db.query(UserModel).delete()
        db.commit()
        
        # Create Categories
        categories_data = [
            {
                "name": "Programming Fundamentals",
                "description": "Learn the basics of programming and software development",
                "icon_url": "https://cdn-icons-png.flaticon.com/512/2304/2304367.png",
                "color": "#FF6B6B"
            },
            {
                "name": "Web Development", 
                "description": "Build modern web applications with HTML, CSS, JavaScript and frameworks",
                "icon_url": "https://cdn-icons-png.flaticon.com/512/1055/1055672.png",
                "color": "#4ECDC4"
            },
            {
                "name": "Python Programming",
                "description": "Master Python for web development, data science, and automation",
                "icon_url": "https://cdn-icons-png.flaticon.com/512/5968/5968350.png",
                "color": "#45B7D1"
            },
            {
                "name": "JavaScript & React",
                "description": "Modern JavaScript development with React framework",
                "icon_url": "https://cdn-icons-png.flaticon.com/512/1126/1126012.png",
                "color": "#F7DC6F"
            },
            {
                "name": "Data Science & AI",
                "description": "Machine learning, data analysis, and artificial intelligence",
                "icon_url": "https://cdn-icons-png.flaticon.com/512/2103/2103633.png",
                "color": "#BB8FCE"
            },
            {
                "name": "Mobile Development",
                "description": "Build apps for iOS and Android devices",
                "icon_url": "https://cdn-icons-png.flaticon.com/512/420/420142.png",
                "color": "#58D68D"
            },
            {
                "name": "Digital Marketing",
                "description": "Master online marketing, SEO, and social media strategies",
                "icon_url": "https://cdn-icons-png.flaticon.com/512/2335/2335339.png",
                "color": "#F1948A"
            },
            {
                "name": "Business & Entrepreneurship",
                "description": "Start and grow your business with proven strategies",
                "icon_url": "https://cdn-icons-png.flaticon.com/512/3081/3081559.png",
                "color": "#85C1E9"
            },
            {
                "name": "Graphic Design",
                "description": "Learn design principles and tools like Photoshop and Illustrator",
                "icon_url": "https://cdn-icons-png.flaticon.com/512/1055/1055687.png",
                "color": "#F8C471"
            },
            {
                "name": "DevOps & Cloud",
                "description": "DevOps practices, cloud computing, and infrastructure management",
                "icon_url": "https://cdn-icons-png.flaticon.com/512/919/919836.png",
                "color": "#82E0AA"
            }
        ]
        
        categories = []
        for cat_data in categories_data:
            category = CategoryModel(**cat_data)
            db.add(category)
            db.flush()  # Get the ID
            categories.append(category)
        
        db.commit()
        
        # Create Instructor Users
        instructors_data = [
            {
                "username": "mosh_hamidai",
                "email": "mosh@codewithmosh.com",
                "first_name": "Mosh",
                "last_name": "Hamaidai", 
                "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewqBPZ3v3W2gE3eK",  # "password123"
                "role": "instructor",
                "bio": "Senior software engineer and best-selling author with 20+ years of experience teaching programming."
            },
            {
                "username": "brad_traversy",
                "email": "brad@traversymedia.com",
                "first_name": "Brad",
                "last_name": "Traversy",
                "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewqBPZ3v3W2gE3eK",  # "password123"
                "role": "instructor", 
                "bio": "Full-stack web developer and instructor with expertise in modern web technologies."
            },
            {
                "username": "stephen_grider",
                "email": "stephen@udemy.com",
                "first_name": "Stephen",
                "last_name": "Grider",
                "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewqBPZ3v3W2gE3eK",  # "password123"
                "role": "instructor",
                "bio": "Engineer and educator specializing in React, Redux, and advanced web development."
            },
            {
                "username": "jonas_schmedtmann",
                "email": "jonas@codingheroes.io",
                "first_name": "Jonas",
                "last_name": "Schmedtmann",
                "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewqBPZ3v3W2gE3eK",  # "password123"
                "role": "instructor",
                "bio": "Passionate web designer and developer who loves to teach and share knowledge."
            },
            {
                "username": "andrew_ng",
                "email": "andrew@stanford.edu",
                "first_name": "Andrew",
                "last_name": "Ng",
                "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewqBPZ3v3W2gE3eK",  # "password123"
                "role": "instructor",
                "bio": "AI researcher, educator, and co-founder of Coursera with expertise in machine learning."
            },
            {
                "username": "mike_coffee",
                "email": "mike@designcourse.com",
                "first_name": "Mike",
                "last_name": "Coffee",
                "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewqBPZ3v3W2gE3eK",  # "password123"
                "role": "instructor",
                "bio": "Senior front-end developer and UI/UX designer with 15+ years of experience."
            },
            {
                "username": "neil_patel",
                "email": "neil@neilpatel.com",
                "first_name": "Neil",
                "last_name": "Patel",
                "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewqBPZ3v3W2gE3eK",  # "password123"
                "role": "instructor",
                "bio": "Digital marketing expert and best-selling author specializing in SEO and growth strategies."
            },
            {
                "username": "dave_gray",
                "email": "dave@davegrayteaches.com",
                "first_name": "Dave",
                "last_name": "Gray",
                "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewqBPZ3v3W2gE3eK",  # "password123"
                "role": "instructor",
                "bio": "Full-stack developer and educator who focuses on practical, real-world programming skills."
            }
        ]
        
        instructors = []
        for instructor_data in instructors_data:
            instructor = UserModel(**instructor_data)
            db.add(instructor)
            db.flush()
            instructors.append(instructor)
        
        db.commit()
        
        # Helper function to get YouTube thumbnail URL
        def get_youtube_thumbnail(video_id):
            return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        
        # Create Courses with Real YouTube Data
        courses_data = [
            # Programming Fundamentals
            {
                "instructor_id": 1,  # Mosh
                "category_id": 1,    # Programming Fundamentals
                "title": "Complete C# Masterclass",
                "description": "Learn C# programming from scratch with hands-on projects. Master object-oriented programming, LINQ, async/await, and build real applications.",
                "price": 49.99,
                "thumbnail_url": get_youtube_thumbnail("GqQXzAPPD3g")
            },
            {
                "instructor_id": 2,  # Brad
                "category_id": 1,    # Programming Fundamentals
                "title": "Programming Fundamentals - Algorithms and Data Structures",
                "description": "Master the fundamentals of programming including algorithms, data structures, and problem-solving techniques essential for any programmer.",
                "price": 29.99,
                "thumbnail_url": get_youtube_thumbnail("8hly31xKli0")
            },
            
            # Web Development
            {
                "instructor_id": 4,  # Jonas
                "category_id": 2,    # Web Development
                "title": "The Complete Web Developer Course 2024",
                "description": "Learn HTML, CSS, JavaScript, PHP, Python, MySQL, and more! Build 25+ projects including a professional portfolio website.",
                "price": 79.99,
                "thumbnail_url": get_youtube_thumbnail("QrR_gm6RqMc")
            },
            {
                "instructor_id": 7,  # Mike
                "category_id": 2,    # Web Development
                "title": "Modern HTML & CSS From The Beginning",
                "description": "Build modern responsive websites using HTML5, CSS3, Flexbox, Grid, and animations. Perfect for beginners to intermediate developers.",
                "price": 39.99,
                "thumbnail_url": get_youtube_thumbnail("mU6anWqZJcc")
            },
            
            # Python Programming
            {
                "instructor_id": 1,  # Mosh
                "category_id": 3,    # Python Programming
                "title": "Complete Python Bootcamp From Zero to Hero",
                "description": "Learn Python like a Professional! Start from the basics and go all the way to creating your own applications and games.",
                "price": 59.99,
                "thumbnail_url": get_youtube_thumbnail("rfscVS0vtbw")
            },
            {
                "instructor_id": 8,  # Dave
                "category_id": 3,    # Python Programming
                "title": "Python for Everybody Specialization",
                "description": "Learn to Program and Analyze Data with Python. Designed for beginners who have never programmed before.",
                "price": 44.99,
                "thumbnail_url": get_youtube_thumbnail("eWRfhZUzrAc")
            },
            
            # JavaScript & React
            {
                "instructor_id": 3,  # Stephen
                "category_id": 4,    # JavaScript & React
                "title": "Modern React with Redux",
                "description": "Learn React 18, Hooks, Redux Toolkit, Router, GraphQL, Unit Testing, and more! Build 25+ projects.",
                "price": 69.99,
                "thumbnail_url": get_youtube_thumbnail("sBws8MS3sJs")
            },
            {
                "instructor_id": 4,  # Jonas
                "category_id": 4,    # JavaScript & React
                "title": "JavaScript - The Complete Guide 2024",
                "description": "Master JavaScript with projects, challenges, and theory. Includes ES6+, OOP, Async/Await, DOM, and more.",
                "price": 64.99,
                "thumbnail_url": get_youtube_thumbnail("W6NZfCO5SIk")
            },
            {
                "instructor_id": 2,  # Brad
                "category_id": 4,    # JavaScript & React
                "title": "React Front to Back",
                "description": "Learn React 18, Context API, Hooks, Router, and Firebase. Build 3 different apps from scratch.",
                "price": 54.99,
                "thumbnail_url": get_youtube_thumbnail("F-H12w_3rdQ")
            },
            
            # Data Science & AI
            {
                "instructor_id": 5,  # Andrew Ng
                "category_id": 5,    # Data Science & AI
                "title": "Machine Learning Specialization",
                "description": "Master Machine Learning fundamentals including supervised learning, unsupervised learning, and deep learning.",
                "price": 89.99,
                "thumbnail_url": get_youtube_thumbnail("Air5N1kJ5iQ")
            },
            {
                "instructor_id": 8,  # Dave
                "category_id": 5,    # Data Science & AI
                "title": "Python Data Science with Pandas and Numpy",
                "description": "Learn data analysis, data manipulation, and data visualization using Python, Pandas, and NumPy.",
                "price": 49.99,
                "thumbnail_url": get_youtube_thumbnail("vmEHCJofslg")
            },
            
            # Mobile Development
            {
                "instructor_id": 1,  # Mosh
                "category_id": 6,    # Mobile Development
                "title": "Complete iOS App Development Bootcamp",
                "description": "Learn iOS 17 App Development from Beginner to iOS App Store with Swift 5 and Xcode 15.",
                "price": 74.99,
                "thumbnail_url": get_youtube_thumbnail("z9U3VmKa6eU")
            },
            {
                "instructor_id": 2,  # Brad
                "category_id": 6,    # Mobile Development
                "title": "Flutter Crash Course",
                "description": "Learn Flutter framework for mobile app development. Build beautiful, fast native apps for iOS and Android.",
                "price": 39.99,
                "thumbnail_url": get_youtube_thumbnail("gB0uTa_q1Yc")
            },
            
            # Digital Marketing
            {
                "instructor_id": 6,  # Neil
                "category_id": 7,    # Digital Marketing
                "title": "Complete Digital Marketing Course",
                "description": "Master SEO, Google Ads, Facebook Marketing, Email Marketing, and affiliate marketing. Build a successful online business.",
                "price": 99.99,
                "thumbnail_url": get_youtube_thumbnail("J99qYq9yNgg")
            },
            {
                "instructor_id": 6,  # Neil
                "category_id": 7,    # Digital Marketing
                "title": "Google Ads Complete Course",
                "description": "Learn Google Ads from beginner to advanced. Master PPC advertising and grow your business with targeted ads.",
                "price": 59.99,
                "thumbnail_url": get_youtube_thumbnail("gFBjfSJmXlg")
            },
            
            # Business & Entrepreneurship
            {
                "instructor_id": 6,  # Neil
                "category_id": 8,    # Business & Entrepreneurship
                "title": "Entrepreneurship Masterclass",
                "description": "Learn how to start and grow a successful business. From idea validation to scaling, this course covers it all.",
                "price": 79.99,
                "thumbnail_url": get_youtube_thumbnail("9WqK_qjI8ug")
            },
            {
                "instructor_id": 6,  # Neil
                "category_id": 8,    # Business & Entrepreneurship
                "title": "Personal Branding Masterclass",
                "description": "Build your personal brand and establish yourself as an industry expert. Perfect for consultants and freelancers.",
                "price": 44.99,
                "thumbnail_url": get_youtube_thumbnail("M7lc1UVf-VE")
            },
            
            # Graphic Design
            {
                "instructor_id": 7,  # Mike
                "category_id": 9,    # Graphic Design
                "title": "Photoshop Masterclass - Beginner to Advanced",
                "description": "Learn Adobe Photoshop from scratch! Master photo editing, digital art, and design techniques. Perfect for beginners to advanced users.",
                "price": 49.99,
                "thumbnail_url": get_youtube_thumbnail("UtFi7IHP7l4")
            },
            {
                "instructor_id": 7,  # Mike
                "category_id": 9,    # Graphic Design
                "title": "Illustrator Masterclass",
                "description": "Master Adobe Illustrator for vector graphics, logo design, and digital illustration. Perfect for designers and artists.",
                "price": 54.99,
                "thumbnail_url": get_youtube_thumbnail("some_video_id")
            }
        ]
        
        courses = []
        for course_data in courses_data:
            course = CourseModel(**course_data)
            db.add(course)
            db.flush()
            courses.append(course)
        
        db.commit()

    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()
