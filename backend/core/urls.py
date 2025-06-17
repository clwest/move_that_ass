from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    UserViewSet,
    ProfileViewSet,
    DailyLockoutViewSet,
    ShamePostViewSet,
    PaddleLogViewSet,
    trigger_shame_view,
    upload_voice_journal,
    create_herd,
    join_herd,
    leave_herd,
    my_herd,
    dashboard_feed,
    update_mood,
    get_mood_avatar_view,

    herd_mood_view,
    check_badges,
    list_badges,
    share_badge,
    create_movement_goal,
    daily_goal_view,
    log_workout,
    generate_workout_plan,
    generate_meal_plan_view,
    generate_donkey_challenge,
    get_today_dashboard,
    profile_view,
    share_to_herd,
    herd_feed,
    register_user,
    CustomAuthToken,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"profiles", ProfileViewSet)
router.register(r"lockouts", DailyLockoutViewSet)
router.register(r"shame-posts", ShamePostViewSet)
router.register(r"paddle-logs", PaddleLogViewSet)

urlpatterns = router.urls + [
    path("register/", register_user),
    path("login/", CustomAuthToken.as_view()),
    path("trigger-shame/", trigger_shame_view),
    path("upload-voice/", upload_voice_journal),
    path("create-herd/", create_herd),
    path("join-herd/", join_herd),
    path("leave-herd/", leave_herd),
    path("my-herd/", my_herd),
    path("dashboard/", dashboard_feed),
    path("update-mood/", update_mood),
    path("mood-avatar/", get_mood_avatar_view),
    path("dashboard-today/", get_today_dashboard),
    path("profile/", profile_view),

    path("herd-mood/", herd_mood_view),
    path("check-badges/", check_badges),
    path("badges/", list_badges),
    path("share-badge/", share_badge),
    path("daily-goal/", daily_goal_view),
    path("create-goal/", create_movement_goal),
    path("generate-workout-plan/", generate_workout_plan),
    path("log-workout/", log_workout),
    path("generate-meal-plan/", generate_meal_plan_view),
    path("generate-challenge/", generate_donkey_challenge),
    path("share-to-herd/", share_to_herd),
    path("herd-feed/", herd_feed),

]
