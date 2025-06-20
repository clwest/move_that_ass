# MoveYourAzz Development

![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)


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
`run-backend` will collect static files before starting the server, so your
local environment matches production.

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

## Register via cURL

```bash
curl -X POST http://127.0.0.1:8000/api/auth/registration/ \
   -H 'Content-Type: application/json' \
   -d '{"username":"alice","email":"alice@mail.com","password1":"Pass123!","password2":"Pass123!"}'
```


## Running Tests

Backend tests run with `make test-backend`.

Flutter widget tests run headlessly. Use `make test-frontend`, which invokes
`flutter test --machine --platform=vm` so no emulator or physical device is
required.

