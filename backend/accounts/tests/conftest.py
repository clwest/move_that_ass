import os
import django

def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
    os.environ.setdefault('CELERY_DISABLED', '1')
    django.setup()
    from django.conf import settings
    settings.CELERY_DISABLED = '1'
