from django.contrib import admin

from .models import MovementChallenge, MovementSession


@admin.register(MovementChallenge)
class MovementChallengeAdmin(admin.ModelAdmin):
    list_display = ("title", "duration_minutes", "created_at")


@admin.register(MovementSession)
class MovementSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "start_time", "duration", "is_complete")

