import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_generate_meme_returns_503_when_celery_unavailable(monkeypatch):
    User = get_user_model()
    user = User.objects.create_user(
        username="memer", email="memer@example.com", password="pass", is_verified=True
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    monkeypatch.setattr("content.views.generate_meme_task", None)

    res = client.post("/api/content/meme/", {"tone": "funny"}, format="json")

    assert res.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert res.data["detail"] == "Celery worker unavailable"
