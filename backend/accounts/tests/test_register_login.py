import pytest
from rest_framework.test import APIClient


pytestmark = pytest.mark.django_db


def test_register_and_login_username_and_email():
    from django.core.cache import cache
    cache.clear()
    client = APIClient()
    payload = {
        "username": "alice",
        "email": "a@b.com",
        "password1": "Demo1234!",
        "password2": "Demo1234!",
    }
    res = client.post("/api/auth/registration/", payload, format="json")
    assert res.status_code == 201
    assert res.data["user"]["username"] == "alice"
    assert res.data["user"]["email"] == "a@b.com"
    assert "pk" in res.data["user"]

    # login using username
    res = client.post("/api/auth/login/", {"username": "alice", "password": "Demo1234!"}, format="json")
    assert res.status_code == 200
    assert "access" in res.data and "refresh" in res.data

    # login using email
    res = client.post("/api/auth/login/", {"email": "a@b.com", "password": "Demo1234!"}, format="json")
    assert res.status_code == 200
    assert "access" in res.data and "refresh" in res.data


def test_no_deprecation_warnings(recwarn):
    client = APIClient()
    payload = {
        "username": "warn", "email": "w@b.com", "password1": "Demo1234!", "password2": "Demo1234!"
    }
    client.post("/api/auth/registration/", payload, format="json")
    messages = [str(w.message) for w in recwarn]
    assert not any("deprecated" in m for m in messages)
