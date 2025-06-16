from rest_framework import viewsets

from .models import MovementChallenge, MovementSession
from .serializers import MovementChallengeSerializer, MovementSessionSerializer


class MovementChallengeViewSet(viewsets.ModelViewSet):
    queryset = MovementChallenge.objects.all()
    serializer_class = MovementChallengeSerializer


class MovementSessionViewSet(viewsets.ModelViewSet):
    queryset = MovementSession.objects.all()
    serializer_class = MovementSessionSerializer
