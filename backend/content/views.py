from rest_framework import viewsets

from .models import GeneratedImage, SocialPost
from .serializers import GeneratedImageSerializer, SocialPostSerializer


class GeneratedImageViewSet(viewsets.ModelViewSet):
    queryset = GeneratedImage.objects.all()
    serializer_class = GeneratedImageSerializer


class SocialPostViewSet(viewsets.ModelViewSet):
    queryset = SocialPost.objects.all()
    serializer_class = SocialPostSerializer
