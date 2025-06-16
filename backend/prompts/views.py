from rest_framework import viewsets

from .models import Prompt, PromptResponse
from .serializers import PromptSerializer, PromptResponseSerializer


class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer


class PromptResponseViewSet(viewsets.ModelViewSet):
    queryset = PromptResponse.objects.all()
    serializer_class = PromptResponseSerializer
