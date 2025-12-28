# 🌱 Skill Sprout Backend

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

A modern, scalable FastAPI backend application for an online learning platform, featuring PostgreSQL database, JWT authentication, and comprehensive course management system.

## 👥 Team

| Sayed Ali | Abdulla Mohammed | Ali Hassan Salman |
|-----------|------------------|-------------------|
| Team Leader & Full-Stack Developer | Full-Stack Developer | Full-Stack Developer |

## ✨ Features

- 🔐 **JWT Authentication** - Secure user authentication and authorization
- 📚 **Course Management** - Complete CRUD operations for courses, categories, and lessons
- 👥 **User Management** - User registration, login, and profile management
- 📝 **Review System** - Course reviews and ratings
- 🎓 **Enrollment System** - Course enrollment and progress tracking
- 🔄 **Database Migrations** - Automated database schema management with Alembic
- 📊 **RESTful API** - Well-documented API endpoints with OpenAPI/Swagger
- 🛡️ **Security** - Password hashing, CORS configuration, and secure practices

## 📖 API Documentation

Once the server is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## Setup Instructions

### 1. Install Dependencies

Using Pipenv:
```bash
pipenv install
pipenv shell
```

### 2. Environment Variables

Create a `.env` file in the root directory based on `.env.example`:

```bash
cp .env.example .env
```

Then edit `.env` with your actual configuration:

```env
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/skill_db
JWT_SECRET=your-generated-secret-key
```

**Generate a secure JWT secret:**
```bash
openssl rand -hex 32
```

### 3. Database Setup

Make sure PostgreSQL is running and create your database:

```bash
psql -U postgres
CREATE DATABASE skill_db;
```

### 4. Run the Application

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Home endpoint
- `POST /api/register` - Register a new user
- `POST /api/login` - Login and get JWT token

## 📁 Project Structure

```
skill-sprout-backend/
├── 📂 alembic/                    # Database migration files
│   ├── env.py.example
│   └── versions/
├── 📂 config/                     # Configuration files
│   ├── environment.py            # Environment variables
│   └── environment.py.example    # Environment template
├── 📂 controllers/                # API route handlers
│   ├── categories.py             # Category endpoints
│   ├── courses.py                # Course endpoints
│   ├── enrollments.py            # Enrollment endpoints
│   ├── lessons.py                # Lesson endpoints
│   ├── reviews.py                # Review endpoints
│   └── users.py                  # User endpoints
├── 📂 dependencies/               # FastAPI dependencies
│   └── get_current_user.py       # JWT authentication
├── 📂 middleware/                 # Custom middleware
│   └── redirect_handler.py       # Request redirect handling
├── 📂 models/                     # SQLAlchemy models
│   ├── base.py                   # Base model class
│   ├── category.py               # Category model
│   ├── course.py                 # Course model
│   ├── enrollment.py             # Enrollment model
│   ├── lesson.py                 # Lesson model
│   ├── review.py                 # Review model
│   └── user.py                   # User model
├── 📂 serializers/                # Pydantic schemas
│   ├── category.py               # Category schemas
│   ├── course.py                 # Course schemas
│   ├── enrollment.py             # Enrollment schemas
│   ├── lesson.py                 # Lesson schemas
│   ├── review.py                 # Review schemas
│   └── user.py                   # User schemas
├── 📄 add_lesson_videos.py        # Utility script
├── 📄 alembic.ini                # Alembic configuration
├── 📄 database.py                # Database connection
├── 📄 debug_json_error.py        # Debug utility
├── 📄 main.py                    # FastAPI application
├── 📄 Pipfile                    # Python dependencies
├── 📄 README.md                  # This file
└── 📄 seed_data.py               # Database seeding script
```

## Database Migrations

To create and run migrations using Alembic:

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create a new migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write clear, concise commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

If you have any questions or need help, please reach out to the team:

- **Sayed Ali** - [GitHub Profile](https://github.com/SayedAliMajed)
- **Project Repository** - [Skill Sprout Backend](https://github.com/SayedAliMajed/skill-sprout-backend)

---

<p align="center">Made with ❤️ by the Skill Sprout Team</p>
