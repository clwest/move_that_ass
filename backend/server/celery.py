import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

app = Celery("server")

# Load task settings from Django settings under the CELERY_* namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Explicitly set broker/backend so a missing env var doesn't break startup
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_RESULT_BACKEND
app.conf.accept_content = ["json"]
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.timezone = "UTC"

# Autodiscover tasks from installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
