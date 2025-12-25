# Task Management System

RESTful API for managing tasks and comments built with Django and Django REST Framework.

## Features

- 🔐 JWT Authentication
- ✅ Task management (CRUD operations)
- 💬 Comment system for tasks
- 👥 User management with search
- 🔍 Filtering and pagination
- 📚 API documentation (Swagger & ReDoc)
- 🐘 PostgreSQL database
- 🐳 Docker support
- 📝 Comprehensive logging
- ✅ 78% test coverage

## Tech Stack

- **Python 3.12**
- **Django 6.0**
- **Django REST Framework 3.16**
- **PostgreSQL 16**
- **Gunicorn** for production
- **Docker & Docker Compose**

## Requirements

- Docker & Docker Compose
- Make (optional, but recommended)

## Quick Start

The easiest way to get started is using the Makefile:

```bash
# 1. Start containers
make up

# 2. Setup project (migrate, collectstatic, create superuser)
make setup

# 3. (Optional) Fill database with test data
make seed

# View available commands
make help
```

That's it! The API will be available at `http://localhost:8000`

## Manual Installation

If you prefer not to use Make:

### 1. Clone the repository

```bash
git clone https://github.com/eugeny-m/smarteducation_tasks_manager_api.git
cd smarteducation_tasks_manager_api
```

### 2. Create `.env` file

```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Build and start containers

View container logs:
```bash
docker-compose logs -f web
```

Access Django shell:
```bash
docker-compose build
docker-compose up -d
```

### 4. Run migrations

View container logs:
```bash
docker-compose logs -f web
```

Access Django shell:
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

### 5. Create superuser

View container logs:
```bash
docker-compose logs -f web
```

Access Django shell:
```bash
docker-compose exec web python manage.py createsuperuser
```

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make help` | Show available commands |
| `make up` | Start Docker containers (auto-creates .env from .env.example if missing) |
| `make setup` | Run migrations, collect static, create superuser |
| `make test` | Run all tests with pytest |
| `make down` | Stop Docker containers |
| `make seed` | Fill database with test data |

### Test Data

The `make seed` command creates:
- **4 users** (1 admin, 3 regular users)
- **6 tasks** (various statuses and assignees)
- **8 comments** (distributed across tasks)

Example users created:
```
Username: admin          Password: admin123      Role: ADMIN
Username: john_doe       Password: john123       Role: USER
Username: jane_smith     Password: jane123       Role: USER
Username: bob_wilson     Password: bob123        Role: USER
```

## API Documentation

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## API Endpoints

### Authentication
- `POST /api/auth/token/` - Obtain JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Users
- `GET /api/users/` - List all users (with search: `?search=username`)
- `GET /api/users/{uuid}/` - Get user details
- `GET /api/users/me/` - Get current authenticated user info

### Tasks
- `GET /api/tasks/` - List tasks (with filters: `?creator={uuid}`, `?assignee={uuid}`, `?is_completed=true`)
- `POST /api/tasks/` - Create task
- `GET /api/tasks/{uuid}/` - Get task details
- `PATCH /api/tasks/{uuid}/` - Update task
- `DELETE /api/tasks/{uuid}/` - Delete task

### Comments
- `GET /api/tasks/{uuid}/comments/` - List task comments
- `POST /api/tasks/{uuid}/comments/` - Create comment

## Project Structure

```
smarteducation/
├── apps/
│   ├── core/           # Base models and shared logic
│   ├── users/          # User model, auth, and serializers
│   └── tasks/          # Tasks, comments, services, filters
├── config/             # Django settings and configuration
├── tests/
│   ├── integration/    # Integration tests
│   └── unit/           # Unit tests
├── logs/               # Application logs (auto-created)
├── docker-compose.yml  # Docker services configuration
├── Dockerfile          # Docker image definition
├── Makefile            # Development commands
└── pytest.ini          # Pytest configuration
```

## Environment Variables

Key environment variables (see `.env.example` for full list):

View container logs:
```bash
docker-compose logs -f web
```

Access Django shell:
```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=smarteducation
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# JWT
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# Logging
LOG_LEVEL=INFO
DJANGO_LOG_LEVEL=INFO
```

## Testing

Run tests with pytest:

View container logs:
```bash
docker-compose logs -f web
```

Access Django shell:
```bash
# Run all tests with coverage report
make test
```

Current test coverage: **77.93%**

Tests are organized in:
- `tests/integration/` - Integration tests for API endpoints
- `tests/unit/` - Unit tests (if needed)

## Logging

Logs are stored in the `logs/` directory:
- `info.log` - All INFO+ level logs
- `error.log` - ERROR level logs only

Logs include:
- Application startup
- User actions (create, update, delete tasks/comments)
- Request/response information

## Development

The application uses Gunicorn with auto-reload in development mode.

View container logs:
```bash
docker-compose logs -f web
```

Access Django shell:
```bash
docker-compose exec web python manage.py shell
```

Access container bash:
```bash
docker-compose exec web bash
```

## License

[Your License Here]
