# Makefile for MoveThatAss project

# Python & Django settings
PYTHON := python3
MANAGE := $(PYTHON) backend/manage.py

# Targets
.PHONY: run migrate makemigrations superuser shell test lint clean reset flutter_run

run:
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
    cd $(BACKEND_DIR) && $(ACTIVATE) && celery -A server worker -l info --concurrency=4


lint:
	@echo "Linting Python code..."
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
	cd frontend && cd momentum_flutter && flutter run --no-publish-port