import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_voice_upload_returns_503_when_celery_unavailable(monkeypatch):
    User = get_user_model()
    user = User.objects.create_user(
        username="vj", email="vj@example.com", password="pass", is_verified=True
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    audio = SimpleUploadedFile("voice.wav", b"audio")

    monkeypatch.setattr("voice_journals.views.process_voice_journal_task", None)

    res = client.post("/api/voice/upload/", {"audio_file": audio})

    assert res.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert res.data["detail"] == "Celery worker unavailable"
