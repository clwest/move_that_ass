from rest_framework import viewsets

from .models import MovementChallenge, MovementSession
from .serializers import MovementChallengeSerializer, MovementSessionSerializer


class MovementChallengeViewSet(viewsets.ModelViewSet):
    """CRUD API for workout challenges."""
    queryset = MovementChallenge.objects.all()
    serializer_class = MovementChallengeSerializer


class MovementSessionViewSet(viewsets.ModelViewSet):
    """Manage individual movement session logs."""
    queryset = MovementSession.objects.all()
    serializer_class = MovementSessionSerializer
