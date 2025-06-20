# Production Deployment

1. Create a `.env` in `backend/` with all required secrets. See `.env.sample` for keys.
2. Build and start the stack:

```bash
docker compose -f docker-compose.prod.yml up -d
```

This launches Gunicorn, Celery, Redis and Nginx. Nginx forwards HTTPS traffic to the `web` service and enforces HSTS. Access the app at `https://localhost` (accept the self‑signed cert in a browser).
