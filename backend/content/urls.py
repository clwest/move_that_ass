from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    GeneratedImageViewSet,
    SocialPostViewSet,
    generate_meme,
    generate_caption_view,
)

router = DefaultRouter()
router.register(r'images', GeneratedImageViewSet)
router.register(r'social-posts', SocialPostViewSet)

urlpatterns = router.urls + [
    path("generate-caption/", generate_caption_view),
    path("generate-meme/", generate_meme),
]
