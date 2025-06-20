import uuid

from celery import shared_task


@shared_task(bind=True, max_retries=3)
def process_voice_journal_task(self, journal_id: int):
    from .models import VoiceJournal
    from .utils.tts_helpers import text_to_speech
    from .utils.voice_helpers import (generate_tags_from_text, summarize_text,
                                      transcribe_audio)

    journal = VoiceJournal.objects.get(pk=journal_id)
    transcript = transcribe_audio(journal.audio_file.path)
    summary = summarize_text(transcript)
    tags = generate_tags_from_text(transcript)
    filename = f"journal_audio_{uuid.uuid4().hex}.mp3"
    output_path = f"media/voice_playback/{filename}"
    tts_path = text_to_speech(summary, output_path)
    if tts_path:
        journal.playback_audio_url = f"/media/voice_playback/{filename}"
    journal.transcript = transcript
    journal.summary = summary
    journal.tags = tags
    journal.save()
    from .serializers import VoiceJournalSerializer

    return VoiceJournalSerializer(journal).data
