from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import GeneratedImage, SocialPost, GeneratedMeme
from .serializers import (
    GeneratedImageSerializer,
    SocialPostSerializer,
    GeneratedMemeSerializer,
)
from .utils.caption_engine import generate_caption
from .utils.meme_engine import fetch_donkey_gif, generate_meme_caption


class GeneratedImageViewSet(viewsets.ModelViewSet):
    queryset = GeneratedImage.objects.all()
    serializer_class = GeneratedImageSerializer


class SocialPostViewSet(viewsets.ModelViewSet):
    queryset = SocialPost.objects.all()
    serializer_class = SocialPostSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_promptcam_caption(request):
    description = request.data.get("description", "")
    tone = request.data.get("tone", "funny")
    caption = generate_caption(description, tone)
    return Response({"caption": caption})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_meme(request):
    """Generate a donkey meme and store it."""

    tone = request.data.get("tone", "funny")
    image_url = fetch_donkey_gif()
    caption = generate_meme_caption(tone)

    meme = GeneratedMeme.objects.create(
        user=request.user, image_url=image_url, caption=caption, tone=tone
    )

    return Response(GeneratedMemeSerializer(meme).data)

