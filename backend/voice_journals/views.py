import uuid

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import VoiceJournal
from .serializers import VoiceJournalSerializer
from .utils.tts_helpers import text_to_speech
from .utils.voice_helpers import (generate_tags_from_text, summarize_text,
                                  transcribe_audio)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_voice_journal(request):
    audio_file = request.FILES.get("audio_file")
    if not audio_file:
        return Response({"error": "audio_file is required"}, status=400)

    journal = VoiceJournal.objects.create(user=request.user, audio_file=audio_file)

    transcript = transcribe_audio(journal.audio_file.path)
    summary = summarize_text(transcript)
    tags = generate_tags_from_text(transcript)

    journal.transcript = transcript
    journal.summary = summary

    filename = f"journal_audio_{uuid.uuid4().hex}.mp3"
    output_path = f"media/voice_playback/{filename}"

    tts_path = text_to_speech(journal.summary, output_path)
    if tts_path:
        journal.playback_audio_url = f"/media/voice_playback/{filename}"

    journal.tags = tags
    journal.save()

    serializer = VoiceJournalSerializer(journal)
    return Response(serializer.data)
