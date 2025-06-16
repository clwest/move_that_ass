from datetime import timedelta
from django.utils import timezone

from core.models import DailyLockout, ShamePost, Profile, Herd


POSITIVE_MOODS = {"hype", "playful", "thoughtful"}
NEGATIVE_MOODS = {"annoyed", "ashamed", "burned out"}


def evaluate_herd_mood(herd: Herd) -> str:
    """Return a simple mood label for the given herd."""
    members = list(herd.members.all())
    if not members:
        return "meh"

    now = timezone.now()
    start_date = now - timedelta(days=3)

    total_shames = 0
    total_lockouts = 0
    mood_score = 0

    for member in members:
        total_shames += ShamePost.objects.filter(
            user=member, date__gte=start_date.date()
        ).count()
        total_lockouts += DailyLockout.objects.filter(
            user=member, date__gte=start_date.date(), is_unlocked=True
        ).count()
        profile = Profile.objects.filter(user=member).first()
        if profile:
            mood = profile.current_mood
            if mood in POSITIVE_MOODS:
                mood_score += 1
            elif mood in NEGATIVE_MOODS:
                mood_score -= 1

    herd_size = len(members)
    days_span = 3 * herd_size
    lockout_rate = total_lockouts / days_span if days_span else 0
    shame_rate = total_shames / days_span if days_span else 0
    avg_mood = mood_score / herd_size

    if lockout_rate > 0.6 and avg_mood > 0.2 and shame_rate < 0.3:
        return "vibing"
    if lockout_rate < 0.3 or avg_mood < -0.2 or shame_rate > 0.5:
        return "struggling"
    return "meh"
