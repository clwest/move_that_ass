# MoveYourAzz Development

This repository contains the Django backend and Flutter frontend.

## Setup

1. Copy `.env.sample` to `.env` and add your API keys (OpenAI, ElevenLabs, GIPHY, etc.).
2. Install backend dependencies and create a virtual environment:
   ```bash
   make install-backend
   ```
3. Apply migrations and start the development server:
   ```bash
   make migrate
   make run-backend
   ```
4. Install Flutter packages:
   ```bash
   make install-frontend
   ```

## Running the Celery Worker

Ensure Redis is running and `REDIS_URL` is set in `.env`. Then start a worker:

```bash
cd backend
source .venv/bin/activate
celery -A server worker -l info
```

## Running the Frontend

From `frontend/momentum_flutter` run:

```bash
make run-frontend
```

If the backend runs elsewhere, pass its URL:

```bash
flutter run --dart-define=API_BASE_URL=http://localhost:8000
```
