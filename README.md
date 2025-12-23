r z# Task Management System

RESTful API for managing tasks and comments built with Django and Django REST Framework.

## Features

- 🔐 JWT Authentication
- ✅ Task management (CRUD operations)
- 💬 Comment system for tasks
- 🔍 Filtering and pagination
- 📚 API documentation (Swagger & ReDoc)
- 🐘 PostgreSQL database
- 🐳 Docker support

## Tech Stack

- **Python 3.12**
- **Django 5.1**
- **Django REST Framework 3.15**
- **PostgreSQL 16**
- **Poetry** for dependency management

## Requirements

- Python 3.12+
- Poetry
- Docker & Docker Compose (for PostgreSQL)

## Installation

### 1. Clone the repository

### 1. Install dependencies with Poetry

```bash
poetry install
```

### 2. Activate virtual environment

```bash
poetry shell
```

### 3. Create `.env` file

```bash
cp .env.example .env
```

### 4. Start services with Docker

```bash
docker-compose up -d
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run development server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/

## Project Structure

- `apps/core/`: Base models and shared logic.
- `apps/users/`: Custom user model and authentication.
- `apps/tasks/`: Tasks and comments logic, including services and filters.
- `config/`: Django project configuration.
