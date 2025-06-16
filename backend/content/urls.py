from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    GeneratedImageViewSet,
    SocialPostViewSet,
    generate_promptcam_caption,
)

router = DefaultRouter()
router.register(r'images', GeneratedImageViewSet)
router.register(r'social-posts', SocialPostViewSet)

urlpatterns = router.urls + [
    path("generate-caption/", generate_promptcam_caption),
]
