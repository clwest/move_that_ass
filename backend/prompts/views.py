from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Prompt, PromptResponse
from .serializers import PromptSerializer, PromptResponseSerializer


class PromptViewSet(viewsets.ModelViewSet):
    """Manage prompt templates for AI interactions."""

    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    permission_classes = [IsAuthenticated]


class PromptResponseViewSet(viewsets.ModelViewSet):
    """Store user submissions generated from prompts."""

    queryset = PromptResponse.objects.all()
    serializer_class = PromptResponseSerializer
    permission_classes = [IsAuthenticated]
