from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

from prompts.models import PromptResponse


class GeneratedImage(models.Model):
    response = models.ForeignKey(PromptResponse, on_delete=models.CASCADE)
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover
        return self.image_url


class SocialPost(models.Model):
    image = models.ForeignKey(GeneratedImage, on_delete=models.CASCADE)
    caption = models.TextField()
    shared_to = models.CharField(max_length=50)
    shared_at = models.DateTimeField(null=True, blank=True)
    was_successful = models.BooleanField(default=False)

    class Meta:
        ordering = ["-shared_at"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.shared_to} {self.shared_at}" if self.shared_at else self.shared_to


class GeneratedMeme(models.Model):
    """Store generated donkey memes and captions."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField()
    caption = models.TextField()
    tone = models.CharField(max_length=20, default="funny")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.user.username} - {self.tone}"

