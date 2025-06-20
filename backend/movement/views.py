from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import MovementChallenge, MovementSession
from .serializers import MovementChallengeSerializer, MovementSessionSerializer


class MovementChallengeViewSet(viewsets.ModelViewSet):
    queryset = MovementChallenge.objects.all()
    serializer_class = MovementChallengeSerializer
    permission_classes = [IsAuthenticated]


class MovementSessionViewSet(viewsets.ModelViewSet):
    queryset = MovementSession.objects.all()
    serializer_class = MovementSessionSerializer
    permission_classes = [IsAuthenticated]
