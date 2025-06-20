# Async AI with Celery

The backend uses Celery for long running GPT and Whisper calls. Make sure Redis is running and then start a worker in a separate terminal:

```bash
cd backend
source .venv/bin/activate
celery -A server worker -l info --concurrency=4
```

API clients should POST to the kick-off endpoints which return a `task_id` and `202` status:

- `POST /api/content/meme/`
- `POST /api/core/meal-plan/`
- `POST /api/core/workout-plan/`
- `POST /api/voice/transcribe/`

Poll task status using `GET /api/core/tasks/<task_id>/` until the state is `SUCCESS`:

```bash
curl /api/core/tasks/<task_id>/
```

When `state` becomes `SUCCESS`, the `data` field will contain the result JSON.
