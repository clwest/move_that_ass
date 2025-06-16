from django.db import models
from django.contrib.auth.models import User


class Prompt(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover
        return self.text[:40]


class PromptResponse(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField()
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.user.username} - {self.prompt_id}"

