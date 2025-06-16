from rest_framework import viewsets
from django.contrib.auth.models import User

from .models import Profile, DailyLockout, ShamePost, PaddleLog
from .serializers import (
    ProfileSerializer,
    DailyLockoutSerializer,
    ShamePostSerializer,
    PaddleLogSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class DailyLockoutViewSet(viewsets.ModelViewSet):
    queryset = DailyLockout.objects.all()
    serializer_class = DailyLockoutSerializer


class ShamePostViewSet(viewsets.ModelViewSet):
    queryset = ShamePost.objects.all()
    serializer_class = ShamePostSerializer


class PaddleLogViewSet(viewsets.ModelViewSet):
    queryset = PaddleLog.objects.all()
    serializer_class = PaddleLogSerializer
