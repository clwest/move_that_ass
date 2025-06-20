from rest_framework.routers import DefaultRouter
from .views import MovementChallengeViewSet, MovementSessionViewSet

router = DefaultRouter()
router.register(r"challenges", MovementChallengeViewSet)
router.register(r"sessions", MovementSessionViewSet)

urlpatterns = router.urls
