from rest_framework.routers import DefaultRouter
from .views import GeneratedImageViewSet, SocialPostViewSet

router = DefaultRouter()
router.register(r'images', GeneratedImageViewSet)
router.register(r'social-posts', SocialPostViewSet)

urlpatterns = router.urls
