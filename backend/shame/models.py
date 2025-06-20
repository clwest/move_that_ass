from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


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


class DailyLockout(models.Model):
    """Tracks whether the user completed required activity for the day."""

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
    """Donkey meme posted when a user misses a requirement."""

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


class Herd(models.Model):
    """Group of users that share memes and badge shoutouts."""

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


class DonkeyChallenge(models.Model):
    """Short challenge issued to motivate the user after failures."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge_text = models.TextField()
    issued_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    is_failed = models.BooleanField(default=False)
    tone = models.CharField(max_length=20, default="mixed")
    auto_generated = models.BooleanField(default=True)

    class Meta:
        ordering = ["-issued_at"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.user.username} - {self.tone}"


class HerdPost(models.Model):
    """Simple post shared with the user's herd."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)  # meme or badge
    caption = models.TextField(blank=True)
    image_url = models.URLField(blank=True, null=True)
    emoji = models.CharField(max_length=5, blank=True)
    badge_name = models.CharField(max_length=100, blank=True)
    likes = models.ManyToManyField(User, related_name="liked_herd_posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.user.username} {self.type} {self.created_at}"
