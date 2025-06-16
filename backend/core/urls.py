from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    ProfileViewSet,
    DailyLockoutViewSet,
    ShamePostViewSet,
    PaddleLogViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'lockouts', DailyLockoutViewSet)
router.register(r'shame-posts', ShamePostViewSet)
router.register(r'paddle-logs', PaddleLogViewSet)

urlpatterns = router.urls
