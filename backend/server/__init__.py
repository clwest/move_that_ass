try:
    from .celery import app as celery_app
except Exception:  # pragma: no cover - Celery optional in tests
    celery_app = None

__all__ = ("celery_app",)
