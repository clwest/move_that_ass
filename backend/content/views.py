from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import GeneratedImage, SocialPost, GeneratedMeme
from .serializers import (
    GeneratedImageSerializer,
    SocialPostSerializer,
    GeneratedMemeSerializer,
)
from .utils.meme_engine import fetch_donkey_gif, generate_meme_caption
from .utils.caption_engine import generate_caption

try:  # Celery tasks may not be available in dev
    from core.tasks import generate_meme_task
except Exception:  # pragma: no cover - fallback when Celery missing
    generate_meme_task = None


class GeneratedImageViewSet(viewsets.ModelViewSet):

    """ViewSet for storing generated images."""

    queryset = GeneratedImage.objects.all()
    serializer_class = GeneratedImageSerializer
    permission_classes = [AllowAny]


class SocialPostViewSet(viewsets.ModelViewSet):

    """CRUD API for social posts created by the app."""

    queryset = SocialPost.objects.all()
    serializer_class = SocialPostSerializer
    permission_classes = [AllowAny]


@api_view(["POST"])
@permission_classes([AllowAny])
def generate_caption_view(request):
    """Generate a caption for a description."""
    description = request.data.get("description", "")
    tone = request.data.get("tone", "funny")
    caption = generate_caption(description, tone)
    return Response({"caption": caption})



@api_view(["POST"])
@permission_classes([AllowAny])
def generate_meme(request):
    """Generate a donkey meme and store it."""

    tone = request.data.get("tone", "funny")

    if generate_meme_task:
        try:
            result = generate_meme_task.delay(tone)
            return Response({"task_id": result.id}, status=202)
        except Exception:  # pragma: no cover - worker or broker failure
            image_url = fetch_donkey_gif()
            caption = generate_meme_caption(tone)
            meme = GeneratedMeme.objects.create(
                user=request.user, image_url=image_url, caption=caption, tone=tone
            )
            return Response(GeneratedMemeSerializer(meme).data)
    else:
        image_url = fetch_donkey_gif()
        caption = generate_meme_caption(tone)
        meme = GeneratedMeme.objects.create(
            user=request.user, image_url=image_url, caption=caption, tone=tone
        )
        return Response(GeneratedMemeSerializer(meme).data)

