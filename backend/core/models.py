from django.db import models
from django.contrib.auth.models import User


class Badge(models.Model):
    """Awarded to users when they hit certain milestones."""

    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    emoji = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["code"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.code


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=64)
    bio = models.TextField(blank=True)
    streak_count = models.IntegerField(default=0)
    last_active = models.DateTimeField(null=True, blank=True)
    current_mood = models.CharField(max_length=20, default="neutral")
    mood_last_updated = models.DateTimeField(null=True, blank=True)
    badges = models.ManyToManyField(
        Badge, related_name="owners", blank=True
    )

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


class BadgeShoutout(models.Model):
    """Record a badge shoutout that can be shared with the user's herd."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    herd = models.ForeignKey(Herd, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.user.username} - {self.badge.code}"


class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)
    duration_minutes = models.IntegerField()
    intensity = models.CharField(max_length=20, default="moderate")
    mood = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    location_name = models.CharField(max_length=100, blank=True)
    gps_lat = models.FloatField(null=True, blank=True)
    gps_lon = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.user.username} {self.activity_type} {self.created_at}"


class MovementGoal(models.Model):
    """User-defined goal for completing a set number of activity sessions."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)
    target_sessions = models.IntegerField()
    current_count = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    is_failed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.user.username} {self.activity_type} {self.target_sessions}" \
            f" {self.start_date}->{self.end_date}"
