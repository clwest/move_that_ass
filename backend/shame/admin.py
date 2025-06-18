from django.contrib import admin
from .models import (
    Badge,
    DailyLockout,
    ShamePost,
    Herd,
    BadgeShoutout,
    DonkeyChallenge,
    HerdPost,
)


@admin.register(DailyLockout)
class DailyLockoutAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "is_unlocked", "minutes_completed")


@admin.register(ShamePost)
class ShamePostAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "was_triggered")


@admin.register(Herd)
class HerdAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "tone", "invite_code")


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")


@admin.register(BadgeShoutout)
class BadgeShoutoutAdmin(admin.ModelAdmin):
    list_display = ("user", "badge", "herd", "created_at")


@admin.register(DonkeyChallenge)
class DonkeyChallengeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "challenge_text",
        "issued_at",
        "expires_at",
        "tone",
        "is_completed",
        "is_failed",
    )


@admin.register(HerdPost)
class HerdPostAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "created_at")
