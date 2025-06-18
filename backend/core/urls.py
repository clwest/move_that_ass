from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    UserViewSet,
    ProfileViewSet,
    PaddleLogViewSet,
    dashboard_feed,
    update_mood,
    get_mood_avatar_view,
    create_movement_goal,
    daily_goal_view,
    log_workout,
    generate_workout_plan,
    generate_meal_plan_view,

    daily_goal_view,
    register_user,
    CustomAuthToken,
    logout_user,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"profiles", ProfileViewSet)

router.register(r"paddle-logs", PaddleLogViewSet)

urlpatterns = router.urls + [
    path("register/", register_user),
    path("login/", CustomAuthToken.as_view()),
    path("logout/", logout_user),
    path("dashboard/", dashboard_feed),
    path("update-mood/", update_mood),
    path("mood-avatar/", get_mood_avatar_view),

    path("daily-goal/", daily_goal_view),
    path("create-goal/", create_movement_goal),
    path("generate-workout-plan/", generate_workout_plan),
    path("log-workout/", log_workout),
    path("generate-meal-plan/", generate_meal_plan_view),
]
