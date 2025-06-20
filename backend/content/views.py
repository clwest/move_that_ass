from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import GeneratedImage, GeneratedMeme, SocialPost
from .serializers import (GeneratedImageSerializer, GeneratedMemeSerializer,
                          SocialPostSerializer)
from .utils.caption_engine import generate_caption

try:
    from core.tasks import generate_meme_task
except Exception:  # pragma: no cover - Celery not loaded
    generate_meme_task = None


class GeneratedImageViewSet(viewsets.ModelViewSet):
    """ViewSet for storing generated images."""

    queryset = GeneratedImage.objects.all()
    serializer_class = GeneratedImageSerializer
    permission_classes = [IsAuthenticated]


class SocialPostViewSet(viewsets.ModelViewSet):
    """CRUD API for social posts created by the app."""

    queryset = SocialPost.objects.all()
    serializer_class = SocialPostSerializer
    permission_classes = [IsAuthenticated]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_caption_view(request):
    """Generate a caption for a description."""
    description = request.data.get("description", "")
    tone = request.data.get("tone", "funny")
    caption = generate_caption(description, tone)
    return Response({"caption": caption})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_meme(request):
    """Kick off meme generation via Celery."""

    tone = request.data.get("tone", "funny")
    task = generate_meme_task.delay(tone)
    return Response({"task_id": task.id}, status=202)
