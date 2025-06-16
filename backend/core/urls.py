from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    UserViewSet,
    ProfileViewSet,
    DailyLockoutViewSet,
    ShamePostViewSet,
    PaddleLogViewSet,
    trigger_shame_view,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'lockouts', DailyLockoutViewSet)
router.register(r'shame-posts', ShamePostViewSet)
router.register(r'paddle-logs', PaddleLogViewSet)

urlpatterns = router.urls + [
    path("trigger-shame/", trigger_shame_view),
]
