# MoveYourAzz Development


This repository contains the Django backend and Flutter frontend for MoveYourAzz.

## Setup

1. Copy `.env.sample` to `.env` in the project root.
2. Fill in the API keys for services like OpenAI, ElevenLabs and GIPHY.
3. Install backend dependencies with `make install-backend`.
4. Run migrations and start the server with `make migrate` and `make run-backend`.


## Setup


The backend uses Celery with Redis for background tasks. Start a worker once your virtual environment is active:


```bash
cd backend
source .venv/bin/activate
celery -A server worker -l info
```


Ensure Redis is running and `REDIS_URL` is set if different from the default.

