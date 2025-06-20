import os
import uuid
from django.conf import settings
from django_ratelimit.decorators import ratelimit

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

try:
    from .tasks import identify_image_task
except Exception:  # pragma: no cover - Celery not loaded
    identify_image_task = None


@api_view(["POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
@ratelimit(key="ip", rate="5/m", block=True)
def identify_image(request):
    file = request.FILES.get("file")
    if not file:
        return Response({"error": "file required"}, status=400)
    filename = f"{uuid.uuid4().hex}_{file.name}"
    dir_path = os.path.join(settings.MEDIA_ROOT, "vision")
    os.makedirs(dir_path, exist_ok=True)
    path = os.path.join(dir_path, filename)
    with open(path, "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)
    task = identify_image_task.delay(path)
    return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)
