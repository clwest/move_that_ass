# Makefile for MoveYourAzz project

PYTHON := python3
MANAGE := $(PYTHON) backend/manage.py
BACKEND_DIR := backend
FRONTEND_DIR := frontend/momentum_flutter
ACTIVATE := . .venv/bin/activate

.PHONY: run run-backend migrate makemigrations superuser shell run-worker test-backend test-frontend lint-backend clean reset flutter_run

run:
	@echo "Starting Django development server..."
	$(MANAGE) runserver

run-backend:
	@echo "Collecting static files..."
	$(MANAGE) collectstatic --noinput
	@echo "Starting Django development server..."
	$(MANAGE) runserver

migrate:
	@echo "Applying migrations..."
	$(MANAGE) migrate

makemigrations:
	@echo "Creating new migrations..."
	$(MANAGE) makemigrations

superuser:
	@echo "Creating superuser..."
	$(MANAGE) createsuperuser

shell:
	$(MANAGE) shell

run-worker:
	cd backend && ../venv/bin/python -m celery -A server worker -l info --concurrency=4

test-backend:
	cd $(BACKEND_DIR) && $(ACTIVATE) && pytest -q

test-frontend:
	cd $(FRONTEND_DIR) && \
	if [ -n "$$FLUTTER_ROOT" ]; then \
	flutter test --machine --platform=vm; \
	else \
	echo "Skipping flutter tests – SDK not available"; \
fi

lint-backend:
	@echo "Linting backend..."
	flake8 backend/

clean:
	@echo "Cleaning .pyc and __pycache__..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

reset:
	@echo "Resetting database (use with caution)..."
	rm -f db.sqlite3
	$(MANAGE) migrate

flutter_run:
	@echo "Starting Flutter app..."
	cd frontend/momentum_flutter && flutter run --no-publish-port
