from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    DailyLockoutViewSet,
    ShamePostViewSet,
    create_herd,
    join_herd,
    leave_herd,
    my_herd,
    herd_feed,
    toggle_like,
    share_to_herd,
    share_badge,
    herd_mood_view,
    check_badges,
    list_badges,
    trigger_shame_view,
    generate_donkey_challenge,
)

router = DefaultRouter()
router.register(r"lockouts", DailyLockoutViewSet)
router.register(r"shame-posts", ShamePostViewSet)

urlpatterns = router.urls + [
    path("trigger-shame/", trigger_shame_view),
    path("create-herd/", create_herd),
    path("join-herd/", join_herd),
    path("leave-herd/", leave_herd),
    path("my-herd/", my_herd),
    path("herd-feed/", herd_feed),
    path("herd-feed/<int:pk>/like/", toggle_like),
    path("share-to-herd/", share_to_herd),
    path("share-badge/", share_badge),
    path("badges/", list_badges),
    path("check-badges/", check_badges),
    path("herd-mood/", herd_mood_view),
    path("generate-challenge/", generate_donkey_challenge),
]
