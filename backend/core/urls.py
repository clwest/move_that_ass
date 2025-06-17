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
    share_badge,
    create_movement_goal,
    log_workout,

)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"profiles", ProfileViewSet)
router.register(r"lockouts", DailyLockoutViewSet)
router.register(r"shame-posts", ShamePostViewSet)
router.register(r"paddle-logs", PaddleLogViewSet)

urlpatterns = router.urls + [
    path("trigger-shame/", trigger_shame_view),
    path("upload-voice/", upload_voice_journal),
    path("create-herd/", create_herd),
    path("join-herd/", join_herd),
    path("leave-herd/", leave_herd),
    path("my-herd/", my_herd),
    path("dashboard/", dashboard_feed),
    path("update-mood/", update_mood),
    path("mood-avatar/", get_mood_avatar_view),

    path("herd-mood/", herd_mood_view),
    path("check-badges/", check_badges),
    path("share-badge/", share_badge),
    path("create-goal/", create_movement_goal),
    path("log-workout/", log_workout),

]
