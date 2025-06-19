from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    """User profile linked to the Django auth user."""

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    display_name = models.CharField(max_length=64)
    bio = models.TextField(blank=True)
    streak_count = models.IntegerField(default=0)
    last_active = models.DateTimeField(null=True, blank=True)
    current_mood = models.CharField(max_length=20, default="neutral")
    mood_last_updated = models.DateTimeField(null=True, blank=True)
    badges = models.ManyToManyField("shame.Badge", related_name="owners", blank=True)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return self.display_name


class PaddleLog(models.Model):
    """Log of paddle sessions with optional mood and photo."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    location = models.CharField(max_length=128, blank=True)
    duration_minutes = models.IntegerField(default=0)
    photo_url = models.URLField(blank=True)
    mood = models.TextField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:  # pragma: no cover
        return f"PaddleLog {self.user.email} {self.date}"


class WorkoutLog(models.Model):
    """Record of a user's workout session details."""

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
        return f"{self.user.email} {self.activity_type} {self.created_at}"


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
        return (
            f"{self.user.email} {self.activity_type} {self.target_sessions}"
            f" {self.start_date}->{self.end_date}"
        )


class DailyGoal(models.Model):
    """Simple per-day goal entry."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.CharField(max_length=50)
    target = models.IntegerField(default=1)

    date = models.DateField()
    goal_type = models.CharField(max_length=20, default="daily")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "date", "goal")
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.user.email} {self.goal} {self.date}"
