# MoveYourAzz Development


This repo contains the Django backend and Flutter frontend projects.

## Getting Started

1. Copy the sample env: `cp backend/.env.sample backend/.env` and edit the
   keys.
2. Install backend dependencies and set up a Python virtual environment
   (or run `make install-backend` which performs these steps):

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

3. Apply migrations and launch the server:

```bash
make migrate
make run-backend
```

4. Install git hooks:

```bash
pre-commit install
```

## Running Celery

Background jobs are handled by Celery with Redis. Start a worker once your env is active:


```bash
cd backend
source .venv/bin/activate
celery -A server worker -l info
```


Make sure Redis is running and `REDIS_URL` in your `.env` points at the broker.
