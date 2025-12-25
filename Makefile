.PHONY: help up setup test down seed

# Default target
help:
	@echo "Smart Education - Available Commands"
	@echo "====================================="
	@echo ""
	@echo "  make up      - Start containers"
	@echo "  make setup   - Setup project (migrate, collectstatic, create superuser)"
	@echo "  make test    - Run all tests"
	@echo "  make down    - Stop containers"
	@echo "  make seed    - Fill database with test data"
	@echo ""

# 1. Start containers
up:
	@echo "Starting containers..."
	docker-compose up -d
	@echo "✅ Containers started"
	@echo "API: http://localhost:8000"
	@echo "Docs: http://localhost:8000/api/docs/"

# 2. Setup project
setup:
	@echo "Setting up project..."
	@echo "Running migrations..."
	docker-compose exec web python manage.py migrate
	@echo "Collecting static files..."
	docker-compose exec web python manage.py collectstatic --noinput
	@echo "Creating superuser..."
	docker-compose exec web python manage.py createsuperuser
	@echo "✅ Setup complete!"

# 3. Run tests
test:
	@echo "Running tests..."
	docker-compose exec web pytest
	@echo "✅ Tests complete!"

# 4. Stop containers
down:
	@echo "Stopping containers..."
	docker-compose down
	@echo "✅ Containers stopped"

# 5. Seed database with test data
seed:
	@echo "Seeding database with test data..."
	docker-compose exec web python manage.py seed_data
	@echo "✅ Database seeded!"
