from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (CurrentProfileView, PaddleLogViewSet, ProfileViewSet,
                    TaskStatusView, UserViewSet, create_movement_goal,
                    daily_goal_view, dashboard_feed, generate_meal_plan_view,
                    generate_workout_plan, get_mood_avatar_view, log_workout,
                    update_mood)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"profiles", ProfileViewSet)

router.register(r"paddle-logs", PaddleLogViewSet)

urlpatterns = router.urls + [
    path("profile/", CurrentProfileView.as_view()),
    path("dashboard/", dashboard_feed),
    path("update-mood/", update_mood),
    path("mood-avatar/", get_mood_avatar_view),
    path("daily-goal/", daily_goal_view),
    path("create-goal/", create_movement_goal),
    path("workout-plan/", generate_workout_plan),
    path("log-workout/", log_workout),
    path("meal-plan/", generate_meal_plan_view),
    path("tasks/<uuid:task_id>/", TaskStatusView.as_view()),
]
