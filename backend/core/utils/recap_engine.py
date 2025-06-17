from datetime import timedelta
from django.utils import timezone
from core.models import ShamePost, VoiceJournal, DailyLockout
from content.models import GeneratedMeme


def generate_weekly_recap(user):
    """Return a textual recap of the user's activity in the last 7 days."""
    now = timezone.now()
    week_ago = now - timedelta(days=7)

    lockouts = DailyLockout.objects.filter(user=user, date__gte=week_ago.date())
    unlocked_days = sum(1 for l in lockouts if l.is_unlocked)

    shames = ShamePost.objects.filter(user=user, date__gte=week_ago.date()).count()
    memes = GeneratedMeme.objects.filter(user=user, created_at__gte=week_ago).count()
    journals = VoiceJournal.objects.filter(user=user, created_at__gte=week_ago)

    total_days = 7
    journal_tags = {}
    for journal in journals:
        for tag in journal.tags or []:
            journal_tags[tag] = journal_tags.get(tag, 0) + 1

    # Tone logic
    if unlocked_days >= 5:
        tone = "legend"
    elif unlocked_days >= 3:
        tone = "resilient"
    elif shames >= 5:
        tone = "struggling"
    else:
        tone = "neutral"

    lines = [
        f"\U0001f434 Weekly Recap for {user.username}",
        f"You moved your azz {unlocked_days}/{total_days} days this week.",
        f"Shame Posts: {shames}",
        f"Memes Created: {memes}",
        f"Voice Journals: {len(journals)}",
        (
            "Top Journal Tags: "
            + (
                ", ".join(f"{k} ({v})" for k, v in journal_tags.items())
                if journal_tags
                else "None"
            )
        ),
    ]

    if tone == "legend":
        lines.append("This donkey salutes you. You've earned a badge in badazzery. 🏆🫏")
    elif tone == "resilient":
        lines.append("You had your off days, but you kept moving. The donkey sees the grind.")
    elif tone == "struggling":
        lines.append("The donkey sighs. We're not mad - just dramatically disappointed.")
    else:
        lines.append("It was a week. Next one's yours.")

    return "\n".join(lines)
