from django.contrib import admin

from .models import (
    DailyLockout,
    PaddleLog,
    Profile,
    ShamePost,
    VoiceJournal,
    Herd,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "display_name",
        "streak_count",
        "last_active",
        "current_mood",
    )


@admin.register(DailyLockout)
class DailyLockoutAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "is_unlocked", "minutes_completed")


@admin.register(ShamePost)
class ShamePostAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "was_triggered")


@admin.register(PaddleLog)
class PaddleLogAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "duration_minutes", "location")


@admin.register(VoiceJournal)
class VoiceJournalAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")


@admin.register(Herd)
class HerdAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "tone", "invite_code")
