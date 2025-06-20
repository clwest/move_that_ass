import os
import django


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
    os.environ.setdefault("RUNNING_TESTS", "1")
    django.setup()
