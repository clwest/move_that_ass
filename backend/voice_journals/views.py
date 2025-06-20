from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import VoiceJournal

try:
    from .tasks import process_voice_journal_task
except Exception:  # pragma: no cover - Celery not loaded
    process_voice_journal_task = None


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def transcribe_voice(request):
    """Kick off voice journal processing via Celery."""
    audio_file = request.FILES.get("audio_file")
    if not audio_file:
        return Response({"error": "audio_file is required"}, status=400)

    journal = VoiceJournal.objects.create(user=request.user, audio_file=audio_file)
    if process_voice_journal_task is None:
        return Response(
            {"detail": "Celery worker unavailable"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    task = process_voice_journal_task.delay(journal.id)
    return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def upload_voice_journal(request):
    """Deprecated path handling with redirect on GET."""
    if request.method == "GET":
        return redirect("/api/voice/upload/", permanent=False)
    return transcribe_voice.__wrapped__(request._request)
