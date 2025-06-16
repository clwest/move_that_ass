from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import GeneratedImage, SocialPost
from .serializers import GeneratedImageSerializer, SocialPostSerializer
from .utils.caption_engine import generate_caption


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
