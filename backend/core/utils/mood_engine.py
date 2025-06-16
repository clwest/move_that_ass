from datetime import timedelta
from django.utils import timezone

from core.models import ShamePost, VoiceJournal
from content.models import GeneratedMeme


def evaluate_user_mood(user):
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)

    shames = ShamePost.objects.filter(user=user, date__gte=one_week_ago).count()
    memes = GeneratedMeme.objects.filter(user=user, created_at__gte=one_week_ago).count()
    journals = VoiceJournal.objects.filter(user=user, created_at__gte=one_week_ago)

    tag_counts = {}
    for journal in journals:
        for tag in journal.tags or []:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    if shames >= 4:
        mood = "ashamed"
    elif tag_counts.get("reflection", 0) >= 3:
        mood = "thoughtful"
    elif tag_counts.get("motivation", 0) >= 2:
        mood = "hype"
    elif tag_counts.get("frustration", 0) >= 2:
        mood = "annoyed"
    elif memes >= 3:
        mood = "playful"
    else:
        mood = "neutral"

    return mood
