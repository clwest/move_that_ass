from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=64)
    bio = models.TextField(blank=True)
    streak_count = models.IntegerField(default=0)
    last_active = models.DateTimeField(null=True, blank=True)
    current_mood = models.CharField(max_length=20, default="neutral")
    mood_last_updated = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.display_name


class DailyLockout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    is_unlocked = models.BooleanField(default=False)
    required_minutes = models.IntegerField(default=30)
    minutes_completed = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "date")
        ordering = ["-date"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.user.username} - {self.date}"


class ShamePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    image_url = models.URLField()
    caption = models.TextField()
    posted_to = models.JSONField(default=list)
    was_triggered = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:  # pragma: no cover
        return f"ShamePost {self.user.username} {self.date}"


class PaddleLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    location = models.CharField(max_length=128, blank=True)
    duration_minutes = models.IntegerField(default=0)
    photo_url = models.URLField(blank=True)
    mood = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:  # pragma: no cover
        return f"PaddleLog {self.user.username} {self.date}"


class VoiceJournal(models.Model):
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
        return f"VoiceJournal {self.user.username} {self.created_at}"


class Herd(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_herds"
    )
    members = models.ManyToManyField(User, related_name="herds")
    tone = models.CharField(
        max_length=20,
        choices=[("roast", "Roast"), ("encourage", "Encourage"), ("mixed", "Mixed")],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    invite_code = models.CharField(max_length=12, unique=True)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.name
