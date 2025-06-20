import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from voice_journals.models import VoiceJournal


@pytest.mark.django_db
def test_upload_and_process_voice_journal(monkeypatch):
    User = get_user_model()
    user = User.objects.create_user(
        username="vj", email="vj@example.com", password="pass", is_verified=True
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    audio = SimpleUploadedFile("voice.wav", b"audio")

    captured = {}

    def fake_delay(jid):
        captured["jid"] = jid
        class R:
            id = "task123"
        return R()

    monkeypatch.setattr(
        "voice_journals.views.process_voice_journal_task.delay", fake_delay
    )

    res = client.post("/api/voice/upload/", {"audio_file": audio})
    assert res.status_code == 202

    journal = VoiceJournal.objects.get()
    assert captured["jid"] == journal.id

    monkeypatch.setattr(
        "voice_journals.utils.voice_helpers.transcribe_audio", lambda path: "hello world"
    )
    monkeypatch.setattr(
        "voice_journals.utils.voice_helpers.summarize_text", lambda text: "summary"
    )
    monkeypatch.setattr(
        "voice_journals.utils.voice_helpers.generate_tags_from_text", lambda text: ["tag1"]
    )
    monkeypatch.setattr(
        "voice_journals.utils.tts_helpers.text_to_speech", lambda text, path: path
    )

    from voice_journals.tasks import process_voice_journal_task

    result = process_voice_journal_task(journal.id)

    journal.refresh_from_db()
    assert journal.transcript == "hello world"
    assert journal.summary == "summary"
    assert journal.tags == ["tag1"]
    assert journal.playback_audio_url
    assert result["id"] == journal.id


@pytest.mark.django_db
def test_old_upload_voice_path_redirects(monkeypatch):
    User = get_user_model()
    user = User.objects.create_user(
        username="vj", email="vj2@example.com", password="pass", is_verified=True
    )
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    audio = SimpleUploadedFile("voice.wav", b"audio")

    monkeypatch.setattr(
        "voice_journals.views.process_voice_journal_task.delay",
        lambda jid: type("R", (), {"id": "task123"})(),
    )

    res = client.post(
        "/api/core/upload-voice/",
        {"audio_file": audio},
    )

    assert res.status_code == 202
    assert res.data["task_id"] == "task123"
