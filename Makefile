# Root Makefile for MoveYourAzz
SHELL := /bin/bash

BACKEND_DIR := backend
FRONTEND_DIR := frontend/momentum_flutter
ACTIVATE = source .venv/bin/activate || true

.PHONY: run-backend migrate makemigrations test-backend lint-backend \
    run-frontend test-frontend lint-frontend install-backend install-frontend \
    azzify reset-db refresh reset-all

# == Backend Commands ==
run-backend:
	cd $(BACKEND_DIR) && $(ACTIVATE) && \
	python manage.py collectstatic --noinput && \
	python manage.py runserver

migrate:
	cd $(BACKEND_DIR) && $(ACTIVATE) && python manage.py migrate

makemigrations:
	cd $(BACKEND_DIR) && $(ACTIVATE) && python manage.py makemigrations

test-backend:
	cd $(BACKEND_DIR) && $(ACTIVATE) && python manage.py test

lint-backend:
	cd $(BACKEND_DIR) && flake8

# == Frontend Commands ==
run-frontend:
    cd $(FRONTEND_DIR) && \
	flutter run --disable-vm-service-publication

test-frontend:
	cd $(FRONTEND_DIR) && flutter test

lint-frontend:
	cd $(FRONTEND_DIR) && flutter analyze

# == Setup ==
install-backend:
	cd $(BACKEND_DIR) && python3 -m venv .venv && $(ACTIVATE) && pip install -r requirements.txt

install-frontend:
	cd $(FRONTEND_DIR) && flutter pub get

# == Utilities ==
azzify:
	cd $(BACKEND_DIR) && python manage.py azzify_texts

reset-db:
	cd $(BACKEND_DIR) && $(ACTIVATE) && python manage.py flush

refresh:
	$(MAKE) migrate && $(MAKE) run-backend

reset-all:
	$(MAKE) reset-db && $(MAKE) run-frontend

