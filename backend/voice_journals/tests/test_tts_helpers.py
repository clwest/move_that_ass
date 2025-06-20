import importlib
from django.conf import settings


def test_voice_id_fallback(monkeypatch):
    """Voice ID defaults to settings value when env not set."""
    monkeypatch.delenv("VOICE_ID", raising=False)
    module = importlib.reload(importlib.import_module("voice_journals.utils.tts_helpers"))
    assert module.VOICE_ID == settings.VOICE_ID == "21m00Tcm4TlvDq8ikWAM"
