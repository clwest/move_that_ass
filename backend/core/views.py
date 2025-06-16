from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .utils.shame_engine import check_and_trigger_shame

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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def trigger_shame_view(request):
    post = check_and_trigger_shame(request.user)
    if not post:
        return Response({"message": "No shame triggered. You're safe... for now."}, status=200)
    return Response({
        "message": "Shame post created.",
        "caption": post.caption,
        "image_url": post.image_url,
    })
