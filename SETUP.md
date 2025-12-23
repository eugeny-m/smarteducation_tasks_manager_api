# Quick Setup Guide

## Step-by-step commands

```bash
# 1. Install dependencies
poetry install

# 2. Activate virtual environment
poetry shell

# 3. Copy environment file
cp .env.example .env

# 4. Start PostgreSQL (and optionally the web app)
docker-compose up -d

# 5. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run server (if not running via docker)
python manage.py runserver
```

## Testing with Docker

If you want to run everything in Docker:

```bash
docker-compose up --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```
