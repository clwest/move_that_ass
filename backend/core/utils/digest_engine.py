from datetime import timedelta
from django.utils import timezone

from ..models import ShamePost, VoiceJournal, DailyLockout
from content.models import GeneratedMeme
from .mood_engine import evaluate_user_mood


def generate_daily_digest(user):
    """Return a summary of the user's activity over the last 24 hours."""

    now = timezone.now()
    since = now - timedelta(hours=24)

    shame_count = ShamePost.objects.filter(user=user, date__gte=since.date()).count()
    meme_count = GeneratedMeme.objects.filter(user=user, created_at__gte=since).count()
    journal_count = VoiceJournal.objects.filter(user=user, created_at__gte=since).count()
    lockout = DailyLockout.objects.filter(user=user, date=since.date()).first()

    herd = user.herds.first()
    herd_name = herd.name if herd else "No herd"
    herd_size = herd.members.count() if herd else 0

    mood = evaluate_user_mood(user)

    # Determine tone
    if lockout and lockout.is_unlocked:
        tone = "positive"
        movement_status = "✅ Completed"
    else:
        movement_status = "❌ Skipped"
        tone = "ashamed" if shame_count else "neutral"

    # Build digest lines
    lines = [f"🐴 Donkey Daily Digest for {user.username}"]
    lines.append(f"Mood: {mood}")
    lines.append(f"Herd: {herd_name} ({herd_size} members)")
    lines.append(f"Movement: {movement_status}")
    lines.append(f"Shames: {shame_count}")
    lines.append(f"Memes Created: {meme_count}")
    lines.append(f"Voice Journals: {journal_count}")

    # Add tone-based commentary
    if tone == "ashamed":
        lines.append("The donkey is not mad. Just disappointed. Again.")
    elif tone == "positive":
        lines.append("You moved your azz. The donkey is proud. 🦯🔥")
    else:
        lines.append("Today was... a day. The donkey remains neutral.")

    return "\n".join(lines)
