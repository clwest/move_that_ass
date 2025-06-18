from django.contrib import admin

from .models import (

    PaddleLog,
    Profile,

    WorkoutLog,
    MovementGoal,

    DailyGoal,
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





@admin.register(PaddleLog)
class PaddleLogAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "duration_minutes", "location")








@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "activity_type",
        "duration_minutes",
        "intensity",
        "created_at",
    )


@admin.register(MovementGoal)
class MovementGoalAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "activity_type",
        "target_sessions",
        "current_count",
        "start_date",
        "end_date",
        "is_completed",
        "is_failed",
        "created_at",
    )








@admin.register(DailyGoal)
class DailyGoalAdmin(admin.ModelAdmin):
    list_display = ("user", "goal", "target", "goal_type", "date")
