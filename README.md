# Skill Sprout Backend

A FastAPI backend application with PostgreSQL database and JWT authentication.

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

## Project Structure

```
.
├── config/
│   └── environment.py      # Environment variable configuration
├── controllers/
│   └── users.py            # User route handlers
├── dependencies/
│   └── get_current_user.py # JWT authentication dependency
├── models/
│   ├── base.py             # Base model with common fields
│   └── user.py             # User model
├── serializers/
│   └── user.py             # Pydantic schemas for validation
├── database.py             # Database configuration
├── main.py                 # FastAPI application entry point
└── Pipfile                 # Python dependencies

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

## Technologies Used

- **FastAPI** - Modern web framework
- **SQLAlchemy 2.0** - ORM with DeclarativeBase pattern
- **PostgreSQL** - Database
- **Pydantic** - Data validation
- **python-jose** - JWT token handling
- **passlib** - Password hashing with bcrypt
- **Alembic** - Database migrations
