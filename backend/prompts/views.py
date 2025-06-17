from rest_framework import viewsets

from .models import Prompt, PromptResponse
from .serializers import PromptSerializer, PromptResponseSerializer


class PromptViewSet(viewsets.ModelViewSet):
    """CRUD API for prompt templates."""
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer


class PromptResponseViewSet(viewsets.ModelViewSet):
    """Manage stored AI prompt responses."""
    queryset = PromptResponse.objects.all()
    serializer_class = PromptResponseSerializer
