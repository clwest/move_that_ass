from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (GeneratedImageViewSet, SocialPostViewSet,
                    generate_caption_view, generate_meme)

router = DefaultRouter()
router.register(r"images", GeneratedImageViewSet)
router.register(r"social-posts", SocialPostViewSet)

urlpatterns = router.urls + [
    path("generate-caption/", generate_caption_view),
    path("meme/", generate_meme),
]
