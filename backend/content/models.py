from django.db import models

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

