from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class VoiceJournal(models.Model):
    """Uploaded audio journal with transcript and summary."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to="voice_journals/")
    transcript = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    playback_audio_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover
        return f"VoiceJournal {self.user.email} {self.created_at}"
