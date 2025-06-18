from rest_framework import serializers
from .models import VoiceJournal


class VoiceJournalSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = VoiceJournal
        fields = "__all__"
        read_only_fields = [
            "user",
            "transcript",
            "summary",
            "playback_audio_url",
            "created_at",
        ]
