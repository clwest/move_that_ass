from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Prompt, PromptResponse
from .serializers import PromptResponseSerializer, PromptSerializer


class PromptViewSet(viewsets.ModelViewSet):
    """CRUD API for prompt templates."""

    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    permission_classes = [IsAuthenticated]


class PromptResponseViewSet(viewsets.ModelViewSet):
    """Manage stored AI prompt responses."""

    queryset = PromptResponse.objects.all()
    serializer_class = PromptResponseSerializer
    permission_classes = [IsAuthenticated]
