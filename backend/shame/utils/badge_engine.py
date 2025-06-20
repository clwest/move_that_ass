from datetime import timedelta
from django.utils import timezone
from shame.models import DailyLockout, ShamePost, Badge
from voice_journals.models import VoiceJournal
from content.models import GeneratedMeme


BADGE_RULES = {
    "streak_7": {
        "name": "7-Day Streak",
        "check": lambda user: all(
            DailyLockout.objects.filter(
                user=user,
                date=timezone.now().date() - timedelta(days=i),
                is_unlocked=True,
            ).exists()
            for i in range(7)
        ),
    },
    "voice_reflection": {
        "name": "Voice of Reflection",
        "check": lambda user: VoiceJournal.objects.filter(user=user).count() >= 5,
    },
    "shame_survivor": {
        "name": "Shame Survivor",
        "check": lambda user: not ShamePost.objects.filter(
            user=user,
            date__gte=timezone.now().date() - timedelta(days=5),
        ).exists(),
    },
    "meme_master": {
        "name": "Meme Master",
        "check": lambda user: GeneratedMeme.objects.filter(user=user).count() >= 10,
    },
    "herd_hero": {
        "name": "Herd Hero",
        "check": lambda user: (
            (herd := user.herds.first())
            and herd.members.count() >= 3
            and all(
                DailyLockout.objects.filter(
                    user=user,
                    date=timezone.now().date() - timedelta(days=i),
                    is_unlocked=True,
                ).exists()
                for i in range(3)
            )
        ),
    },
}


def evaluate_badges(user, save=True):
    """Check all badge rules and award new badges."""
    profile = user.profile
    newly_earned = []

    for code, rule in BADGE_RULES.items():
        badge = Badge.objects.filter(code=code, is_active=True).first()
        if not badge:
            continue
        if profile.badges.filter(id=badge.id).exists():
            continue
        try:
            passed = rule["check"](user)
        except Exception:
            passed = False
        if passed:
            if save:
                profile.badges.add(badge)
            newly_earned.append(badge)
    return newly_earned
