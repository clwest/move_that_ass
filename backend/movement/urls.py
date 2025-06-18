from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import MovementChallengeViewSet, MovementSessionViewSet

router = DefaultRouter()
router.register(r"challenges", MovementChallengeViewSet)
router.register(r"sessions", MovementSessionViewSet)

urlpatterns = router.urls
