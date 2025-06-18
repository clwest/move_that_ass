# MoveYourAzz Development

This repo contains the backend (Django) and frontend (Flutter) projects.

## Celery Worker

The backend uses Celery with Redis for background tasks.
Start a worker after your virtual environment is active:

```bash
cd backend
source .venv/bin/activate
celery -A server worker -l info
```

Ensure Redis is running and `REDIS_URL` is set if different from the default.
